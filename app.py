from flask import Flask, render_template, request, redirect

app = Flask(__name__)

orders = []


@app.route("/")
def home():
    return render_template("index.html", orders=orders)


@app.route("/order", methods=["POST"])
def create_order():
    product = request.form["product"]
    quantity = request.form["quantity"]
 
    order = {
        "product": product,
        "quantity": quantity
    }

    orders.append(order)

    return redirect("/")
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    print("Webhook received:", data)

    return {
        "message": "Webhook received successfully"
    }, 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)