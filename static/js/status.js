window.addEventListener('load', function () {
    let stripe;
    let formData = new FormData()
    formData.append('csrfmiddlewaretoken', Cookies.get('csrftoken'))
    fetch('/payments/status/', {
        method: 'POST',
        body: formData,
    })
        .then(function (response) {
            return response.json()
        })
        .then(function (data) {
            stripe = Stripe(data.stripePublicKey);

            const clientSecret = new URLSearchParams(window.location.search).get(
                'payment_intent_client_secret'
            );


            stripe.retrievePaymentIntent(clientSecret).then(({paymentIntent}) => {
                const message = document.querySelector('#message')

                // Inspect the PaymentIntent `status` to indicate the status of the payment
                // to your customer.
                //
                // Some payment methods will [immediately succeed or fail][0] upon
                // confirmation, while others will first enter a `processing` state.
                //
                // [0]: https://stripe.com/docs/payments/payment-methods#payment-notification
                switch (paymentIntent.status) {
                    case 'succeeded':
                        message.innerText = 'Success! Payment received.';
                        $('#success-button').removeClass('d-none')
                        break;

                    case 'processing':
                        message.innerText = "Payment processing. We'll update you when payment is received.";
                        break;

                    case 'requires_payment_method':
                        message.innerText = 'Payment failed. Please try another payment method.';
                        // Redirect your user back to your payment page to attempt collecting
                        // payment again
                        break;

                    default:
                        message.innerText = 'Something went wrong.';
                        break;
                }
            });

        })
});