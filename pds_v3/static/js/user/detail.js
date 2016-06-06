
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

// Toggle description box size
function showDescription() {
	$(document).ready(function() {
		$('#pd-description-small').toggleClass('hidden');
		$('#pd-description-full').toggleClass('hidden');

		$btn = $('#more-btn');
		if ( $btn.text() == 'Show More') {
			$btn.text('Show Less');
		}
		else if ( $btn.text() == 'Show Less') {
			$btn.text('Show More');
		}
	});
}


/*---------------------------*/
//      Comment Section      //
/*---------------------------*/

//delete a comment
$('.delete').click(function() {
  var comment_id = $(this).val();
  var csrf = $("input[name='csrfmiddlewaretoken']").val();

  data = {
    csrfmiddlewaretoken: csrf,
    comment_id: comment_id
  };

  $.ajax({
    type: "POST",
    url: "/pd/session/comment/delete/",
    data: data,
    success: function(data) {
      location.reload();
    }
  });
});

$.fn.setCursorPosition = function (pos) {
  this.each(function (index, elem) {
    if (elem.setSelectionRange) {
      elem.setSelectionRange(pos, pos);
    } else if (elem.createTextRange) {
      var range = elem.createTextRange();
      range.collapse(true);
      range.moveEnd('character', pos);
      range.moveStart('character', pos);
      range.select();
    }
  });
  return this;
};

// toggles the reply boxes
$('.toggle-reply').click(function() {
  var $comment_reply = $(this).parent('.comment-footer').siblings('.comment-reply');
  $comment_reply.toggleClass('hidden');
  $comment_reply_all = $('.comment-reply');
  $comment_reply_all.not($comment_reply).addClass('hidden');
  $form_group = $comment_reply_all.children('.form-group');
  $form_group.removeClass('has-error has-feedback');

  $textarea = $comment_reply.children('.form-group').children("textarea");
  var textarea_text = $textarea.text();
  console.log("lol"+textarea_text);
  $textarea.focus().val('').val(textarea_text);

});

// removes error on focus out if theirs text in the reply box
$("textarea").focusout(function() {
  var $curr = $(this);
  var $form_group = $curr.parent('.form-group');
  var msg = $curr.val();
  if ($form_group.hasClass('has-error') && $.trim(msg).length > 0) {
    $form_group.removeClass('has-error has-feedback');
  }
});

// submit a comment
$("button[name^='reply-btn']").click(function() {
  var $curr = $(this);
  var msg = $curr.siblings("textarea").val();
  var csrf = $("#pd_id").next().val();
  var pd_id = $("#pd_id").val();
  var reply_id = $curr.val();
  if ($.trim(msg).length <= 0) {
    $curr.parent(".form-group").addClass("has-error has-feedback");
  } else {
    var data = {
        msg: msg,
        reply_id: reply_id,
        pd_id: pd_id,
        csrfmiddlewaretoken: csrf
     };
     $.ajax({
       type: "POST",
       url: "/pd/session/comment/",
       data: data,
       success: function() {
         location.reload();
       }
      });
  }
});
