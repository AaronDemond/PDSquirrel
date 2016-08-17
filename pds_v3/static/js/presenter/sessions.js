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
	hidePreview();

	if ($(infolink).text() ==  '(info ▴)') {
		hideStatus();
		return;
	}

    hideStatus();
    var row_id = "#status-" + id;
    $(infolink).text('(info ▴)');
    $(row_id).toggleClass("hidden");

}

function hidePreview() {
	// removes all preview contents from page and
	// puts link at proper state

	$('.preview-link').text('Listen ▾');
	$(".preview-bar").each(function() {
			$(this).empty();
	});
}

function previewAudio(id, preview_link) {
	/* fills preview container with audio and toggles
	 * button arrow text */

	// Hide other drop downs
	hideCancelBar();
	hideStatus();
	hideSuspend();

	// id of the row to insert audio
	var row_id = "#preview-" + id;

	// Formatted audio template to insert
	var html = '<div class="col-lg-12 preview-col"> \
		<audio id="player" style="width: 100%"controls> \
			<source src="/audio/'+id+'" type="audio/mpeg"> \
			</audio> \
		</div>';

	// Clear audio elements from page
	$(".preview-bar").each(function() {
		$(this).empty();
	});

	// Change arrow to closed state on all other links
	$(".preview-link").each(function() {
		if ( !$(this).is($(preview_link)) ) {
			$(this).text('Listen ▾');
		}
	});

	// Toggle state of arrow in clicked preview button
	if ($(preview_link).text() == 'Listen ▾' ) {
		$(preview_link).text('Listen ▴');
		$(row_id).append(html);

	} else {
		$(preview_link).text('Listen ▾');
		$(row_id).empty();

	}

}

function showRemove(id, suslink) {
    hideCancelBar();
		hideStatus();
		hidePreview();

    if ($(suslink).text() == 'Remove ▴') {
		hideSuspend();
		return;
	}
    hideSuspend();
    var row_id = "#remove-" + id;
    $(row_id).toggleClass("hidden");
    $(suslink).text('Remove ▴');

}

function showSuspendCancel(id, suslink) {
    hideSuspend();
	hideStatus();
	hidePreview();

    if ($(suslink).text() == 'Cancel removal ▴') {
		hideCancelBar();
		return;
	}

    hideCancelBar();
    var row_id = "#remove-cancel-" + id;
    $(suslink).text('Cancel removal ▴');
    $(row_id).toggleClass("hidden");
}
