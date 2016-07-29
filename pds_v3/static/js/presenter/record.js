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

function showTrimInfo(triminfolink) {
	row_id = '#triminfo';
	$(row_id).toggleClass("hidden");
	if ($(triminfolink).text() == '(info ▾)'){
		$(triminfolink).text('(info ▴)');
	}
	else {
		$(triminfolink).text('(info ▾)');
	}
}
function closeInfo() {
	$('#info-row').addClass('hidden');
	$('#infoLink').text('(info ▾)');
}
function closeTrim() {
	$('#triminfo').addClass('hidden');
	$('#trimbtn').text('(info ▾)')
}
