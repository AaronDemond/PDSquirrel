function showInfo(infolink){
	row_id = "#info-row";
	$(row_id).toggleClass("hidden");
	if ($(infolink).text() == '(info ▾)'){
		$(infolink).text('(info ▴)');
	}
	else {
		$(infolink).text('(info ▾)');
	}
}
function closeInfo() {
	$('#info-row').addClass('hidden');
	$('#infoLink').text('(info ▾)');
}
