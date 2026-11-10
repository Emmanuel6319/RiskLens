
class Asset:
    """Anything the business owns and would lose money without."""

    def __init__(self, name, owner, value_usd):
        self.name = name
        self.owner = owner
        self.value_usd = value_usd

    def describe(self):
        return f"{self.name} (owner: {self.owner}, value: ${self.value_usd:,})"

    def value_level(self):
        if self.value_usd > 10000:
            return "High"
        else:
            return "Low"


class PhysicalAsset(Asset):
    def __init__(self, name, owner, value_usd, location):
        super().__init__(name, owner, value_usd)
        self.location = location


class DataAsset(Asset):
    def __init__(self, name, owner, value_usd, contains_pii, classification="Internal"):
        super().__init__(name, owner, value_usd)
        self.contains_pii = contains_pii
        self.classification = classification

    def describe(self):
        pii = "contains PII" if self.contains_pii else "no PII"
        return f"{super().describe()} [{self.classification}, {pii}]"


# NEW: SoftwareAsset child class
class SoftwareAsset(Asset):
    def __init__(self, name, owner, value_usd, version):
        super().__init__(name, owner, value_usd)
        self.version = version

    def describe(self):
        return f"{super().describe()} (version: {self.version})"


# NEW: Function to find DataAssets containing PII
def get_pii_assets(assets):
    return [
        asset for asset in assets
        if isinstance(asset, DataAsset) and asset.contains_pii
    ]


class Customer:
    def __init__(self, name, phone):
        self.name = name
        self._phone = phone
        self.orders = []

    def add_order(self, total):
        self.orders.append(total)

    def total_spend(self):
        return sum(self.orders)

    def masked_phone(self):
        return self._phone[:4] + "*" * (len(self._phone) - 6) + self._phone[-2:]


class PremiumCustomer(Customer):
    DISCOUNT = 0.10

    def total_spend(self):
        return super().total_spend() * (1 - self.DISCOUNT)


# Asset list
assets = [
    PhysicalAsset("POS terminal", "Cashier", 1500, "Front counter"),
    DataAsset("Prescription records", "Pharmacist", 100000, contains_pii=True, classification="Restricted"),
    DataAsset("Price list", "Manager", 500, contains_pii=False, classification="Public"),
    SoftwareAsset("Windows Server", "IT Manager", 15000, "2025")
]


# Display all assets and their value levels
print("ALL ASSETS:")
for a in assets:
    print(a.describe())
    print("Value level:", a.value_level())
    print()


# Display only DataAssets containing PII
print("ASSETS CONTAINING PII:")
pii_assets = get_pii_assets(assets)

for asset in pii_assets:
    print(asset.describe())


# Customer demonstration
print("\nCUSTOMER INFORMATION:")
maria = PremiumCustomer("Maria Lopez", "6145550142")
maria.add_order(25)
maria.add_order(40)

print(maria.name, maria.masked_phone(), f"${maria.total_spend():,.2f}")
print("Is Maria a Customer?", isinstance(maria, Customer))
