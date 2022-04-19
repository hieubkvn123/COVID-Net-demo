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
                let payload = res.data['payload'][0]
                // let nric = payload['nric_fin'] .
                // let fname = payload['fname'] .
                // let lname = payload['lname'] .
                // let phone = payload['phone'] .
                // let gender = payload['gender'] .
                // let dob = payload['dob'] .
                // let datetime = payload['date_time']
                // let result = payload['result']
                // let confidence = payload['confidence']
                // let xray_url = payload['xray_img_url']

                console.log(payload.date_time)

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
            })
            .catch(err => {
                if(err.response) 
                    toastr.error(err.response.data['msg'])         
            })
    } );
})