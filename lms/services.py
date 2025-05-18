import stripe

from config.settings import api_key


def create_stripe_product(name: str) -> stripe.Product:
    """Create product in stripe"""
    stripe.api_key = api_key
    return stripe.Product.create(name=name)


def create_price(product_id: int, total_cost: float) -> stripe.Price:
    """Create price for product in stripe"""
    stripe.api_key = api_key
    return stripe.Price.create(
        currency="usd",
        unit_amount=int(total_cost*100),
        product=product_id,
    )


def create_stripe(price_id: int) -> stripe.checkout.Session:
    """Creation session"""
    stripe.api_key = api_key
    return stripe.checkout.Session.create(
                success_url="http://127.0.0.1:8000/success/",
                cancel_url="http://127.0.0.1:8000/cancel/",
                line_items=[{"price": price_id, "quantity": 1}],
                mode="payment",
            )
