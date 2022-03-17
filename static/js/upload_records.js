// For Image uploading
function preview() {
    frame.src = URL.createObjectURL(event.target.files[0]);
}
function clearImage() {
    document.getElementById('formFile').value = null;
    frame.src = "/static/media/xray_placeholder.png";
}

// Functions after load
$(document).ready(() => {
    // For fade-in form animation
    $(".fadeIn").fadeIn('slow').removeClass('hidden')

    // For the upload of records
    $("#create_record_btn").click(() => {
        // Get all form information
        let fname = $("#create-record-form #fname").val()
        let lname = $("#create-record-form #lname").val()
        let nric = $("#create-record-form #nric").val()
        let gender = $("#create-record-form #gender").val()
        let dob = $("#create-record-form #dob").val()
        let phone = $("#create-record-form #phone").val()

        // Check emptiness - like my soul
        if(fname == "" || lname == "" || nric == "" || dob == "" || phone == "")
            alert("Please fill in all particulars for patient")
        else {
            const data = { fname, lname, nric, gender, dob, phone }

            // Send the data to the API 
            axios.post('/records/create', data, {'Content-Type' : 'application/json'})
                .then(response => {
                    console.log('Records created successfully ... ')
                    alert('Records created successfully')
                })
                .catch(err => {
                    console.log('Something wrong happened ... ')
                })
        }
    })
})