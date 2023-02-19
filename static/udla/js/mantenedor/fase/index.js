$(document).ready(function () {
    $(document).on('click', '#btn_crear_fase', function (e) {
        e.preventDefault();
        $('#mdl_modulo').modal('show');
        $('#mdl_modulo #contenido').html('<br><div class="text-center"><img class="js-loader"></div>');
        $('#mdl_modulo #contenido').load("/mantenedor/fase/crear/", function () {
            $('#mdl_modulo .modal-footer .btn_accion').text('Guardar').attr('id', 'btn_guardar');
        });
    });
    $(document).on('click', '#btn_guardar', function (e) {
        e.preventDefault();
        Swal.fire({
            title: '¿Está seguro de crear esta fase?',
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                let formData = new FormData($('#form_crear_fase').get(0));
                $.ajax({
                    type: 'POST',
                    url: "/mantenedor/fase/crear/",
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
                                'El fase fue creada con exito!',
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


    $(document).on('click', '.btn_eliminar_fase', function (e) {
        e.preventDefault();
        let fase = $(this).attr('fase');
        Swal.fire({
            title: '¿Está seguro de eliminar esta fase?',
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: fase,
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


    $(document).on('click', '.btn_actualizar_fase', function (e) {
        e.preventDefault();
        let fase_id = $(this).attr('fase');
        $('#mdl_modulo').modal('show');
        $('#mdl_modulo #contenido').html('<br><div class="text-center"><img class="js-loader"></div>');
        $('#mdl_modulo #contenido').load(`/mantenedor/fase/${fase_id}/actualizar/`, function () {
            $('#mdl_modulo .modal-footer .btn_accion').text('Modificar').attr('id', 'btn_actualizar');
        });
    });

    $(document).on('click', '#btn_actualizar', function (e) {
        e.preventDefault();
        Swal.fire({
            title: '¿Está seguro de modificar esta fase?',
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                let url = $('#form_modificar_fase').attr('action');
                let formData = new FormData($('#form_modificar_fase').get(0));
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
                                'El fase fue modificada con exito!',
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
});