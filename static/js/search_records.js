jQuery(() => {
    let table = $('#sortTable').DataTable({
        'pageLength' : 20
    });

    $("#sortTable_filter input")
        .attr("placeholder", "Search")    

    $("#sortTable_filter label").css("font-weight", "bold")

    $('#sortTable tbody').on('click', 'tr', function () {
        // Extract the row
        var data = table.row( this ).data()

        // Extract the NRIC from the row
        let nric = data[0]
        let datetime = data[2]

        // Make the modal dialog appear with information corresponding to the NRIC
        // ... 
        // alert(nric)
        axios.post('/records/get_diagnosis', { nric, datetime }, { 'Content-Type' : 'application/json' })
            .then(res => {
                console.log(res.data['payload'])
            })
            .catch(err => {
                if(err.response) 
                    toastr.error(err.response.data['msg'])         
            })
    } );
})