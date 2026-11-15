import pytest
from shopping_cart import item_total, cart_discount, shipping_fee

# --- Comprehensive Branch Coverage Tests for shopping_cart.py ---
# These tests ensure all decision branches (True and False outcomes) and
# boundary conditions are thoroughly exercised to achieve 100% branch coverage.

# ============================================================================
# 1. item_total(category, price, qty)
# ============================================================================
# Decision 1: category not in GST_RATE
def test_item_total_valid_category_food():
    # Valid category 'food' (GST 5%)
    assert item_total("food", 100, 2) == 210

def test_item_total_valid_category_clothing():
    # Valid category 'clothing' (GST 12%)
    assert item_total("clothing", 100, 2) == 224

def test_item_total_valid_category_electronics():
    # Valid category 'electronics' (GST 18%)
    assert item_total("electronics", 100, 2) == 236

def test_item_total_unknown_category_raises():
    # Invalid category branch -> raises ValueError
    with pytest.raises(ValueError, match="unknown category"):
        item_total("books", 100, 2)

# Decision 2: price < 0 or qty <= 0
def test_item_total_negative_price_raises():
    # price < 0 evaluates to True -> raises ValueError
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", -1, 5)

def test_item_total_zero_qty_raises():
    # price >= 0, qty <= 0 evaluates to True -> raises ValueError
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", 100, 0)

def test_item_total_negative_qty_raises():
    # qty < 0 evaluates to True -> raises ValueError
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", 100, -3)

def test_item_total_zero_price_valid():
    # price == 0 and qty > 0 -> valid calculation
    assert item_total("food", 0, 5) == 0

# Decision 3: qty >= 10 (bulk discount: 10% off amount before GST)
def test_item_total_bulk_discount_true():
    # qty >= 10 is True: 100 * 10 = 1000; discount = 100; amount = 900; + 5% = 945
    assert item_total("food", 100, 10) == 945

def test_item_total_bulk_discount_false():
    # qty >= 10 is False (qty = 9): 100 * 9 = 900; no bulk discount; + 5% = 945
    assert item_total("food", 100, 9) == 945


# ============================================================================
# 2. cart_discount(cart_value, is_prime, coupon)
# ============================================================================
# Decision 1: cart_value >= 5000 -> 500
def test_cart_discount_above_5000():
    assert cart_discount(5500, False, "NONE") == 500

def test_cart_discount_exactly_5000():
    assert cart_discount(5000, False, "NONE") == 500

# Decision 2: cart_value >= 2000 (< 5000) -> 200
def test_cart_discount_between_2000_and_5000():
    assert cart_discount(3000, False, "NONE") == 200

def test_cart_discount_exactly_2000():
    assert cart_discount(2000, False, "NONE") == 200

# Decision 3: cart_value < 2000 -> 0
def test_cart_discount_below_2000():
    assert cart_discount(1999, False, "NONE") == 0

def test_cart_discount_zero_value():
    assert cart_discount(0, False, "NONE") == 0

# Decision 4: is_prime -> discount += 100
def test_cart_discount_prime_true():
    # 500 (tier) + 100 (prime) = 600
    assert cart_discount(5000, True, "NONE") == 600

def test_cart_discount_prime_false():
    # 500 (tier) + 0 (prime) = 500
    assert cart_discount(5000, False, "NONE") == 500

# Decision 5: coupon == "FLAT10" and cart_value >= 1000
def test_cart_discount_coupon_flat10_eligible():
    # coupon is FLAT10 and cart_value >= 1000 -> adds cart_value // 10
    # 200 (tier) + 200 (coupon) = 400
    assert cart_discount(2000, False, "FLAT10") == 400

def test_cart_discount_coupon_flat10_threshold():
    # cart_value == 1000 -> 0 (tier) + 100 (coupon) = 100
    assert cart_discount(1000, False, "FLAT10") == 100

def test_cart_discount_coupon_flat10_ineligible_cart_value():
    # coupon is FLAT10 but cart_value < 1000 -> condition False
    assert cart_discount(999, False, "FLAT10") == 0

def test_cart_discount_coupon_other_eligible_cart_value():
    # coupon is NOT FLAT10 but cart_value >= 1000 -> condition False
    assert cart_discount(2000, False, "SAVE50") == 200

def test_cart_discount_coupon_other_ineligible_cart_value():
    # coupon is NOT FLAT10 and cart_value < 1000 -> condition False
    assert cart_discount(500, False, "SAVE50") == 0


# ============================================================================
# 3. shipping_fee(cart_value, is_prime, is_express)
# ============================================================================
# Decision 1: is_prime (fee = 0)
def test_shipping_fee_prime_standard():
    assert shipping_fee(100, True, False) == 0

# Decision 2: not prime, cart_value >= 500 (fee = 0)
def test_shipping_fee_non_prime_cart_500():
    assert shipping_fee(500, False, False) == 0

def test_shipping_fee_non_prime_cart_above_500():
    assert shipping_fee(1500, False, False) == 0

# Decision 3: not prime, cart_value < 500 (fee = 40)
def test_shipping_fee_non_prime_cart_below_500():
    assert shipping_fee(499, False, False) == 40

def test_shipping_fee_non_prime_cart_zero():
    assert shipping_fee(0, False, False) == 40

# Decision 4 & 5: is_express (fee += 100) and nested if is_prime (fee -= 50)
def test_shipping_fee_express_prime():
    # fee starts 0 -> +100 -> -50 = 50
    assert shipping_fee(100, True, True) == 50

def test_shipping_fee_express_non_prime_free_tier():
    # fee starts 0 -> +100 = 100
    assert shipping_fee(500, False, True) == 100

def test_shipping_fee_express_non_prime_standard_tier():
    # fee starts 40 -> +100 = 140
    assert shipping_fee(200, False, True) == 140

def test_shipping_fee_standard_non_express_prime():
    # is_express is False -> inner prime check bypassed
    assert shipping_fee(1000, True, False) == 0
