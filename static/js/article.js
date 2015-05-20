/**
 * Created by root on 15-4-15.
 */
$(function(){
    $(".forum_list li").hover(function(){
        $(this).addClass('active');
    },function(){
        $(this).removeClass('active');
    });


    jQuery('.counter').counterUp({
        delay: 10,
        time: 1000
    });



})