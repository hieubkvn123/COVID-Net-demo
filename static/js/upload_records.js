// For Image uploading
function preview() {
    frame.src = URL.createObjectURL(event.target.files[0]);
}
function clearImage() {
    document.getElementById('xray-file').value = null;
    frame.src = "/static/media/xray_placeholder.png";
}

// Functions after load
jQuery(() => {
    // For fade-in form animation
    $(".fadeIn").fadeIn('slow').removeClass('hidden')

    // For the upload of records
    $("#create_record_btn").on("click", () => {
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
                    alert(response.data['msg'])
                })
                .catch(err => {
                    console.log(err.response.data['msg'])
                })

            // Check if X-Ray image is provided
            let file = document.querySelector("#xray-file")
            if(file.files.length > 0) { // Image exists 
                let formData = new FormData()
                formData.append("xray", file.files[0])
                formData.append("nric", nric)
                
                axios.post("/records/upload_xray", formData, {'Content-Type' : 'multipart/form-data'})
                    .then(response => {
                        console.log(response.data['msg'])
                        let diagnosis_result = response.data['payload']['result']
                        let diagnosis_confidence = response.data['payload']['confidence']

                        if(diagnosis_result === "negative")
                            $("#diagnosis-result").html(diagnosis_result).css("color", "green")
                        else 
                            $("#diagnosis-result").html(diagnosis_result).css("color", "red")
                            
                        $("#confidence").html(diagnosis_confidence)

                        toastr.success(response.data['msg'])
                    })
                    .catch(err => {
                        if(err.response)
                            toastr.error(err.response.data['msg'])
                    })
            }
        }
    })
})