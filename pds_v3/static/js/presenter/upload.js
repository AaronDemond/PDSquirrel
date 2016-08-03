
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
