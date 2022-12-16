$(document).ready(function () {
    $(document).on('click', '#btn_cambio_perfil', function (e) {
        e.preventDefault();
        $('#mdl_cambio_perfil').modal('show');
        $.ajax({
            type: 'GET',
            url: '/perfil/cambio/',
            beforeSend: function (xhr, settings) {
                $('#mdl_cambio_perfil #contenido').html('<br><div class="text-center"><img class="loadding-spinner"></div>');
                $('.btn').hide();
            },
            success: function (data, status, xhr) {
                $('#mdl_cambio_perfil #contenido').html(data);
            },
        });
    });
    $(document).on('click', '.btn_seleccionar_perfil', function (e) {
        let perfil = document.createElement("input")
        perfil.setAttribute("type", "hidden")
        perfil.setAttribute("name", "perfil")
        perfil.setAttribute("value", $(this).attr('perfil'));
        document.getElementById("form_cambio_perfil").appendChild(perfil)
        let token = document.createElement("input")
        token.setAttribute("type", "hidden")
        token.setAttribute("name", "csrfmiddlewaretoken")
        token.setAttribute("value", $('input[name=csrfmiddlewaretoken]').val());
        document.getElementById("form_cambio_perfil").appendChild(token)
        document.getElementById("form_cambio_perfil").submit();
    });
    $('.modal').modal({
        backdrop: 'static',
        keyboard: false
    })
});