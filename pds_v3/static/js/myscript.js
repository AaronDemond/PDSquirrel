
$(document).ready(function() {
	$('.nav li').click(function() {
	$(".nav li").removeClass('active');
	$(this).addClass('active');
    });
});

function loadXMLDoc(url,div, direct_to)
{
    // Changes url to have flag set incase user refreshes

    var xmlhttp;
    //url = 'https://www.pdsquirrel.ca';
    url = 'http://127.0.0.1' + url;
    console.log('url used: ' + url);

    xmlhttp = new XMLHttpRequest();
    //url = 'https://www.pdsquirrel.ca//user/presenter/dash/?myaccount';
    xmlhttp.onreadystatechange = function(){
	if (xmlhttp.readyState==4) {
	    $(div).html(xmlhttp.responseText);
	}
    }
    xmlhttp.open("GET",url,true);
    //xmlhttp.setRequestHeader('Access-Control-Allow-Origin', 'https://www.pdsquirrel.ca');
    xmlhttp.send();
    window.history.pushState("state", direct_to, "?direct_to=" + direct_to);
}
