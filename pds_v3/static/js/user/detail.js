
// stripe
    Stripe.setPublishableKey('pk_test_URIzgmhYoVYuzDm9Q98RHkIQ');
    jQuery(function($) {
      $('#payment-form').submit(function(event) {
        var $form = $(this);
		var $url = $form.attr('action');

		if (document.getElementById('e_card').checked == true) {
			event.preventDefault();
			$form.find('button').prop('disabled', true);
			$.ajax({
				type: "POST",
				url:	$url,
				data: $form.serialize(),
			}).done(function(data) {
				$form.append(data);
			}).fail(function(data) {
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
	  var $url = $form.attr('action');

      if (response.error) {
        // Show the errors on the form
        $form.find('.payment-errors').text(response.error.message);
        $form.find('button').prop('disabled', false);
      } else {
        // response contains id and card, which contains additional card details
        var token = response.id;
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
$(document).on("click", ".delete", function() {
  var comment_id = $(this).val();
  var del_btn = $(this);
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
		// Remove comment
		$('#comment-' + comment_id).remove();
		// If not a child, then comment is a parent, so we remove its replies.
		if (del_btn.parents('div.reply').length == 0)
			$('#comment-' + comment_id + '-replies').remove();
    }
  });
});

$(document).on("click", "#main-textarea", function() {
	$(this).siblings("button").removeClass("hidden");
	$('.comment-reply').addClass('hidden');
});

$(document).on("click", ".reply-textarea", function() {
	$(this).siblings("button").removeClass("hidden");
	$('#main-textarea').siblings("button").addClass("hidden");
});

$(document).on("click", ".toggle-reply", function() {
  var $comment_reply = $(this).parent('.comment-footer').siblings('.comment-reply');
  $comment_reply.toggleClass('hidden');
  $comment_reply_all = $('.comment-reply');
  $comment_reply_all.not($comment_reply).addClass('hidden');
  $form_group = $comment_reply_all.children('.form-group');
  $form_group.removeClass('has-error has-feedback');

  $textarea = $comment_reply.children('.form-group').children("textarea");
  var textarea_text = $textarea.text();
  $textarea.focus().val('').val(textarea_text);

  $('#main-comment-btn').addClass('hidden');
  $('#main-comment-cancel-btn').addClass('hidden');


  $('.edit-section').addClass('hidden');
  $('.comment-footer').removeClass('hidden');
  $('.comment-body').removeClass('hidden');
});

// removes error on focus out if theres text in the reply box
$(document).on("focusout", "textarea", function() {
  var $curr = $(this);
  var $form_group = $curr.parent('.form-group');
  var msg = $curr.val();
  if ($form_group.hasClass('has-error') && $.trim(msg).length > 0) {
    $form_group.removeClass('has-error has-feedback');
  }

});

$(document).on('click', ".cancel-comment-btn", function cancelComment() {
	var text_area = $(this).siblings("textarea");
	$('.comment-reply').addClass('hidden');
	text_area.val('');

});
$(document).on('click', "#main-comment-cancel-btn", function cancelComment() {
	$(this).siblings("button").addClass('hidden');
	$(this).addClass('hidden');

});

// submit a comment
$(document).on("click", "button[name^='reply-btn']", function() {
  var $curr = $(this);
  var msg = $curr.siblings("textarea").val();
  var csrf = $("#pd_id").next().val();
  var pd_id = $("#pd_id").val();
  var reply_id = $curr.val();
  var parent_id = $(this).attr("__parent");
  if ($.trim(msg).length <= 0) {
    $curr.parent(".form-group").addClass("has-error has-feedback");
  } else {

    var data = {
        msg: msg,
        reply_id: reply_id,
        pd_id: pd_id,
		parent_id: parent_id,
        csrfmiddlewaretoken: csrf
     };

     $.ajax({
       type: "POST",
       url: "/pd/session/comment/",
       data: data,
       success: function(comment_data) {
			$curr.siblings("textarea").val('');
			$('.comment-reply').addClass('hidden');
		   if (typeof parent_id !== typeof undefined && parent_id !== false) {
				visual_parent_row = $("#comment-" + reply_id + "-replies");
				visual_parent_row.append(comment_data);
			}	else {
			   $('#comment-holder').prepend(comment_data);
		   }

       	}
      });
  }
});

/* Toggle edit comment section */
$(document).on("click", ".toggle-edit", function() {
  var $curr = $(this);
  var $comment_footer = $curr.parent('.comment-footer');

  var $edit_section = $comment_footer.siblings('.edit-section');
  var $comment_body = $comment_footer.siblings('.comment-body');
  var comment_text = $.trim($comment_body.text());

  $edit_section.removeClass('hidden');
  $comment_footer.addClass('hidden');
  $comment_body.addClass('hidden');

  var $edit_section_all = $('.edit-section').not($edit_section);
  var $comment_footer_all = $('.comment-footer').not($comment_footer);
  var $comment_body_all = $('.comment-body').not($comment_body);
  $edit_section_all.addClass('hidden');
  $comment_footer_all.removeClass('hidden');
  $comment_body_all.removeClass('hidden');

  $('.comment-reply').addClass('hidden');
  $('.form-group').removeClass("has-error has-feedback");

  $edit_section.children('.form-group').children('textarea').val(comment_text)

});

/* Cancel a comment edit */
$(document).on("click", ".cancel-edit-btn", function(){
  close_curr_edit(this);
});

/* Submit edit */
$(document).on("click", ".submit-edit-btn", function() {
  var curr = this;
  var $curr = $(this);
  var $form_group = $curr.parent('.form-group');

  var $textarea = $curr.siblings("textarea");
  var msg = $textarea.val();

  var csrf = $("#pd_id").next().val();
  var pd_id = $curr.val();
  var comment_id = $curr.val();

  if ($.trim(msg).length <= 0) {
    $form_group.addClass("has-error has-feedback");
  } else {

    var data = {
        msg: msg,
        comment_id: comment_id,
        pd_id: pd_id,
        csrfmiddlewaretoken: csrf
     };
     $.ajax({
       type: "POST",
       url: "/pd/session/comment/edit/",
       data: data,
       success: function(comment_data) {
         $form_group.parent('.edit-section').siblings('.comment-body').html(msg);
         close_curr_edit(curr);
       }
     });
   }
});

function close_curr_edit(curr) {
  var $curr = $(curr);
  var $form_group = $curr.parent('.form-group');
  var $edit_section = $form_group.parent('.edit-section');
  var $comment_footer = $edit_section.siblings('.comment-footer');
  var $comment_body = $edit_section.siblings('.comment-body');

  $edit_section.addClass('hidden');
  $comment_footer.removeClass('hidden');
  $comment_body.removeClass('hidden');

}
