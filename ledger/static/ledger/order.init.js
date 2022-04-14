// Function to highlight part of the string before first semicolon(:) char
function formatProduct (product) {
  if (!product.id) {
    return product.text;
  }

  var $product = $('<span><strong></strong><span></span></span>');

  // Use .text() instead of HTML string concatenation to avoid script injection issues
  var str = product.text;
  $product.find("strong").text(str.slice(0, str.indexOf(':') + 1));
  $product.find("span").text(str.slice(str.indexOf(':') + 1));

  return $product;
};

// Prepare Select2 parameters (we need them twice to re-bind them in new row
const select2ProductOptions = {
    templateSelection: formatProduct,
    ajax: {
        data: function (params) {
            // extra handler to pass order's currency to backend so only required prices/discounts
            // will be returned. Empty Currency field should be processed on backend side
            var currencyData = $('select#id_Currency').select2('data');
            var query = {
                q: params.term,
                cur: currencyData[0].text
            }
            return query;
        }
    }
};

function onProductSelect(event) {
    var productData = event.params.data;
    var parentRow = $(event.target).closest("div.position-form");
    var elPrice = $(parentRow).find("input[name$='Price']");
    var elQty = $(parentRow).find("input[name$='-Quantity']");
    // Update Price and Qty (if necessary) input in the same row after new selection
    if (elQty.val() == "") { elQty.val(1); }
    elPrice.val(productData.price).trigger('input');    // and then fire "input" event
}

// Initialize Select2 elements
$("select.select2[name='Customer']").select2();
$("select.select2[name='Currency']").select2();
$("div.position-form select.select2[name$='Product']")
    .select2(select2ProductOptions)
    .on("select2:select", onProductSelect);

// Initialize FlatPickr elements
$("input.dateinput").flatpickr();

$("div.position-form").formset({
    prefix: "customerorderposition_set",
    formTemplate: "div#positions-empty_form",
    formCssClass: "position-form",
    deleteContainerClass: "remove-position-placeholder",
    deleteCssClass: "btn btn-danger",
    deleteText: "<i class='bi bi-trash'></i>",
    addContainerClass: 'add-position-placeholder',
    addCssClass: "btn btn-warning",
    addText: "<i class='bi bi-plus-square'></i> Add Position",
    added: function(row) {
        var product = row.find("select.select2[name$='Product']");
        // Event handlers are cloned with each new form, so we first unbind
        // all unnecessary handlers on the select box
        product.unbind();
        // And re-initialize it with a brand-new set of handlers:
        product
            .select2(select2ProductOptions)
            .on("select2:select", onProductSelect);
    }
});


// This handler assignment is dynamic, based on permanent container and further element filtering
$("div#positions-rows").on("input", "input[type='number']", function(event) {
    var parentRow = $(event.target).closest("div.position-form");

    var valPrice = Number($(parentRow).find("input[name$='-Price']").val());
    var valQty = Number($(parentRow).find("input[name$='-Quantity']").val());
    var valDiscount = Number($(parentRow).find("input[name$='-Discount']").val());

    const subtotal = (valPrice * valQty) - valDiscount;
    //const sum = $amount2.get().reduce((sum, el) => sum + +el.value, 0);
    var elSubtotal = $(parentRow).find("input[name$='-subtotal']");
    elSubtotal.val(subtotal.toFixed(2)).trigger("change");
});

$("div#positions-rows").on("change", "input[name$='-subtotal']", function() {
    // I love this trick
    const elSubtotals = $("div#positions-rows").find("input[name$='-subtotal']");
    const sum = $(elSubtotals).get().reduce((sum, el) => sum + +el.value, 0);
    var elTotal = $("#positions-total");
    $(elTotal).val(sum.toFixed(2));
});
