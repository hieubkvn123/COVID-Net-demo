$(document).ready(function() {
    $('#sortTable').DataTable({
        'pageLength' : 20
    });

    $("#sortTable_filter input").addClass('form-control')
        .attr("placeholder", "Search")
        .css("display", "block")
        
        $("#sortTable_filter label").css("font-weight", "bold")
})