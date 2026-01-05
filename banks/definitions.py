from .base import BankSite

class BankOfAmerica(BankSite):
    def __init__(self):
        super().__init__("Bank of America", "https://www.bankofamerica.com/")

class Chase(BankSite):
    def __init__(self):
        super().__init__("Chase", "https://www.chase.com/")

class Citi(BankSite):
    def __init__(self):
        super().__init__("Citi", "https://www.citi.com/")

class CapitalOne(BankSite):
    def __init__(self):
        super().__init__("Capital One", "https://www.capitalone.com/")
