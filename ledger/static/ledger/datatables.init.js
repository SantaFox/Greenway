/* Custom filtering function which will search data in column four between two values */
$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        var order_amount = parseFloat( data[3] ) || 0;
        var order_paid = parseFloat( data[4] ) || 0;
        // 0 - all
        // 1 - active
        // 2 - (pending)
        // 3 - not delivered
        // 4 - not paid
        // 5 - completed
        var filter = parseInt( $('#order-selectinput').val(), 10 );

        if ( filter == 0 ) {
            return true;
        } else if ( filter == 1 ) {
            if ( order_amount != order_paid ) {
                return true;
            }
        } else if ( filter == 2 ) {
        } else if ( filter == 3 ) {
        } else if ( filter == 4 ) {
        } else if ( filter == 5 ) {
        }
        return false;
    }
);

// datatable
$(document).ready(function() {
    var table = $('.datatable').DataTable( {
        'columnDefs': [
            {
                'targets': [ 4 ],           // get_paid_amount
                'visible': false
            }
        ]
    } );

    // Event listener to the two range filtering inputs to redraw on input
    $('#order-selectinput').change( function() {
        table.draw();
    } );

    $(".dataTables_length select").addClass('form-select form-select-sm');
});