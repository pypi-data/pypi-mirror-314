"""
Timeline related panels

a Timeline is a <ul> consisting of successive <li> that will be displayed left/right
"""

import typing
import logging
import datetime
from dataclasses import dataclass

from caerp.consts.permissions import PERMISSIONS
from caerp.controllers.business import (
    currently_invoicing,
    get_amount_to_invoice_ttc,
    get_deposit_deadlines,
    get_estimation_deadlines,
    get_deposit_deadlines,
    get_intermediate_deadlines,
    get_sold_deadlines,
    get_amount_to_invoice_ht,
    get_task_outside_payment_deadline,
)

from caerp.models.project.business import Business, BusinessPaymentDeadline
from caerp.models.task import Estimation, Invoice, CancelInvoice, Task
from caerp.utils.datetimes import format_date
from caerp.utils.strings import (
    format_amount,
    format_cancelinvoice_status,
    format_estimation_status,
    format_invoice_status,
)
from caerp.utils.widgets import POSTButton, Link

from caerp.views.business.routes import (
    BUSINESS_ITEM_INVOICING_ROUTE,
    BUSINESS_PAYMENT_DEADLINE_ITEM_ROUTE,
    BUSINESS_ITEM_PROGRESS_INVOICING_ROUTE,
)
from caerp.views.task.utils import task_pdf_link, get_task_url

from caerp.panels import BasePanel

logger = logging.getLogger(__name__)


@dataclass
class Action:
    title: str
    button: POSTButton
    description: typing.Optional[str] = None
    # Doit-on masquer le cadre et juste afficher le bouton "+" au milieu
    reduced: typing.Optional[bool] = False


@dataclass
class WrappedDeadline:
    """Wrapper aroung BusinessPaymentDeadline used for the timeline"""

    model: BusinessPaymentDeadline
    is_sold: bool = False
    amount_ht: int = 0
    time_state: str = "current"


@dataclass
class WrappedTask:
    """Wrapper aroung Task used for the timeline"""

    model: Task
    current: bool = False


def progress_invoicing_url(business, request, _query={}):
    """
    Build the progress invoicing invoicing url

    :rtype: str
    """
    return request.route_path(
        BUSINESS_ITEM_PROGRESS_INVOICING_ROUTE, id=business.id, _query=_query
    )


def _get_sort_representation(item: typing.Union[Task, WrappedDeadline]) -> list:
    """
    Build representations of the item used to sort Tasks and BusinessPaymentDeadlines
    1- by date
    2- by item type (Task > BusinessPaymentDeadline)
    3- by order (for BusinessPaymentDeadline)

    Used to sort element in the timeline
    """
    item_type_index = 2
    if isinstance(item, Task):
        item_type_index = 0
        d = item.date
        return [d.year, d.month, d.day, item_type_index]
    elif isinstance(item, WrappedDeadline):
        item_type_index = 1
        if item.model.invoiced and item.model.invoice:
            d = item.model.invoice.date
            item_type_index = 0
        elif item.model.date and item.model.date != item.model.estimation.date:
            d = item.model.date
        else:
            # On construit une date arbitraire qui nous permet d'ordonner les éléments
            if item.model.deposit:
                day = 1
            day = item.model.order + 2
            month = 1
            if day > 28:
                day = day - (28 * int(day / 28))
                month = int(day / 28) + 1
            d = datetime.date(3000, month, day)

        return [d.year, d.month, d.day, item_type_index]


class BusinessClassicTimelinePanel(BasePanel):
    """
    Panel rendering a timeline of a business in classic mode

    Shows :
    - Estimations
    - CancelInvoices
    - Invoices
    - BusinessPaymentDeadlines
    - Additional actions

    In the order defined through the _get_sort_representation

    # Cases

    1- We are waiting for a new intermediate invoice
    2- We are waiting for the sold invoice
    3- An Invoice is currently under edition / waiting for validation
    4- All invoices were generated
    """

    panel_name = "payment_deadline_timeline"
    template = "caerp:templates/panels/business/payment_deadline_timeline.mako"

    def __init__(self, context, request):
        super().__init__(context, request)

        self.intermediate_deadlines, self.sold_deadlines = self._get_wrapped_deadlines()

        # Où on en est dans cette affaire
        self.status = self._status()

    def _get_wrapped_deadlines(
        self,
    ) -> typing.Tuple[typing.List[WrappedDeadline], typing.List[WrappedDeadline]]:
        """
        Wrap deadlines for the timeline adding some order related informations
        """
        intermediate = []
        time_state = "current"
        for deadline in get_deposit_deadlines(self.request, self.context):
            if deadline.invoiced:
                state = "past"
            else:
                state = time_state
                time_state = "future"
            intermediate.append(
                WrappedDeadline(
                    model=deadline,
                    time_state=state,
                    amount_ht=deadline.amount_ht,
                )
            )
        for deadline in get_intermediate_deadlines(self.request, self.context):
            if deadline.invoiced:
                state = "past"
            else:
                state = time_state
                time_state = "future"
            intermediate.append(
                WrappedDeadline(
                    model=deadline,
                    time_state=state,
                    amount_ht=deadline.amount_ht,
                )
            )

        sold = []
        for deadline in get_sold_deadlines(self.request, self.context):
            if deadline.invoiced:
                state = "past"
            else:
                state = time_state
                time_state = "future"
            sold.append(
                WrappedDeadline(
                    model=deadline,
                    time_state=state,
                    is_sold=True,
                    amount_ht=deadline.amount_ht,
                )
            )
        return intermediate, sold

    def _status(self):
        if currently_invoicing(self.request, self.context):
            return "currently_invoicing"
        elif any(
            [not deadline.model.invoiced for deadline in self.intermediate_deadlines]
        ):
            return "intermediate_deadline"
        elif any([not deadline.model.invoiced for deadline in self.sold_deadlines]):
            return "sold_deadline"
        else:
            return "invoiced"

    def _get_add_more_invoice_button(self):
        """
        Build a button to generate a new intermediary invoice
        """
        url = self.request.route_path(
            BUSINESS_ITEM_INVOICING_ROUTE,
            id=self.context.id,
            deadline_id=0,
        )
        button = POSTButton(
            url=url,
            label="Ajouter",
            icon="file-invoice-euro",
            css="btn small icon",
            title="Générer une facture intermédiaire",
        )
        return Action(
            title="Ajouter une facture intermédiaire",
            description=(
                "Générer une facture intermédiaire qui n'était pas prévue dans"
                " le devis initial"
            ),
            button=button,
            reduced=True,
        )

    def _get_not_invoiced_intermediate_deadlines(self, estimation):
        for deadline in get_estimation_deadlines(self.request, estimation):
            if not deadline.invoice:
                yield deadline

    def _update_sold_item_amount(self, sold_deadline: WrappedDeadline):
        """
        Update the amount to invoice of the sold deadlines
        """
        amount_to_invoice = get_amount_to_invoice_ht(
            self.request, self.context, sold_deadline.model.estimation
        )
        other_deadlines_amount = sum(
            deadline.amount_ht or 0
            for deadline in self._get_not_invoiced_intermediate_deadlines(
                sold_deadline.model.estimation
            )
            if deadline != sold_deadline.model
        )
        sold_deadline.amount_ht = amount_to_invoice - other_deadlines_amount
        return sold_deadline

    def _get_sold_date(self):
        """
        Retourne la date de la dernière facture de solde
        ou None si le solde n'a pas été facturé
        """
        sold_date = None
        for deadline in self.sold_deadlines:
            if deadline.model.invoiced:
                sold_date = deadline.model.invoice.date
        return sold_date

    def collect_items(self):
        """
        Produce a generator for item that should be displayed in the timeline
        Estimations
        Invoices
        CancelInvoices
        BusinessPaymentDeadlines
        """
        sold_date = self._get_sold_date()

        # Le devis et les factures non associées à des échéances de facturation
        # (datées d'avant le solde si ce dernier a déjà été facturé)
        tasks = get_task_outside_payment_deadline(
            self.request, self.context, max_date=sold_date
        )
        # Toutes les échéances intermédiaires
        tasks.extend(self.intermediate_deadlines)
        tasks.sort(key=_get_sort_representation)

        # Le bouton pour générer une nouvelle facture pas prévue avant le solde
        if not self.context.invoiced:
            if self.status == "sold_deadline":
                tasks.append(self._get_add_more_invoice_button())

        # Le solde
        for deadline in self.sold_deadlines:
            tasks.append(self._update_sold_item_amount(deadline))

        # Les factures non associées à des échéances de facturation et datées
        # d'après le solde, mais seulement si le solde a déjà été facturé
        if sold_date:
            more_tasks = get_task_outside_payment_deadline(
                self.request, self.context, min_date=sold_date
            )
            more_tasks.sort(key=_get_sort_representation)
            tasks.extend(more_tasks)

        return tasks

    def __call__(self):
        return {
            "to_invoice": get_amount_to_invoice_ht(self.request, self.context),
            "foreseen_to_invoice": self.context.amount_foreseen_to_invoice(),
            "items": self.collect_items(),
            "status": self.status,
        }


class BusinessProgressInvoicingTimeLinePanel(BasePanel):
    """Panel rendering a timeline of a business in classic mode"""

    panel_name = "progress_invoicing_timeline"
    template = "caerp:templates/panels/business/progress_invoicing_timeline.mako"

    def collect_items(self):
        tasks = get_task_outside_payment_deadline(self.request, self.context)

        if not get_amount_to_invoice_ht(self.request, self.context) == 0:
            deposit_deadlines = get_deposit_deadlines(self.request, self.context)
            time_state = "current"
            for deposit_deadline in deposit_deadlines:
                if not deposit_deadline.invoiced:
                    state = time_state
                    time_state = "future"
                else:
                    state = "past"
                tasks.append(
                    WrappedDeadline(
                        model=deposit_deadline,
                        time_state=state,
                        amount_ht=deposit_deadline.amount_ht,
                    )
                )
            tasks.sort(key=_get_sort_representation)

            invoicing = currently_invoicing(self.request, self.context)
            tasks.append(
                Action(
                    title="Facture de situation",
                    description=(
                        "Générer une nouvelle facture de situation basée sur "
                        "l'avancement de l'affaire"
                    ),
                    button=POSTButton(
                        url=progress_invoicing_url(self.context, self.request),
                        label="Générer la facture",
                        title="Facture sur le pourcentage d'avancement de l'affaire",
                        icon="file-invoice-euro",
                        css="btn small icon",
                        disabled=invoicing,
                    ),
                )
            )
            tasks.append(
                Action(
                    title="Facture de solde",
                    description="Générer la facture de solde de cette affaire",
                    button=POSTButton(
                        url=progress_invoicing_url(
                            self.context,
                            self.request,
                            _query={"action": "sold"},
                        ),
                        label="Générer la facture",
                        title="Facturer le solde de cette affaire",
                        icon="file-invoice-euro",
                        css="btn small icon",
                        disabled=invoicing,
                    ),
                )
            )
        return tasks

    def __call__(self):
        logger.debug("Items {}".format(self.collect_items()))
        return {
            "to_invoice": get_amount_to_invoice_ttc(self.request, self.context),
            "items": self.collect_items(),
        }


class BusinessPaymentDeadlineTimelinePanelItem(BasePanel):
    """Render a Business payment deadline timeline item"""

    template = (
        "caerp:templates/panels/business/business_payment_deadline_timeline_item.mako"
    )

    def _get_title(self):
        if self.context.is_sold:
            result = f"Échéance : {self.context.model.description}"
            if self.context.model.description != "Solde":
                result += " (solde)"
        else:
            result = f"Échéance : {self.context.model.description}"
        return result

    def _get_description(self):
        invoice = self.context.model.invoice
        estimation_number = ""
        if len(self.context.model.business.estimations) > 1:
            estimation_number = (
                f"du devis {self.context.model.estimation.internal_number} "
            )
        if invoice is not None:
            date_str = format_date(invoice.date)
            amount_ttc = format_amount(invoice.total(), precision=5)
            amount_ht = format_amount(invoice.total_ht(), precision=5)
            status_str = format_invoice_status(invoice, full=True)
            result = ""
            if estimation_number:
                result += f"Facturation {estimation_number}<br />"
            if self.context.model.invoiced:
                result += (
                    f"Facturée le {date_str} : {amount_ttc}&nbsp;€&nbsp;TTC "
                    f"({amount_ht}&nbsp;€&nbsp;HT)<br />"
                    f"{status_str}"
                )
            else:
                result += (
                    f"Facture en cours d'édition le {date_str} : "
                    f"{amount_ttc}&nbsp;€&nbsp;TTC "
                    f"({amount_ht}&nbsp;€&nbsp;HT)<br />"
                    f"{status_str}"
                )
            return result
        else:
            date_str = ""
            if self.context.model.date:
                date_str = " le {} ".format(format_date(self.context.model.date))

            estimation_number = ""
            if len(self.context.model.business.estimations) > 1:
                estimation_number = (
                    f"du devis {self.context.model.estimation.internal_number} "
                )

            if self.context.is_sold:
                amount_ht = format_amount(self.context.amount_ht, precision=5)
                result = (
                    f"Solde {estimation_number}à facturer{date_str}: "
                    f"{amount_ht}&nbsp;€&nbsp;HT"
                )
                if self.context.amount_ht < 0:
                    result += (
                        "<br /><strong>Attention</strong> : La somme déjà facturée et les échéances de "
                        "facturation prévue dépassent le montant du devis initial"
                    )
                return result
            else:
                amount_ttc = format_amount(self.context.model.amount_ttc, precision=5)
                amount_ht = format_amount(self.context.model.amount_ht, precision=5)

                return (
                    f"Facturation {estimation_number}prévue initialement {date_str}: "
                    f"{amount_ttc}&nbsp;€&nbsp;TTC "
                    f"({amount_ht}&nbsp;€&nbsp;HT)"
                )

    def _get_css_data(self):
        if self.context.time_state == "past":
            status_css = "valid"
            icon = "check"
        elif self.context.time_state == "future":
            icon = "clock"
            status_css = "draft"
        else:
            status_css = "caution"
            if self.context.model.invoicing():
                icon = "euro-sign"
            else:
                icon = "clock"

        return dict(
            status_css=status_css,
            time_css=self.context.time_state,
            icon=icon,
            current=self.context.time_state == "current",
        )

    def _get_more_links(self):
        if self.request.has_permission(
            PERMISSIONS["context.edit_business_payment_deadline"], self.context.model
        ):
            yield Link(
                self.request.route_path(
                    BUSINESS_PAYMENT_DEADLINE_ITEM_ROUTE,
                    id=self.context.model.id,
                    _query={"action": "edit"},
                ),
                label="",
                title="Modifier cette échéance",
                icon="pen",
                css="btn icon only unstyled",
                popup=True,
            )
        if self.request.has_permission(
            PERMISSIONS["context.delete_business_payment_deadline"], self.context.model
        ):
            yield POSTButton(
                url=self.request.route_path(
                    BUSINESS_PAYMENT_DEADLINE_ITEM_ROUTE,
                    id=self.context.model.id,
                    _query={"action": "delete"},
                ),
                label="",
                title="Supprimer cette échéance",
                icon="trash-alt",
                css="btn btn-danger icon only unstyled",
                confirm="Voulez-vous vraiment supprimer cette échéance ?",
            )

    def _get_main_links(self, business):

        if self.context.model.invoice:
            if not self.context.model.invoiced:
                yield Link(
                    url=get_task_url(self.request, self.context.model.invoice),
                    label="Voir la facture",
                    icon="file-invoice-euro",
                    css="btn small icon",
                )
            else:
                yield task_pdf_link(
                    self.request,
                    task=self.context.model.invoice,
                    link_options={
                        "css": "btn icon only",
                        "label": "",
                        "title": "Voir le PDF de cette facture",
                    },
                )
                yield Link(
                    get_task_url(self.request, self.context.model.invoice),
                    label="",
                    icon="arrow-right",
                    css="btn icon only",
                    title="Voir le détail de cette facture",
                )
        else:
            disabled = currently_invoicing(self.request, business)
            url = self.request.route_path(
                BUSINESS_ITEM_INVOICING_ROUTE,
                id=business.id,
                deadline_id=self.context.model.id,
            )
            if disabled:
                title = (
                    "Vous ne pouvez pas générer de nouvelle facture car "
                    "une facture est en cours d'édition"
                )
            else:
                title = "Générer la facture pour cette échéance"
            yield POSTButton(
                url=url,
                label="Facturer",
                title=title,
                icon="file-invoice-euro",
                css="btn btn-primary small icon",
                disabled=disabled,
            )

    def __call__(self, business=None, **options):
        css_data = self._get_css_data()
        return dict(
            title=self._get_title(),
            deadline=self.context,
            description=self._get_description(),
            main_links=list(self._get_main_links(business)),
            more_links=list(self._get_more_links()),
            **css_data,
        )


class BaseTaskTimelinePanelItem(BasePanel):
    template = "caerp:templates/panels/business/task_timeline_item.mako"

    def _get_title(self):
        return self.context.name

    def _get_description(self):
        return ""

    def _get_date_string(self):
        return self.context.date.strftime("%d/%m/%Y")

    def _get_main_links(self):
        yield task_pdf_link(
            self.request,
            task=self.context,
            link_options={
                "css": "btn icon only",
                "label": "",
                "title": "Voir le PDF de ce devis",
            },
        )
        yield Link(
            get_task_url(self.request, self.context),
            label="",
            icon="arrow-right",
            css="btn icon only",
            title="Voir le détail de ce devis",
        )

    def _get_status_css_data(self):
        result = {}
        if self.context.status == "draft":
            result["status_css"] = "draft"
            result["icon"] = "pen"

        elif self.context.status == "wait":
            result["status_css"] = "caution"
            result["icon"] = "clock"

        elif self.context.status == "invalid":
            result["status_css"] = "danger"
            result["icon"] = "times"
        else:
            result["status_css"] = "success"
            result["icon"] = "check"
        return result

    def _get_css_data(self):
        return self._get_status_css_data()

    def __call__(self, business=None, **options):
        css_data = self._get_css_data()
        return dict(
            task=self.context,
            title=self._get_title(),
            date_string=self._get_date_string(),
            main_links=list(self._get_main_links()),
            description=self._get_description(),
            **css_data,
        )


class EstimationTimelinePanelItem(BaseTaskTimelinePanelItem):
    def _get_title(self):
        prefix = ""
        if "devis" not in self.context.name.lower():
            prefix = "Devis : "
        return f"{prefix}{self.context.name}"

    def _get_description(self):
        return format_estimation_status(self.context, full=True)

    def _get_date_string(self):
        result = super()._get_date_string()
        return f"Devis {self.context.internal_number} daté du {result}"

    def _get_css_data(self):
        result = self._get_status_css_data()
        if self.context.status == "valid":
            if self.context.signed_status == "aborted":
                result["status_css"] = "draft"
                result["icon"] = "times"
            elif self.context.signed_status == "signed" or self.context.geninv:
                result["status_css"] = "valid"
                if self.context.geninv:
                    result["icon"] = "euro-sign"
                else:
                    result["icon"] = "check"
            else:
                result["status_css"] = "valid"
                result["icon"] = "clock"

        return result


class InvoiceTimelinePanelItem(BaseTaskTimelinePanelItem):
    def _get_title(self):
        prefix = ""
        if "facture" not in self.context.name.lower():
            prefix = "Facture : "

        result = f"{prefix}{self.context.name}"
        if self.context.official_number:
            result += f" - N°{self.context.official_number}"
        return result

    def _get_description(self):
        return format_invoice_status(self.context, full=True)

    def _get_date_string(self):
        date_string = super()._get_date_string()
        result = f"Facturé le {date_string}"
        return result

    def _get_css_data(
        self,
    ):
        result = self._get_status_css_data()

        if self.context.status == "valid":
            if self.context.paid_status == "resulted":
                result["icon"] = "euro-sign"
                return result
            elif self.context.paid_status == "paid":
                result["icon"] = "euro-slash"
            else:
                result["icon"] = "check"
        if self.context.cancelinvoices:
            result["status_css"] = "draft"
        return result


class CancelInvoiceTimelinePanelItem(BaseTaskTimelinePanelItem):
    def _get_title(self):
        prefix = ""
        if "avoir" not in self.context.name.lower():
            prefix = "Avoir : "

        result = f"{prefix}{self.context.name}"
        if self.context.official_number:
            result += f" - N°{self.context.official_number}"
        return result

    def _get_description(self):
        return format_cancelinvoice_status(self.context, full=True)

    def _get_date_string(self):
        date_string = super()._get_date_string()
        result = f"Avoir daté du {date_string}"
        return result


class ActionTimeLineItemPanel(BasePanel):
    """Render an Action as a timeline item"""

    template = "caerp:templates/panels/business/button_timeline_item.mako"

    def __call__(self, business=None, **options):
        status_css = "caution"
        time_css = "current"
        if self.context.button.disabled:
            status_css = "draft"
            time_css = "future"
        if self.context.reduced:
            li_css = "action reduced"
        else:
            li_css = "action"
        return {
            "title": self.context.title,
            "description": self.context.description,
            "button": self.context.button,
            "status_css": status_css,
            "time_css": time_css,
            "li_css": li_css,
            "plus_button": self.context.reduced,
        }


def includeme(config):
    for panel in (
        BusinessClassicTimelinePanel,
        BusinessProgressInvoicingTimeLinePanel,
    ):
        config.add_panel(
            panel,
            name=panel.panel_name,
            context=Business,
            renderer=panel.template,
        )

    for panel, context in (
        (BusinessPaymentDeadlineTimelinePanelItem, WrappedDeadline),
        (EstimationTimelinePanelItem, Estimation),
        (InvoiceTimelinePanelItem, Invoice),
        (CancelInvoiceTimelinePanelItem, CancelInvoice),
        (ActionTimeLineItemPanel, Action),
    ):
        config.add_panel(
            panel,
            name="timeline_item",
            context=context,
            renderer=panel.template,
        )
