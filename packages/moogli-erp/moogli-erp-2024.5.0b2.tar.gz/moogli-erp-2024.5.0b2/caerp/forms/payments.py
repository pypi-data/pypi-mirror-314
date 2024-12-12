import colander
import deform

from caerp.models.payments import (
    PaymentMode,
    BankAccount,
    Bank,
)
from caerp.models.task import Invoice
from caerp.models.expense.sheet import ExpenseSheet
from caerp.models.supply.supplier_invoice import SupplierInvoice

from caerp import forms


def get_amount_topay(kw):
    """
    Retrieve the amount to be paid regarding the context
    """
    topay = 0
    context = kw["request"].context
    if isinstance(context, (Invoice, ExpenseSheet, SupplierInvoice)):
        topay = context.topay()
    else:
        if hasattr(context, "parent"):
            document = context.parent
            if hasattr(document, "topay"):
                topay = document.topay()
                if hasattr(context, "get_amount"):
                    topay += context.get_amount()
    return topay


@colander.deferred
def deferred_amount_default(node, kw):
    """
    default value for the payment amount
    """
    topay = get_amount_topay(kw)

    # Avoid pre-filling the <input> with "0.0", as
    # to have less clicks to do.
    if topay == 0:
        topay = colander.null
    return topay


@colander.deferred
def deferred_payment_mode_widget(node, kw):
    """
    dynamically retrieves the payment modes
    """
    modes = [(mode.label, mode.label) for mode in PaymentMode.query()]
    return deform.widget.SelectWidget(values=modes)


@colander.deferred
def deferred_payment_mode_validator(node, kw):
    return colander.OneOf([mode.label for mode in PaymentMode.query()])


@colander.deferred
def deferred_bank_account_widget(node, kw):
    """
    Renvoie le widget pour la sélection d'un compte bancaire
    """
    options = [(bank.id, bank.label) for bank in BankAccount.query()]
    widget = forms.get_select(options)
    return widget


@colander.deferred
def deferred_bank_account_validator(node, kw):
    return colander.OneOf([bank.id for bank in BankAccount.query()])


@colander.deferred
def deferred_customer_bank_widget(node, kw):
    """
    Renvoie le widget pour la sélection d'une banque client
    """
    options = [(bank.id, bank.label) for bank in Bank.query()]
    options.insert(0, ("", ""))
    widget = forms.get_select(options)
    return widget


@colander.deferred
def deferred_customer_bank_validator(node, kw):
    return colander.OneOf([bank.id for bank in Bank.query()])
