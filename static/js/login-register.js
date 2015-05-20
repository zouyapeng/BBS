/**
 * Created by root on 15-4-17.
 */
$(function(){
    WENDA.bootstrap_validator();

    $("#login_form").on('ajax.success', function (e, data) {
        var self = $(this);
        if(data.status){
            location.href = data.url||'/';
        }else{
            var bv = self.data('bootstrapValidator');
            $.each(data.fields, function(){
                $.fn.bootstrapValidator.add_error(self, this.name, this.msg);

            });
            bv.disableSubmitButtons(false);
        }
    }).on('ajax.error', function (e, data) {
    });
})