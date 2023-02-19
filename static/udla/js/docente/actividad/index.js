$(document).ready(function () {
    $(document).on('click', '#btn_crear_actividad', function (e) {
        e.preventDefault();
        url = `/docente/seccion/${$('#seccion').val()}/actividad/crear/`;
        $('#mdl_modulo').modal('show');
        $('#mdl_modulo #contenido').html('<br><div class="text-center"><img class="js-loader"></div>');
        $('#mdl_modulo #contenido').load(url, function () {
            $('#mdl_modulo .modal-footer .btn_accion').text('Guardar').attr('id', 'btn_guardar');
            $('#mdl_modulo #contenido form').attr('action', url);
        });
    });
    $(document).on('click', '#btn_guardar', function (e) {
        e.preventDefault();
        url = $('#form_crear_actividad').attr('action');
        Swal.fire({
            title: '¿Está seguro de crear esta actividad?',
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                let formData = new FormData($('#form_crear_actividad').get(0));
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: formData,
                    cache: false,
                    processData: false,
                    contentType: false,
                    beforeSend: function () {
                        Swal.fire({
                            imageUrl: '<br><div class="text-center"><img class="js-loader"></div>',
                            showCancelButton: false,
                            showConfirmButton: false,
                            allowOutsideClick: false,
                        });
                        $('.swal2-container.swal2-backdrop-show').css('background', 'rgba(255,255,255,.8)');
                        $('.swal2-popup').css('background', 'transparent');
                    },
                    success: function (response) {
                        if (response['estado'] == 0) {
                            $('#mdl_modulo').modal('hide');
                            Swal.fire(
                                'Creado!',
                                'El actividad fue creada con exito!',
                                'success'
                            )
                            setTimeout(function(){
                                location.reload();
                            }, 2000);
                            
                        }
                        else {
                            Swal.fire(
                                'Alerta!',
                                response['error'],
                                'warning'
                            )
                        }
                    },
                    error: function () {
                        swal.close();
                    },
                });
            }
        })
    });
    $(document).on('click', '.column_order', function (e) {
        e.preventDefault();
        let campo = $(this).text().trim().replace(" ", "_")
        $("input[name='orden']").val(campo);
        document.getElementById("form_filtro_orden").submit();
    });
    $(document).on('click', '.btn_eliminar_actividad', function (e) {
        e.preventDefault();
        let actividad = $(this).attr('actividad');
        Swal.fire({
            title: '¿Está seguro de eliminar esta actividad?',
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: actividad,
                    type: 'DELETE',
                    headers:{"X-CSRFToken": $('input[name=csrfmiddlewaretoken]').val()},
                    beforeSend: function () {
                        Swal.fire({
                            imageUrl: '<br><div class="text-center"><img class="js-loader"></div>',
                            showCancelButton: false,
                            showConfirmButton: false,
                            allowOutsideClick: false,
                        });
                        $('.swal2-container.swal2-backdrop-show').css('background', 'rgba(255,255,255,.8)');
                        $('.swal2-popup').css('background', 'transparent');
                    },
                    success: function (response) {
                        Swal.fire(
                            response['respuesta'],'',
                            'success'
                        )
                        setTimeout(function(){
                            location.reload();
                        }, 2000);
                    },
                    error: function () {
                        swal.close();
                    },
                });
            }
        });
    });
    $(document).on('click', '.btn_actualizar_actividad', function (e) {
        e.preventDefault();
        let url = $(this).attr('actividad');
        $('#mdl_modulo').modal('show');
        $('#mdl_modulo #contenido').html('<br><div class="text-center"><img class="js-loader"></div>');
        $('#mdl_modulo #contenido').load(url, function () {
            $('#mdl_modulo .modal-footer .btn_accion').text('Modificar').attr('id', 'btn_actualizar');
            $('#mdl_modulo #contenido form').attr('action', url);
        });
    });
    $(document).on('click', '#btn_actualizar', function (e) {
        e.preventDefault();
        Swal.fire({
            title: '¿Está seguro de modificar esta actividad?',
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                let url = $('#form_modificar_actividad').attr('action');
                let formData = new FormData($('#form_modificar_actividad').get(0));
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: formData,
                    cache: false,
                    processData: false,
                    contentType: false,
                    beforeSend: function () {
                        Swal.fire({
                            imageUrl: '<br><div class="text-center"><img class="js-loader"></div>',
                            showCancelButton: false,
                            showConfirmButton: false,
                            allowOutsideClick: false,
                        });
                        $('.swal2-container.swal2-backdrop-show').css('background', 'rgba(255,255,255,.8)');
                        $('.swal2-popup').css('background', 'transparent');
                    },
                    success: function (response) {
                        if (response['estado'] == 0) {
                            $('#mdl_modulo').modal('hide');
                            Swal.fire(
                                'Modificado!',
                                'El actividad fue modificada con exito!',
                                'success'
                            )
                            setTimeout(function(){
                                location.reload();
                            }, 2000);
                        }
                        else {
                            Swal.fire(
                                'Alerta!',
                                response['error'],
                                'warning'
                            )
                        }
                    },
                    error: function () {
                        swal.close();
                    },
                });
            }
        })
    });
    $(document).on('change', '#mdl_modulo form', function (e) {
        let button = $('#mdl_modulo .modal-footer .btn_accion').html()
        let action = $(this).attr('action')
        let params = $(this).serialize()
        let fullpath = decodeURI(action+'?'+params)
        $('#mdl_modulo #contenido').load(fullpath, function () {
            $('#mdl_modulo .modal-footer .btn_accion').html(button)
            $('#mdl_modulo #contenido form').attr('action', action);
        });
    });
});