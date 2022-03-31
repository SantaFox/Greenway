// datatable
$(document).ready(function() {
    var table = $('.datatable').DataTable( {
        columnDefs: [ {
            targets: 2,
            render: DataTable.render.ellipsis( 40, true, true )
        }, {
            targets: [ 3, 4, 5, 6, 7 ],
            createdCell: function (td, cellData, rowData, row, col) {
                if (cellData < 0) {
                    $(td).addClass('text-danger')
                }
            }
        } ],
        rowGroup: {
            dataSrc: 0
        },
        createdCell: function (td, cellData, rowData, row, col) {
            if (cellData < 0) {
                $(td).addClass('text-danger')
            }
        }
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