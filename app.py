from flask import Flask, render_template, request, redirect
import requests
import hmac
import hashlib

app = Flask(__name__)
WEBHOOK_SECRET = "my-secret-key"

orders = []
received_orders = []


@app.route("/")
def home():
    return render_template(
        "index.html",
        orders=orders,
        received_orders=received_orders
    )


@app.route("/order", methods=["POST"])
def create_order():
    product = request.form["product"]
    quantity = request.form["quantity"]

    order = {
        "product": product,
        "quantity": quantity
    }

    orders.append(order)

    payload = str(order).encode()

    signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    requests.post(
        "http://127.0.0.1:5000/webhook",
        json=order,
        headers={"X-Webhook-Signature": signature}
    )

    return redirect("/")


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    received_signature = request.headers.get("X-Webhook-Signature")

    payload = str(data).encode()

    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    if not received_signature or not hmac.compare_digest(
        received_signature,
        expected_signature
    ):
        return {
            "message": "Invalid webhook signature"
        }, 401

    received_orders.append(data)

    print("Verified webhook received:", data)

    return {
        "message": "Webhook verified successfully"
    }, 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)