// enable/disable notification checkbox if comments are toggled
$("#comment_chk").change( function() {
	if ($(this).prop('checked') == true) {
		$('#notification_comment_chk').prop('disabled', false);
	} else {
		$('#notification_comment_chk').prop('checked', false);
		$('#notification_comment_chk').prop('disabled', true);
	}
});

