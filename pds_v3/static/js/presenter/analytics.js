
$("#analytics-form").submit(function(event) {

	// Keep page from reloading
	event.preventDefault();
	var $form = $(this);

	// Serialize date for server
	var	start_val = $form.find("input[name='start']").val();
	var	end_val = $form.find("input[name='end']").val();
	var	csrf = $form.find("input[name='csrfmiddlewaretoken']").val();
	var	url = $form.attr("action");
	var	start_date = new Date(start_val);
	var	end_date = new Date(end_val);

	// If date passes, append table returned
	if (start_date>end_date) {
		alert("The start date is greater then the end date unable to display report");
	} else {
		var posting = $.post(url, { start: start_val, end: end_val, csrfmiddlewaretoken : csrf } );
		posting.done(function(data) {
			$("#result").empty();
			$("#result").append(data);
		});
	}
});
