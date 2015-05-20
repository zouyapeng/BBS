/**
 * Created by root on 15-4-15.
 */

$(function () {
    WENDA.bootstrap_validator();
    autosize($('.autosize'));

    $("#reply_form").on('ajax.success', function (e, data) {
        var self = $(this);
        location.reload();
    }).on('ajax.error', function (e, data) {
    });


//    open-comment
    var add_comment = function(ul, obj){
        ul.append(_.template($("#comment-template").html())(obj));
    };
    $(".open-comment").click(function(){
        var self = $(this);
        var c = $(self.attr("data-comment-content"));
        if(c.length){
            if(c.is(":hidden")){
                self.addClass("active");
                c.show();
                var resource_url = self.attr('data-resource');
                self.removeAttr('data-resource');
                if(resource_url){
                    c.find('form').data("comment-btn", self);
                    $('.loading', c).show();
                    $.get(resource_url, function(data){
                        $('.loading', c).hide();
                        if(!data.objects.length){
                            $('.empty', c).show();
                        }else{
                            $.each(data.objects, function(){
                                add_comment(c.find(".wd-comment-list ul"), this);
                            });
                        }

                    })
                }
            }else{
                self.removeClass("active");
                c.hide();
            }

        }
    });

    $(".wd-comment-form form").on('ajax.success', function (e, data) {
        var count = $(this).data("comment-btn").children(".count");
        count.text(parseInt(count.text())+1);
        add_comment($('.wd-comment-list ul', $(this).parents('.wd-comment')), data);
        $(this).parents(".wd-comment").find(".empty").hide();
        $(this).data('bootstrapValidator').resetForm(true);
    }).on('ajax.error', function (e, data) {

    });

});