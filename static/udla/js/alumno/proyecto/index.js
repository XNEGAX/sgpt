$(document).ready(function () {
    summernote_list.forEach(function (item) {
        $('#' + item).summernote({
            height: 600,
            toolbar: [
                ['font', ['bold', 'underline', 'clear']],
                ['para', ['ul', 'ol', 'paragraph']],
            ]
        });
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
        cargarModal.postFormData(formData,'#mdl_modulo')
        
    });
});