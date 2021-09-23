import math


def sub_total(value_list):
    value = sum(value_list)
    return value


def consumption_tax(value_list):
    value = sub_total(value_list)
    value = value * 0.10
    value = math.floor(value)
    return value


def total_amount(value_list):
    value = sub_total(value_list) + consumption_tax(value_list)
    return value


def gross_profit(sales_unit_price_list, purchase_unit_price_list):
    value = (sum(sales_unit_price_list)) - (sum(purchase_unit_price_list))
    return value


def gross_margin(sales_unit_price_list, purchase_unit_price_list):
    try:
        value = gross_profit(
            sales_unit_price_list,
            purchase_unit_price_list) / sub_total(sales_unit_price_list) * 100
        return value
    except ZeroDivisionError:
        return 0
