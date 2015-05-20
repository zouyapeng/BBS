/**
 * Created by root on 15-4-8.
 */



// jQuery扩展
(function ($)
{
    $.fn.serializeObject = function() {
        var o = {};
        $.each($(this).serializeArray(), function(){
            if(o[this.name]){
                if(!$.isArray(o[this.name])){
                    o[this.name] = [o[this.name]]
                }
                o[this.name].push(this.value)
            }else{
                o[this.name] = this.value;
            }

        })
        return o;
    };
    $.fn.extend(
        {
            insertAtCaret: function (textFeildValue)
            {
                var textObj = $(this).get(0);
                if (document.all && textObj.createTextRange && textObj.caretPos)
                {
                    var caretPos = textObj.caretPos;
                    caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == '' ?
                        textFeildValue + '' : textFeildValue;
                }
                else if (textObj.setSelectionRange)
                {
                    var rangeStart = textObj.selectionStart,
                        rangeEnd = textObj.selectionEnd,
                        tempStr1 = textObj.value.substring(0, rangeStart),
                        tempStr2 = textObj.value.substring(rangeEnd);
                    textObj.value = tempStr1 + textFeildValue + tempStr2;
                    textObj.focus();
                    var len = textFeildValue.length;
                    textObj.setSelectionRange(rangeStart + len, rangeStart + len);
                    textObj.blur();
                }
                else
                {
                    textObj.value += textFeildValue;
                }
            },

            highText: function (searchWords, htmlTag, tagClass)
            {
                return this.each(function ()
                {
                    $(this).html(function high(replaced, search, htmlTag, tagClass)
                    {
                        var pattarn = search.replace(/\b(\w+)\b/g, "($1)").replace(/\s+/g, "|");

                        return replaced.replace(new RegExp(pattarn, "ig"), function (keyword)
                        {
                            return $("<" + htmlTag + " class=" + tagClass + ">" + keyword + "</" + htmlTag + ">").outerHTML();
                        });
                    }($(this).text(), searchWords, htmlTag, tagClass));
                });
            },

            outerHTML: function (s)
            {
                return (s) ? this.before(s).remove() : jQuery("<p>").append(this.eq(0).clone()).html();
            }
        });

    $.extend(
        {
            // 滚动到指定位置
            scrollTo : function (type, duration, options)
            {
                if (typeof type == 'object')
                {
                    if(!$(type).length)return;
                    var type = $(type).offset().top
                }
                $('html, body').animate({
                    scrollTop: type
                }, {
                    duration: duration
                });
            }
        })

})(jQuery);


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});
var WENDA = function(){
    var init = function(){
        if(location.hash)$.scrollTo($(location.hash), 1000);

        $("#search").submit(function(){
            var q = $(this).find('input[name=q]').val();
            if(!$.trim(q).length){
                return false;
            }
        })

        $("#notifications_li").hover(function(){
            $(this).children('div.dropdown').show();
        }, function(){
            $(this).children('div.dropdown').hide();
        })

        $('[data-toggle="tooltip"]').tooltip();
        $("#header .dropdown-li").hover(function(){
            $(this).addClass('active');
        }, function(){
            $(this).removeClass('active');
        });
    };
    var btn_click = function(){

    $(".favorite_tag[data-content_object]").click(function(){
        var content_object = $(this).attr('data-content_object');
        var self = $(this);
        $.ajax({
            type: 'POST',
            dataType:'json',
            contentType:'application/json;charset=UTF-8',
            url: '/api/account/favorite/',
            data: $.toJSON({content_object:content_object}),
            success: function(data, v2, v3){
                if(v3.status==204){
                    self.removeClass("exists");
                    self.children('span').text("收藏");

                }else{
                    self.children('span').text("取消收藏");
                    self.addClass("exists");
                }
            },
            error:function(data){
            }
        });
    });
    $(".focus_tag[data-content_object]").click(function(){
        var content_object = $(this).attr('data-content_object');
        var self = $(this);
        $.ajax({
            type: 'POST',
            dataType:'json',
            contentType:'application/json;charset=UTF-8',
            url: '/api/account/focus/',
            data: $.toJSON({content_object:content_object}),
            success: function(data, v2, v3){
                var count = parseInt(self.children('.count').text());
                if(v3.status==204){
                    //delete
                    self.children('.count').text(count-1);
                    self.children('span').text("关注");
                    self.removeClass("exists");
                }else{
                    self.children('.count').text(count+1);
                    self.children('span').text("取消关注");
                    self.addClass("exists");

                }
            },
            error:function(data){
            }
        });
    });
    $(".thank_tag[data-content_object]").click(function(){
        var content_object = $(this).attr('data-content_object');
        var self = $(this);
        $.ajax({
            type: 'POST',
            dataType:'json',
            contentType:'application/json;charset=UTF-8',
            url: '/api/account/thank/',
            data: $.toJSON({content_object:content_object}),
            success: function(data, v2, v3){
                if(v3.status==204){
                    self.removeClass("exists");
                    self.children('span').text("感谢");

                }else{
                    self.children('span').text("取消感谢");
                    self.addClass("exists");
                }
            },
            error:function(data){
            }
        });
    });
    $(".accuracy_tag[data-content_object]").click(function(){
        var content_object = $(this).attr('data-content_object');
        var self = $(this);
        $.ajax({
            type: 'POST',
            dataType:'json',
            contentType:'application/json;charset=UTF-8',
            url: '/api/account/accuracy/',
            data: $.toJSON({content_object:content_object}),
            success: function(data, v2, v3){
                if(v3.status==204){
                    self.removeClass("exists");
                    self.children('span').text("不是答案");

                }else{
                    self.children('span').text("取消不是答案");
                    self.addClass("exists");
                }
            },
            error:function(data){
            }
        });
    });
    $(".vote_tag[data-content_object]").click(function(){
        var content_object = $(this).attr('data-content_object');
        var self = $(this);
        var count = parseInt(self.children('span').text());
        var val = self.attr("data-value")==1?true:false;
        $.ajax({
            type: 'POST',
            dataType:'json',
            contentType:'application/json;charset=UTF-8',
            url: '/api/account/vote/',
            data: $.toJSON({content_object:content_object, agree: val}),
            success: function(data, v2, v3){
                if(data){
                    var sib = self.siblings(".vote_tag.active");
                    if(sib.length){
                        sib.removeClass("active");
                        var sib_count = parseInt(sib.children('span').text());
                        sib.children('span').text(sib_count-1);
                    }
                    console.log(count)
                    self.addClass("active");
                    self.children('span').text(count+1);
                }else{
                    self.removeClass("active");
                    self.children('span').text(count-1);
                }
            },
            error:function(data){
            }
        });
    });
    };
    var bootstrap_validator = function(){
        $("form[data-validator]").bootstrapValidator().on('success.form.bv', function (e) {
            e.preventDefault();
            var self = $(this);
            $.ajax({
                type: self.attr("method"),
                dataType:'json',
                contentType:'application/json;charset=UTF-8',
                url: self.attr("action"),
                data: $.toJSON(self.serializeObject()),
                success: function(data,v2, v3){
                    self.trigger('ajax.success', [data,v2, v3])
                },
                error:function(data){
                    self.data('bootstrapValidator').disableSubmitButtons(false);
                    self.trigger('ajax.error', data)
                }
            });

        });
        $.fn.bootstrapValidator.add_error = function(form, field, msg){
            var bv = form.data('bootstrapValidator');
            var $f = bv._cacheFields[field];
            var $message = bv._getMessageContainer($f, bv.options.group);
            var small = $f.data('bv.messages').find('.help-block[data-bv-validator="'+field+'_error"][data-bv-for="' + field + '"]');
            if(!small.length)
            $('<small/>', {"class": 'help-block', "data-bv-validator": field+'_error',
                   'data-bv-for':field
            }).css("display", 'none').appendTo($message);
            bv.updateMessage($f, field+"_error", msg);
            bv.updateStatus($f, 'INVALID', field+'_error')
        }
    };

    return {
        ajax_error:function(data){
            var msg = '服务器错误';
            if(data.responseJSON){
                if(data.responseJSON.error){
                    msg = data.responseJSON.error;
                }
            }
            WENDA.alert(msg, 'danger');
        },
        init:init,
        alert: function(content, type){
            $('#msgModal').find('.modal-body .alert').attr('class', 'alert alert-'+(type||'info')).html(content);
            $('#msgModal').modal('show');
        },
        notifications: function(){
            $("[data-notification]").click(function(){
                var self = $(this);
                $.ajax({
                    type: "PUT",
                    dataType:'json',
                    contentType:'application/json;charset=UTF-8',
                    url: self.attr('data-notification'),
                    data: $.toJSON({unread: false}),
                    success: function(data){
                        self.parents(".notification").removeClass("unread");
                        self.remove();
                    }
                })

                return false;
            })
        },
        btn_click:btn_click,
        bootstrap_validator:bootstrap_validator,
        uploda_setting:{
        url: "/api/attachment/attachment/",
            maxFileSize: 10000000,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png|zip|doc|docx|rar|pdf|psd|gz)$/i,
            dataType: 'json',
            messages: {
                acceptFileTypes: '文件类型无效',
                maxFileSize: '文件太大'
            }
    }
    }
}();


$(function () {
    WENDA.init();
    WENDA.notifications();
    WENDA.btn_click();

})