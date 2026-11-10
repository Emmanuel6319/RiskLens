class Asset:
    """Anything the business owns and would lose money without."""

    def __init__(self, name, owner, value_usd):
        self.name = name
        self.owner = owner              # the person responsible for it
        self.value_usd = value_usd

    def describe(self):
        return f"{self.name} (owner: {self.owner}, value: ${self.value_usd:,})"


class PhysicalAsset(Asset):
    def __init__(self, name, owner, value_usd, location):
        super().__init__(name, owner, value_usd)
        self.location = location


class DataAsset(Asset):
    def __init__(self, name, owner, value_usd, contains_pii, classification="Internal"):
        super().__init__(name, owner, value_usd)
        self.contains_pii = contains_pii
        self.classification = classification   # Public, Internal, Confidential, Restricted

    def describe(self):                         # override: add the data details
        pii = "contains PII" if self.contains_pii else "no PII"
        return f"{super().describe()} [{self.classification}, {pii}]"


class Customer:
    def __init__(self, name, phone):
        self.name = name
        self._phone = phone     # PII: the underscore says "don't touch this directly"
        self.orders = []        # list of order totals in dollars

    def add_order(self, total):
        self.orders.append(total)

    def total_spend(self):
        return sum(self.orders)

    def masked_phone(self):
        return self._phone[:4] + "*" * (len(self._phone) - 6) + self._phone[-2:]


class PremiumCustomer(Customer):
    DISCOUNT = 0.10

    def total_spend(self):      # override: premium customers pay 10% less
        return super().total_spend() * (1 - self.DISCOUNT)


assets = [
    PhysicalAsset("POS terminal", "Cashier", 1_500, "Front counter"),
    DataAsset("Prescription records", "Pharmacist", 100_000, contains_pii=True, classification="Restricted"),
    DataAsset("Price list", "Manager", 500, contains_pii=False, classification="Public"),
]
for a in assets:
    print(a.describe())

maria = PremiumCustomer("Maria Lopez", "6145550142")
maria.add_order(25)
maria.add_order(40)
print(maria.name, maria.masked_phone(), f"${maria.total_spend():,.2f}")
print("Is Maria a Customer?", isinstance(maria, Customer))