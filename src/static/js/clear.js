$(document).ready(() => {
    $(".file-clear-button").click(() => {
        $.ajax({
            type: "DELETE",
            url: "/clear",
            complete: () => {
                window.location.replace("/")
            }
        })
    })
})