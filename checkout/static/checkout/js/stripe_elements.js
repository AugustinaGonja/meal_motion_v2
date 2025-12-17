const stripe_public_key = document.getElementById("id_stripe_public_key").textContent.slice(1, -1);
const client_secret = document.getElementById("id_client_secret").textContent.slice(1, -1);

// Initialise Stripe

const stripe = Stripe(stripe_public_key);
const elements = stripe.elements();


// Stripe CSS Styles

const style = {
    base: {
      color: '#000',
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSize: '16px',
      fontSmoothing: 'antialiased',
      '::placeholder': {
        color: '#aab7c4',
      },
    },
    invalid: {
      iconColor: '#dc3545',
      color: '#dc3545',
    },
};

// Create card element & mount

const card = elements.create('card', {style});
card.mount('#card-element');

// Handle real-time validation errors

card.addEventListener('change', function(event) { 
    const errorDiv = document.getElementById('card-errors');
    if (event.error) {
        const html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span> 
            <span>${event.error.message}</span>
        `;
        errorDiv.innerHTML = html;
    } else {
        errorDiv.textContent = '';
    }
});