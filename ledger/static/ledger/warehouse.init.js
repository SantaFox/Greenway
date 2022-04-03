$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        var amount_in_stock = parseFloat( data[3] ) || 0;
        var amount_receiving = parseFloat( data[4] ) || 0;
        var amount_delivering = parseFloat( data[5] ) || 0;
        var amount_reserved = parseFloat( data[6] ) || 0;
        var amount_available = parseFloat( data[7] ) || 0;
        // 0 - all
        // 1 - show in stock
        // 2 - show receivable
        // 3 - show deliverable
        // 4 - show reserved
        // 5 - show available
        var filter = parseInt( $('#order-selectinput').val(), 10 );

        if ( filter == 0 ) {
            return true;
        } else if ( filter == 1 && amount_in_stock != 0 ) {
            return true;
        } else if ( filter == 2 && amount_receiving != 0 ) {
            return true;
        } else if ( filter == 3 && amount_delivering != 0 ) {
            return true;
        } else if ( filter == 4 && amount_reserved != 0 ) {
            return true;
        } else if ( filter == 5 && amount_available != 0 ) {
            return true;
        }
        return false;
    }
);


// datatable
$(document).ready(function() {
    var table = $('.datatable').DataTable( {
        dom: '<"toolbar">frtip',
        columnDefs: [ {
            targets: 2,
            render: DataTable.render.ellipsis( 70, true, true )
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

    // Event listener to the two range filtering inputs to redraw on input
    $('#order-selectinput').change( function() {
        table.draw();
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