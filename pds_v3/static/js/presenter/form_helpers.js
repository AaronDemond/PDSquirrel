// enable/disable notification checkbox if comments are toggled
$("#comment_chk").change( function() {
	if ($(this).prop('checked') == true) {
		$('#notification_comment_chk').prop('disabled', false);
	} else {
		$('#notification_comment_chk').prop('checked', false);
		$('#notification_comment_chk').prop('disabled', true);
	}
});

var file_counter = 1 + ($('#file_select > option').length);
function addAttachment(){
	if (file_counter < 5) {
		file_counter++;
		file_counter_str = file_counter.toString();
		file_id = '#file-upload-'.concat(file_counter_str)
		var new_div = '<div class="control-group"><label for="">Attachment #'.concat(file_counter_str).concat('</label><input type="file" class="form-control" name="').concat(file_id).concat('" ></div>');
		$('#file-upload-container').append(new_div);
	} else {
		alert("You have added the maximum number of additional file fields to the form");
	}
}

function anotherFile() {
	$('#addfile').removeClass('hidden');
}
