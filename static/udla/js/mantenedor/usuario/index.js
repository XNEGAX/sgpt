$(document).ready(function () {
    $(document).on('click', '#btn_crear_usuario', function (e) {
        e.preventDefault();
        $('#mdl_modulo').modal('show');
        $('#mdl_modulo #contenido').html('<br><div class="text-center"><img class="js-loader"></div>');
        $('#mdl_modulo #contenido').load("/mantenedor/usuario/crear/", function () {
            $('#mdl_modulo .modal-footer .btn_accion').text('Guardar').attr('id', 'btn_guardar');
        });
    });
    $(document).on('click', '#btn_guardar', function (e) {
        e.preventDefault();
        Swal.fire({
            title: '¿Está seguro de crear este usuario?',
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                let formData = new FormData($('#form_crear_usuario').get(0));
                perfiles = []
                $("#mdl_modulo .form-check").find('input[type="checkbox"]').each(function () {
                    var elemento = this;
                    if ($(elemento).is(':checked')) {
                        perfiles.push(elemento.value)
                    }
                });
                formData.delete('perfiles[]');
                formData.append('perfiles[]', perfiles);
                $.ajax({
                    type: 'POST',
                    url: "/mantenedor/usuario/crear/",
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
                                'El usuario fue creado con exito!',
                                'success'
                            )
                            setTimeout(function(){
                                window.location.href = location.protocol + '//' + location.host + location.pathname;;
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

    $(".btn_habilitar_usuario").change(function () {
        let usuario_id = $(this).val();
        let estado = $(this).is(':checked')? 1:0
        $.ajax({
            url: '/mantenedor/usuario/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'usuario_id': usuario_id,
                'estado': estado,
            },
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
                    window.location.href = location.protocol + '//' + location.host + location.pathname;;
                }, 2000);
            },
            error: function () {
                swal.close();
            },
        });
    });

    $(document).on('click', '.btn_impersonar_usuario', function (e) {
        e.preventDefault();
        Swal.fire({
            title: '¿Está seguro de impersonar a este usuario?',
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                $(this).parents('form').submit();
            }
        })
    });

    $(document).on('click', '.btn_actualizar_usuario', function (e) {
        e.preventDefault();
        let usuario_id = $(this).attr('usuario');
        $('#mdl_modulo').modal('show');
        $('#mdl_modulo #contenido').html('<br><div class="text-center"><img class="js-loader"></div>');
        $('#mdl_modulo #contenido').load(`/mantenedor/usuario/${usuario_id}/actualizar/`, function () {
            $('#mdl_modulo .modal-footer .btn_accion').text('Modificar').attr('id', 'btn_actualizar');
        });
    });

    $(document).on('click', '#btn_actualizar', function (e) {
        e.preventDefault();
        Swal.fire({
            title: '¿Está seguro de modificar este usuario?',
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                let url = $('#form_modificar_usuario').attr('action');
                let formData = new FormData($('#form_modificar_usuario').get(0));
                perfiles = []
                $("#mdl_modulo .form-check").find('input[type="checkbox"]').each(function () {
                    var elemento = this;
                    if ($(elemento).is(':checked')) {
                        perfiles.push(elemento.value)
                    }
                });
                formData.delete('perfiles[]');
                formData.append('perfiles[]', perfiles);
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
                                'El usuario fue modificado con exito!',
                                'success'
                            )
                            setTimeout(function(){
                                window.location.href = location.protocol + '//' + location.host + location.pathname;;
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