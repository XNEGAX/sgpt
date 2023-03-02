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

    $(document).on('click', '.btn_configuracion_base', function (e) {
        e.preventDefault();
        e.stopPropagation();
        const seccion = $(this).attr('seccion');
        Swal.fire({
            title: "Configuración de actividades",
            html: getHtmlSwal(
                "¿Desea aplicar la configuración incluida en el sistema?"
                , "Seleccione una opción para continuar "
            ),
            icon: 'info',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Si</span>',
            showDenyButton: true,
            denyButtonText: '<span class="pull-left"></span><span class="bold">No</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            console.log(result)
            $('#selected').val(seccion);
            if (result.isConfirmed) {
                $('#configuration').val(1);
                $('[type="submit"]').click();
            }
            else if (result.isDenied) {
                $('#configuration').val(0);
                $('[type="submit"]').click();
            }
        })
    });
});