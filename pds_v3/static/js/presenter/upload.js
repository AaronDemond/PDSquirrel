
/*	file counter gets increased with each upload, resets on page reload.
	adds a div with a label and new file input box to form
	server loops through files
*/

var file_counter = 1;
function addAttachment(){
	if (file_counter < 5) {
		file_counter++;
		file_counter_str = file_counter.toString();
		file_id = '#file-upload-'.concat(file_counter_str)
		var new_div = '<div class="control-group"><label for="">Attachment #'.concat(file_counter_str).concat('</label><input type="file" class="form-control file-input" name="').concat(file_id).concat('" ></div>');
		$('#file-upload-container').append(new_div);
	} else {
		alert("You have added the maximum number of additional file fields to the form");
	}
}

function anotherFile() {
	$('#addfile').removeClass('hidden');
}

$("form").submit(function() {
	$('#loader').removeClass('hidden');
	$('fieldset').addClass('hidden');
	});
$('#online').click(function () {

	$('#online_input').prop('disabled', false);
	var upload_input = $('#upload_input')
	upload_input.prop('disabled', true);
	upload_input.val('');
});
$('#upload').click(function() {
	$('#upload_input').prop('disabled', false);
	var online_input = $('#online_input');
	online_input.prop('disabled', true);
	online_input.val('');
});
