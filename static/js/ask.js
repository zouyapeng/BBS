/**
 * Created by root on 15-4-10.
 */

$(function () {
    autosize($('.autosize'));
    var converter1 = new Markdown.Converter();
    var editor1 = new Markdown.Editor(converter1, $('.mde-edit'), $('#mde-preview'));
    editor1.run();



    var tags = $("#id_tags").val();
    $("#id_tags").val('');

    var tagApi = $("#id_tags").tagsManager({
        prefilled:function(){
            return  $.grep(tags.split(','), function(item){
                return item.length
            })
        },
        maxTags:5,
        hiddenTagListName:'tags'
    });

    $("#id_tags").typeahead(null, {
      name: 'countries',
      displayKey: 'title',
      source: function(query, render){
          $.get('/api/tag/tag/?title__icontains='+query).success(function(data){
              render(data.objects)
          })

      }
    }).on('typeahead:selected', function (e, d) {
        tagApi.tagsManager("pushTag", d.title);
        $(this).typeahead('val', '');
    });

    var method = $('#form').attr("method");
    if(method=='POST'){



//    表单
    var t, old_title;
    var related_loading = false;
    $("#id_title").keyup(function(){
        clearTimeout(t);
        var val = $.trim($("#id_title").val());
        if(val.length>2&&!related_loading&&old_title!=val)
        t = setTimeout(function(){
            related_loading = true;
            old_title = val;
            $.get("/api/question/question/related/", {q: val, limit:2}, function(data){
                related_loading = false;
                if(data.objects&&data.objects.length)
                    $(".related").removeClass("hide").find('ul').html( _.template($("#related-template").html())(data));
                else
                    $(".related").addClass("hide");

                $("#related_tag").html("");
                if(data.kw){
                    var tags = $(_.template($("#related-tag-template").html())({tags:data.kw}));
                    tags.find(".tag-item").click(function(){
                        tagApi.tagsManager("pushTag", $(this).text());
                        $(this).parent().remove();
                    })
                    $("#related_tag").append(tags);
                }
            })
        }, 500);
    }).on('blur', function () {
        related_loading = false;
        $("#id_title").keyup();
    });
    }



    var validTags = function(){
        if(method!='POST')return true;

        var vf = $('#form').data('bootstrapValidator');
        var val = $.trim($('input[name=tags]').val());
        if(val&&val.split(',').length<5){
            vf.getFieldElements("tags").data('bv.messages').find('.help-block[data-bv-validator][data-bv-for="tags"]').hide();
            vf.getFieldElements("tags").parents('.form-group').addClass('has-success').removeClass('has-error');
            return true;
        }
        vf.getFieldElements("tags").data('bv.messages').find('.help-block[data-bv-validator][data-bv-for="tags"]').show();
        vf.getFieldElements("tags").parents('.form-group').removeClass('has-success').addClass('has-error');
        return false;

    }

    $('#form').bootstrapValidator({
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            title: {
                validators: {
                    notEmpty: {
                        message: '标题不能为空'
                    },
                    stringLength: {
                        min: 2,
                        max: 50,
                        message: '您的提问标题为2~50个字，请精简或将更多内容输入到问题补充中'
                    }
                }
            },
            tags: {
                validators: {
                    notEmpty: {
                        message: '标签不能为空'
                    }
                }

            }

        }
    }).on('success.form.bv', function (e) {
        e.preventDefault();
        var self = $(this);
        if(validTags()){
            $.ajax({
                type: method,
                dataType:'json',
                contentType:'application/json;charset=UTF-8',
                url: self.attr("action"),
                data: $.toJSON(self.serializeObject()),
                success: function(data){
                    location.href = data.absolute_url;
                },
                error:function(data){
                    self.data('bootstrapValidator').disableSubmitButtons(false);
                }
            });
        }else{
            self.data('bootstrapValidator').disableSubmitButtons(false);
        }
    });


//    图片上传
    $("#files .install").click(function(){
        $('.mde-input').insertAtCaret("\n[attachment]" + $(this).attr("data-id") + "[/attachment]\n");
    });
    $("#files .del").click(function(){
        $(this).parents('.file-item').remove();
    });

    var instButton = $('<a/>')
            .prop('disabled', true)
            .text("插入")
            .attr('href', 'javascript:;')
            .on('click', function () {
                var $this = $(this),
                    data = $this.data();
                    $('.mde-input').insertAtCaret("\n[attachment]" + data.result.id + "[/attachment]\n");
            });
    var delButton = $('<a/>')
            .prop('disabled', true)
            .text("删除")
            .attr('href', 'javascript:;')
            .on('click', function () {
                var $this = $(this),
                    data = $this.data();
                data.context.remove();
            });
    var input = $('<input/>').attr({type: "hidden", name:'attachment'});
    $('#fileupload').fileupload(WENDA.uploda_setting)
        .on('fileuploadadd', function (e, data) {

        data.context = $('<div/>', {class:'col-sm-4 file-item'}).appendTo('#files');
        $.each(data.files, function (index, file) {
            var node = $('<div/>', {class:"con"}).text(file.name);

            if (!index) {
                node
                    .append($('<div/>', {class:'meta'}))
//                        .append(instButton.clone(true).data(data))
//                    .append(delButton.clone(true).data(data)));
            }
            node.appendTo(data.context);
        });
    })
.on('fileuploadprocessalways', function (e, data) {
        var index = data.index,
            file = data.files[index],
            node = $(data.context.children()[index]);
        if (file.preview) {
            node
                .prepend($("<div/>", {class:"preview loading"}).append(file.preview).append($("<i/>", {class:'fa fa-spinner'})));
        }else{
            node.prepend($("<div/>", {class:"preview loading"}).append($("<i/>", {class:'fa fa-file-o'})))
        }
        if (file.error) {
            node
                .append('<br>')
                .append($('<span class="text-danger"/>').text(file.error));
        }
    }).on('fileuploaddone', function (e, data) {
            $(data.context).find(".preview.loading").removeClass('loading');
            $(data.context).find(".meta").append(instButton.clone(true).data(data)).append(delButton.clone(true).data(data)).append(input.clone(true).attr({value:data.result.id}));
    })
})