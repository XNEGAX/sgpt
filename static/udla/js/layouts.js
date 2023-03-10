'use strict';

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
            $(cuerpo).load(this.url, function () {
                $(modal + ' .modal-footer .btn_accion').css("display", "none");
                $(modal + ' .modal-footer button[data-bs-dismiss=modal]').text('cerrar');
                closeLoader()
            });
        } catch (error) {
            console.error(error);
        }

    }
    getModalFormGetCreateView(modal) {
        try {
            openLoader()
            const cuerpo = modal + ' #contenido'
            const url = this.url
            $(cuerpo).load(url, function () {
                $(modal).modal('show');
                $(modal + ' .modal-footer .btn_accion').text('Guardar').attr('id', 'btn_guardar');
                $(modal + ' .modal-body form').attr('action', url).attr('id', 'form_crear');
                closeLoader()
            });
        } catch (error) {
            console.error(error);
        }
    }
    getOffcanvasFormGetCreateView(modal,btn_id='form_crear') {
        try {
            openLoader()
            const cuerpo = modal + ' #contenido'
            const url = this.url
            $(cuerpo).load(url, function () {
                $(modal).offcanvas("toggle");
                $(modal + ' .modal-footer .btn_accion').text('Guardar').attr('id', 'btn_guardar');
                $(modal + ' .modal-body form, '+modal + ' .offcanvas-footer form').attr('action', url).attr('id', btn_id);
                closeLoader()
            });
        } catch (error) {
            console.error(error);
        }

    }
    getModalFormGetUpdateView(modal) {
        try {
            openLoader()
            const cuerpo = modal + ' #contenido'
            const url = this.url
            $(cuerpo).load(url, function () {
                $(modal).modal('show');
                $(modal + ' .modal-footer .btn_accion').text('actualizar').attr('id', 'btn_actualizar');
                $(modal + ' .modal-body form').attr('action', url).attr('id', 'form_actualizar');
                closeLoader()
            });
        } catch (error) {
            console.error(error);
        }

    }
    post(params) {
        params = Object.assign(params, this.params);
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
                ).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = location.protocol + '//' + location.host + location.pathname + window.location.search;
                    }
                });
            },
            error: function () {
                closeLoader()
            },
        });
    }
    patch(params) {
        $.ajax({
            url: this.url,
            type: 'PATCH',
            data: params,
            headers: { "X-CSRFToken": $('input[name=csrfmiddlewaretoken]').val() },
            beforeSend: function () {
                openLoader()
            },
            success: function (response) {
                Swal.fire(
                    response['respuesta'], '',
                    'success'
                ).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = location.protocol + '//' + location.host + location.pathname + window.location.search;
                    }
                })
            },
            error: function () {
                closeLoader()
            },
        });
    }
    put(params) {
        $.ajax({
            url: this.url,
            type: 'PUT',
            data: params,
            headers: { "X-CSRFToken": $('input[name=csrfmiddlewaretoken]').val() },
            beforeSend: function () {
                openLoader()
            },
            success: function (response) {
                Swal.fire(
                    response['respuesta'], '',
                    'success'
                ).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = location.protocol + '//' + location.host + location.pathname + window.location.search;
                    }
                })
            },
            error: function () {
                closeLoader()
            },
        });
    }
    delete() {
        $.ajax({
            url: this.url,
            type: 'DELETE',
            headers: { "X-CSRFToken": $('input[name=csrfmiddlewaretoken]').val() },
            beforeSend: function () {
                openLoader()
            },
            success: function (response) {
                Swal.fire(
                    response['respuesta'], '',
                    'success'
                ).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = location.protocol + '//' + location.host + location.pathname + window.location.search;
                    }
                })
            },
            error: function () {
                closeLoader()
            },
        });
    }
    postFormData(formData, modal, alerta = true) {
        const url = this.url
        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            beforeSend: function () {
                if (alerta === true) {
                    openLoader()
                }
            },
            success: function (response) {
                if (response['estado'] == 0) {
                    $(modal).modal('hide');
                    Swal.fire(
                        response['mensaje'], '',
                        'success'
                    ).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = location.protocol + '//' + location.host + location.pathname + window.location.search
                        }
                    })
                }
                else if (response['estado'] == 3) {
                    console.log(response['mensaje'])
                    if (alerta === true) {
                        closeLoader()
                    }
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
                if (alerta === true) {
                    closeLoader()
                }
            },
        });
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

function getHtmlSwal(title, message) {
    return `
    <div class="card-body">
        <h5 class="card-title">
            <font style="vertical-align: inherit;">
                <font style="vertical-align: inherit;">
                    ${title}
                </font>
            </font>
        </h5>
        <p class="card-text">
            <font style="vertical-align: inherit;">
                <font style="vertical-align: inherit;">
                    ${message}
                </font>
            </font>
        </p>
    </div>`
}

function validateForm(form) {
    let status = true;
    $("#" + form + ' :input').each(function () {
        if (this.value == "") {
            Swal.fire(
                'Complete los datos solicitados', '',
                'warning'
            )
            status = false;
        }
        if (status===false) {
            console.log(this)
            console.log(this.value)
        }
        
    });
    return status;
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
                    $('.modal').modal('hide');
                    $('[data-bs-dismiss="offcanvas"]').click();
                }
            })

        }
    });

    $(document).on('click', '.btn_info', function (e) {
        const titulo = $(this).attr('titulo');
        const info = $(this).attr('info');
        if (![null, '', undefined].includes(titulo) && ![null, '', undefined].includes(info)) {
            Swal.fire({
                title: '<h5 class="card-title text-primary fw-bold text-uppercase">' + titulo + '</h5>',
                html: '<p class="text-justify">' + info + '</p>',
                focusConfirm: false,
                confirmButtonText:
                    '<i class="fa fa-thumbs-up"></i> Cerrar',
            })
        }
        else {
            alert('No tiene las configuraciones solicitadas')
        }
    });
    //init fix summernote paragraph
    $(document).on('click', '.note-btn.dropdown-toggle', function (e) {
        $(this).closest('.note-btn-group').children('ul').addClass('show');
    })
    $(document).on('click', '.note-dropdown-menu.dropdown-menu.show button', function (e) {
        $('.note-dropdown-menu.dropdown-menu.show').removeClass('show');
    })
    //finaly fix summernote paragraph

    //fix min number
    $(document).on('change', '[type="number"]', function () {
        if (!$(this).val() || (parseInt($(this).val()) <= 11 && parseInt($(this).val()) >= $(this).attr('min')));
        else $(this).val($(this).data("old"));
    });


    $(document).on('change', '.input_image_row [type="file"]', function (e) {
        const nofile = $('.input_image_row [class*="col-"] .input_image_description').html();
        let tipo = [".jpg", ".jpeg", "png"]
        if ($(this).attr('accept') === 'application/pdf') {
            tipo = [".pdf"]
        }
        if (this.files.length == 0) {
            $('.input_image_row [class*="col-"] .input_image_description').html(nofile);
        }
        else {

            let sFileName = this.files[0].name;
            let _validFileExtensions = tipo;
            if (sFileName.length > 0) {
                let blnValid = false;
                for (let j = 0; j < _validFileExtensions.length; j++) {
                    let sCurExtension = _validFileExtensions[j];
                    if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
                        blnValid = true;
                        break;
                    }
                }
                if (!blnValid) {
                    Swal.fire(
                        'El formato del archivo no es valido!',
                        'Formatos permitidos *' + tipo.join(", "),
                        'warning'
                    )
                    $('.input_image_row [class*="col-"] .input_image_description').html(nofile);
                } else {
                    $('.input_image_row [class*="col-"] .input_image_description').html(sFileName);
                }
            }
        }
    });
});