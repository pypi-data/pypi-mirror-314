import datetime
import logging

from caerp.consts.permissions import PERMISSIONS
from pyramid.httpexceptions import HTTPFound
from deform_extensions import GridFormWidget
from caerp.controllers.state_managers.payment import check_node_resulted

from caerp.models.services.user import UserPrefsService

from caerp.forms.tasks.payment import (
    get_form_grid_from_request,
    get_payment_schema,
)

from caerp.models.task.payment import BaseTaskPayment
from caerp.models.task import Invoice
from caerp.utils.widgets import Link
from caerp.utils.strings import format_amount

from caerp.interfaces import IPaymentRecordService

from caerp.export.task_pdf import ensure_task_pdf_persisted

from caerp.events.document_events import StatusChangedEvent

from caerp.views import (
    BaseFormView,
    BaseView,
    PopupMixin,
    TreeMixin,
    submit_btn,
    cancel_btn,
)
from caerp.views.task.utils import get_task_url
from caerp.views.invoices.invoice import InvoicePaymentView as InvoicePaymentTabView
from .base import (
    BasePaymentDeleteView,
    BasePaymentEditView,
    PaymentRemittanceMixin,
    get_delete_confirm_message,
    get_warning_message,
)


logger = logging.getLogger(__name__)


class InvoicePaymentView(BaseView, TreeMixin):
    """
    Simple payment view
    """

    route_name = "payment"

    @property
    def tree_url(self):
        return self.request.route_path("payment", id=self.context.id)

    @property
    def title(self):
        return "Paiement pour la facture {0}".format(
            self.context.task.official_number,
        )

    def stream_actions(self):
        parent_url = get_task_url(self.request, self.context.task, suffix="/general")
        if self.request.has_permission(PERMISSIONS["context.edit_payment"]):
            _query = dict(action="edit")
            if self.request.is_popup:
                _query["popup"] = 1

            edit_url = self.request.route_path(
                "payment", id=self.context.id, _query=_query
            )

            yield Link(
                edit_url,
                label="Modifier",
                title="Modifier les informations du paiement",
                icon="pen",
                css="btn btn-primary",
            )
        if self.request.has_permission(PERMISSIONS["context.delete_payment"]):
            _query = dict(action="delete", come_from=parent_url)
            if self.request.is_popup:
                _query["popup"] = 1

            confirm = get_delete_confirm_message(self.context, "encaissement", "cet")
            yield Link(
                self.request.route_path(
                    "payment",
                    id=self.context.id,
                    _query=_query,
                ),
                label="Supprimer",
                title="Supprimer le paiement",
                icon="trash-alt",
                confirm=confirm,
                css="negative",
            )
        if self.request.has_permission(PERMISSIONS["context.gen_inverse_payment"]):
            _query = dict(action="gen_inverse")
            if self.request.is_popup:
                _query["popup"] = 1

            yield Link(
                self.request.route_path("payment", id=self.context.id, _query=_query),
                label="Annuler",
                title="Génère un encaissement négatif annulant comptablement celui-ci",
                icon="exchange",
                css="btn-primary negative",
            )

    def get_export_button(self):
        if not self.request.has_permission(PERMISSIONS["global.manage_accounting"]):
            return
        if self.context.exported:
            label = "Forcer l'export des écritures pour cet encaissement"
        else:
            label = "Générer les écritures pour cet encaissement"

        return Link(
            self.request.route_path(
                "/export/treasury/payments/{id}",
                id=self.context.id,
                _query=dict(come_from=self.tree_url, force=True),
            ),
            label=label,
            title=label,
            icon="file-export",
            css="btn btn-primary",
        )

    def __call__(self):
        self.populate_navigation()
        return dict(
            title=self.title,
            actions=self.stream_actions(),
            export_button=self.get_export_button(),
            money_flow_type="Cet encaissement",
            document_number=f"Facture {self.context.task.official_number}",
        )


class InvoicePaymentAddView(BaseFormView, PaymentRemittanceMixin, TreeMixin):
    buttons = (submit_btn, cancel_btn)
    add_template_vars = (
        "help_message",
        "error_msg",
        "warn_message",
    )
    route_name = "/invoices/{id}/addpayment"

    def __init__(self, context, request=None):
        super().__init__(context, request)
        self.error_msg = None
        self._warn_message = None

    @property
    def title(self):
        return (
            "Enregistrer un encaissement pour la facture "
            "{0.official_number}".format(self.context)
        )

    @property
    def help_message(self):
        return (
            "Enregistrer un paiement pour la facture {0} dont le montant "
            "ttc restant à payer est de {1} €".format(
                self.context.official_number,
                format_amount(self.context.topay(), precision=5),
            )
        )

    @property
    def warn_message(self):
        if getattr(self, "_warn_message", None) is not None:
            return self._warn_message

    def get_schema(self):
        return self.schema_factory()

    def before(self, form):
        BaseFormView.before(self, form)
        self.populate_navigation()
        appstruct = {"amount": self.context.topay()}
        form.set_appstruct(appstruct)
        grid = get_form_grid_from_request(self.request)
        form.widget = GridFormWidget(named_grid=grid)

    def redirect(self):
        return HTTPFound(
            self.request.route_path(
                "/invoices/{id}/payment",
                id=self.context.id,
            )
        )

    def notify(self):
        self.request.registry.notify(
            StatusChangedEvent(
                self.request,
                self.context,
                self.context.paid_status,
            )
        )

    def submit_success(self, appstruct):
        """
        Launched when the form was successfully validated
        """
        logger.debug("Submitting a new Payment")
        # Vérification du numéro de remise
        if "bank_remittance_id" not in appstruct:
            remittance_id = ""
        else:
            remittance_check_return = self.check_payment_remittance(appstruct)
            remittance_id = appstruct["bank_remittance_id"]
            if remittance_check_return is not None:
                logger.debug("  + Returning a confirmation form")
                return remittance_check_return

        # Si on a pas d'erreur on continue le traitement
        if self.error_msg is None:
            logger.debug("  + There was no error checking payment remittance")
            # On s'assure qu'on a bien un pdf dans le cache
            ensure_task_pdf_persisted(self.context, self.request)
            # Enregistrement de l'encaissement
            payment_service = self.request.find_service(IPaymentRecordService)
            force_resulted = appstruct.pop("resulted", False)

            # Computing the resulting payment depending on what has already
            # been paid and the different TVA rates
            submitted_amount = appstruct["amount"]
            payments = self.context.compute_payments(submitted_amount)

            for payment in payments:
                # Construire un nouvel appstruct correspondant
                tva_payment = {}
                # BaseTaskPayment fields
                tva_payment["date"] = appstruct["date"]
                tva_payment["amount"] = payment["amount"]
                tva_payment["tva_id"] = payment["tva_id"]

                # Payment fields
                if "mode" in appstruct:
                    tva_payment["mode"] = appstruct["mode"]
                if "bank_id" in appstruct:
                    tva_payment["bank_id"] = appstruct.get("bank_id")
                if "bank_remittance_id" in appstruct:
                    tva_payment["bank_remittance_id"] = remittance_id
                if "check_number" in appstruct:
                    tva_payment["check_number"] = appstruct["check_number"]
                if "customer_bank_id" in appstruct:
                    tva_payment["customer_bank_id"] = appstruct["customer_bank_id"]
                if "issuer" in appstruct:
                    tva_payment["issuer"] = appstruct["issuer"]

                # Record the payment
                payment_service.add(self.context, tva_payment)

            check_node_resulted(
                self.request, self.context, force_resulted=force_resulted
            )
            self.context.historize_paid_status(self.request.identity)
            self.request.dbsession.merge(self.context)
            # Mémorisation du dernier numéro de remise utilisé
            UserPrefsService.set(self.request, "last_bank_remittance_id", remittance_id)
            # Notification et redirection
            self.notify()
            return self.redirect()
        else:
            logger.debug("  - There are error messages to display")

    def cancel_success(self, appstruct):
        return self.redirect()

    cancel_failure = cancel_success


class InvoicePaymentEditView(BasePaymentEditView, PaymentRemittanceMixin):
    title = "Modification d'un encaissement"
    add_template_vars = (
        "help_message",
        "error_msg",
        "warn_message",
    )
    route_name = "payment"

    def __init__(self, context, request=None):
        super().__init__(context, request)
        self.error_msg = None
        self._warn_message = None

    # TreeMixin properties
    @property
    def tree_url(self):
        return self.request.route_path("payment", id=self.context.id)

    def get_schema(self):
        return self.schema_factory()

    @property
    def help_message(self):
        return "Modifier le paiement pour la facture {0} d'un montant \
            de {1} €".format(
            self.context.invoice.official_number,
            format_amount(self.context.amount, precision=5),
        )

    @property
    def warn_message(self):
        # On passe par une variable privée pour permettre l'utilisation d'une property
        # qui sera donc calculée dynamiquement
        if getattr(self, "_warn_message", None) is not None:
            return self._warn_message
        return get_warning_message(self.context, "encaissement", "cet")

    def before(self, form):
        super().before(form)
        grid = get_form_grid_from_request(self.request)
        form.widget = GridFormWidget(named_grid=grid)
        return form

    def edit_payment(self, appstruct):
        payment_service = self.request.find_service(IPaymentRecordService)
        # update the payment
        payment = payment_service.update(self.context, appstruct)
        return payment

    def after_parent_save(self, parent):
        # After Invoice has been saved, historize its status
        parent.historize_paid_status(self.request.identity)

    def submit_success(self, appstruct):
        """
        handle successfull submission of the form

        Wraps standard submi_success method by adding the support for
        PaymentRemittance (Through the mixin)
        """
        logger.debug("Submitting a Payment edition")
        # Vérification du numéro de remise
        if (
            "bank_remittance_id" in appstruct
            and self.context.bank_remittance_id != appstruct["bank_remittance_id"]
        ):  # noqa
            remittance_check_return = self.check_payment_remittance(
                appstruct, self.context.bank_remittance_id
            )
            if remittance_check_return is not None:
                logger.debug("  + Returning a confirmation form")
                return remittance_check_return
        # Si on a pas d'erreur on continue le traitement
        if self.error_msg is None:
            logger.debug("  + There was no error checking payment remittance")
            return super().submit_success(appstruct)
        else:
            logger.debug("  - There are error messages to display")


class InvoicePaymentDeleteView(BasePaymentDeleteView):
    def on_after_delete(self):
        self.context.parent.historize_paid_status(self.request.identity)

    def delete_payment(self):
        """
        Delete the payment instance from the database
        """
        # On fait appel au pyramid_service définit pour l'interface
        # IPaymentRecordService (voir pyramid_services)
        # Il est possible de changer de service en en spécifiant un autre dans
        # le fichier .ini de l'application
        payment_service = self.request.find_service(IPaymentRecordService)
        payment_service.delete(self.context)

    def parent_url(self, parent_id):
        """
        Parent url to use if a come_from parameter is missing

        :param int parent_id: The id of the parent object
        :returns: The url to redirect to
        :rtype: str
        """
        return self.request.route_path("/invoices/{id}/payment", id=parent_id)


class GenInversePaymentView(BasePaymentEditView, PopupMixin):
    """
    Generate a payment canceling the original one (context)
    """

    @property
    def warn_message(self):
        return ""

    def get_schema(self):
        return get_payment_schema(gen_inverse_payment=True)

    def get_default_appstruct(self, submitted=None) -> dict:
        """
        Build a dict with the values used to generate a payment
        Uses submitted data to update the values if provided
        """
        result = {
            "date": datetime.date.today(),
            "amount": -1 * self.context.amount,
            "tva_id": self.context.tva_id,
        }
        for key in (
            "mode",
            "bank_id",
            "bank_remittance_id",
            "check_number",
            "customer_bank_id",
            "issuer",
        ):
            if hasattr(self.context, key):
                result[key] = getattr(self.context, key)
        if submitted and "date" in submitted:
            result["date"] = submitted["date"]
        return result

    def before(self, form):
        super().before(form)
        grid = get_form_grid_from_request(self.request)
        form.widget = GridFormWidget(named_grid=grid)

    def redirect(self, appstruct=None):
        if self.request.is_popup:
            self.add_popup_response()
            return self.request.response
        return HTTPFound(
            get_task_url(self.request, self.context.task, suffix="/payment")
        )

    def merge_appstruct(self, appstruct, model):
        """Generate a payment canceling the original one (context)"""
        task = self.context.task
        payment_service = self.request.find_service(IPaymentRecordService)
        payment_data = self.get_default_appstruct(submitted=appstruct)
        # Record the payment
        payment = payment_service.add(task, payment_data)

        check_node_resulted(self.request, task)
        task.historize_paid_status(self.request.identity)
        self.request.dbsession.merge(task)
        return payment


def includeme(config):
    config.add_tree_view(
        InvoicePaymentView,
        parent=InvoicePaymentTabView,
        permission=PERMISSIONS["company.view"],
        renderer="/payment.mako",
        context=BaseTaskPayment,
    )
    config.add_tree_view(
        InvoicePaymentAddView,
        parent=InvoicePaymentTabView,
        permission=PERMISSIONS["context.add_payment_invoice"],
        renderer="base/formpage.mako",
        context=Invoice,
    )
    config.add_tree_view(
        InvoicePaymentEditView,
        parent=InvoicePaymentView,
        permission=PERMISSIONS["context.edit_payment"],
        request_param="action=edit",
        renderer="/base/formpage.mako",
        context=BaseTaskPayment,
    )
    config.add_view(
        InvoicePaymentDeleteView,
        route_name="payment",
        permission=PERMISSIONS["context.delete_payment"],
        request_param="action=delete",
        context=BaseTaskPayment,
    )
    config.add_view(
        GenInversePaymentView,
        route_name="payment",
        request_param="action=gen_inverse",
        permission=PERMISSIONS["context.gen_inverse_payment"],
        renderer="/base/formpage.mako",
        context=BaseTaskPayment,
    )
