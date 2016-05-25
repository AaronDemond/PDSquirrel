
// stripe

    Stripe.setPublishableKey('pk_test_URIzgmhYoVYuzDm9Q98RHkIQ');
    jQuery(function($) {
      $('#payment-form').submit(function(event) {
        var $form = $(this);
		var $url = $form.attr('action');

		if (document.getElementById('e_card').checked == true) {
			event.preventDefault();
			$form.find('button').prop('disabled', true);
			console.log('existing card used');
			$.ajax({
				type: "POST",
				url:	$url,
				data: $form.serialize(),
			}).done(function(data) {
				$form.append(data);
			}).fail(function(data) {
			console.log('failed');
			});
			return false;
		}
		if (document.getElementById('n_card').checked == true) {
			// Disable the submit button to prevent repeated clicks
			$form.find('button').prop('disabled', true);

			Stripe.card.createToken($form, stripeResponseHandler);

			// Prevent the form from Sessiange pn with the default action
			return false;
		}
      });
    });

    function stripeResponseHandler(status, response) {
      var $form = $('#payment-form');

      if (response.error) {
        // Show the errors on the form
        $form.find('.payment-errors').text(response.error.message);
        $form.find('button').prop('disabled', false);
      } else {
        // response contains id and card, which contains additional card details
        var token = response.id;
		console.log(token);
        // Insert the token into the form so it gets submitted to the server
        $form.append($('<input type="hidden" name="stripeToken" />').val(token));

        // and submit
		$.ajax({
			type: "POST",
			url:	$url,
			data: $form.serialize(),
		}).done(function(data) {
			$form.append(data);
		}).fail(function(data) {
			console.log('failed');
		});
      }
    };

// radio button toggling

$(document).ready(function() {

	var $new_radio = document.getElementById('n_card');
	var $existing_radio = document.getElementById('e_card');
	var $cancel_btn_one = document.getElementById('cancel_btn_one');

	$('#existing_card_col :input').prop('disabled', true);
	$('#new_card_col :input').prop('disabled', true);


	$cancel_btn_one.onclick = function(e) {
		e.preventDefault();
		$('#payment-modal').modal('hide');
		$('#existing_card_col :input').val('');
		$('#new_card_col :input').val('');
	}

	$new_radio.onclick = function() {
		$existing_radio.checked = false;
		$('#existing_card_col :input').prop('disabled', true);
		$('#new_card_col :input').prop('disabled', false);
		$('#existing_card_col :input').val('');
	}
	$existing_radio.onclick = function() {
		$new_radio.checked = false;
		$('#new_card_col :input').prop('disabled', true);
		$('#existing_card_col :input').prop('disabled', false);
		$('#new_card_col :input').val('');

	}
});
