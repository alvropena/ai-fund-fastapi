import numpy as np
import pandas as pd

def calculate_dcf(free_cash_flows, discount_rate, growth_rate, terminal_growth=0.02):
    dcf = 0
    for i, cash_flow in enumerate(free_cash_flows, 1):
        dcf += cash_flow / (1 + discount_rate) ** i
    terminal_value = free_cash_flows[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
    dcf += terminal_value / (1 + discount_rate) ** len(free_cash_flows)
    return dcf

def calculate_pe_ratio(price, earnings_per_share):
    return price / earnings_per_share

def calculate_pb_ratio(price, book_value_per_share):
    return price / book_value_per_share

def calculate_peg_ratio(pe_ratio, earnings_growth_rate):
    return pe_ratio / earnings_growth_rate

def calculate_ev_ebitda(enterprise_value, ebitda):
    return enterprise_value / ebitda

def calculate_debt_to_equity(total_debt, shareholder_equity):
    """
    Debt-to-Equity (D/E) Ratio
    Formula: Total Debt / Shareholder Equity
    """
    if shareholder_equity == 0:
        return None  # Avoid division by zero
    return total_debt / shareholder_equity

def calculate_return_on_equity(net_income, shareholder_equity):
    """
    Return on Equity (ROE)
    Formula: Net Income / Shareholder Equity
    """
    if shareholder_equity == 0:
        return None  # Avoid division by zero
    return net_income / shareholder_equity

def calculate_current_ratio(current_assets, current_liabilities):
    """
    Current Ratio
    Formula: Current Assets / Current Liabilities
    """
    if current_liabilities == 0:
        return None  # Avoid division by zero
    return current_assets / current_liabilities

def calculate_gross_margin(revenue, cost_of_goods_sold):
    """
    Gross Margin
    Formula: (Revenue - Cost of Goods Sold) / Revenue * 100
    """
    if revenue == 0:
        return None  # Avoid division by zero
    return (revenue - cost_of_goods_sold) / revenue * 100