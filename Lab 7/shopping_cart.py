ZONES = {"1": "North", "2": "North", "3": "West", "4": "West",
         "5": "South", "6": "South", "7": "East", "8": "East"}

def cart_total(cart):
    """
    Computes total price from a CSV of items in name:pricexqty format.
    Hardened against invalid types, malformed strings, and negative values.
    """
    if not cart or not isinstance(cart, str):
        return 0
    total = 0
    for item in cart.split(','):
        item = item.strip()
        if not item or ':' not in item:
            continue
        parts = item.split(':', 1)
        name, rest = parts[0], parts[1]
        if 'x' not in rest:
            continue
        rest_parts = rest.split('x', 1)
        price_str, qty_str = rest_parts[0].strip(), rest_parts[1].strip()
        try:
            price = int(price_str)
            qty = int(qty_str)
            if price >= 0 and qty >= 0:
                total += price * qty
        except ValueError:
            continue
    return total

def promo_percent(code):
    """
    Extracts promo discount percentage from promo codes (e.g., 'OFF20').
    Hardened against null/invalid input, missing 'OFF' token, and non-numeric suffixes.
    """
    if not code or not isinstance(code, str):
        return 0
    code_upper = code.upper().strip()
    if 'OFF' not in code_upper:
        return 0
    parts = code_upper.split('OFF', 1)
    candidate = parts[1].strip()
    digits = ''
    for ch in candidate:
        if ch.isdigit():
            digits += ch
        else:
            break
    if digits:
        return int(digits)
    return 0

def delivery_zone(pincode):
    """
    Determines delivery zone based on the first digit of pincode.
    Hardened against null/empty pincodes, invalid types, and unmapped zones.
    """
    if not pincode or not isinstance(pincode, str):
        return "Unknown"
    pincode = pincode.strip()
    if not pincode:
        return "Unknown"
    return ZONES.get(pincode[0], "Unknown")

def main():
    print("==== Running cart_total ====")
    user_input = input("Enter cart as name:pricexqty CSV (e.g. pen:10x2,book:250x1): ")
    result = cart_total(user_input)
    print("Cart Total:", result)

    print("\n==== Running promo_percent ====")
    user_input = input("Enter a promo code (e.g. OFF20): ")
    result = promo_percent(user_input)
    print("Discount Percent:", result)

    print("\n==== Running delivery_zone ====")
    user_input = input("Enter a 6 digit pincode (e.g. 560085): ")
    result = delivery_zone(user_input)
    print("Delivery Zone:", result)

if __name__ == "__main__":
    main()
