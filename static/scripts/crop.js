(() => {
$(document).ready(() => {
    
    const image = document.getElementById('image');
    const cropper = new Cropper(image, {
        aspectRatio: 600 / 448,
    });

    $("#crop").on("click", () => {
        let data = cropper.getData();
        $('input[name="x"]').val(data.x);
        $('input[name="y"]').val(data.y);
        $('input[name="width"]').val(data.width);
        $('input[name="height"]').val(data.height);
        $('input[name="rotate"]').val(data.rotate);
        $( "form" ).first().trigger( "submit" );
    });

    $("#rotate").on("click", () => {
        cropper.rotate(90)
    });

});
})();