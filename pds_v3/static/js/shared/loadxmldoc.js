
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
	if ( typeof window.history.pushState !== 'undefined')
    window.history.pushState("state", direct_to, "?direct_to=" + direct_to);
	else
		$(this).addClass('active');
}
