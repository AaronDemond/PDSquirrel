
    $(document).ready(function(){

    // toggling between search and browse

    function search(){
  	    $('#browse-options').addClass('hidden');
        $('#search-options').removeClass('hidden');
        $('#search-toggle').addClass('active');
  	    $('#browse-toggle').removeClass('active');
    }
    function browse(){
        $('#search-options').addClass('hidden');
        $('#browse-options').removeClass('hidden');
        $('#browse-toggle').addClass('active');
	      $('#search-toggle').removeClass('active');
    }

        $("#search-toggle").click(function(){
            search();
        });
        $("#browse-toggle").click(function(){
            browse();
        });

    });
