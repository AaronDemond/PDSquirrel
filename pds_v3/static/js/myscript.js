
$(document).ready(function() {
	$('#pres-hub-nav li').click(function() {
	$("#pres-hub-nav li").removeClass('active');
	$(this).addClass('active');
    });
});

function loadXMLDoc(url,div, direct_to) {
	$.ajax( {
		type: "GET",
		url: url,
		success: function(data) {
			$(div).html( data );
		}
	});
	if (typeof context !== 'undefined' && context.state === "running" ) {
			context.close();
	}
    window.history.pushState("state", direct_to, "?direct_to=" + direct_to);
}
