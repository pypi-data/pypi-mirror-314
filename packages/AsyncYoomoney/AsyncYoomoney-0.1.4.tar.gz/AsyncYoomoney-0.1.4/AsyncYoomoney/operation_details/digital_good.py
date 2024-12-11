from typing import List

from AsyncYoomoney.operation_details.digital_product import DigitalProduct
from AsyncYoomoney.operation_details.digital_bonus import DigitalBonus



class DigitalGood:
    def __init__(self,
                 products: List[DigitalProduct],
                 bonuses: List[DigitalBonus]
                 ):
        self.products = products
        self.bonuses = bonuses
