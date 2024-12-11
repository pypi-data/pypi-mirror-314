"""
    Invoice's payment model
"""
import logging
import datetime
from itertools import groupby
from operator import itemgetter

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    BigInteger,
    Boolean,
    String,
    ForeignKey,
    extract,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from caerp_base.models.base import (
    DBBASE,
    default_table_args,
)
from caerp_base.models.mixins import (
    TimeStampedMixin,
)
from caerp.compute.math_utils import (
    integer_to_amount,
    compute_tva_from_ttc,
)
from caerp.models.export.accounting_export_log import (
    payment_accounting_export_log_entry_association_table,
)

logger = logging.getLogger(__name__)


class BaseTaskPayment(TimeStampedMixin, DBBASE):
    __tablename__ = "base_task_payment"
    __table_args__ = default_table_args
    __mapper_args__ = {
        "polymorphic_on": "type_",
        "polymorphic_identity": "base_task_payment",
    }
    internal = False
    precision = 5

    id = Column(Integer, primary_key=True)
    # Le type du paiement (permet de les différencier via le polymorphisme)
    type_ = Column(
        "type_",
        String(30),
        info={"colanderalchemy": {"exclude": True}},
        nullable=False,
    )
    task_id = Column(
        Integer,
        ForeignKey("task.id", ondelete="cascade"),
        info={"colanderalchemy": {"title": "Identifiant du document"}},
    )
    date = Column(
        DateTime(),
        default=datetime.datetime.now,
        info={"colanderalchemy": {"title": "Date de remise"}},
    )
    amount = Column(
        BigInteger(),
        info={"colanderalchemy": {"title": "Montant"}},
    )

    tva_id = Column(
        ForeignKey("tva.id"),
        info={"colanderalchemy": {"title": "Tva associée à ce paiement"}},
        nullable=True,
    )
    user_id = Column(
        ForeignKey("accounts.id", ondelete="set null"),
        info={"colanderalchemy": {"title": "Utilisateur"}},
    )
    exported = Column(Boolean(), default=False)
    # relationships
    user = relationship(
        "User",
        info={"colanderalchemy": {"exclude": True}},
    )
    tva = relationship("Tva", info={"colanderalchemy": {"exclude": True}})
    task = relationship(
        "Task",
        primaryjoin="Task.id==BaseTaskPayment.task_id",
        back_populates="payments",
    )
    exports = relationship(
        "PaymentAccountingExportLogEntry",
        secondary=payment_accounting_export_log_entry_association_table,
        back_populates="exported_payments",
    )

    # Usefull aliases
    @hybrid_property
    def year(self):
        return self.date.year

    @year.expression
    def year(cls):
        return extract("year", cls.date)

    @property
    def invoice(self):
        return self.task

    @property
    def parent(self):
        return self.task

    def get_amount(self) -> int:
        return self.amount

    def get_tva_amount(self) -> float:
        return compute_tva_from_ttc(self.amount, self.tva.value, float_format=False)

    def get_company_id(self) -> int:
        return self.task.company_id


class Payment(BaseTaskPayment):
    """
    Payment entry
    """

    __tablename__ = "payment"
    __table_args__ = default_table_args
    __mapper_args__ = {"polymorphic_identity": "payment"}
    id = Column(
        ForeignKey("base_task_payment.id", ondelete="CASCADE"),
        primary_key=True,
        info={"colanderalchemy": {"exclude": True}},
    )
    bank_id = Column(
        ForeignKey("bank_account.id"),
        info={"colanderalchemy": {"title": "Compte bancaire"}},
    )
    issuer = Column(
        String(255),
        info={"colanderalchemy": {"title": "Émetteur du paiement"}},
    )
    customer_bank_id = Column(
        ForeignKey("bank.id"),
        info={"colanderalchemy": {"title": "Banque de l'émetteur du paiement"}},
        nullable=True,
    )
    check_number = Column(
        String(50),
        info={"colanderalchemy": {"title": "Numéro de chèque"}},
        nullable=True,
    )
    bank_remittance_id = Column(
        String(255),
        ForeignKey("bank_remittance.id"),
        nullable=True,
        info={"colanderalchemy": {"title": "Identifiant de remise en banque"}},
    )
    mode = Column(String(50))

    # relationships
    bank = relationship(
        "BankAccount",
        back_populates="payments",
        info={"colanderalchemy": {"exclude": True}},
    )
    customer_bank = relationship("Bank", info={"colanderalchemy": {"exclude": True}})
    bank_remittance = relationship(
        "BankRemittance",
        primaryjoin="BankRemittance.id==Payment.bank_remittance_id",
    )

    def __str__(self):
        return (
            "<Payment id:{s.id} task_id:{s.task_id} amount:{s.amount} mode:{s.mode}"
            " date:{s.date}".format(s=self)
        )

    def __json__(self, request):
        bank = self.customer_bank
        if bank:
            label = self.customer_bank.label
        else:
            label = ""
        return dict(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            mode=self.mode,
            amount=integer_to_amount(self.amount, self.precision),
            bank_remittance_id=self.bank_remittance_id,
            label=self.bank_remittance_id,
            date=self.date,
            exported=self.exported,
            task_id=self.task_id,
            bank_id=self.bank_id,
            bank=self.bank.label,
            tva_id=self.tva_id,
            tva=integer_to_amount(self.tva.value, 2),
            user_id=self.user_id,
            customer_bank_id=self.customer_bank_id,
            customer_bank=label,
            check_number=self.check_number,
            issuer=self.issuer,
        )


class BankRemittance(TimeStampedMixin, DBBASE):
    """
    Remises en banque
    """

    __tablename__ = "bank_remittance"
    __table_args__ = default_table_args
    id = Column(
        "id",
        String(255),
        primary_key=True,
        info={"colanderalchemy": {"title": "Numéro de remise"}},
    )
    payment_mode = Column(String(120), info={"colanderalchemy": {"title": "Type"}})
    bank_id = Column(
        Integer,
        ForeignKey("bank_account.id"),
        info={"export": {"exclude": True}},
        nullable=True,
    )
    remittance_date = Column(
        DateTime(),
        info={"colanderalchemy": {"title": "Date de remise"}},
        nullable=True,
    )
    closed = Column(
        Boolean(),
        info={"colanderalchemy": {"exclude": True}},
    )

    bank = relationship(
        "BankAccount",
        primaryjoin="BankAccount.id==BankRemittance.bank_id",
        info={"colanderalchemy": {"exclude": True}},
    )
    payments = relationship(
        "Payment",
        primaryjoin="Payment.bank_remittance_id==BankRemittance.id",
        order_by="Payment.date",
        back_populates="bank_remittance",
        info={"colanderalchemy": {"exclude": True}},
    )

    def get_total_amount(self):
        total_amount = 0
        for payment in self.payments:
            total_amount += payment.amount
        return total_amount

    def is_exported(self):
        for payment in self.payments:
            if payment.exported == 0:
                return False
        return True

    def get_grouped_payments(self):
        """
        Retourne la liste des encaissements d'une remise groupés par
        pièce (eg: chèque qui règle plusieurs factures) pour les exports
        """
        payments_list = []
        for payment in self.payments:
            bank_label = ""
            if payment.customer_bank:
                bank_label = payment.customer_bank.label
            payment_detail = {
                "id": payment.id,
                "date": payment.date,
                "bank_label": bank_label,
                "issuer": payment.issuer,
                "check_number": payment.check_number,
                "invoice_ref": payment.task.get_main_sequence_number(),
                "code_compta": payment.task.company.code_compta,
                "amount": payment.amount,
            }
            payments_list.append(payment_detail)
        grouper = itemgetter(
            "date", "bank_label", "issuer", "check_number", "code_compta"
        )
        grouped_payments = []
        sorted_payments = sorted(payments_list, key=itemgetter("date", "id"))
        for key, grp in groupby(sorted_payments, grouper):
            temp_dict = dict(
                list(
                    zip(
                        ["date", "bank_label", "issuer", "check_number", "code_compta"],
                        key,
                    )
                )
            )
            temp_dict["invoice_ref"] = ""
            temp_dict["amount"] = 0
            for item in grp:
                ref = "{} + ".format(item["invoice_ref"])
                if temp_dict["invoice_ref"] != ref:
                    temp_dict["invoice_ref"] += ref
                temp_dict["amount"] += item["amount"]
            if len(temp_dict["invoice_ref"]) > 3:
                temp_dict["invoice_ref"] = temp_dict["invoice_ref"][0:-3]
            grouped_payments.append(temp_dict)
        return grouped_payments

    def __json__(self, request):
        return dict(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            payment_mode=self.payment_mode,
            bank_id=self.bank_id,
            remittance_date=self.remittance_date,
            closed=self.closed,
            bank=self.bank.label,
            payments=[payment.__json__(request) for payment in self.payments],
            total_amount=integer_to_amount(self.get_total_amount(), 5),
            exported=self.is_exported(),
        )
