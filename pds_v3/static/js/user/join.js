
// on click
function ref(){
  $( "#capdiv" ).load( "/cap_ref/" );
}



$('input, select').focusout(function() {
  var $curr = $(this);
  var $parent = $(this).parent("div");
  var curr_id = $curr.attr('id');
  var curr_val = $curr.val();
  var error_occured = true;               // error assumed happen for concise code
  var error_text = "";                    // text defining the error

  if(curr_val=="") {
    if ($curr.prop('tagName') =='SELECT')
      error_text = "Please select a value";
    else
      error_text = "Please enter a value";

  } else if (curr_id == "email" && curr_val.search(/\S*@\S*\.\S*/)== -1) {
    error_text = "Please enter a valid email";

  } else if (curr_id == "email" && curr_val != $('#vemail').val()) {
     error_text = "Your email does not match";

  } else if (curr_id == "vemail" && curr_val != $('#email').val()) {
    error_text = "Your email does not match";

  } else if (curr_id == "pass" && curr_val.length < 8) {
    error_text = "You password needs to be atleast 8 characters";

  } else if (curr_id == "pass" && curr_val != $('#vpass').val()) {
     error_text = "Your password does not match";

  } else if (curr_id == "vpass" && curr_val != $('#pass').val()) {
    error_text = "Your password does not match";

  } else { // no errors found
    error_occured = false;
  }

  if (error_occured) {
    if (curr_id == "vpass") { // move vpass error messages to pass and warning sign on pass
      $curr = $("#pass");
      $curr.parent('div').removeClass("has-success");
      $curr.parent('div').addClass("has-error has-feedback");

    } else if (curr_id == "pass") {  // errors on pass and vpass on pass errors
      $("#vpass").parent('div').removeClass("has-success");
      $("#vpass").parent('div').addClass("has-error has-feedback");

    } else if (curr_id == "vemail") {
      $curr = $("#email");
      $curr.parent('div').removeClass("has-success");
      $curr.parent('div').addClass("has-error has-feedback");

    } else if (curr_id == "email") {
      $("#vemail").parent('div').removeClass("has-success");
      $("#vemail").parent('div').addClass("has-error has-feedback");
    }

    $parent.removeClass("has-success");
    $parent.addClass("has-error has-feedback");
  } else  {
    // syncing up password & email success
    if (curr_id == "vpass") {
      var pass = $('#pass');
      pass.parent("div").removeClass("has-error");
      pass.parent("div").addClass("has-success has-feedback");
      pass.next('.help-block').text(error_text);

    } else if (curr_id == "pass") {
      var vpass = $('#vpass');
      vpass.parent("div").removeClass("has-error");
      vpass.parent("div").addClass("has-success has-feedback");
      vpass.next('.help-block').text(error_text);
      
    } else if (curr_id == "vemail") {
      var email = $('#email');
      email.parent("div").removeClass("has-error");
      email.parent("div").addClass("has-success has-feedback");
      email.next('.help-block').text(error_text);

    } else if (curr_id == "email") {
      var vemail = $('#vemail');
      vemail.parent("div").removeClass("has-error");
      vemail.parent("div").addClass("has-success has-feedback");
      vemail.next('.help-block').text(error_text);
    }
    $parent.removeClass("has-error");
    $parent.addClass("has-success has-feedback");
  }

  $curr.siblings('.help-block').text(error_text);
});

$('#joinform').submit(function() {
  if ( $('#termbox').is(':checked') == 0 ) {
    $('#darken').siblings('.help-block').text("Please check the agreement");
    return false;
  }
});
