(() => {
$(document).ready(() => {
    const image = document.getElementById('image');
    const cropper = new Cropper(image, {
        aspectRatio: 600 / 448,
    });

    $("#crop").on("click", () => {
        console.log(cropper.getData());
    });

    $("#rotate").on("click", () => {
        cropper.rotate(90)
    });
});
})();