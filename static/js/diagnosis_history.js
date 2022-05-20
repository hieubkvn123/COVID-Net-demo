jQuery(() => {
    // For fade-in form animation
    $(".fadeIn").fadeIn('slow').removeClass('hidden')
    $('#search-result-cancel').on("click", () => {
        $("#diagnosisHistoryModal").modal("toggle") // Close modal
    })

    // Make diagnosis history table a DataTable
    table_diagnosis_history = $('#diagnosis-history-table').DataTable({
        'pageLength' : 10
    });

    $("#search_diagnosis_btn").on("click", () => {
        // Retrieve all information from form
        let nric = $("#search-record-form #nric").val()
        let fname = $("#search-record-form #fname").val()
        let lname = $("#search-record-form #lname").val()
        let date = $("#search-record-form #date").val()
        let result = $("#search-record-form #covidResult").val()

        let payload = { nric, fname, lname, date, result }
        let headers = {
            'headers' : {
                'Content-Type' : 'application/json'
            }
        }

        // POST the data to server
        axios.post('/diagnosis/search_diagnosis', payload, headers)
            .then(res => {
                // Clear current table
                table_diagnosis_history.clear().draw()

                // Open hidden result panel
                $("#diagnosisHistoryModal").modal("toggle")
                
                // Render the rows
                let tbody = $('#diagnosis-history-table tbody');
                let rows = res.data['payload']
                for(var i = 0; i < rows.length; i++) {
                    let row = rows[i]
                    table_diagnosis_history.row.add([
                        row['nric_fin'],
                        row['fname'] + ' ' + row['lname'],
                        row['date_time'],
                        row['result']
                    ]).draw()
                }
            })
            .catch(err => {
                if(err.response)
                    alert(err.response.data['msg'])
            })
    })
})