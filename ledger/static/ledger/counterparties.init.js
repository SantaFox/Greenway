/* Custom filtering function which will search data in column four between two values */
$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        var isCustomer = data[5].toLowerCase() == 'true' ? true : false;
        var isSupplier = data[6].toLowerCase() == 'true' ? true : false;
        // 0 - all
        // 1 - customers
        // 2 - suppliers
        var filter = parseInt( $('#order-selectinput').val(), 10 );

        if ( filter == 0 ) {
            return true;
        } else if ( filter == 1 ) {
            if ( isCustomer ) {
                return true;
            }
        } else if ( filter == 2 ) {
            if ( isSupplier ) {
                return true;
            }
        }
        return false;
    }
);

// datatable
$(document).ready(function() {
    var table = $('.datatable').DataTable( {
        stateSave: true,
        'columnDefs': [
            {
                'targets': [ 5, 6 ],           // IsCustomer, IsSupplier
                'visible': false,
                'searchable': true
            }
        ]
    } );

    // Event listener to the two range filtering inputs to redraw on input
    $('#order-selectinput').change( function() {
        table.draw();
    } );

    $(".dataTables_length select").addClass('form-select form-select-sm');
});