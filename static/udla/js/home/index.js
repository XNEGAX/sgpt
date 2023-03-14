$(document).ready(function () {
    $(document).on('change', '#year', function (e) {
        $('#form_secciones_docente_home').submit();
    });
    $(document).on('change', '#seccion', function (e) {
        $('#form_secciones_docente_home').submit();
    });
    $(document).on('click', '#btn_avanzar_actividades_del_6_al_10', function (e) {
        let actividades_del_6_al_10 = document.getElementsByClassName("actividades_del_6_al_10");
        
        for (var i = 0; i < actividades_del_6_al_10.length; i++) {
            $(actividades_del_6_al_10[i]).removeClass('d-none').addClass('d-flex');
        }
        let actividades_del_1_al_5 = document.getElementsByClassName("actividades_del_1_al_5");
        for (var i = 0; i < actividades_del_1_al_5.length; i++) {
            $(actividades_del_1_al_5[i]).removeClass('d-flex').addClass('d-none');
        }
        $('#btn_volver_actividades_del_1_al_5').removeClass('d-none').addClass('d-flex');
        $(this).removeClass('d-flex').addClass('d-none');
    });
    $(document).on('click', '#btn_volver_actividades_del_1_al_5', function (e) {
        let actividades_del_6_al_10 = document.getElementsByClassName("actividades_del_6_al_10");
        
        for (var i = 0; i < actividades_del_6_al_10.length; i++) {
            $(actividades_del_6_al_10[i]).removeClass('d-flex').addClass('d-none');
        }
        let actividades_del_1_al_5 = document.getElementsByClassName("actividades_del_1_al_5");
        for (var i = 0; i < actividades_del_1_al_5.length; i++) {
            $(actividades_del_1_al_5[i]).removeClass('d-none').addClass('d-flex');
        }
        $('#btn_avanzar_actividades_del_6_al_10').removeClass('d-none').addClass('d-flex');
        $(this).removeClass('d-flex').addClass('d-none');
    });

    
});