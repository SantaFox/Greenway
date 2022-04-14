// datatable
$(document).ready(function() {
    var table = $('.datatable').DataTable( {
        dom: '<"toolbar">frt',
        columnDefs: [ {
            targets: [ 2, 3, 4, 5 ],
            render: DataTable.render.number('\'', '.', 2),
            createdCell: function (td, cellData, rowData, row, col) {
                if (cellData < 0) {
                    $(td).addClass('text-danger')
                }
            }
        } ],
        rowGroup: {
            dataSrc: 0,
            startRender: function ( rows, group ) {
                var sumFinal = rows
                    .data()
                    .pluck(5)
                    .reduce( function (a, b) {
                        return a + b*1;
                    }, 0);

                return '<div class="row"><div class="col-6">'+ group + '</div><div class="col-6 text-end">' +
                    $.fn.dataTable.render.number('\'', '.', 2).display( sumFinal ) + '</div></div>';
            }
        }
    } );


    //Buttons examples
//    var table = $('#datatable-buttons').DataTable({
//        lengthChange: false,
//        buttons: ['copy', 'excel', 'pdf']
//    });

//    table.buttons().container()
//        .appendTo('#datatable-buttons_wrapper .col-md-6:eq(0)');

    // Post-initialization styling
    // $(".dataTables_length select").addClass('form-select form-select-sm');
} );