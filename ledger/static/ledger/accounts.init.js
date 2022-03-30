// datatable
$(document).ready(function() {
    var table = $('.datatable').DataTable( {
        stateSave: true
    } );

    $(".dataTables_length select").addClass('form-select form-select-sm');
});