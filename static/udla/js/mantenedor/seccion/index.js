$(document).ready(function () {
    $(document).on('click', '#btn_crear_seccion', function (e) {
        e.preventDefault();
        $('#mdl_modulo .modal-lg').removeClass("modal-lg").addClass("modal-sm");
        $('#mdl_modulo').modal('show');
        $('#mdl_modulo #contenido').html('<br><div class="text-center"><img class="js-loader"></div>');
        $('#mdl_modulo #contenido').load("/mantenedor/seccion/crear/", function () {
            $('#mdl_modulo .modal-footer .btn_accion').text('Guardar').attr('id', 'btn_guardar').css("display","block")
            $('#mdl_modulo .modal-footer button[data-bs-dismiss=modal]').text('cancelar');
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
                                'El seccion fue creada con exito!',
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


    $(document).on('click', '.btn_eliminar_seccion', function (e) {
        e.preventDefault();
        let seccion = $(this).attr('seccion');
        Swal.fire({
            title: '¿Está seguro de eliminar esta seccion?',
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bolond">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: seccion,
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


    $(document).on('click', '.btn_actualizar_seccion', function (e) {
        e.preventDefault();
        $('#mdl_modulo .modal-lg').removeClass("modal-lg").addClass("modal-sm");
        let seccion_id = $(this).attr('seccion');
        $('#mdl_modulo').modal('show');
        $('#mdl_modulo #contenido').html('<br><div class="text-center"><img class="js-loader"></div>');
        $('#mdl_modulo #contenido').load(`/mantenedor/seccion/${seccion_id}/actualizar/`, function () {
            $('#mdl_modulo .modal-footer .btn_accion').text('Modificar').attr('id', 'btn_actualizar').css("display","block")
            $('#mdl_modulo .modal-footer button[data-bs-dismiss=modal]').text('cancelar');
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
                                'El seccion fue modificada con exito!',
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
    $(document).on('click', '.btn_administrar_seccion', function (e) {
        e.preventDefault();
        $('#mdl_modulo .modal-sm').removeClass("modal-sm").addClass("modal-lg");
        let seccion_id = $(this).attr('seccion');
        $('#mdl_modulo').modal('show');
        $('#mdl_modulo #contenido').html('<br><div class="text-center"><img class="js-loader"></div>');
        $('#mdl_modulo #contenido').load(`/mantenedor/seccion/${seccion_id}/administrar/`, function () {
            $('#mdl_modulo .modal-footer .btn_accion').css("display","none");
            $('#mdl_modulo .modal-footer button[data-bs-dismiss=modal]').text('cerrar');
            recargar_tabla('profesor',seccion_id)
            recargar_tabla('alumno',seccion_id)
            $("#cmb_profesor").select2({
                dropdownParent: $('#div_cmb_profesor'),
                placeholder: 'Ingrese rut del profesor',
                minimumInputLength: 2,
                allowClear: true,
                ajax: {
                    type: 'POST',
                    url: "/mantenedor/usuario/buscar/",
                    dataType: 'json',
                    delay: 250,
                    data: function (params) {
                        return {
                            rut: params.term,
                            parametro: 'rut',
                            perfil: 'profesor',
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                        };
                    },
                    processResults: function (data) {
                        return {
                            results: data.items,
                        };
                    },
                }
            }).on('select2:select', function (e) {
                var data = e.params.data;
                $.ajax({
                    url: `/mantenedor/seccion/${seccion_id}/asignar/profesor/${data.id}/`,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
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
                        recargar_tabla('profesor',seccion_id)
                    },
                    error: function () {
                        swal.close();
                    },
                });
            });
            $("#cmb_alumno").select2({
                dropdownParent: $('#div_cmb_alumno'),
                placeholder: 'Ingrese rut del alumno',
                minimumInputLength: 2,
                allowClear: true,
                ajax: {
                    type: 'POST',
                    url: "/mantenedor/usuario/buscar/",
                    dataType: 'json',
                    delay: 250,
                    data: function (params) {
                        return {
                            rut: params.term,
                            parametro: 'rut',
                            perfil: 'alumno',
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                        };
                    },
                    processResults: function (data) {
                        return {
                            results: data.items,
                        };
                    },
                }
            }).on('select2:select', function (e) {
                var data = e.params.data;
                $.ajax({
                    url: `/mantenedor/seccion/${seccion_id}/asignar/alumno/${data.id}/`,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
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
                        estado = 'success'
                        if (response['estado'] === '1') {
                            estado = 'error'
                        }
                        else if (response['estado'] === '2') {
                            estado = 'warning'
                        }
                        Swal.fire(
                            response['respuesta'],'',
                            estado
                        )
                        recargar_tabla('alumno',seccion_id)
                    },
                    error: function () {
                        swal.close();
                    },
                });
            });
        });
    });

    $(document).on('click', '.btn_eliminar_usuario_seccion', function (e) {
        e.preventDefault();
        let seccion = $(this).attr('seccion');
        Swal.fire({
            title: '¿Está seguro de quitar a esta persona de la seccion?',
            icon: 'warning',
            confirmButtonColor: '#EB6923',
            confirmButtonText: '<span class="pull-left"></span><span class="bold">Aceptar</span>',
            cancelButtonText: '<span class="pull-left"></span><span class="bold">Cancelar</span>',
            allowOutsideClick: false,
            showCancelButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: seccion,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
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
                        recargar_tabla(response['perfil'],response['seccion'])
                    },
                    error: function () {
                        swal.close();
                    },
                });
            }
        });
    });

    $(document).on('change', '#year', function (e) {
        $('[type="submit"]').click();
    });

});

function recargar_tabla(perfil,seccion_id) {
    $('#tbl_administrar_'+perfil).DataTable({
        "bFilter": true,
        "bLengthChange": false,
        "destroy": true,
        "searching": false,
        "bInfo": false,
        "responsive": false,
        "autoWidth": false,
        "oLanguage": {
            "sLengthMenu": "_MENU_ ",
            "sInfo": "<b>_START_ a _END_</b> de _TOTAL_ Registros"
        },
        "ajax": {
            url: `/mantenedor/seccion/${seccion_id}/listar/${perfil}/`,
            type: 'POST',
            data: {
                'perfil': perfil,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            },
        },
        "columns": [
            { "data": "rut" },
            { "data": "nombre_completo" },
            { "data": "btn_eliminar_usuario_seccion" },
        ],
        "columnDefs": [
            { className: "text-left", "targets": [0] },
            { className: "text-left", "targets": [1] },
            { className: "text-center", "targets": [2] },
        ],
    });
}