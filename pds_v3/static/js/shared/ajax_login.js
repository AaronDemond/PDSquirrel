$(document).ready(function(){

	$( "#login-form" ).submit(function(event) {
		console.log("login function");
		$("#login-msg").html("Loading, please wait..");
		event.stopPropagation();
		var url = "/user/login/";
		$.ajax({
			type: "POST",
			url: url,
			data: $("#login-form").serialize(),
			success: function(data)
			{

				if (data == 'success') {
					location.reload(true); // true = query server again, rather than load from (local) cache
				}
				else {
					$("#login-msg").html(data);
				}

			}
			});
	return false;
	});

});
