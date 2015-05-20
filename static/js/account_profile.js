/**
 * Created by root on 15-4-16.
 */
$(function () {
    $("#id_birthday").daterangepicker({
        format: 'YYYY-MM-DD',
        singleDatePicker: true,
        showDropdowns: true
    });


    $("#profile_form").on('ajax.success', function (e, data) {
        location.reload();
    }).on('ajax.error', function (e, data) {
    });
})