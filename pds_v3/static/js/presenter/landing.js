function showTakesInfo() {

	$('#takeInfo').toggleClass('hidden');

	if ($('#infoLink').text() == '(info ▴)') {

		$('#infoLink').text('(info ▾)');
	} else {
		$('#infoLink').text('(info ▴)');
	}
}
