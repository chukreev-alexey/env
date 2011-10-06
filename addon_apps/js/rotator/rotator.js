$(document).ready(function(){
    var is_auto = false;
    
    $("#RotatorWraper > .RotatorContainer:first > .RotatorItem:gt(0)").hide();
    $("#LeftRotatorArrow, #RightRotatorArrow").click(function(){
        if (!is_auto) {
            clearInterval(intervalID);
        }
        $("#LeftRotatorArrow, #RightRotatorArrow").hide();
        var is_left = $(this).is("#LeftRotatorArrow");
        var rotator_container = $("#RotatorWraper > .RotatorContainer:first");
        var active_rotator = {};
        var after_animate_css = {'margin-left': 0, 'left': 0};
        var current_rotator = rotator_container.children(".RotatorItem:visible:first");
        if (!current_rotator.hasClass("RotatorItem")){
            current_rotator = $("#RotatorWraper > .RotatorContainer > .RotatorItem:first");
        }
        var left_shift = ((is_left) ? '+' : '-') + '=' + current_rotator.outerWidth();
        if (is_left) {
            active_rotator = current_rotator.prev(".RotatorItem");
            rotator_container.css({'margin-left': '-100%'});
            if (!active_rotator.hasClass("RotatorItem")) {
                active_rotator = rotator_container.children(".RotatorItem:last").detach().prependTo(rotator_container);
            }
        }
        else {
            active_rotator = current_rotator.next(".RotatorItem");
            if (!active_rotator.hasClass("RotatorItem")) {
                active_rotator = rotator_container.children(".RotatorItem:first").detach().appendTo(rotator_container);
                after_animate_css = {'margin-left': 0, 'left': rotator_container.css('left')}
            }
        }
        active_rotator.show();
        rotator_container.animate(
            {left: left_shift},
            1000,
            function (){
                current_rotator.hide();
                rotator_container.css(after_animate_css);
                $("#LeftRotatorArrow, #RightRotatorArrow").show();
            }
        );
    });
    
    if ($("#RotatorWraper .RotatorItem").length > 1) {
		// Start rotator cycle
		var intervalID = setInterval(
			function(){
				is_auto = true;
				$("#RightRotatorArrow").click();
				is_auto = false;
			},
			5000
		);
	}

    
    
});