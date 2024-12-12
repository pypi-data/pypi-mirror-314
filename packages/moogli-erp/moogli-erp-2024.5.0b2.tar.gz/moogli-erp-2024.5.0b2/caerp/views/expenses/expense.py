"""
    Expense handling view
"""
import logging
from caerp.consts.permissions import PERMISSIONS
from typing import Dict

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPForbidden,
)

from caerp.forms.expense import get_add_edit_sheet_schema
from caerp.forms.files import get_file_upload_schema

from caerp.utils import strings
from caerp.models.company import Company
from caerp.models.expense.sheet import (
    ExpenseKmLine,
    ExpenseLine,
    ExpenseSheet,
    get_expense_sheet_name,
)
from caerp.models.expense.types import (
    ExpenseTelType,
)
from caerp.models.user.user import User
from caerp.utils.image import ImageResizer
from caerp.utils.widgets import (
    ViewLink,
)
from caerp.export.expense_excel import (
    XlsExpense,
)
from caerp.export.excel import (
    make_excel_view,
)
from caerp.resources import (
    expense_resources,
)
from caerp.views import (
    BaseFormView,
    BaseView,
    DeleteView,
    JsAppViewMixin,
    TreeMixin,
)
from caerp.views.files.routes import NODE_FILE_API
from caerp.views.render_api import (
    month_name,
    format_account,
)
from caerp.views.files.views import (
    FileUploadView,
)

logger = logging.getLogger(__name__)


def get_expense_sheet(year, month, cid, uid):
    """
    Return the expense sheet for the given 4-uple
    """
    return (
        ExpenseSheet.query()
        .filter(ExpenseSheet.year == year)
        .filter(ExpenseSheet.month == month)
        .filter(ExpenseSheet.company_id == cid)
        .filter(ExpenseSheet.user_id == uid)
        .first()
    )


def get_new_expense_sheet(year, month, title, cid, uid):
    """
    Return a new expense sheet for the given 4-uple
    """
    expense = ExpenseSheet()
    expense.name = get_expense_sheet_name(month, year)
    expense.year = year
    expense.month = month
    expense.title = title
    expense.company_id = cid
    expense.user_id = uid
    query = ExpenseTelType.query()
    query = query.filter(ExpenseTelType.active == True)  # noqa
    teltypes = query.filter(ExpenseTelType.initialize == True)  # noqa
    for type_ in teltypes:
        line = ExpenseLine(type_id=type_.id, ht=0, tva=0, description=type_.label)
        expense.lines.append(line)
    return expense


def get_redirect_btn(request, id_):
    """
    Button for "go back to project" link
    """


def populate_actionmenu(request, tolist=False):
    """
    Add buttons in the request actionmenu attribute
    """
    link = None
    if isinstance(request.context, Company):
        link = ViewLink(
            "Revenir à la liste des notes de dépenses",
            path="company_expenses",
            id=request.context.id,
        )
    elif isinstance(request.context, ExpenseSheet):
        if tolist:
            link = ViewLink(
                "Revenir à la liste des notes de dépenses",
                path="company_expenses",
                id=request.context.company_id,
            )
        else:
            link = ViewLink(
                "Revenir à la note de dépenses",
                path="/expenses/{id}",
                id=request.context.id,
            )
    if link is not None:
        request.actionmenu.add(link)


def get_formatted_user_vehicle_information_sentence(
    vehicle_fiscal_power, vehicle_registration
):
    """
    Return a formatted sentence with vehicle information
    :param vehicle_fiscal_power:
    :param vehicle_registration:
    :return: String
    """
    formatted_sentence = ""
    sentence = []
    if vehicle_fiscal_power:
        sentence.append("Puissance fiscale {}CV ".format(vehicle_fiscal_power))
    if vehicle_registration:
        sentence.append("Plaque {}".format(vehicle_registration))
    if len(sentence) > 0:
        formatted_sentence = "({})".format(";".join(sentence))
    return formatted_sentence


class ExpenseSheetAddView(BaseFormView):
    """
    A simple expense sheet add view
    """

    schema = get_add_edit_sheet_schema()

    @property
    def title(self):
        if isinstance(self.context, User):
            user = self.context
        else:
            user = User.get(self.request.matchdict["uid"])
        return "Ajouter une note de dépenses ({})".format(
            user.label,
        )

    def before(self, form):
        populate_actionmenu(self.request)

    def redirect(self, sheet):
        return HTTPFound(self.request.route_path("/expenses/{id}", id=sheet.id))

    def create_instance(self, appstruct):
        """
        Create a new expense sheet instance
        """
        year = appstruct["year"]
        month = appstruct["month"]
        title = None
        if "title" in appstruct:
            title = appstruct["title"]
        if isinstance(self.context, Company):
            company_id = self.context.id
            user_id = self.request.matchdict["uid"]
        elif isinstance(self.context, User):
            if len(self.context.companies) > 0:
                company_id = self.context.companies[0].id
                user_id = self.context.id
            else:
                raise HTTPForbidden()
        else:
            raise HTTPForbidden()
        result = get_new_expense_sheet(year, month, title, company_id, user_id)
        return result

    def submit_success(self, appstruct):
        sheet = self.create_instance(appstruct)
        self.dbsession.add(sheet)
        self.dbsession.flush()
        return self.redirect(sheet)

    def submit_failure(self, e):
        BaseFormView.submit_failure(self, e)


class ExpenseSheetEditInfosView(BaseFormView):
    """
    Expense sheet edit infos (year, month, title) view
    """

    schema = get_add_edit_sheet_schema()

    @property
    def title(self):
        return "Modification de la note de dépenses de {0} pour la période de {1} {2}".format(
            format_account(self.request.context.user),
            month_name(self.context.month),
            self.context.year,
        )

    def before(self, form):
        populate_actionmenu(self.request)
        form.set_appstruct(
            {
                "month": self.context.month,
                "year": self.context.year,
                "title": self.context.title if self.context.title else "",
            }
        )

    def redirect(self, sheet):
        return HTTPFound(self.request.route_path("/expenses/{id}", id=sheet.id))

    def submit_success(self, appstruct):
        sheet = self.context
        sheet.year = appstruct["year"]
        sheet.month = appstruct["month"]
        sheet.title = None
        if "title" in appstruct:
            sheet.title = appstruct["title"]
        self.dbsession.merge(sheet)
        self.dbsession.flush()
        return self.redirect(sheet)

    def submit_failure(self, e):
        BaseFormView.submit_failure(self, e)


class ExpenseSheetEditView(BaseView, JsAppViewMixin, TreeMixin):
    route_name = "/expenses/{id}"

    @property
    def tree_url(self):
        return self.request.route_path(self.route_name, id=self.current().id)

    @property
    def title(self):
        current = self.current()

        return "Note de dépenses de {0} pour la période de {1} {2}".format(
            format_account(current.user),
            month_name(current.month),
            current.year,
        )

    def current(self):
        """
        Renvoie le contexte pour la génération des informations de breadcrumb
        (title, tree_url)
        """
        if isinstance(self.context, ExpenseSheet):
            current = self.context
        elif hasattr(self.context, "parent"):
            current = self.context.parent
        else:
            raise Exception(
                f"No ExpenseSheet could be retrieved from context {self.context}"
            )
        return current

    def context_url(self, _query: Dict[str, str] = {}):
        return self.request.route_path(
            "/api/v1/expenses/{id}",
            id=self.request.context.id,
            _query=_query,
        )

    def more_js_app_options(self):
        logger.debug("more_js_app_options")

        result = super().more_js_app_options()
        result["file_upload_url"] = self.request.route_path(
            NODE_FILE_API, id=self.context.id
        )
        result["edit"] = False
        if self.request.has_permission(PERMISSIONS["context.edit_expensesheet"]):
            result["edit"] = True
        logger.debug(result)
        return result

    def __call__(self):
        populate_actionmenu(self.request, tolist=True)
        expense_resources.need()

        sheets = (
            ExpenseSheet.query()
            .filter(ExpenseSheet.year == self.context.year)
            .filter(ExpenseSheet.company_id == self.context.company_id)
            .filter(ExpenseSheet.user_id == self.context.user_id)
            .filter(ExpenseSheet.status == "valid")
            .filter(ExpenseSheet.kmlines.any())
        )
        sheets_id = [sheet.id for sheet in sheets.all()]
        kmlines = (
            ExpenseKmLine.query().filter(ExpenseKmLine.sheet_id.in_(sheets_id)).all()
        )
        kmlines_current_year = sum([line.km for line in kmlines])

        user_vehicle_information = get_formatted_user_vehicle_information_sentence(
            self.context.user.vehicle_fiscal_power,
            self.context.user.vehicle_registration,
        )
        ret = dict(
            kmlines_current_year=kmlines_current_year,
            context=self.context,
            title=self.title,
            status_history=self.context.statuses,
            user_vehicle_information=user_vehicle_information,
        )
        ret["js_app_options"] = self.get_js_app_options()
        logger.debug(ret)
        return ret


class ExpenseSheetDeleteView(DeleteView):
    """
    Expense deletion view

    Current context is an expensesheet
    """

    delete_msg = "La note de dépenses a bien été supprimée"

    def redirect(self):
        url = self.request.route_path("company_expenses", id=self.context.company.id)
        return HTTPFound(url)


class ExpenseSheetDuplicateView(BaseFormView):
    form_options = (("formid", "duplicate_form"),)
    schema = get_add_edit_sheet_schema()

    @property
    def title(self):
        return "Dupliquer la note de dépenses de {0} {1}".format(
            strings.month_name(self.context.month),
            self.context.year,
        )

    def before(self, form):
        populate_actionmenu(self.request)
        if self.context.title:
            form.set_appstruct({"title": "Copie de {}".format(self.context.title)})

    def redirect(self, sheet):
        return HTTPFound(self.request.route_path("/expenses/{id}", id=sheet.id))

    def submit_success(self, appstruct):
        logger.debug("# Duplicating an expensesheet #")
        sheet = self.context.duplicate(appstruct["year"], appstruct["month"])
        sheet.title = None
        if "title" in appstruct:
            sheet.title = appstruct["title"]
        self.dbsession.add(sheet)
        self.dbsession.flush()
        logger.debug(
            "ExpenseSheet {0} was duplicated to {1}".format(self.context.id, sheet.id)
        )
        return self.redirect(sheet)

    def submit_failure(self, e):
        BaseFormView.submit_failure(self, e)


def excel_filename(request):
    """
    return an excel filename based on the request context
    """
    exp = request.context
    filename = "ndf_{0}_{1}_{2}_{3}".format(
        exp.year,
        exp.month,
        exp.user.lastname,
        exp.user.firstname,
    )
    if exp.title:
        filename += "_{}".format(exp.title[:50])
    filename += ".xlsx"
    return filename


class ExpenseFileUploadView(FileUploadView):
    def get_schema(self):
        return get_file_upload_schema([ImageResizer(1200, 1200, "PDF")])


def add_routes(config):
    """
    Add module's related routes
    """
    config.add_route("expenses", "/expenses")

    config.add_route(
        "user_expenses", "/company/{id}/{uid}/expenses", traverse="/companies/{id}"
    )
    config.add_route(
        "user_expenses_shortcut", "/user_expenses/{id}", traverse="/users/{id}"
    )

    config.add_route(
        "/expenses/{id}",
        r"/expenses/{id:\d+}",
        traverse="/expenses/{id}",
    )

    for extension in ("xls",):
        config.add_route(
            "/expenses/{id}.xlsx",
            r"/expenses/{id:\d+}.xlsx",
            traverse="/expenses/{id}",
        )

    for action in (
        "delete",
        "duplicate",
        "addfile",
        "edit",
    ):
        config.add_route(
            "/expenses/{id}/%s" % action,
            r"/expenses/{id:\d+}/%s" % action,
            traverse="/expenses/{id}",
        )


def includeme(config):
    """
    Declare all the routes and views related to this module
    """
    add_routes(config)

    config.add_view(
        ExpenseSheetAddView,
        route_name="user_expenses",
        permission=PERMISSIONS["context.add_expensesheet"],
        renderer="base/formpage.mako",
        context=Company,
    )
    config.add_view(
        ExpenseSheetAddView,
        route_name="user_expenses_shortcut",
        permission=PERMISSIONS["global.access_ea"],
        renderer="base/formpage.mako",
        context=User,
    )

    config.add_tree_view(
        ExpenseSheetEditView,
        route_name="/expenses/{id}",
        renderer="expenses/expense.mako",
        permission=PERMISSIONS["company.view"],
        layout="opa",
        context=ExpenseSheet,
    )

    config.add_view(
        ExpenseSheetDeleteView,
        route_name="/expenses/{id}/delete",
        permission=PERMISSIONS["context.delete_expensesheet"],
        request_method="POST",
        require_csrf=True,
        context=ExpenseSheet,
    )

    config.add_view(
        ExpenseSheetDuplicateView,
        route_name="/expenses/{id}/duplicate",
        renderer="base/formpage.mako",
        # Cette permission est checkée au niveau de la company parente
        permission=PERMISSIONS["context.add_expensesheet"],
        context=ExpenseSheet,
    )

    # Xls export
    config.add_view(
        make_excel_view(excel_filename, XlsExpense),
        route_name="/expenses/{id}.xlsx",
        permission=PERMISSIONS["company.view"],
        context=ExpenseSheet,
    )
    # File attachment
    config.add_view(
        ExpenseFileUploadView,
        route_name="/expenses/{id}/addfile",
        renderer="base/formpage.mako",
        permission=PERMISSIONS["context.add_file"],
        context=ExpenseSheet,
    )

    config.add_view(
        ExpenseSheetEditInfosView,
        route_name="/expenses/{id}/edit",
        permission=PERMISSIONS["context.edit_expensesheet"],
        renderer="base/formpage.mako",
        context=ExpenseSheet,
    )
