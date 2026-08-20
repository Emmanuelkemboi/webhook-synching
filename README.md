# Webhook Order Synchronization

A simple Python Flask project demonstrating how webhooks can synchronize orders between two systems.

The project simulates an order system where an order created from one end is sent through a webhook and received by another end. It also demonstrates webhook security using **HMAC-SHA256 signatures**.

---

## Technologies

* Python
* Flask
* Requests
* HMAC-SHA256
* HTML
* Git
* GitHub

---

## Project Structure

```text
webhook-synching/
│
├── app.py
├── requirements.txt
├── README.md
│
└── templates/
    └── index.html
```

---

## Main Files

### `app.py`

The main Flask application.

It contains:

* Flask configuration
* Home page route
* Order creation
* Webhook sending
* Webhook receiving
* HMAC-SHA256 signature generation
* Webhook signature verification
* Temporary order storage

### `templates/index.html`

Contains the simple web interface for:

* Entering a product
* Entering a quantity
* Creating an order
* Viewing created orders
* Viewing received orders

### `requirements.txt`

Contains the Python dependencies required to run the project.

```text
Flask
requests
```

### `README.md`

Contains the project documentation, setup instructions, usage instructions, testing information, and explanation of the webhook implementation.

---

# Setting Up the Project

## 1. Clone the Repository

Clone the project from GitHub:

```bash
git clone https://github.com/Emmanuelkemboi/webhook-synching.git
```

Move into the project directory:

```bash
cd webhook-synching
```

---

## 2. Create a Virtual Environment

Creating a virtual environment keeps the project's Python dependencies separate from other Python projects.

On Windows:

```powershell
python -m venv venv
```

---

## 3. Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

After activation, the terminal should show:

```text
(venv)
```

---

## 4. Install Dependencies

Install the required packages:

```powershell
pip install -r requirements.txt
```

---

# Running the Project

Start the Flask application:

```powershell
python app.py
```

The application will run at:

```text
http://127.0.0.1:5000
```

Open the address in a web browser.

---

# Using the Application

The application provides a simple order form.

Enter a product and quantity.

For example:

```text
Product: Colgate
Quantity: 5
```

Click **Place Order**.

The application then:

1. Creates the order.
2. Generates an HMAC-SHA256 signature.
3. Sends the order to the `/webhook` endpoint.
4. Receives the webhook.
5. Verifies the signature.
6. Accepts the valid webhook.
7. Stores the received order.

---

# API Endpoints

## Home Page

```http
GET /
```

Displays the main order interface.

Local URL:

```text
http://127.0.0.1:5000/
```

---

## Create Order

```http
POST /order
```

Creates a new order and sends it through the webhook.

Example order:

```json
{
  "product": "Colgate",
  "quantity": 5
}
```

---

## Webhook Receiver

```http
POST /webhook
```

Receives the order from the sending system and verifies the webhook signature.

Local URL:

```text
http://127.0.0.1:5000/webhook
```

Example JSON payload:

```json
{
  "product": "Colgate",
  "quantity": 5
}
```

The request also contains the following header:

```text
X-Webhook-Signature
```

---

# How the Webhook Works

The project demonstrates a simple synchronization process between **System A** and **System B**.

```text
User creates an order
        │
        ▼
    System A
        │
        ▼
Generate HMAC-SHA256
    signature
        │
        ▼
   POST /webhook
        │
        ▼
    System B
        │
        ▼
 Verify signature
        │
    ┌───┴───┐
    ▼       ▼
  Valid   Invalid
    │       │
    ▼       ▼
 Accept   Reject
    │       │
    ▼       ▼
 Store     401
 Order
```

## Step 1: Order Creation

The user creates an order through the web interface.

Example:

```json
{
  "product": "Colgate",
  "quantity": 5
}
```

The order is received by System A.

## Step 2: Generate Signature

System A generates an HMAC-SHA256 signature using the order data and a shared secret.

```text
Order Data + Shared Secret
          │
          ▼
     HMAC-SHA256
          │
          ▼
       Signature
```

## Step 3: Send Webhook

System A sends the order to:

```http
POST /webhook
```

The request contains the order data and the generated signature.

## Step 4: Receive Webhook

System B receives the webhook request.

## Step 5: Verify Signature

System B generates its own expected signature using the same shared secret.

The received signature is compared with the expected signature.

## Step 6: Accept or Reject

If the signatures match, the order is accepted.

If they do not match, the request is rejected.

---

# Webhook Security

The project uses **HMAC-SHA256** to verify incoming webhook requests.

The sender and receiver share a secret key.

The sender creates a signature:

```text
Order Data
    +
Shared Secret
    │
    ▼
HMAC-SHA256
    │
    ▼
Signature
```

The receiver creates its own expected signature and compares it with the received signature.

## Valid Request

```text
Received Signature
        │
        ▼
Expected Signature
        │
        ▼
       MATCH
        │
        ▼
   Accept Order
        │
        ▼
      200 OK
```

## Invalid Request

```text
Received Signature
        │
        ▼
Expected Signature
        │
        ▼
    NO MATCH
        │
        ▼
  Reject Request
        │
        ▼
401 Unauthorized
```

This prevents the receiving system from blindly accepting unauthorized webhook requests.

---

# Testing the Application

## Test 1: Valid Order

Start the application:

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Create an order:

```text
Product: Colgate
Quantity: 5
```

Click **Place Order**.

The application should:

1. Create the order.
2. Generate the signature.
3. Send the webhook.
4. Receive the webhook.
5. Verify the signature.
6. Accept the order.
7. Add the order to the received orders list.

The terminal should display a message similar to:

```text
Webhook received:
{'product': 'Colgate', 'quantity': 5}
```

---

## Test 2: Invalid Webhook

A webhook containing an incorrect signature should be rejected.

Expected response:

```http
401 Unauthorized
```

Example response:

```json
{
  "message": "Invalid webhook signature"
}
```

The invalid order should not be accepted.

This confirms that webhook signature verification is working correctly.

---

# Polling vs Webhooks

## Polling

With polling, one system repeatedly asks another system whether anything has changed.

```text
System A → Any new orders?
System B → No

System A → Any new orders?
System B → No

System A → Any new orders?
System B → Yes
```

This can result in unnecessary requests when there are no new events.

---

## Webhooks

With a webhook, the system that detects an event automatically sends information to another system.

```text
New Order
    │
    ▼
System A
    │
    │ Webhook
    ▼
System B
```

System B does not need to repeatedly ask System A whether a new order exists.

This project demonstrates the webhook approach.

---

# Learning Outcomes

This project helped demonstrate and reinforce:

* What a webhook is
* How webhooks differ from polling
* How webhook events can synchronize data between systems
* How HTTP POST requests deliver events
* How Flask routes work
* How to create a webhook receiver using Flask
* How to send HTTP requests using Python Requests
* How JSON data is sent and received
* How HMAC-SHA256 signatures work
* Why webhook requests should be verified
* How valid webhook requests are accepted
* How invalid webhook requests are rejected
* How to test webhook functionality
* How to use Git for version control
* How to use GitHub to track development

---

# Development Process

The project was developed incrementally using Git and GitHub.

The development process included commits for different stages:

```text
Initial project setup
        ↓
Set up project dependencies
        ↓
Create Flask application
        ↓
Create order interface
        ↓
Connect order form to backend
        ↓
Add webhook receiver
        ↓
Store received orders
        ↓
Send orders through webhook
        ↓
Add webhook signature verification
        ↓
Document the project
```

Using separate commits made it easier to track the changes made during development.

---

# Current Limitations

This is a learning prototype and is not intended for production use.

Current limitations include:

* Orders are stored only in memory.
* Orders are lost when the application restarts.
* System A and System B are simulated within the same Flask application.
* The webhook secret is currently stored directly in the source code.
* There is no database.
* There is no webhook retry mechanism.
* There is no message queue.
* There is no replay-attack protection.
* There is no timestamp validation.
* There is no rate limiting.
* Flask's development server is being used.

---

# Future Improvements

Possible improvements include:

* Store orders in a database such as MongoDB or PostgreSQL.
* Move the webhook secret into environment variables.
* Separate System A and System B into independent services.
* Add webhook retry handling.
* Add timestamps to webhook requests.
* Add replay-attack protection.
* Add automated tests.
* Add better error handling.
* Add logging and monitoring.
* Add a message queue.
* Improve the user interface.
* Add persistent order history.
* Deploy the application to the cloud.

---

# Project Status

**Completed — Learning Prototype**

The project currently demonstrates:

```text
Order Creation
      ↓
Webhook Sending
      ↓
Webhook Receiving
      ↓
HMAC-SHA256 Signature Verification
      ↓
Valid / Invalid Request Handling
      ↓
Order Synchronization
```

---

# Repository

GitHub Repository:

https://github.com/Emmanuelkemboi/webhook-synching

---

# Author

**Emmanuel Kemboi**

GitHub:

https://github.com/Emmanuelkemboi

---

# License

This project was created for learning and educational purposes.
