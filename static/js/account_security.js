/**
 * Created by root on 15-4-16.
 */

$(function () {
    $("#password_form").on('ajax.success', function (e, data) {
//        location.reload();
        var self = $(this);
        if(data.status){
            $("#alert").addClass('alert-success show').removeClass('alert-danger').text('修改成功').show();
            self.data('bootstrapValidator').resetForm(true);
        }else{
            $("#alert").removeClass('alert-success').addClass('alert-danger show').text(data.msg||'修改失败').show();
            self.data('bootstrapValidator').disableSubmitButtons(false);

        }
    }).on('ajax.error', function (e, data) {
        $("#alert").removeClass('alert-success').addClass('alert-danger show').text("服务器错误").show();
    });
})