// Select2
$(".select2").select2();
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