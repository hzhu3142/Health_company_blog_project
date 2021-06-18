#donation/view.py

from flask import render_template, request, redirect, url_for, Blueprint
import stripe

donation = Blueprint('donation', __name__)

public_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'

stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

@donation.route('/donation')
def dona():
    return render_template('donation.html', public_key=public_key)

@donation.route('/donation/thankyou')
def thankyou():
    return render_template('thankyou.html')

@donation.route('/donation/payment', methods=['POST'])
def payment():

    # CUSTOMER INFORMATION
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    # CHARGE/PAYMENT INFORMATION
    charge = stripe.Charge.create(
        amount=2000,
        currency="usd",
        description="Donation",
        source="tok_visa",  # obtained with Stripe.js
        idempotency_key='fNuRHNzYl2KO8x0q'
    )
    return redirect(url_for('donation.thankyou'))