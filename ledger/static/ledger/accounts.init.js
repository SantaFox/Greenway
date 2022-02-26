// datatable
$(document).ready(function() {
    var table = $('.datatable').DataTable( {
        stateSave: true
//        'columnDefs': [
//            {
//                'targets': [ 5, 6 ],           // IsCustomer, IsSupplier
//                'visible': false,
//                'searchable': true
//            }
//        ]
    } );

    $(".dataTables_length select").addClass('form-select form-select-sm');
});