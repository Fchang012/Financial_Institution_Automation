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

class Vanguard(BankSite):
    def __init__(self):
        super().__init__("Vanguard", "https://investor.vanguard.com/")

class TRowePrice(BankSite):
    def __init__(self):
        super().__init__("T. Rowe Price", "https://www.troweprice.com/en/us")

class ETrade(BankSite):
    def __init__(self):
        super().__init__("E*TRADE", "https://us.etrade.com/home/welcome-back")

class Fidelity(BankSite):
    def __init__(self):
        super().__init__("Fidelity", "https://www.fidelity.com/")
