"""
    Custom colander types
"""
import colander
from caerp.compute.math_utils import (
    amount,
    integer_to_amount,
)


def specialfloat(self, value):
    """
    preformat the value before passing it to the float function
    """
    if isinstance(value, (str, bytes)):
        value = value.replace("€", "").replace(",", ".").replace(" ", "")
    return float(value)


class QuantityType(colander.Number):
    """
    Preformat entry supposed to be numeric entries
    """

    num = specialfloat


class AmountType(colander.Number):
    """
    preformat an amount before considering it as a float object
    then *100 to store it into database
    """

    num = specialfloat

    def __init__(self, precision=2):
        colander.Number.__init__(self)
        self.precision = precision

    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null

        try:
            return str(integer_to_amount(self.num(appstruct), self.precision))
        except Exception:
            raise colander.Invalid(
                node,
                '"{val}" n\'est pas un montant valide'.format(val=appstruct),
            )

    def deserialize(self, node, cstruct):
        if cstruct != 0 and not cstruct:
            return colander.null

        try:
            return amount(self.num(cstruct), self.precision)
        except Exception:
            raise colander.Invalid(
                node, '"{val}" n\'est pas un montant valide'.format(val=cstruct)
            )


class Integer(colander.Number):
    """
    Fix https://github.com/Pylons/colander/pull/35
    """

    num = int

    def serialize(self, node, appstruct):
        if appstruct in (colander.null, None):
            return colander.null
        try:
            return str(self.num(appstruct))
        except Exception:
            raise colander.Invalid(
                node, "'${val}' n'est pas un nombre".format(val=appstruct)
            )


class CsvTuple(colander.SchemaType):
    def serialize(self, node, appstruct):
        if appstruct in (colander.null, None):
            return colander.null
        return tuple((a for a in appstruct.split(",") if a))

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null

        if not colander.is_nonstr_iter(cstruct):
            raise colander.Invalid(
                node,
                colander._("${cstruct} is not iterable", mapping={"cstruct": cstruct}),
            )

        return ",".join(cstruct)
