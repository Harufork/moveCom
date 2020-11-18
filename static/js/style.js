$(document).ready(function(){
	$(".mainpanel").hide();
	$(".hidepanel").click(function(){
		var dataAttrib = this.getAttribute("data-selecthide");
		if (dataAttrib !== null) {
			$(dataAttrib).animate({
                width: "toggle"
            });
			var tx = $(this).text();
			if( tx === "]" ){
				$(this).text("[");
			} else if ( tx === "[" ) {
				$(this).text("]");
			}; 
		}
	});


});
