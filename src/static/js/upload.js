$(document).ready(() => {
    $(".submission-form").submit((event) => {
        const formData = new FormData(event.target)
    
        $.ajax({
            data: formData,
            type: "POST",
            url: "/upload",
            contentType: false,
            processData: false,
            async: false,
            error: (jqXHR) => {
                alert(jqXHR.responseText)
            },
            success: () => {
                window.location.replace("/")
            }
        })
    })
})