from collections import Counter

class Entry:
    def __init__(self, entry_id: int, date: str, amount: float, category: str, description: str, entry_type: str):
        self._entry_id = entry_id
        self._date = date
        self._amount = amount
        self._category = category
        self._description = description
        self._entry_type = entry_type

    @property
    def entry_id(self):
        return self._entry_id

    @property
    def date(self):
        return self._date

    @property
    def amount(self):
        return self._amount

    @property
    def category(self):
        return self._category

    @property
    def description(self):
        return self._description

    @property
    def entry_type(self):
        return self._entry_type


class Budget:
    def __init__(self, name: str, min_amount: float):
        self._name = name
        self._min_amount = min_amount
        self.entries = []

    def generate_id(self) -> int:
        if self.entries:
            new_id = max(entry.entry_id for entry in self.entries) + 1
        else:
            new_id = 1
        return new_id

    def can_add_entry(self, amount: float, category: str, description: str, entry_type: str, date: str) -> bool:
        if amount < self._min_amount:
            return False
        if entry_type not in ["kulu", "tulu"]:
            return False
        if not category:
            return False
        if not date:
            return False
        return True

    def add_entry(self, amount: float, category: str, description: str, entry_type: str, date: str):
        if not self.can_add_entry(amount, category, description, entry_type, date):
            return None

        entry_id = self.generate_id()
        new_entry = Entry(entry_id, date, amount, category, description, entry_type)
        self.entries.append(new_entry)
        return new_entry

    def can_remove_entry(self, entry_id: int) -> bool:
        for entry in self.entries:
            if entry.entry_id == entry_id:
                return True
        return False

    def remove_entry(self, entry_id: int):
        if self.can_remove_entry(entry_id):
            self.entries = [entry for entry in self.entries if entry.entry_id != entry_id]

    def get_all_entries(self):
        return self.entries

    def get_expenses(self):
        return [entry for entry in self.entries if entry.entry_type == "kulu"]

    def get_incomes(self):
        return [entry for entry in self.entries if entry.entry_type == "tulu"]

    def get_expenses_by_amount_desc(self):
        return sorted(self.get_expenses(), key=lambda entry: entry.amount, reverse=True)

    def get_incomes_by_amount_desc(self):
        return sorted(self.get_incomes(), key=lambda entry: entry.amount, reverse=True)

    def get_average_expense(self):
        expenses = self.get_expenses()
        if not expenses:
            return 0
        total_expense = sum(entry.amount for entry in expenses)
        return total_expense / len(expenses)

    def get_average_income(self):
        incomes = self.get_incomes()
        if not incomes:
            return 0
        total_income = sum(entry.amount for entry in incomes)
        return total_income / len(incomes)

    def get_biggest_expense(self):
        expenses = self.get_expenses()
        return max(expenses, key=lambda entry: entry.amount, default=None)

    def get_smallest_expense(self):
        expenses = self.get_expenses()
        return min(expenses, key=lambda entry: entry.amount, default=None)

    def get_biggest_income(self):
        incomes = self.get_incomes()
        return max(incomes, key=lambda entry: entry.amount, default=None)

    def get_smallest_income(self):
        incomes = self.get_incomes()
        return min(incomes, key=lambda entry: entry.amount, default=None)

    def get_total(self):
        total_income = sum(entry.amount for entry in self.get_incomes())
        total_expense = sum(entry.amount for entry in self.get_expenses())
        return total_income - total_expense

    def sum_recursive(self, entries, n=0):
        if n == len(entries):
            return 0
        return entries[n].amount + self.sum_recursive(entries, n + 1)

    def get_total_recursive(self):
        total_income = self.sum_recursive(self.get_incomes())
        total_expense = self.sum_recursive(self.get_expenses())
        return total_income - total_expense

    def get_recursive_total(self):
        return self.get_total_recursive()

    def get_summary_by_category(self):
        summary = {}
        for entry in self.entries:
            summary[entry.category] = summary.get(entry.category, 0) + entry.amount
        return summary

    def get_most_common_category(self):
        categories = [entry.category for entry in self.entries]
        if not categories:
            return ""
        return Counter(categories).most_common(1)[0][0]
