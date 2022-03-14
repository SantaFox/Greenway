function formatProduct (product) {
  if (!product.id) {
    return product.text;
  }

  var $product = $(
    '<span><strong></strong><span></span></span>'
  );

  // Use .text() instead of HTML string concatenation to avoid script injection issues
  var str = product.text;
  $product.find("strong").text(str.slice(0, str.indexOf(':') + 1));
  $product.find("span").text(str.slice(str.indexOf(':') + 1));

  return $product;
};

// Select2
$("select.select2[name='Customer']").select2();
$("select.select2[name='Currency']").select2();
$("div.position-form select.select2[name$='Product']").select2({
    templateSelection: formatProduct,
    ajax: {
        data: function (params) {
            var currencyData = $('select#id_Currency').select2('data');
            var query = {
                q: params.term,
                cur: currencyData[0].text
            }

            // Query parameters will be ?q=[term]&type=public
            return query;
        }
    }
}).on("select2:select", function(event) {
    var productData = event.params.data;
    var priceElement = $(event.target).closest("div.row").find("input[name$='Price']");

    priceElement.val(productData.price);
});

$("input.dateinput").flatpickr();
$("div.position-form").formset({
    prefix: "customerorderposition_set",
    formTemplate: "div#empty_form",
    deleteContainerClass: "remove-placeholder",
    deleteCssClass: "btn btn-danger",
    deleteText: "<i class='uil-trash-alt'></i>",
    addContainerClass: 'position-add-placeholder',
    addCssClass: "btn btn-warning",
    addText: "<i class='uil-link-add'></i> Add Position",
    added: function(row) {
        var product = row.find("select.select2[name$='Product']");
        // Event handlers are cloned with each new form, so we first unbind
        // all unnecessary handlers on the select box
        product.unbind();
        // And re-initialize it with a brand-new set of handlers:
        product.select2({
            templateSelection: formatProduct
        });
    }
});


//    show: function () {
//        $(this).slideDown();
//    },
//    hide: function (deleteElement) {
//        if(confirm('Are you sure you want to delete this element?')) {
//            $(this).slideUp(deleteElement);
//        }
//    },


// https://www.brennantymrak.com/articles/django-dynamic-formsets-javascript
// https://stackoverflow.com/questions/15161982/how-to-submit-a-form-and-formset-at-the-same-time