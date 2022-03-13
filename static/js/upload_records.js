// For Image uploading
function preview() {
    frame.src = URL.createObjectURL(event.target.files[0]);
}
function clearImage() {
    document.getElementById('formFile').value = null;
    frame.src = "/static/media/xray_placeholder.png";
}

// For animation
$(document).ready(() => {
    $(".fadeIn").fadeIn('slow').removeClass('hidden')
})