$(document).ready(function () {
    $("img[data-zoom]").each( function (index) {
        new Drift($(this)[0], {
            paneContainer: $(this).parent().find(".image-zoom-pane")[0]
        })
    })
});