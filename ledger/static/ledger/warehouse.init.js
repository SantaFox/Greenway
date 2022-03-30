// datatable
$(document).ready(function() {
    var table = $('.datatable').DataTable( {
        "columnDefs": [ {
            "targets": 2,
            "render": function ( data, type, row, meta ) {
                return type === 'display' && data.length > 40 ?
                    '<span title="'+data+'">'+data.substr( 0, 38 )+'...</span>' :
                    data;
            }
        } ]
    } );

    //Buttons examples
//    var table = $('#datatable-buttons').DataTable({
//        lengthChange: false,
//        buttons: ['copy', 'excel', 'pdf', 'colvis']
//    });

//    table.buttons().container()
//        .appendTo('#datatable-buttons_wrapper .col-md-6:eq(0)');
        
        $(".dataTables_length select").addClass('form-select form-select-sm');
} );