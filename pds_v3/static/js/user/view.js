
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

// toggles the reply boxes
$('.toggle-reply').click(function() {
  var $comment_reply = $(this).parent('.comment-footer').siblings('.comment-reply')
  $comment_reply.toggleClass('hidden');
  $comment_reply_all = $('.comment-reply');
  $comment_reply_all.not($comment_reply).addClass('hidden');
  $comment_reply_all.children('.form-group').removeClass('has-error has-feedback');
});

// removes error on focus out if theirs text in the reply box
$("textarea").focusout(function() {
  var $curr = $(this); //$.trim(msg).length <= 0
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
