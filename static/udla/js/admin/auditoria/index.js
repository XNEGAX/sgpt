$(document).ready(function () {
    $(document).on('change', '#modelo', function (e) {
        $('#form_auditoria').submit();
    });
});