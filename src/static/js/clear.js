$(document).ready(() => {
    $(".file-clear-button").click(() => {
        $.ajax({
            type: "DELETE",
            url: "/clear",
            async: false,
            error: () => {
                alert("Clear fail!")
            },
            success: () => {
                window.location.replace("/")
            }
        })
    })
})