// https://stackoverflow.com/questions/52379847/django-file-upload-with-ajax-fueled-progress-bar

$(document).ready(function() {

    $('#upload_progress_form').on('submit', function(event) {
        event.preventDefault();

        var post_data = new FormData($("#upload_progress_form")[0]);

        $.ajax({
            url: "#",
            type: "POST",
            data: post_data,
            cache: false,
            processData: false,
            contentType: false,
            beforeSend: function() {
                // 
            },
            xhr: function() {
                var xhr = new window.XMLHttpRequest();

                xhr.upload.addEventListener("progress", function(evt) {
                    var percent = Math.round(evt.loaded/evt.total * 100)
                    $('#upload_progress_button').attr('disabled', true)
                    $('#upload_progress_button').get(0).innerText = "Uploading: " + percent + "%"
                }, false);

                xhr.upload.addEventListener("load", function(evt) {
                    $('#upload_progress_button').css('background-color', 'green')
                    $('#upload_progress_button').get(0).innerText = "Finishing Upload... Please Wait..."
                }, false);

                return xhr;
            },
            success: function(result) {
                console.log(result)
            },
            error: function(result) {
                console.log(result)
            },
        }).done(function(response) {
            window.location.reload()
        });
    });
});
