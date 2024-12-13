import pytest
from solveit.finance.calculator import FinancialCalculator

@pytest.fixture
def calculator():
    return FinancialCalculator()

def test_compound_interest(calculator):
    result = calculator.compound_interest(
        principal=1000,
        rate=0.05,
        time=2,
        compounds_per_year=12
    )
    assert round(result['final_amount'], 2) == 1104.94
    assert round(result['interest_earned'], 2) == 104.94

def test_loan_payment(calculator):
    result = calculator.loan_payment(
        principal=100000,
        rate=0.05,
        years=30
    )
    assert round(result['monthly_payment'], 2) == 536.82
    assert round(result['total_interest'], 2) == 93255.78

def test_zero_principal(calculator):
    result = calculator.compound_interest(
        principal=0,
        rate=0.05,
        time=1
    )
    assert result['final_amount'] == 0
    assert result['interest_earned'] == 0

def test_invalid_rate(calculator):
    with pytest.raises(ValueError):
        calculator.compound_interest(
            principal=1000,
            rate=-0.05,  # Negative rate
            time=1
        ) 