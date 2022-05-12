jQuery(() => {
    table = $('#sortTable').DataTable({
        'pageLength' : 20,
        'createdRow' : function( row, data, dataIndex ) {
            if(data[3] == 'NONE') {
                $( row ).addClass('row-disabled')
            }
        }
    });

    $("#sortTable_filter input")
        .attr("placeholder", "Search")    

    $("#sortTable_filter label").css("font-weight", "bold")

    // Event handler for clicking to view a record.
    $('#sortTable tbody').on('click', 'tr', function () {
        // Extract the row
        var data = table.row( this ).data()
        var row_id = table.row( this ).index()

        // Extract the NRIC from the row
        let nric = data[0]
        let datetime = data[2]

        // Disable the update button by default
        $("#info-update-btn").attr("disabled", true)

        // Make the modal dialog appear with information corresponding to the NRIC
        axios.post('/diagnosis/get_diagnosis', { nric, datetime }, { 'Content-Type' : 'application/json' })
            .then(res => {
                // Retrieve the payload from server
                let payload = res.data['payload'][0]

                // Fill basic particulars
                $("#info-nric").val(payload.nric_fin)
                $("#info-fname").val(payload.fname)
                $("#info-lname").val(payload.lname)
                $("#info-phone").val(payload.phone)
                $("#info-gender").val(payload.gender)
                $("#info-dob").val(payload.dob)
                $("#info-datetime").val(payload.date_time)
                $("#info-result").val(payload.result).css("color", payload.result === "negative" ? "green" : "red")
                $("#info-confidence").val(payload.confidence).css("color", payload.result === "negative" ? "green" : "red")

                // Change image source
                $("#patient-info-xray-img").attr("src", payload.xray_img_url)

                // Store in local storage
                localStorage.setItem("current_nric", payload.nric_fin)
                localStorage.setItem("row_id", row_id)

                // Change modal dialog title
                $("#patient-diagnosis-info-modal-title").html(`Diagnosis no. ${payload.nric_fin} - ${payload.date_time}`)

                // Show the modal
                $("#diagnosisModal").modal("toggle")
            })
            .catch(err => {
                if(err.response) 
                    toastr.error(err.response.data['msg'])         
            })
    } );

    // Off click event for disabled rows
    $('#sortTable tbody').on('click', 'tr.row-disabled', function () { return false });
})