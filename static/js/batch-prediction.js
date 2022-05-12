jQuery(() => {
    $(".input-images").imageUploader()

    // Event handler for batch diagnosis button click
    $("#batch-prediction-btn").on("click", (e) => {
        e.preventDefault()

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

                console.log(res.data['payload'])
            })
            .catch(err => {
                if(err.response)
                    alert(err.response.data['msg'])
                else 
                    console.log(err)
            })
    })
})