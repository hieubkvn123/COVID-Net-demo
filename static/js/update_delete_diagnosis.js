jQuery(() => {
    // Event handler for any record field changes in the single record view
    $("#patient-diagnosis-info-modal input").on("keyup", () => {
        $("#info-update-btn").attr("disabled", false)
    })

    // Event handler for clicking update button
    $("#info-update-btn").on("click", async () => {
        // Get all needed information
        let nric = $("#info-nric").val()
        let fname = $("#info-fname").val()
        let lname = $("#info-lname").val()
        let phone = $("#info-phone").val()
        let gender = $("#info-gender").val()
        let dob = $("#info-dob").val()
        let datetime = $("#info-datetime").val()

        let old_nric = localStorage.getItem("current_nric")
        let row_id = localStorage.getItem("row_id")
        // console.log(old_nric, row_id) // For debugging
        
        let payload = { nric, old_nric, fname, lname, phone, gender, dob, datetime }

        // Submit the information for update to endpoint
        await axios.post('/diagnosis/update_diagnosis', payload , { 'Content-Type' : 'application/json' })
            .then(res => {
                // Get server's response and display response message
                alert(res.data['msg'])

                // Close modal
                $("#diagnosisModal").modal("toggle")
            })
            .catch(err => {
                if(err.response)
                    toastr.error(err.response.data['msg'])
                else
                    console.log(err)
            })
        
        // Update rows in the client side
        let new_name = `${fname} ${lname}`
        let temp = table.row(row_id).data()
        temp[0] = nric 
        temp[1] = new_name
        $('#sortTable').dataTable().fnUpdate(temp,row_id,undefined,false);

        // Modify the rest of the rows with the same NRIC
        table.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
            var data = this.data();

            if(data[0] === nric) {
                data[1] = new_name 
                $('#sortTable').dataTable().fnUpdate(data,rowIdx,undefined,false);
            }
        } );
    })

    // Event handler for clicking the delete button
    $("#info-delete-btn").on("click", async () => {
        let nric = localStorage.getItem("current_nric")
        let datetime = $("#info-datetime").val()

        let row_id = localStorage.getItem("row_id")

        let payload = { nric, datetime }

        // Submit the information for delete endpoint
        await axios.post('/diagnosis/delete_diagnosis', payload, { 'Content-Type' : 'application/json' })
            .then(res => {
                // Get server's response and display response message
                alert(res.data['msg'])

                // Close modal
                $("#diagnosisModal").modal("toggle")
            })
            .catch(err => {
                if(err.response)
                    toastr.error(err.response.data['msg'])
                else
                    console.log(err)
            })

        // Delete the row in client-side
        table.row(row_id).remove().draw()
    })
})