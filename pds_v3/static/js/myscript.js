
$(document).ready(function() {
	$('.nav li').click(function() {
	$(".nav li").removeClass('active');
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
    window.history.pushState("state", direct_to, "?direct_to=" + direct_to);
}
