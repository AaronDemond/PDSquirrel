
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});

Stripe.setPublishableKey('pk_test_URIzgmhYoVYuzDm9Q98RHkIQ');
jQuery(function($) {
  $('#payment-form').submit(function(event) {
    var $form = $(this);

    // Disable the submit button to prevent repeated clicks
    $form.find('button').prop('disabled', true);

    Stripe.card.createToken($form, stripeResponseHandler);

    // Prevent the form from Sessiange pn with the default action
    return false;
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
    // Insert the token into the form so it gets submitted to the server
    $form.append($('<input type="hidden" name="stripeToken" />').val(token));


    // and submit
    $form.get(0).submit();
  }
};

function makeEmailVisible(){
$('#email-confirm-td').removeClass("hidden");
$('#email').removeAttr("disabled");
$('#email-box-2').removeAttr("disabled");
    $('#type').val("email");
}

function makePassVisible(){
  $('#pass-box-1').removeAttr("disabled");
  $('#pass-box-2').removeAttr("disabled");
  $('#pass-box-3').removeAttr("disabled");
  $('#pass-confirm-td').removeClass("hidden");
  $('#pass-auth-tr').removeClass("hidden");
  $('#type').val("password");
}


// Not used
  function makeVisible(id){
  $('#save-btn').removeAttr("");
  $('#save-btn').removeClass("hidden");

  if (id == first_name)
    $('#first_name').removeAttr("");
  if (id == last_name)
    $('#last_name').removeAttr("");
  if (id == email) {

    $('#email-confirm-td').removeClass("hidden");
    $('#email-box-2').removeAttr("disabled");
    $('#email-box-2').removeAttr("");
    $('#email-box-2').addClass("hidden");

  }
  if (id == 4) {
    $('#pass-box-1').removeAttr("disabled");
    $('#pass-box-2').removeAttr("disabled");
    $('#pass-box-3').removeAttr("disabled");
    $('#pass-confirm-td').removeClass("hidden");
    $('#pass-auth-tr').removeClass("hidden");
  }
  if (id == 5) {
    $('#society').removeAttr("");
  }

}

$(".delform").submit(function() {
  var c = confirm("Are you sure you want to remove this card?");
  return c;
});

$(".memsubmit").click(function() {
  $("#btnholder").empty();
  $("#btnholder").append("<button id='memsubform' onclick='memsubform()' class='btn btn-success'>Confirm</button>");
});

function memsubform() {
    $("#memform").submit();
}

$('#cancel_btn').click(function(e) {
	$('#myModal').modal('toggle');
	$("form#payment-form :input").each( function() {
		$(this).val('');
	});

});
