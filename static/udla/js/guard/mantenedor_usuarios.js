$(document).ready(function () {
    $(document).on('click', '#btn_crear_usuario', function (e) {
        e.preventDefault();
        $('#mdl_crud_usuario').modal('show');
        $('#mdl_crud_usuario #contenido').html('<br><div class="text-center"><img class="loadding-spinner"></div>');
        $('#mdl_crud_usuario #contenido').load("/mantenedor/usuario/crear/", function () {
        });
    });
});