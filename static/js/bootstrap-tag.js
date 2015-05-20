/* ==========================================================
 * bootstrap-tag.js v2.3.0
 * https://github.com/fdeschenes/bootstrap-tag
 * ==========================================================
 * Copyright 2012 Francois Deschenes.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================== */

!function ($) {

    'use strict' // jshint ;_;

    var Tag = function (element, options) {
        this.element = $(element)
        this.options = $.extend(true, {}, $.fn.tag.defaults, options)
        this.values = $.grep($.map(this.element.val().split(','), $.trim), function (value) {
            return value.length > 0
        })
        this.show()
    }

    Tag.prototype = {
        constructor: Tag, show: function () {
            var that = this

            that.element.parent().prepend(that.element.detach().hide())
            that.element
                .wrap($('<div class="tags">'))
                .parent()
                .on('click', function () {
                    that.input.focus()
                })

            if (that.values.length) {
                $.each(that.values, function () {
                    that.createBadge(this)
                })
            }

            that.loading = $("<i/>").addClass("fa fa-spinner hide").insertAfter(that.element);
            that.dropdown = $("<div/>").addClass("tag-dropdown hide").insertAfter(that.element);
            that.dropdown.append($("<p/>").addClass("title").html("没有找到相关结果"));


            that.input = $('<input maxlength="10" type="text">')
                .attr('placeholder', that.options.placeholder)
                .insertAfter(that.element)
                .on('focus', function () {
                    that.element.parent().addClass('tags-hover');
                    that.skip = true;
                })
                .on('blur', function () {
//                    if (!that.skip) {
//                        that.process()

//                        that.tags.children('.tag').removeClass('tag-important')
//                    }
                    that.t = setTimeout(function(){
                        if (!that.skip) {
                            that.element.parent().removeClass('tags-hover');
                            that.tags.children('.tag').removeClass('tag-important')
                            that.input.val("");
                            that.process();
                        }
                    }, 500)
                    that.skip = false
                    that.setTimeout(true);
                })
                .on("keyup", function(){
                    that.setTimeout();
                })
                .on('keydown', function (event) {
                    if (event.keyCode == 188 || event.keyCode == 13 || event.keyCode == 9) {
                        if ($.trim($(this).val()) && ( !that.element.siblings('.typeahead').length || that.element.siblings('.typeahead').is(':hidden') )) {
                            if (event.keyCode != 9) event.preventDefault()
                            that.process()
                        } else if (event.keyCode == 188) {
                            if (!that.options.autocompleteOnComma) {
                                event.preventDefault()
                                that.process()
                            }
                            else if (!that.element.siblings('.typeahead').length || that.element.siblings('.typeahead').is(':hidden')) {
                                event.preventDefault()
                            } else {
                                that.input.data('typeahead').select()
                                event.stopPropagation()
                                event.preventDefault()
                            }
                        }
                    } else if (!$.trim($(this).val()) && event.keyCode == 8) {
                        var count = that.tags.children('.tag').length
                        if (count) {
                            var tag = that.tags.children('.tag:eq(' + (count - 1) + ')')
                            if (tag.hasClass('tag-important')) {
                                that.remove(count - 1)
                            }
                            else {
                                tag.addClass('tag-important')
                            }
                        }
                    } else {
                        that.tags.children('.tag').removeClass('tag-important')
                    }
                });

            that.tags = $("<span/>").insertAfter(that.element);
            this.element.trigger('shown')
        }, setTimeout: function () {
            var that = this;
            clearTimeout(that.time);
            that.loading.addClass("hide");
            if(that.old_value != that.input.val()&&that.options.source){
                if(that.input.val()){
                    that.loading.removeClass("hide");
                    that.time = setTimeout(function () {
                        that.old_value = that.input.val();
                        that.getSource();
                    }, 1000);
                }

            }
        }, getSource: function(){
            var that = this;
            if(that.input.val()){
                that.options.source(that.input.val(), function(data){
                    that.dropdown.find(".tag-item").remove();
                    that.dropdown.find("p.title").addClass("hide")
                    that.loading.addClass("hide");
                    if(data, data.length){
                        that.dropdown.append($.map(data, function(item){
                            return that.createItem(item, data)
                        }));
                    }
                    var item = that.createItem(null, data);
                    if(item)
                    that.dropdown.append(that.createItem(null, data))
                    that.dropdown.removeClass("hide")

                });
            }

        }, createItem: function(item, data){
            var that = this;
            var e;
            if(item)
                e = that.options.formatItem(item);
            else
                e = that.options.createItem(that.input.val(), data);
            if(e)
            e.click(function(){
                that.input.val(e.data("tag-val"));
                that.process()
            });
            return e;

        }, inValues: function (value) {
            if (this.options.caseInsensitive) {
                var index = -1
                $.each(this.values, function (indexInArray, valueOfElement) {
                    if (valueOfElement.toLowerCase() == value.toLowerCase()) {
                        index = indexInArray
                        return false
                    }
                })
                return index
            } else {
                return $.inArray(value, this.values)
            }
        }, createBadge: function (value) {
            var that = this

            $('<span/>', {'class': "tag"})
                .append($("<i/>", {class: "fa fa-tags"}))
                .append($("<b/>").text(value.toString()))
                .append($('<button type="button" class="close">&times;</button>')
                    .on('click', function () {
                        that.remove(that.tags.children('.tag').index($(this).closest('.tag')))
                    })
            )
                .appendTo(that.tags)
        }, add: function (value) {
            var that = this

            if (!that.options.allowDuplicates) {
                var index = that.inValues(value)
                if (index != -1) {
                    var badge = that.tags.children('.tag:eq(' + index + ')')
                    badge.addClass('tag-warning')
                    setTimeout(function () {
                        $(badge).removeClass('tag-warning')
                    }, 500)
                    return
                }
            }

            this.values.push(value)
            this.createBadge(value)

            this.element.val(this.values.join(', '))
            this.element.trigger('added', [value])
        }, remove: function (index) {
            if (index >= 0) {
                var value = this.values.splice(index, 1)
                this.tags.children('.tag:eq(' + index + ')').remove()
                this.element.val(this.values.join(', '))

                this.element.trigger('removed', [value])
            }
        }, process: function () {
            var values = $.grep($.map(this.input.val().split(','), $.trim), function (value) {
                    return value.length > 0
                }),
                that = this
            $.each(values, function () {
                that.add(this)
            })
            this.input.val('');
            this.old_value = "";
            that.dropdown.addClass("hide");
        }, skip: false
    }

    var old = $.fn.tag

    $.fn.tag = function (option) {
        return this.each(function () {
            var that = $(this)
                , data = that.data('tag')
                , options = typeof option == 'object' && option
            if (!data) that.data('tag', (data = new Tag(this, options)))
            if (typeof option == 'string') data[option]()
        })
    }

    $.fn.tag.defaults = {
        allowDuplicates: false, caseInsensitive: true, autocompleteOnComma: false, placeholder: '', source: []
    }

    $.fn.tag.Constructor = Tag

    $.fn.tag.noConflict = function () {
        $.fn.tag = old
        return this
    }

}(window.jQuery)
