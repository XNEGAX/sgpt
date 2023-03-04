$(document).ready(function () {
    $('#summernote').summernote();
    summernote_list.forEach(function (item) {
        $('#'+item).summernote({
            height: 600,
            toolbar: [
                ['font', ['bold', 'underline', 'clear']],
                ['para', ['ul', 'ol', 'paragraph']],
              ]
        });
    });
    
});