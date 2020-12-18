	$(".mainpanel").hide();
	$(".additionallylist").hide();
	$(".accbtms").hide();
	$(".notificationdiv").hide();
$(document).ready(function(){


	$('.mask-phone').mask('+7(999)999-99-99');


	
	$(".hidepanel").click(function(){
		var dataAttrib = this.getAttribute("data-selecthide");
		if (dataAttrib !== null) {
			$(dataAttrib).animate({width: "toggle"},300);
			var tx = $(this).text();
			if( tx === "]" ){
				$(this).text("[");
			} else if ( tx === "[" ) {
				$(this).text("]");
			}; 
		}
	});

	
	$(".additionally").click(function(){
		$(".additionallylist").animate({
			top: "toggle",
		},300);
		var tx = $(this).text();
		if( tx === "Ещё ▽" ){
			$(this).text("Ещё ▲");
		} else if ( tx === "Ещё ▲" ) {
			$(this).text("Ещё ▽");
		}; 
	});

	
	$(".hideabtn").click(function(){
		$(".accbtms").animate({
			top: "toggle",
			height: "toggle"
		},300);
	});
	$(".accountbtm").click(function(){
		$(".accbtms").animate({
			top: "toggle",
			height: "toggle"
		},300);
	});


	function showNewContent() {
 		$('.notificationlist').show('normal',hideLoader)
	}

	function hideLoader() {
 		$('.notificationlist').fadeOut('normal');
	}

	function loadContent() {
 		
	}



	$(".hidenotificationlist").click(function(){
		$(".notificationdiv").animate({
			top: "toggle",
			height: "toggle"
		},250, "linear");
	});


	var toc = $('.newrequestmove').find('input[name=time_of_completion]');
	var tp =$('.newrequestmove').find('select[name=time_type]');
	if (tp.val() == 'o') { 
		toc.show(); 
		toc.prop('required', true);
	}else{
		toc.hide();
		toc.prop('required', false);
	};
	tp.change(function() {
 		if ($( this ).val() == 'o') { 
 			toc.show(); 
 			toc.prop('required', true);
 		}else{
 			toc.hide();
 			toc.prop('required', false);
 		};
	});


	var count_id = $('#routs_count').attr("value"); 
	var li = $('#zero_route').clone();
	$("#add_route").click(function(){
		if (count_id<10) {
			var li_clone = li.attr("id", "").clone();
			li_clone.children('#point_a0').attr("name", 'point_a' + count_id).attr("value", "").attr("class", "");
			li_clone.children('#point_b0').attr("name", 'point_b' + count_id).attr("value", "").attr("class", "");
			li_clone.children('label').detach();
			count_id++;
			$('#adding_route').append(li_clone);
		}else if(count_id==10){
			count_id++;
			$('#adding_route').append('<p>Если вы являетесь корпаративным клиентом, то свяжитесь с нами!</p>');
		}
	});	
});
