$(document).ready(() => {
    $(".submission-form").submit((event) => {
        const formData = new FormData(event.target)
    
        $.ajax({
            data: formData,
            type: "POST",
            url: "/upload",
            contentType: false,
            processData: false,
            success: () => {
                $(".submission-form").trigger("reset")
            },
            error: () => {
                $(".submission-form").trigger("reset")
            }
        })
    })
})