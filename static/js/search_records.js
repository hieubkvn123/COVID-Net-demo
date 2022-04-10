$(document).ready(function() {
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

        // Make the modal dialog appear with information corresponding to the NRIC
        // ... 
        alert(nric)
    } );
})