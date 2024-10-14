from financial_models import calculate_pe_ratio

def test_calculate_pe_ratio():
    price = 150
    eps = 5
    assert calculate_pe_ratio(price, eps) == 30
