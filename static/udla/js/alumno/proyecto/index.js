function get_tabla_archivos() {
    let tbody = ''
    $.each(archivos_list, function (key, value) {
        let icono = (value['tipo']=='pdf')?'file':'image'
        tbody += `
        <tr class="archivos_temporales tr_${key}_archivos">
            <td class="text-start">${value['orden']}${key+1}</td>
            <td class="text-start">${value['nombre']}</td>
            <td class="text-center"><i class="bx bx-${icono} text-success clickeable btn_ver_archivo" file="${value['archivo']}" tipo="${value['tipo']}" title="${value['nombre']}"></i></td>
            <td class="text-center"><i class="bx bx-trash text-danger clickeable btn_eliminar_archivos_temporal" key="${btoa(value['nombre'])}" tipo="${value['tipo']}"></i></td>
        </tr>`
    });
    $("#tabla_archivos tbody").html(tbody);
    let rowCount = $('#tabla_archivos tbody tr').length;
    if (rowCount == 0) {
        tbody = '<tr id="sin_archivos"><td colspan="8" class="text-center">No existe información disponible, por el momento.</td></tr>'
        $("#tabla_archivos tbody").html(tbody);
    }
    else {
        $('#tabla_archivos #sin_archivos').remove();

    }
}

$(document).ready(function () {

    summernote_list.forEach(function (item) {
        $('#' + item).summernote({
            height: 600,
            toolbar: [
                ['font', ['bold', 'underline', 'clear']],
                ['para', ['ul', 'ol', 'paragraph']],
            ],
            callbacks: {
                onBlur: function () {
                    const url = $('#form_responder_actividad').attr('action');
                    const cargarModal = new Microservicio(url)
                    const formData = new FormData($('#form_responder_actividad').get(0));
                    cargarModal.postFormData(formData, '#mdl_modulo',false)
                }
            }
        });
    });

    $(document).on('click', '#btn_guardar_actividad', function (e) {
        e.preventDefault();
        Swal.fire({
            html: getHtmlSwal(
                "¿Está seguro de publicar esta respuesta?"
                , ""
            ),
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                $('#publicar').val(1);
                const url = $('#form_responder_actividad').attr('action');
                const cargarModal = new Microservicio(url)
                const formData = new FormData($('#form_responder_actividad').get(0));
                cargarModal.postFormData(formData, '#mdl_modulo')
            }
        })
    });


    $(document).on('click', '#btn_agregar_tarea', function (e) {
        e.preventDefault();
        e.stopPropagation();
        const url = `/alumno/proyecto/${$('#proyecto_id').val()}/tarea/crear/`
        const cargarModal = new Microservicio(url)
        cargarModal.getOffcanvasFormGetCreateView('#mdl_modulo')
    })

    $(document).on('click', '#btn_guardar', function (e) {
        e.preventDefault();
        const url = $('#contenido form').attr('action');
        const cargarModal = new Microservicio(url)
        const formData = new FormData($('#contenido form').get(0));
        cargarModal.postFormData(formData, '#mdl_modulo')
    });

    $(document).on('click', '.btn_actualizar_tarea', function (e) {
        e.preventDefault();
        e.stopPropagation();
        const url = $(this).attr('url');
        const cargarModal = new Microservicio(url)
        cargarModal.getOffcanvasFormGetCreateView('#mdl_modulo')
    })

    $(document).on('click', '.btn_eliminar_tarea', function (e) {
        e.preventDefault();
        const url = $(this).attr('url');
        const cargarModal = new Microservicio(url)
        cargarModal.delete()
    });

    if ($('#tabla_archivos').length) {
        get_tabla_archivos()
    }

    $(document).on('click', '#btn_agregar_archivos', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $('#mdl_modulo').offcanvas("toggle");
        $('#mdl_modulo #contenido-archivos').show();
        $('#mdl_modulo .modal-footer .btn_accion').text('Subir').attr('id', 'btn_subir_archivos');
        $('#mdl_modulo .modal-body form').attr('id', 'form_subir_archivo');
    })

    $(document).on('click', '#btn_subir_archivos', function (e) {
        e.preventDefault();
        e.stopPropagation();
        if (validateForm('form_subir_archivo')) {
            const url = location.protocol + '//' + location.host + location.pathname
            const cargarModal = new Microservicio(url)
            const formData = new FormData($('#form_subir_archivo').get(0));
            formData.append('publicar', 1);
            cargarModal.postFormData(formData, '#mdl_modulo');
        }
    })

    $(document).on('click', '.btn_ver_archivo', function (e) {
        let html = ''
        if ($(this).attr('tipo')=='jpeg') {
            html = `<img src="data:image/png;base64, ${$(this).attr('file')}" style="max-width:1600px !important"/>`
        }
        else{
            html = `<iframe
            src="data:application/pdf;base64,${$(this).attr('file')}" width=100% height=600></iframe>`
        }
        Swal.fire({
            title: $(this).attr('title'),
            html: html,
            width: 1600,
            heightAuto: true,
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cerrar</span>',
        })
        $('.swal2-container.swal2-backdrop-show').css('background', 'rgba(255,255,255,.8)');
    })

    $(document).on('click', '.btn_eliminar_archivos_temporal', function (e) {
        const url = `/alumno/proyecto/${$('#proyecto_id').val()}/actividad/${$("input[name=actividad_id]").val()}/archivo/eliminar/`
        const archivo = $(this).attr('key');
        const servicio = new Microservicio(url)
        Swal.fire({
            html: getHtmlSwal(
                "¿Está seguro de eliminar este archivo?"
                , ""
            ),
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                servicio.post({'archivo':archivo})
            }
        })
    })

    $(document).on('click', '#btn_ver_bitacora', function (e) {
        e.preventDefault();
        e.stopPropagation();
        const url = `/alumno/proyecto/${$('#proyecto_id').val()}/actividad/${$("input[name=actividad_id]").val()}/bitacora/listar/`
        const cargarModal = new Microservicio(url)
        cargarModal.getOffcanvasFormGetCreateView('#bitacora_canvas','form_nuevo_comentario')
        $('#bitacora_canvas .offcanvas-body #contenido form').attr('id', 'form_responder_comentario');
    })

    $(document).on('click', '.btn_enviar_comentario', function (e) {
        e.preventDefault();
        e.stopPropagation();
        if (validateForm('form_nuevo_comentario')) {
            const url = $('#form_nuevo_comentario').attr('action')
            const cargarModal = new Microservicio(url)
            const formData = new FormData($('#form_nuevo_comentario').get(0));
            cargarModal.postFormData(formData, '#bitacora_canvas');
        }
    })
    $(document).on('click', '.btn_responder_comentario', function (e) {
        e.preventDefault();
        e.stopPropagation();
        let form = $(this).parents('form:first')
        if (validateForm('form_responder_comentario')) {
            const url = `/alumno/proyecto/${$('#proyecto_id').val()}/actividad/${$("input[name=actividad_id]").val()}/bitacora/listar/?bitacora_padre_id=${$(this).attr('value')}`;
            const cargarModal = new Microservicio(url)
            const formData = new FormData(form.get(0));
            cargarModal.postFormData(formData, '#bitacora_canvas');
        }
    })
    
    
});