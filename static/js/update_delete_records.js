jQuery(() => {
    // Function for closing info modal
    function close_patient_modal() {
        $("#exampleModal").modal("toggle")
    }

    // Event handler for any record field changes in the single record view
    $("#patient-info-modal input").on("keyup", () => {
        $("#info-update-btn").attr("disabled", false)
    })

    // Event handler for clicking update button
    $("#info-update-btn").on("click", () => {
        // Get all needed information
        let nric = $("#info-nric").val()
        let fname = $("#info-fname").val()
        let lname = $("#info-lname").val()
        let phone = $("#info-phone").val()
        let gender = $("#info-gender").val()
        let dob = $("#info-dob").val()
        let datetime = $("#info-datetime").val()

        // Submit the information for update to endpoint

        // Get server's response and display response message

        // Update information on the client's side
        
        // Close modal
        close_patient_modal()
    })
})