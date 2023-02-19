$(document).ready(function () {
    $(document).on('click', '.btn_participantes', function (e) {
        e.preventDefault();
        $('#mdl_modulo').modal('show');
        const url = $(this).attr('url');
        const cargarModal = new Microservicio(url)
        cargarModal.getModalFormOnlyClose('#mdl_modulo')
    });

    $(document).on('change', '#year', function (e) {
        $('[type="submit"]').click();
    });
});