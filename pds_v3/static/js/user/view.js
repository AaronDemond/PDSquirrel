// aria-expanded
// write your own data-toggle later

// url: /pd/session/comment/

$("button[name^='reply-btn']").click(function() {
  var $curr = $(this);
  var msg = $curr.siblings("textarea").val();
  var csrf = $("input[name='csrfmiddlewaretoken']").val();
  var pd_id = $("#pd_id").val();
  var reply_id = $curr.val();

  var data = {
                msg: msg,
                reply_id: reply_id,
                pd_id: pd_id,
                csrfmiddlewaretoken: csrf
             };
             
  console.log(data);
  /*
  $.ajax({
    type: "POST",
    url: "/pd/session/comment/",
    data: data,
    success: function() {
      location.reload();
    }
  });
  */
});
