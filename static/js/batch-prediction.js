jQuery(() => {
    $(".input-images").imageUploader()

    // Event handler for batch diagnosis button click
    $("#batch-prediction-btn").on("click", (e) => {
        e.preventDefault()

        // Clear the modal content
        $("#pred-result-modal").empty()

        // Retrive all files from input field
        let file_input_id = $(".image-uploader input[type='file']").attr("id")
        let files = document.getElementById(file_input_id).files 

        let formData = new FormData()
        let headers = {
            'headers' : {
                'Content-Type' : 'multipart/form-data'
            }
        }
        for(var i = 0; i < files.length; i++) {
            formData.append(`file-${i+1}`, files[i])
        }

        // Send request to server
        axios.post('/diagnosis/create_batch_diagnosis', formData, headers)
            .then(res => {
                alert(res.data['msg'])

                // Write the results on the the modal
                let results = res.data['payload']
                for(var i = 0; i < results.length; i++) {
                    $("<div>")
                        .html(`
                            <div class='result-item'>
                                <strong>NRIC/FIN:</strong>  <span>${results[i]['nric']}</span><br>
                                <strong>Result:</strong>  <span class='result ${results[i]['result']}'>${results[i]['result']}</span><br>
                                <strong>Confidence:</strong>  <span class='confidence ${results[i]['result']}'>${results[i]['confidence']}</span><br>
                                <strong>Message:</strong>  <span>${results[i]['msg']}</span><br>
                                <hr/>
                            </div>
                        `)
                    .appendTo("#pred-result-modal")
                }

                $("#predResultModal").modal("toggle")
            })
            .catch(err => {
                if(err.response)
                    alert(err.response.data['msg'])
                else 
                    console.log(err)
            })
    })

    // Event handler for clicking cancel result on modal dialog
    $("#pred-result-cancel").on("click", () => {
        $("#predResultModal").modal("toggle")
    })
})