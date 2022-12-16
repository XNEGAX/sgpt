$(document).ready(function () {
    $(document).on('click', '#btn_crear_usuario', function (e) {
        e.preventDefault();
        $('#mdl_crud_usuario').modal('show');
        $('#mdl_crud_usuario #contenido').html('<br><div class="text-center"><img class="loadding-spinner"></div>');
        $('#mdl_crud_usuario #contenido').load("/mantenedor/usuario/crear/", function () {
            $('#mdl_crud_usuario .modal-footer .btn_accion').text('Guardar').attr('id', 'btn_guardar');
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
                $(".form-check").find('input[type="checkbox"]').each(function () {
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
                            imageUrl: '<br><div class="text-center"><img class="loadding-spinner"></div>',
                            showCancelButton: false,
                            showConfirmButton: false,
                            allowOutsideClick: false,
                        });
                        $('.swal2-container.swal2-backdrop-show').css('background', 'rgba(255,255,255,.8)');
                        $('.swal2-popup').css('background', 'transparent');
                    },
                    success: function (response) {
                        console.log(response)
                        if (response['estado'] == 0) {
                            $('#mdl_crud_usuario').modal('hide');
                            Swal.fire(
                                'Creado!',
                                'El usuario fue creado con exito!',
                                'success'
                            )
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