import json
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_products(path='products.json'):
    """Loads product configurations from a JSON file."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("Error: products.json not found.")
        return None
    except json.JSONDecodeError:
        logging.error("Error: products.json is not valid JSON.")
        return None

def calculate_price(product):
    """Calculates the final price for a single product based on its config."""
    if not product:
        return 0.0

    price = product.get('base_price', 0)
    
    # Apply tax (but bug: applied after discount, which is wrong)
    tax_rate = product.get('tax_rate', 0)
    
    # Apply discount (bug: simplistic scaling; prompt will require proper tiered %)
    discount_tier = product.get('discount_tier', 1)
    discount_amount = price * (0.1 * discount_tier)  # Over-discounts for higher tiers
    
    price -= discount_amount
    
    price += price * tax_rate  # Wrong order: tax after discount
    
    # No shipping or error handling
    
    return price

def main():
    """Main function to run price calculations for all products."""
    products = load_products()
    if products:
        for prod_id, prod_config in products.items():
            final_price = calculate_price(prod_config)
            print(f"The calculated final price for '{prod_config['name']}' (ID: {prod_id}) is: ${final_price:.2f}")

if __name__ == "__main__":
    main()