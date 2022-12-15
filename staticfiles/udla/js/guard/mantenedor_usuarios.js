// function recargar_tabla_usuarios() {
//     $('#lista_usuarios').DataTable({
//         "sPaginationType": "full_numbers",
//         // "bFilter": true,
//         // "bLengthChange": false,
//         // "scrollCollapse": true,
//         // "destroy": true,
//         // "searching": true,
//         // "bInfo": false,
//         // "responsive": true,
//         // "autoWidth": false,
//         // "sort": false,
//         "ajax": {
//             url: "/mantenedor/usuario/",
//             type: 'POST',
//             dataSrc:"",
//             data: {
//                 'accion':0,
//                 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
//             },
//             beforeSend: function () {
//                 Swal.fire({
//                     // imageUrl: '/static/img/demo/progress.svg',
//                     showCancelButton: false,
//                     showConfirmButton: false,
//                     allowOutsideClick: false,
//                 });
//                 $('.swal2-container.swal2-backdrop-show').css('background', 'rgba(255,255,255,.8)');
//                 $('.swal2-popup').css('background', 'transparent');
//             },
//             complete: function () {
//                 swal.close();
//             },
//             error: function () {
//                 swal.close();
//             },
//         },
//         "columns": [
//             { "data": "id" },
//             { "data": "username" },
//             { "data": "nombre_completo" },
//             { "data": "correo" },
//         ],
//         "oLanguage": {
//             "sLengthMenu": "_MENU_ ",
//             "sInfo": "<b>_START_ a _END_</b> de _TOTAL_ Registros"
//         },
//     });
// }

// $(document).ready(function () {
//     recargar_tabla_usuarios()
//     Swal.fire({
//         // imageUrl: '/static/img/demo/progress.svg',
//         showCancelButton: false,
//         showConfirmButton: false,
//         allowOutsideClick: false,
//     });
// });