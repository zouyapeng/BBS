/**
 * Created by root on 15-4-15.
 */

$(function () {
    WENDA.bootstrap_validator();
    autosize($('.autosize'));
    var converter1 = new Markdown.Converter();
    var editor1 = new Markdown.Editor(converter1, $('.mde-edit'), $('#mde-preview'));
    editor1.run();



    $("#form").on('ajax.success', function (e, data) {
        var self = $(this);
        location.href = data.absolute_url;
    }).on('ajax.error', function (e, data) {
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
    });
    var related_loading, old_title, t;
    $('#id_title').on('blur', function () {
        var val = $.trim($("#id_title").val());
        if(val.length>2&&!related_loading&&old_title!=val){
            related_loading = true;
            old_title = val;

            $.get("/api/tag/tag/related/", {q: val}, function(data){
                related_loading = false;
                $("#related_tag").html("");
                if(data.length){
                    var tags = $(_.template($("#related-tag-template").html())({tags:data}));
                    tags.find(".tag-item").click(function(){
                        tagApi.tagsManager("pushTag", $(this).text());
                        $(this).parent().remove();
                    })
                    $("#related_tag").append(tags);
                }
            })
        }
    });

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
})