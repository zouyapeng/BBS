/**
 * Created by root on 15-4-12.
 */
$(function(){
    WENDA.bootstrap_validator();
    if(window.autosize) autosize($('.autosize'));


    $("#invite_form").submit(function(){
        var self = $(this);
        var val = $.trim(self.find("input[name=recipient]").val());
        if(!val){
            WENDA.alert("邀请人不能为空", 'warning');
        return false;
        }
        $.ajax({
            type: self.attr("method"),
            dataType:'json',
            contentType:'application/json;charset=UTF-8',
            url: self.attr("action"),
            data: $.toJSON(self.serializeObject()),
            success: function(data){
                self.find("input[name=recipient]").val('');
                WENDA.alert("邀请成功", 'success');
            },
            error:function(data){
                WENDA.ajax_error(data);
            }
        });
        return false;
    });
     $("#id_recipient").typeahead(null, {
      name: 'countries',
      displayKey: 'username',
      source: function(query, render){
          $.get('/api/account/user/username/?q='+query).success(function(data){
              render(data)
          })
      }
    });

    $(".answer-item").hover(function(){
        $(this).addClass("active");
    }, function(){
        $(this).removeClass("active");
    })


    $("#answer_form").on('ajax.success', function (e, data) {
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


})