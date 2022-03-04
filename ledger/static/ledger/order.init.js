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
$("select.select2[name$='Product']").select2({
    templateSelection: formatProduct
});
$(".dateinput").flatpickr();
$('.repeater').repeater({
    defaultValues: {
        'textarea-input': 'foo',
        'text-input': 'bar',
        'select-input': 'B',
        'checkbox-input': ['A', 'B'],
        'radio-input': 'B'
    },
    show: function () {
        $(this).slideDown();
    },
    hide: function (deleteElement) {
        if(confirm('Are you sure you want to delete this element?')) {
            $(this).slideUp(deleteElement);
        }
    },
});

// https://www.brennantymrak.com/articles/django-dynamic-formsets-javascript
// https://stackoverflow.com/questions/15161982/how-to-submit-a-form-and-formset-at-the-same-time