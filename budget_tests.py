import pytest
from budget import *

@pytest.mark.timeout(1.0)
def test_can_add_entry_invalid_amount_below_min():
    budget = Budget("test", 10)
    assert not budget.can_add_entry(5, "kulu", "Palk", "tulu", "2024-01-01")

@pytest.mark.timeout(1.0)
def test_can_add_entry_negative_amount():
    budget = Budget("test", 0)
    assert not budget.can_add_entry(-10, "kulu", "Palk", "tulu", "2024-01-01")

@pytest.mark.timeout(1.0)
def test_can_add_entry_invalid_type():
    budget = Budget("test", 0)
    assert not budget.can_add_entry(10, "kulu", "Palk", "asdasd", "2024-01-01")

@pytest.mark.timeout(1.0)
def test_can_add_entry_invalid_date():
    budget = Budget("test", 0)
    assert not budget.can_add_entry(10, "kulu", "Palk", "tulu", "")

@pytest.mark.timeout(1.0)
def test_can_add_entry_valid():
    budget = Budget("eelarve_nimi4", 0)
    result = budget.can_add_entry(100, "tulu", "Palk", "tulu", "2024-01-01")
    assert result is True

@pytest.mark.timeout(1.0)
def test_add_entry_adds_entry_to_budget():
    budget = Budget("eelarve_nimi5", 0)
    entry = budget.add_entry(100, "tulu", "Palk", "tulu", "2024-01-01")
    assert entry is not None
    assert entry.amount == 100
    assert len(budget.entries) == 1

@pytest.mark.timeout(1.0)
def test_add_entry_same_content_multiple_times():
    budget = Budget("eelarve_nimi6", 0)
    e1 = budget.add_entry(20, "kulu", "toit", "kulu", "2024-01-01")
    e2 = budget.add_entry(20, "kulu", "toit", "kulu", "2024-01-01")
    assert e1 is not None and e2 is not None
    assert len(budget.entries) == 2

@pytest.mark.timeout(1.0)
def test_can_remove_entry_nonexistent():
    budget = Budget("eelarve_nimi7", 0)
    assert not budget.can_remove_entry(999)

@pytest.mark.timeout(1.0)
def test_remove_entry_existing():
    budget = Budget("eelarve_nimi8", 0)
    entry = budget.add_entry(20, "kulu", "toit", "kulu", "2024-01-01")
    budget.remove_entry(entry.entry_id)
    assert len(budget.entries) == 0

@pytest.mark.timeout(1.0)
def test_remove_entry_nonexistent_does_not_change_budget():
    budget = Budget("eelarve_nimi9", 0)
    budget.add_entry(20, "kulu", "toit", "kulu", "2024-01-01")
    budget.remove_entry(999)
    assert len(budget.entries) == 1

@pytest.mark.timeout(1.0)
def test_get_expenses_sorted_desc():
    budget = Budget("eelarve_nimi10", 0)
    budget.add_entry(10, "kulu", "toit", "kulu", "2024-01-01")
    budget.add_entry(20, "kulu", "pood", "kulu", "2024-01-01")
    expenses = budget.get_expenses_by_amount_desc()
    assert expenses[0].amount >= expenses[1].amount

@pytest.mark.timeout(1.0)
def test_get_incomes_sorted_desc():
    budget = Budget("eelarve_nimi11", 0)
    budget.add_entry(100, "tulu", "palk", "tulu", "2024-01-01")
    budget.add_entry(50, "tulu", "palk", "tulu", "2024-01-01")
    incomes = budget.get_incomes_by_amount_desc()
    assert incomes[0].amount >= incomes[1].amount

@pytest.mark.timeout(1.0)
def test_average_expense():
    budget = Budget("eelarve_nimi12", 0)
    budget.add_entry(10, "kulu", "mingi_asi", "kulu", "2024-01-01")
    budget.add_entry(20, "kulu", "pood", "kulu", "2024-01-01")
    avg = budget.get_average_expense()
    assert avg == 15

@pytest.mark.timeout(1.0)
def test_average_income():
    budget = Budget("eelarve_nimi13", 0)
    budget.add_entry(100, "tulu", "palk", "tulu", "2024-01-01")
    budget.add_entry(50, "tulu", "side_hustle", "tulu", "2024-01-01")
    avg = budget.get_average_income()
    assert avg == 75

@pytest.mark.timeout(1.0)
def test_biggest_and_smallest_expense():
    budget = Budget("eelarve_nimi14", 0)
    e1 = budget.add_entry(10, "kulu", "kohvi", "kulu", "2024-01-01")
    e2 = budget.add_entry(30, "kulu", "toit", "kulu", "2024-01-01")
    biggest = budget.get_biggest_expense()
    smallest = budget.get_smallest_expense()
    assert biggest.amount == 30
    assert smallest.amount == 10

@pytest.mark.timeout(1.0)
def test_biggest_and_smallest_income():
    budget = Budget("eelarve_nimi15", 0)
    e1 = budget.add_entry(100, "tulu", "Palk", "tulu", "2024-01-01")
    e2 = budget.add_entry(50, "tulu", "palk", "tulu", "2024-01-01")
    biggest = budget.get_biggest_income()
    smallest = budget.get_smallest_income()
    assert biggest.amount == 100
    assert smallest.amount == 50

@pytest.mark.timeout(1.0)
def test_total_and_recursive_total():
    budget = Budget("eelarve_nimi16", 0)
    budget.add_entry(100, "tulu", "raha", "tulu", "2024-01-01")
    budget.add_entry(50, "tulu", "raha", "tulu", "2024-01-01")
    budget.add_entry(30, "kulu", "toit", "kulu", "2024-01-01")
    total = budget.get_total()
    recursive_total = budget.get_recursive_total()
    assert total == recursive_total
    assert total == 120
