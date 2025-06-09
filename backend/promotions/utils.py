"""
Utility functions for the promotions app.
"""
from decimal import Decimal, ROUND_HALF_UP


def calculate_sale_price(original_price, discount_percentage):
    """
    Calculate the sale price based on original price and discount percentage.
    
    Args:
        original_price (Decimal): The original price of the product
        discount_percentage (Decimal): The discount percentage to apply
        
    Returns:
        Decimal: The calculated sale price after discount
    """
    if original_price is None or discount_percentage is None:
        return None
    
    discount = (Decimal(discount_percentage) / 100) * Decimal(original_price)
    sale_price = Decimal(original_price) - discount
    
    # Round to 2 decimal places
    return sale_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calculate_discount_percentage(original_price, sale_price):
    """
    Calculate the discount percentage based on original price and sale price.
    
    Args:
        original_price (Decimal): The original price of the product
        sale_price (Decimal): The sale price of the product
        
    Returns:
        Decimal: The calculated discount percentage
    """
    if original_price is None or sale_price is None or Decimal(original_price) == 0:
        return None
    
    discount = Decimal(original_price) - Decimal(sale_price)
    percentage = (discount / Decimal(original_price)) * 100
    
    # Round to 2 decimal places
    return percentage.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def apply_discount(original_price, discount_percentage):
    """
    Apply a discount to a price and return both the sale price and savings.
    
    Args:
        original_price (Decimal): The original price of the product
        discount_percentage (Decimal): The discount percentage to apply
        
    Returns:
        tuple: (sale_price, savings) - The calculated sale price and amount saved
    """
    if original_price is None or discount_percentage is None:
        return None, None
    
    original_price = Decimal(original_price)
    discount_percentage = Decimal(discount_percentage)
    
    savings = (discount_percentage / 100) * original_price
    sale_price = original_price - savings
    
    # Round to 2 decimal places
    sale_price = sale_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    savings = savings.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return sale_price, savings
