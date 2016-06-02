// aria-expanded
// write your own data-toggle later

// comment url: /pd/session/comment/
// delete url: /pd/session/comment/delete/

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

$("button[name^='reply-btn']").click(function() {
  var $curr = $(this);
  var msg = $curr.siblings("textarea").val();
  var csrf = $("input[name='csrfmiddlewaretoken']").val();
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

/*
$("textarea").keypress(function(event) {
  var key = event.which;
  if (key == 13) {
    event.preventDefault();
    console.log("Text");
    return false;
  }
});
*/
