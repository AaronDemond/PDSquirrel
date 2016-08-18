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
/*
span not required

example:
<a name="js-info-X">(info <span>&#9662;</span>)</a>
<div name="js-info-X" class="hidden">
...
<button name="js-info-X">...</button>
</div>

<script>
info_box_activate(); // Reload info box for ajax
</script>
*/
info_box_activate();

function info_box_activate() {
	var js_info = $("[name^='js-info-']");
	js_info.filter('a').click(function() {
		var $curr = $(this);
		var curr_name = $curr.attr('name');
		var $info_box = $('[name="'+curr_name+'"]').filter('div');
		var $arrow = $curr.children('span');
		if ( $info_box.hasClass('hidden') ) { // if hidden -> display

			$info_box.removeClass('hidden'); // Display info box
			var $all_other_info = $("[name^='js-info-']"); // all other info elements
			$all_other_info.filter('div').not($info_box).addClass('hidden'); // hide all other info boxes
			$all_other_info.filter('a').children('span').html('&#9662;'); // flip all other info arrows
			$arrow.html('&#9652;');

		} else { // if visible -> hide

			$info_box.addClass('hidden');
			$arrow.html('&#9662;');
		}
	});

	// cancel / close button
	js_info.filter('button').click(function() {
		var $curr = $(this);
		var curr_name = $curr.attr('name');
		var $info_box = $('[name="'+curr_name+'"]').filter('div');
		$('[name="'+curr_name+'"]').filter('a').children('span').html('&#9662;'); // flip arrow

		$info_box.addClass('hidden');
	});

}
