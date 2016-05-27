$('a').click(function() {
	$('.msg-container').empty();
});

function hideStatus() {
    $('.status-bar').addClass('hidden');
    $('.status-link').text('(info ▾)');
}


function hideSuspend() {
    $('.removal-bar').addClass('hidden');
    $('.suspend-link').text('Remove ▾');

}

function hideCancelBar() {
    $('.cancel-removal-bar').addClass('hidden');
    $('.cancel-removal-link').text('Cancel removal ▾');
}

function showStatus(id, infolink) {
	hideCancelBar();
	hideSuspend();

	if ($(infolink).text() ==  '(info ▴)') {
		hideStatus();
		return;
	}

    hideStatus();
    row_id = "#status-" + id;
    $(infolink).text('(info ▴)');
    $(row_id).toggleClass("hidden");

}


function showRemove(id, suslink) {
    hideCancelBar();
		hideStatus();

    if ($(suslink).text() == 'Remove ▴') {
		hideSuspend();
		return;
	}
    hideSuspend();
    row_id = "#remove-" + id;
    $(row_id).toggleClass("hidden");
    $(suslink).text('Remove ▴');

}

function showSuspendCancel(id, suslink) {
    hideSuspend();
	hideStatus();

    if ($(suslink).text() == 'Cancel removal ▴') {
		hideCancelBar();
		return;
	}

    hideCancelBar();
    row_id = "#remove-cancel-" + id;
    $(suslink).text('Cancel removal ▴');
    $(row_id).toggleClass("hidden");
}

