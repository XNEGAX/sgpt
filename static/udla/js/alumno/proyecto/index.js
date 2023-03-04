$(document).ready(function () {
    $('#summernote').summernote();
    summernote_list.forEach(function (item) {
        $('#'+item).summernote({
            height: 200,
        });
    });
    
});