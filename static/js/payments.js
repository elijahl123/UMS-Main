window.addEventListener('load', function () {
    let stripe;

    let clientSecret;
    let formData = new FormData()
    formData.append('csrfmiddlewaretoken', Cookies.get('csrftoken'))
    fetch('/payments/create-subscription/' + type + '/', {
        method: 'POST',
        body: formData,
    })
        .then(function (response) {
            return response.json()
        })
        .then(function (data) {
            clientSecret = data.clientSecret
            stripe = Stripe(data.stripePublicKey);
            const options = {
                clientSecret: clientSecret,

                appearance: {
                    theme: 'flat',

                    variables: {
                        colorPrimary: 'var(--main-color)',
                        colorBackground: 'whitesmoke',
                        colorText: 'black',
                    }

                },
            };


            const elements = stripe.elements(options);


            const paymentElement = elements.create('payment');
            paymentElement.mount('#payment-element');

            const form = document.getElementById('payment-form');

            form.addEventListener('submit', async (event) => {
                event.preventDefault();

                const {error} = await stripe.confirmPayment({
                    elements,
                    confirmParams: {
                        return_url: window.location.origin + "/payments/status/",
                    }
                });

                if (error) {
                    // This point will only be reached if there is an immediate error when
                    // confirming the payment. Show error to your customer (e.g., payment
                    // details incomplete)
                    alert(error.message)
                } else {
                    // Your customer will be redirected to your `return_url`. For some payment
                    // methods like iDEAL, your customer will be redirected to an intermediate
                    // site first to authorize the payment, then redirected to the `return_url`.
                }
            });

        })
});