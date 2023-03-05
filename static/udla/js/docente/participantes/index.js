$(document).ready(function () {
    $(document).on('click', '.btn_aprobar', function (e) {
        e.preventDefault();
        const url = $(this).attr('url');
        const tipo = $(this).attr('tipo');
        const id = $(this).attr('proyecto');
        const nombre = $(this).attr('nombre');
        const descripcion = $(this).attr('descripcion');
        const peticion = new Microservicio(url)
        let title = 'Cambiar estado proyecto'
        let html = getHtmlSwal(
            "El proyecto se encuentra rechazado"
            , "Seleccione una opcion para continuar"
        )
        if (tipo === '0') {
            title = 'Cambiar estado proyecto'
            html = getHtmlSwal(
                "Una vez aprobado el proyecto el alumno podra iniciar con sus actividades"
                , ` <h5 class="card-title text-start mt-5" style="font-size: 14px !important;"><strong>PROYECTO</strong>: ${nombre}</h5>
                        <p class="card-text text-justify" style="font-size: 14px !important;">
                        <strong>RESEÑA</strong>: ${descripcion}
                    </p>`
            )
        }
        Swal.fire({
            title: title,
            html: html,
            icon: 'warning',
            input: 'textarea',
            inputAttributes: {
                label:'Ingrese motivo del rechazo',
                id:'motivo_rechazo_proyecto'
            },
            width: '1200px',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aprobar</span>',
            showDenyButton: true,
            denyButtonText: '<span class="pull-left"></span><span class="bold">Rechazar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
            preDeny: (motivo) => {
                return new Promise(function (resolve, reject) {
                    const motivo_rechazo_proyecto = $('textarea.swal2-textarea').val();
                    if (motivo_rechazo_proyecto != undefined && motivo_rechazo_proyecto !=null && motivo_rechazo_proyecto!= '') {
                        resolve()
                    }
                    else{
                        $('.swal2-actions button').prop("disabled", false);
                        $('.swal2-checkbox').attr('style','display: block;').html(` <label for="swal2-checkbox" class="swal2-checkbox text-danger" style="display: block;">Ingrese motivo del rechazo (obligatorio)</label>`);
                    }
                    setTimeout(function () {
                        setTimeout(function () {
                            $('.swal2-checkbox').attr('style', 'display: none;');
                        }, 1000)
                    }, 1500)
                })
            },
        }).then((result) => {
            if (result.isDismissed != true) {
                peticion.put({
                    id:id,
                    motivo_rechazo:$('textarea.swal2-textarea').val(),
                    ind_aprobado: result.isConfirmed || !result.isDenied
                })
            }
        })
    });

    $(document).on('change', '#year', function (e) {
        $('[type="submit"]').click();
    });
});