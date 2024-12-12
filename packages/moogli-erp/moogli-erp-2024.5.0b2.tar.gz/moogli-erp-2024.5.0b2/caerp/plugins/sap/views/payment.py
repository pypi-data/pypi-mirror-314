from caerp.views.payment.invoice import InvoicePaymentAddView
from caerp.consts.permissions import PERMISSIONS
from ..forms.tasks.payment import get_sap_payment_schema


class SAPInvoicePaymentAddView(InvoicePaymentAddView):
    @staticmethod
    def schema_factory(*args, **kwargs):
        return get_sap_payment_schema(*args, **kwargs)


def includeme(config):
    config.add_view(
        SAPInvoicePaymentAddView,
        route_name="/invoices/{id}/addpayment",
        permission=PERMISSIONS["context.add_payment_invoice"],
        renderer="base/formpage.mako",
    )
