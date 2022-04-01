$(document).ready(() => {
    $(".file-clear-button").click(() => {
        $.ajax({
            type: "DELETE",
            url: "/clear",
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