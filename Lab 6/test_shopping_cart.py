import pytest
from shopping_cart import item_total, cart_discount, shipping_fee

# --- Unit & Branch Coverage Tests for Shopping Cart ---

# 1. item_total tests
def test_food_item():
    assert item_total("food", 100, 2) == 210

def test_clothing_item():
    assert item_total("clothing", 100, 2) == 224

def test_electronics_item():
    assert item_total("electronics", 100, 2) == 236

def test_item_total_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        item_total("invalid_category", 100, 2)

def test_item_total_negative_price():
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", -5, 2)

def test_item_total_zero_or_negative_qty():
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", 100, 0)
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", 100, -2)

def test_item_total_bulk_discount():
    # qty >= 10 applies 10% discount on amount before GST
    assert item_total("food", 100, 10) == 945

def test_item_total_no_bulk_discount():
    assert item_total("food", 100, 9) == 945


# 2. cart_discount tests
def test_cart_discount_tier_5000():
    assert cart_discount(5000, False, "NONE") == 500

def test_cart_discount_tier_2000():
    assert cart_discount(2000, False, "NONE") == 200

def test_cart_discount_tier_below_2000():
    assert cart_discount(1500, False, "NONE") == 0

def test_cart_discount_prime():
    assert cart_discount(5000, True, "NONE") == 600

def test_cart_discount_coupon_flat10():
    assert cart_discount(2000, False, "FLAT10") == 400
    assert cart_discount(800, False, "FLAT10") == 0

def test_cart_discount_coupon_other():
    assert cart_discount(2000, False, "OTHER") == 200


# 3. shipping_fee tests
def test_free_shipping():
    assert shipping_fee(1000, False, False) == 0

def test_free_shipping_prime():
    assert shipping_fee(100, True, False) == 0

def test_standard_shipping_below_500():
    assert shipping_fee(400, False, False) == 40

def test_express_shipping_prime():
    assert shipping_fee(100, True, True) == 50

def test_express_shipping_non_prime():
    assert shipping_fee(600, False, True) == 100
    assert shipping_fee(400, False, True) == 140
