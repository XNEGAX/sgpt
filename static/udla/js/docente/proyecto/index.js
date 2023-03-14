$(document).ready(function () {
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