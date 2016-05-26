
// on click
function ref(){
  $( "#capdiv" ).load( "/cap_ref/" );
}

$('input').focusout(function() {
  var curr = $(this);
  console.log("1");
  if(curr.val()==="") {
    console.log("to");
    curr.next('.help-block').text("Please enter a value");
  } else {
    curr.next('.help-block').text("");

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
