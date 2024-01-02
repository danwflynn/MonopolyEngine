from space import Space
from enum import Enum


class TaxType(Enum):
    INCOME_TAX = "Income Tax"
    LUXURY_TAX = "Luxury Tax"


class Tax(Space):
    def __init__(self, tax_type: TaxType):
        super().__init__(tax_type.value)
        self.tax_type = tax_type
        self.tax = 75 if tax_type == TaxType.LUXURY_TAX else 200
