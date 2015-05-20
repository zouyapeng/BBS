/**
 * Created by root on 15-4-19.
 */
$(function(){
    if(window.Markdown&&$('.mde-edit').length){
        var converter1 = new Markdown.Converter();
        var editor1 = new Markdown.Editor(converter1, $('.mde-edit'), $('#mde-preview'));
        editor1.run();
    }
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
    $('#fileupload').fileupload({
        url: "/api/attachment/attachment/",
            maxFileSize: 10000000,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png|zip|doc|docx|rar|pdf|psd)$/i,
            dataType: 'json',
            messages: {
                acceptFileTypes: '文件类型无效',
                maxFileSize: '文件太大'
            }
    })
        .on('fileuploadadd', function (e, data) {

        data.context = $('<div/>', {class:'col-sm-4 file-item'}).appendTo('#files');
        $.each(data.files, function (index, file) {
            var node = $('<div/>', {class:"con"}).text(file.name);

            if (!index) {
                node
                    .append($('<div/>', {class:'meta'}))
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