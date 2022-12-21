$(document).ready(function () {
    $(document).on('click', '#btn_crear_seccion', function (e) {
        e.preventDefault();
        $('#mdl_crud_seccion').modal('show');
        $('#mdl_crud_seccion #contenido').html('<br><div class="text-center"><img class="loadding-spinner"></div>');
        $('#mdl_crud_seccion #contenido').load("/mantenedor/seccion/crear/", function () {
            $('#mdl_crud_seccion .modal-footer .btn_accion').text('Guardar').attr('id', 'btn_guardar');
        });
    });
    $(document).on('click', '#btn_guardar', function (e) {
        e.preventDefault();
        Swal.fire({
            title: '¿Está seguro de crear esta seccion?',
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                let formData = new FormData($('#form_crear_seccion').get(0));
                $.ajax({
                    type: 'POST',
                    url: "/mantenedor/seccion/crear/",
                    data: formData,
                    cache: false,
                    processData: false,
                    contentType: false,
                    beforeSend: function () {
                        Swal.fire({
                            imageUrl: '<br><div class="text-center"><img class="loadding-spinner"></div>',
                            showCancelButton: false,
                            showConfirmButton: false,
                            allowOutsideClick: false,
                        });
                        $('.swal2-container.swal2-backdrop-show').css('background', 'rgba(255,255,255,.8)');
                        $('.swal2-popup').css('background', 'transparent');
                    },
                    success: function (response) {
                        if (response['estado'] == 0) {
                            $('#mdl_crud_seccion').modal('hide');
                            Swal.fire(
                                'Creado!',
                                'El seccion fue creado con exito!',
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

    $(".btn_habilitar_seccion").change(function () {
        let seccion_id = $(this).val();
        let estado = $(this).is(':checked')? 1:0
        $.ajax({
            url: '/mantenedor/seccion/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'seccion_id': seccion_id,
                'estado': estado,
            },
            beforeSend: function () {
                Swal.fire({
                    imageUrl: '<br><div class="text-center"><img class="loadding-spinner"></div>',
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
            },
            error: function () {
                swal.close();
            },
        });
    });

    $(document).on('click', '.btn_impersonar_seccion', function (e) {
        e.preventDefault();
        Swal.fire({
            title: '¿Está seguro de impersonar a esta seccion?',
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

    $(document).on('click', '.btn_actualizar_seccion', function (e) {
        e.preventDefault();
        let seccion_id = $(this).attr('seccion');
        $('#mdl_crud_seccion').modal('show');
        $('#mdl_crud_seccion #contenido').html('<br><div class="text-center"><img class="loadding-spinner"></div>');
        $('#mdl_crud_seccion #contenido').load(`/mantenedor/seccion/${seccion_id}/actualizar/`, function () {
            $('#mdl_crud_seccion .modal-footer .btn_accion').text('Modificar').attr('id', 'btn_actualizar');
        });
    });

    $(document).on('click', '#btn_actualizar', function (e) {
        e.preventDefault();
        Swal.fire({
            title: '¿Está seguro de modificar esta seccion?',
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                let url = $('#form_modificar_seccion').attr('action');
                let formData = new FormData($('#form_modificar_seccion').get(0));
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: formData,
                    cache: false,
                    processData: false,
                    contentType: false,
                    beforeSend: function () {
                        Swal.fire({
                            imageUrl: '<br><div class="text-center"><img class="loadding-spinner"></div>',
                            showCancelButton: false,
                            showConfirmButton: false,
                            allowOutsideClick: false,
                        });
                        $('.swal2-container.swal2-backdrop-show').css('background', 'rgba(255,255,255,.8)');
                        $('.swal2-popup').css('background', 'transparent');
                    },
                    success: function (response) {
                        if (response['estado'] == 0) {
                            $('#mdl_crud_seccion').modal('hide');
                            Swal.fire(
                                'Modificado!',
                                'El seccion fue modificado con exito!',
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