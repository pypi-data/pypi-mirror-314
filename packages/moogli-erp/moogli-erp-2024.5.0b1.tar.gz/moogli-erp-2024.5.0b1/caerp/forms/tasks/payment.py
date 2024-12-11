"""
    form schemas for invoices related views
"""
import colander
import deform

from caerp.models.payments import (
    BankAccount,
)
from caerp.consts import (
    AMOUNT_PRECISION,
    PAYMENT_EPSILON,
)
from caerp.models.task.invoice import Invoice
from caerp.utils.strings import format_amount
from caerp import forms
from caerp.forms.custom_types import AmountType
from caerp.forms.payments import (
    get_amount_topay,
    deferred_amount_default,
    deferred_payment_mode_widget,
    deferred_payment_mode_validator,
    deferred_bank_account_widget,
    deferred_bank_account_validator,
    deferred_customer_bank_widget,
    deferred_customer_bank_validator,
)

PAYMENT_GRID = (
    (("date", 6),),
    (
        ("mode", 6),
        ("amount", 6),
    ),
    (
        ("bank_remittance_id", 6),
        ("bank_id", 6),
    ),
    (("check_number", 6),),
    (
        ("customer_bank_id", 6),
        ("issuer", 6),
    ),
    (("resulted", 12),),
)
INTERNAL_PAYMENT_GRID = (
    (
        ("date", 6),
        ("amount", 6),
    ),
    (("resulted", 12),),
)


def get_invoice_from_context(request):
    if isinstance(request.context, Invoice):
        return request.context
    else:
        return request.context.invoice


def get_form_grid_from_request(request):
    invoice = get_invoice_from_context(request)
    if invoice.internal:
        return INTERNAL_PAYMENT_GRID
    else:
        return PAYMENT_GRID


@colander.deferred
def deferred_bank_remittance_id_default(node, kw):
    """
    Default value for the bank remittance id
    """
    from caerp.models.services.user import UserPrefsService

    id = UserPrefsService.get(kw["request"], "last_bank_remittance_id")
    if id is None:
        return ""
    else:
        return id


@colander.deferred
def deferred_issuer_default(node, kw):
    """
    Default value for payment's issuer
    """
    invoice = get_invoice_from_context(kw["request"])
    return invoice.customer.label


@colander.deferred
def deferred_total_validator(node, kw):
    """
    Validate the amount to keep the sum under the total
    """
    topay = get_amount_topay(kw)

    # We insert a large epsilon to allow larger payments to be registered
    if topay < 0:
        min_value = topay - PAYMENT_EPSILON
        max_value = 0
        min_msg = "Le montant ne peut être inférieur à {}".format(
            format_amount(min_value, precision=AMOUNT_PRECISION, grouping=False)
        )
        max_msg = "Le montant doit être négatif"
    else:
        min_value = 0
        max_value = topay + PAYMENT_EPSILON
        min_msg = "Le montant doit être positif"
        max_msg = "Le montant ne doit pas dépasser {} (total TTC - somme \
        des paiements + montant d'un éventuel avoir)".format(
            format_amount(topay, precision=AMOUNT_PRECISION, grouping=False)
        )
    return colander.Range(
        min=min_value,
        max=max_value,
        min_err=min_msg,
        max_err=max_msg,
    )


class PaymentSchema(colander.MappingSchema):
    """
    colander schema for payment recording
    """

    come_from = forms.come_from_node()
    date = forms.today_node()
    amount = colander.SchemaNode(
        AmountType(5),
        title="Montant de l'encaissement",
        description="En cas d'encaissement partiel d'une facture avec la"
        " présence de plusieurs taux de TVA, la TVA sera ventilée au prorata"
        " du montant du paiement, soit un encaissement par taux de TVA.",
        validator=deferred_total_validator,
        default=deferred_amount_default,
    )
    mode = colander.SchemaNode(
        colander.String(),
        title="Mode de paiement",
        widget=deferred_payment_mode_widget,
        validator=deferred_payment_mode_validator,
    )
    issuer = colander.SchemaNode(
        colander.String(),
        title="Émetteur du paiement",
        default=deferred_issuer_default,
    )
    customer_bank_id = colander.SchemaNode(
        colander.Integer(),
        title="Banque de l'émetteur du paiement",
        widget=deferred_customer_bank_widget,
        validator=deferred_customer_bank_validator,
        missing=colander.drop,
    )
    check_number = colander.SchemaNode(
        colander.String(),
        title="Numéro de chèque",
        validator=forms.max_len_validator(50),
        missing=colander.drop,
    )
    bank_remittance_id = colander.SchemaNode(
        colander.String(),
        title="Numéro de remise en banque",
        description="Permet d'associer cet encaissement à une "
        "remise en banque (laisser vide si pas de remise)",
        default=deferred_bank_remittance_id_default,
        validator=forms.max_len_validator(255),
        missing=colander.drop,
    )
    bank_id = colander.SchemaNode(
        colander.Integer(),
        title="Compte bancaire",
        widget=deferred_bank_account_widget,
        validator=deferred_bank_account_validator,
        default=forms.get_deferred_default(BankAccount),
        description="Configurables dans Configuration - Module Ventes - "
        "Configuration comptable des encaissements",
    )
    resulted = colander.SchemaNode(
        colander.Boolean(),
        title=None,
        label="Soldée",
        description="Indique que la facture est soldée (ne recevra plus "
        "de paiement), si le montant indiqué correspond au montant "
        "de la facture celle-ci est soldée automatiquement",
        default=False,
        missing=False,
    )


def remove_attrs_on_internal_payment(schema, kw):
    """
    After schema attributes not used for internal payments
    """
    invoice = get_invoice_from_context(kw["request"])
    if invoice.internal:
        for field in [
            "mode",
            "issuer",
            "customer_bank_id",
            "check_number",
            "bank_remittance_id",
            "bank_id",
        ]:
            del schema[field]


def get_payment_schema(
    with_new_remittance_confirm: bool = False, gen_inverse_payment: bool = False
):
    """
    Returns the schema for payment registration

    :param with_new_remittance_confirm: if True, a new remittance confirmation field is added
    :param gen_inverse_payment: if True, some fields are made read-only
    """
    schema = PaymentSchema().clone()

    schema.after_bind = remove_attrs_on_internal_payment
    if with_new_remittance_confirm:
        schema.add_before(
            "bank_id",
            colander.SchemaNode(
                colander.Boolean(),
                name="new_remittance_confirm",
                title="",
                label="Confirmer la création de cette remise en banque",
                default=False,
                missing=False,
                widget=deform.widget.HiddenWidget(),
            ),
        )

    if gen_inverse_payment:
        for field in [
            "amount",
            "mode",
            "issuer",
            "customer_bank_id",
            "check_number",
            "bank_remittance_id",
            "bank_id",
        ]:
            if field in schema:
                schema[field].widget = deform.widget.TextInputWidget(readonly=True)
                schema[field].validator = None
                schema[field].description = None
                schema[field].missing = colander.drop

    return schema
