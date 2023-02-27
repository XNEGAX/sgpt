$(document).ready(function () {
    $(document).on('click', '.btn_traer_modal', function (e) {
        e.preventDefault();
        e.stopPropagation();
        const url = $(this).attr('href');
        const accion = $(this).attr('accion');
        const cargarModal = new Microservicio(url)
        if (accion==='1') {
            Swal.fire({
                title: "Definir proyecto",
                html: getHtmlSwal(
                    "No has creado tu proyecto aun!"
                    ,"Presiona aceptar para continuar"
                ),
                icon: 'warning',
                confirmButtonColor: '#EB6923',
                confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
                cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
                allowOutsideClick: false,
                showCancelButton: true,
            }).then((result) => {
                if (result.isConfirmed) {
                    cargarModal.getModalFormGetCreateView('#mdl_modulo')
                    
                }
            })
        }
        else if (accion==='2') {
            Swal.fire({
                title: "Pendiente de aprobación",
                html: getHtmlSwal(
                    "Podras editar el proyecto las veces que sean necesarias, mientras este no se encuentre aprobado"
                    ,"Presiona editar para continuar"
                ),
                icon: 'warning',
                confirmButtonColor: '#EB6923',
                confirmButtonText: '<span class="pull-left"></span><span class="bold">Editar</span>',
                cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
                allowOutsideClick: false,
                showCancelButton: true,
            }).then((result) => {
                if (result.isConfirmed) {
                    cargarModal.getModalFormGetUpdateView('#mdl_modulo')
                }
            })
        }
        else{
            window.location.href = url
        }
        
    });
    $(document).on('click', '#btn_guardar', function (e) {
        e.preventDefault();
        const url = $('#mdl_modulo form').attr('action');
        Swal.fire({
            html: getHtmlSwal(
                "¿Está seguro de crear este proyecto?"
                ,"Una vez creado, debes esperar la aprobación de tu profesor para continuar"
            ),
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                let formData = new FormData($('#mdl_modulo form').get(0));
                const cargarModal = new Microservicio(url)
                cargarModal.postFormData(formData, '#mdl_modulo')
            }
        })
    });
    $(document).on('click', '#btn_actualizar', function (e) {
        e.preventDefault();
        const url = $('#mdl_modulo form').attr('action');
        Swal.fire({
            html: getHtmlSwal(
                "¿Está seguro de actualizar este proyecto?"
                ,""
            ),
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                let formData = new FormData($('#mdl_modulo form').get(0));
                const cargarModal = new Microservicio(url)
                cargarModal.postFormData(formData, '#mdl_modulo')
            }
        })
    });
});