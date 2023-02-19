'use strict';

function SetCaretAtEnd(elem) {
    var elemLen = elem.value.length;
    if (document.selection) {
        elem.focus();
        var oSel = document.selection.createRange();
        oSel.moveStart('character', -elemLen);
        oSel.moveStart('character', elemLen);
        oSel.moveEnd('character', 0);
        oSel.select();
    }
    else if (elem.selectionStart || elem.selectionStart == '0') {
        elem.selectionStart = elemLen;
        elem.selectionEnd = elemLen;
        elem.focus();
    }
}

function openLoader() {
    Swal.fire({
        showCancelButton: false,
        showConfirmButton: false,
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading()
        },
    });
    $('.swal2-container.swal2-backdrop-show').css('background', 'rgba(255,255,255,.8)');
    $('.swal2-popup').css('background', 'transparent');
}

function closeLoader() {
    swal.close();
}

class Microservicio {
    constructor(url) {
        this.url = url;
        this.params = {};
        this.params['csrfmiddlewaretoken'] = $('input[name=csrfmiddlewaretoken]').val()
    }
    post(params) {
        $.ajax({
            url: this.url,
            type: 'POST',
            data: params,
            beforeSend: function () {
                openLoader()
            },
            success: function (response) {
                Swal.fire(
                    response['respuesta'], '',
                    'success'
                )
                setTimeout(function () {
                    location.reload();
                }, 2000);
            },
            error: function () {
                closeLoader()
            },
        });
    }
    get() {
        $.ajax({
            url: this.url,
            type: 'GET',
            beforeSend: function () {
                openLoader()
            },
            success: function (response) {
                console.log(response)
            },
            complete: function () {
                closeLoader()
            },
            error: function (error) {
                console.log(error)
                closeLoader()
            },
        });
    }
    getModalForm(modal, accion, id) {
        openLoader()
        $(modal).load(this.url, function (responseText, textStatus, req) {
            console.log(responseText, textStatus, req)
            $(modal + ' .modal-footer .btn_accion').text(accion).attr('id', id);
            closeLoader()
        });
    }
    getModalFormOnlyClose(modal) {
        try {
            openLoader()
            const cuerpo = modal + ' #contenido'
            $(cuerpo).load(this.url, function (responseText, textStatus, req) {
                $(modal + ' .modal-footer .btn_accion').css("display", "none");
                $(modal + ' .modal-footer button[data-bs-dismiss=modal]').text('cerrar');
                closeLoader()
            });
        } catch (error) {
            console.error(error);
        }

    }
    datatable(id, args) {
        $(id).DataTable({
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
                url: this.url,
                type: 'POST',
                data: params
            },
            "columns": args['columns'],
            "columnDefs": args['columnDefs'],
        });
    }
}

$(document).ready(function () {
    $(document).on('click', '#btn_cambio_perfil', function (e) {
        e.preventDefault();
        $('#mdl_cambio_perfil').modal('show');
        $.ajax({
            type: 'GET',
            url: '/perfil/cambio/',
            beforeSend: function (xhr, settings) {
                $('#mdl_cambio_perfil #contenido').html('<br><div class="text-center"><img class="js-loader"></div>');
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

    $(document).ajaxComplete(function (event, xhr, settings) {
        if (xhr.status == 403) {
            Swal.fire({
                icon: 'error',
                title: 'Error 403',
                text: 'Necesita permisos para realizar esta acción',
                position: 'top',
            }).then((result) => {
                if (result.isConfirmed) {
                    $('#mdl_modulo').modal('hide');
                }
            })

        }
    });

    $(document).ajaxError(function (event, request, settings) {
        alert("Oops!!");
    });
    $.ajaxSetup({
        timeout: 5000,
        error: function (event, request, settings) {
            alert("Oops!");
        }
    });
});