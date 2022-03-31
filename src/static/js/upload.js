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
            error: () => {
                alert("Upload fail!")
            },
            success: () => {
                window.location.replace("/")
            }
        })
    })
})