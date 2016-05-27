
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
  console.log($curr);

  if(curr_val=="") {
    if ($curr.prop('tagName') =='SELECT')
      error_text = "Please select a value";
    else
      error_text = "Please enter a value";

  } else if (curr_id == "email" && curr_val.search(/\S*@\S*\.\S*/)== -1) {
    error_text = "Please enter a valid email";

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
    }
    $parent.removeClass("has-success");
    $parent.addClass("has-error has-feedback");
  } else  {
    // syncing up password success
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
    }
    console.log(curr_id);
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

//$('#joinform').submit(function() {
// error handler for submitting the join form
/*
  $('#term-help').remove();
  $('#page-alerts').empty();
  $('#page-alerts').addClass("hidden");
  var error = 0;
  var p_error = 0;
  // text_input is div holding inputs that contain text inputs

  */
  //return false;
  /*
  try {
    for (var text_field in text_input) {
      if (text_input.hasOwnProperty(text_field)) {
        if (text_input[text_field].val()==="") {
          text_input[text_field]
        }
      }
    }
  } catch (e) {
    console.log(e);
  } finally {
    return false;
  }
*/

   /*
  if ( $('#email').val() == "" || $('#first_name').val() == "" || $('#last_name').val() == "" || $('#email').val() == "" || $('#id_captcha_0').val() == "" || $('#termbox').is(':checked') == 0) {
    $('#example').click();
    error++;
  }
  if ( $('#termbox').is(':checked') == 0 ) {
    $('#termdiv').append("<p class=\"bg-danger\" id = \"term-help\" style=\"background-color: white; font-size: 1.2em; color: rgb(169, 68, 66); font-weight: bold\" c>You must accept the terms and conditions to use PD Squirrel</p>");
  }

  $('.help-block').remove();
  $('.form-group').removeClass('has-error');

  if ( $('#email').val() != $('#vemail').val() ) {
    $('#emailgroup').addClass("has-error");
    $('#vemailgroup').addClass("has-error");
    $('#emailgroup').append("<span id=\"emailhelp\" class=\"help-block\">Emails do not match</span>");
    $('#vemailgroup').append("<span id=\"vemailhelp\" class=\"help-block\">Emails do not match</span>");
    error++;
  }
  if ( $('#pass').val() != $('#vpass').val() ) {
    $('#passgroup').addClass("has-error");
    $('vpassgroup').addClass("has-error");
    $('#passgroup').append("<span id=\"passmatchhelp\" class=\"help-block\">Passwords do not match</span>");
    $('#vpassgroup').append("<span class=\"help-block\">Passwords do not match</span>");
    p_error++;
    error++;
  }

  if ( $('#pass').val().length < 8 ) {
    p_error++;
    error++;
    $('#passgroup').addClass("has-error");
    $('#passgroup').append("<span id=\"passlenhelp\" class=\"help-block\">Password must be over 8 characters long</span>");
  }

  if (error > 0) {
     return false;
  } else {
      return true;
  }*/

//});
