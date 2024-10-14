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

# Add more models as needed
