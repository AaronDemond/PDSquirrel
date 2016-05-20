// Directs to appropriate sub page after form POST

$(document).ready(function() {

	$('button').click(function() {
	     $('button').removeClass('active');
	     $(this).addClass('active');
	});

	if ("{{direct_to}}" == "sessions") {
	    loadXMLDoc('/user/presenter/dash/?mysessions', '#page-content');
	    $("li").removeClass("active");
	    $("#sessions-link").addClass("active");
	}

	else if  ("{{direct_to}}" == "upload") {
	    loadXMLDoc('/ajax-test', '#page-content');
	    $("li").removeClass("active");
	    $("#upload-link").addClass("active");

	}

	else if  ("{{direct_to}}" == "info") {
	    loadXMLDoc('/user/presenter/dash/?myaccount', '#page-content');
	    $("li").removeClass("active");
	    $("#info-link").addClass("active");
	}

	else if  ("{{direct_to}}" == "recorder") {
	    loadXMLDoc('/record/', '#page-content');
	    $("li").removeClass("active");
	    $("#record-link").addClass("active");
	}

	
	else if  ("{{direct_to}}" == "analytics") {
	    loadXMLDoc('/user/presenter/dash/?analytics', '#page-content');
	    $("li").removeClass("active");
	    $("#analytics-link").addClass("active");
	}

	else if  ("{{direct_to}}" == "private") {
	    loadXMLDoc('/user/presenter/dash/?myinfo', '#page-content');
	    $("li").removeClass("active");
	    $("#private-info-link").addClass("active");
	}

	else {
	    loadXMLDoc('/user/presenter/dash/?landing', '#page-content');
	    $("li").removeClass("active");
	    $("#dash-link").addClass("active");
	}

	$("a").click(function() {
	    $(".msg-container").empty();
    	});
});
