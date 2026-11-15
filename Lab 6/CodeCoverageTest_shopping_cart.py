import pytest
from shopping_cart import item_total, cart_discount, shipping_fee

# --- Code Coverage Tests for shopping_cart.py ---

# 1. Tests for item_total
def test_item_total_valid_food():
    assert item_total("food", 100, 2) == 210

def test_item_total_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        item_total("books", 100, 1)

def test_item_total_invalid_price():
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", -10, 2)

def test_item_total_invalid_qty():
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", 100, 0)

def test_item_total_bulk_discount():
    # qty >= 10 applies 10% discount before GST
    # 100 * 10 = 1000 -> 1000 - 100 = 900 -> 900 + (900 * 5 // 100) = 945
    assert item_total("food", 100, 10) == 945


# 2. Tests for cart_discount
def test_cart_discount_above_5000():
    # cart_value >= 5000 gives 500 discount
    assert cart_discount(6000, False, "NONE") == 500

def test_cart_discount_between_2000_and_5000():
    # cart_value >= 2000 gives 200 discount
    assert cart_discount(3000, False, "NONE") == 200

def test_cart_discount_below_2000():
    # cart_value < 2000 gives 0 discount
    assert cart_discount(1500, False, "NONE") == 0

def test_cart_discount_prime_member():
    # prime members get +100 discount
    assert cart_discount(5000, True, "NONE") == 600

def test_cart_discount_flat10_coupon():
    # coupon FLAT10 and cart_value >= 1000 gives extra 10% of cart_value
    assert cart_discount(2000, False, "FLAT10") == 400


# 3. Tests for shipping_fee
def test_shipping_fee_prime_standard():
    # prime gives free shipping
    assert shipping_fee(100, True, False) == 0

def test_shipping_fee_non_prime_above_500():
    # cart_value >= 500 gives free shipping
    assert shipping_fee(500, False, False) == 0

def test_shipping_fee_non_prime_below_500():
    # cart_value < 500 incurs 40 fee
    assert shipping_fee(200, False, False) == 40

def test_shipping_fee_express_prime():
    # express adds 100, but prime reduces 50 -> fee = 50
    assert shipping_fee(100, True, True) == 50

def test_shipping_fee_express_non_prime():
    # express adds 100 -> fee = 0 + 100 = 100
    assert shipping_fee(600, False, True) == 100
