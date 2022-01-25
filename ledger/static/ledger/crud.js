var initialize_checkboxes = function(){
    // Select/Deselect checkboxes
    var checkbox = $('table tbody input[type="checkbox"]');
    $("#selectAll").click(function(){
        if(this.checked){
            checkbox.each(function(){
                this.checked = true;
            });
        } else{
            checkbox.each(function(){
                this.checked = false;
            });
        }
    });
    checkbox.click(function(){
        if(!this.checked){
            $("#selectAll").prop("checked", false);
        }
    });
};

$(document).ready(function(){
    $('.modal form').on('submit', function (e) {

        var csrf_cookie = function() {
            var cookieValue = null,
                name = 'csrftoken';
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        };

        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type:'POST',
            data: $(this).serialize(),  // $(this).serializeObject(),
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_cookie());
            },
            success:function(response){
                let result = response.status;
                if (result == 'success') {
                    $('.modal').each(function(){
                        $(this).modal('hide');
                    });
                    /* TODO: We should check for instruction here, and reload page OR refresh parent */
                    location.reload();
                } else {
                    if (response.message) {
                        add_alert(response.message.text, response.message.level);
                    }
                    console.log(response.errors)
                }
            },
            error:function(){
                add_alert('Internal server error, please contacts support', 'Error');
            },
        });
    });
});

/*
    Обработчик добавления или редактирования объекта из строки в основной таблице страницы.
    Если у кнопки, вызвавшей обработчик, прописан data-id, то это редактирование указанного объекта (так оформлены
    кнопки в таблице); если не прописан - то это добавление (кнопка в шапке или в подвале табличной субформы).
    Если у кнопки, вызвавшей обработчик, прописан data-parent-id, то эта информация также передаётся в обработчик. По
    идее, это нужно только при добавлении, т.к. при редактировании запись не может переноситься в другой родительский
    объект (к примеру, оплата не может преноситься в другой заказ).
    Если это редактирование, то запрашивается список нужных полей для редактирования (так как в таблице могут быть
    не все) через AJAX по адресу, указанному в параметрах формы. Дальше все поля формы заполняются из полученных
    с сервера данных. Для positionsCount и paymentsCount специальные обработчики, указывающие количество
    строк в соответствующих подтаблицах.
    Если это добавление, то используются поля, запрошенные с сервера.
*/
$(document).ready(function() {
    $('.editModal').on('show.bs.modal', function (event) {

        var zIndex = 1040 + (10 * $('.modal:visible').length);
        $(this).css('z-index', zIndex);
        setTimeout(function() {
            $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
        }, 0);

        var button = $(event.relatedTarget) // Button that triggered the modal
        var modal = $(this)

        // We get "id" from data-* attributes of calling button and "parent_id" from hidden fields
        // in the form that contained calling button
        var itemId = button.data('id') // Extract info from data-* attributes
        var parentId = $(button).closest("form").find('input[type="hidden"][name="parent_id"]').val();

        var ajaxData = {}
        if (itemId) ajaxData.id = itemId;
        if (parentId) ajaxData.parent_id = parentId;

        if (itemId) {
            $(modal).find('.modal-footer input[name="action"]').val('edit');
        } else {
            $(modal).find('.modal-footer input[name="action"]').val('add');
        };

        $.ajax({
            url: $(modal).find('form').attr('action'),
            type: 'GET',
            data: ajaxData,
            dataType: 'json',
            success: function(response) {
                for (var i in response) {
                    if (i == 'positions_count') {
                        var span = $(modal).find('#positionsCount');
                        span.text('('+response[i]+')');
                    } else if (i == 'payments_count') {
                        var span = $(modal).find('#paymentsCount');
                        span.text('('+response[i]+')');
                    } else {
                        var formElement = $(modal).find('.modal-body [name="' + i + '"],.modal-footer [name="' + i + '"]');
                        if (formElement.attr('type') == 'checkbox'){
                            formElement.prop('checked', response[i]);
                        } else {
                            formElement.val(response[i]);
                        }
                    }
                }
            },
            error: function() {
                add_alert('Internal server error, please contacts support', 'Error');
            },
        });

    });
})

/*
    Обработчик удаления объекта из строки в основной таблице страницы.
    Запрашивается список связанных объектов через AJAX по адресу, указанному в параметрах формы, которые
    заполняется при формировании шаблона. Этот обработчик в
    В случае получения "Ok" формируется текст подтверждения и разблокируется кнопка Submit, которая также вызывает
    AJAX обработчик, но уже с методом POST, чтобы отделить запрос от действия. Результат работы запроса
    отражается в блоке Messages
    Для того, чтобы при повторном открытии модального окна не было старого текста, при закрытии весь блок
    перезаписывается из сохраненной версии
*/
$(document).ready(function() {
    $('#deleteModal').on('show.bs.modal', function (event) {

        var $ul = $('<ul class="small"></ul>');
        function getList(item, $list) {
            $.each(item, function(key, value) {
              var $li = $('<li />');
              $li.append(key);
              var $subul = $("<ul/>");
              $.each(value, function(i) {
                var subli = $('<li/>')
                  .text(value[i])
                  .appendTo($subul);
              });
              $li.append($subul).appendTo($list);
            });
        }

        var zIndex = 1040 + (10 * $('.modal:visible').length);
        $(this).css('z-index', zIndex);
        setTimeout(function() {
            $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
        }, 0);

        var button = $(event.relatedTarget) // Button that triggered the modal
        var modal = $(this)
        var itemId = button.data('id') // Extract info from data-* attributes
        $.ajax({
            url: $(modal).find('form').attr('action'),
            type: 'GET',
            data: {id: itemId},
            dataType: 'json',
            success: function(response) {
                var header = $(modal).find('.modal-body #deleteQuestion');
                var content = $(modal).find('.modal-body #deleteContent');
                if (response.status == 'ok') {
                    header.text('Are you sure you want to delete this Record?');
                    content.html('<p class="text-warning"><small>This action cannot be undone.</small></p>');
                    $(modal).find('.modal-body input[name="id"]').val(itemId);
                    $(modal).find('input[type="submit"]').prop('disabled', false);
                } else {
                    header.text('Record deletion is not possible. There are related objects exist:');
                    content.empty();
                    getList(response.related, $ul);
                    $ul.appendTo(content);
                    $(modal).find('input[type="submit"]').prop('disabled', true);
                };
            },
            error: function() {
                add_alert('Internal server error, please contacts support', 'Error');
            },
        });
    });

    $('#deleteModal').on('hidden.bs.modal', function () {
        /* I have no idea why to use extra clone(), but without it after first ReplaceWith
         all changes will reflect savedDelete as well */
        $('#deleteModal').replaceWith(savedDelete.clone(true))
    });
})

var savedDelete;

$(document).ready(function() {
    savedDelete = $('#deleteModal').clone(true);
})

$(document).ready(function() {
    $('.tableModal').on('show.bs.modal', function (event) {

        var zIndex = 1040 + (10 * $('.modal:visible').length);
        $(this).css('z-index', zIndex);
        setTimeout(function() {
            $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
        }, 0);

        var modal = $(this);
        var button = $(event.relatedTarget); // Button that triggered the modal

        // We get "id" from previous window (it should be an order id by design of this screen
        // and save it in hidden field of table modal form for further child forms
        var itemId = $(button).closest("form").find('input[type="hidden"][name="id"]').val();
        $(modal).find('form .modal-footer input[type="hidden"][name="parent_id"]').val(itemId); // Child form may need it

        $.ajax({
            url: $(modal).find('form').attr('action'),
            type: 'GET',
            data: {id: itemId},
            dataType: 'json',
            success: function(response) {
                var content = $(modal).find('.modal-body');
                if (response.status == 'success') {
                    content.empty();
                    $(response.table).appendTo(content);
                    initialize_checkboxes();
                } else {
                    add_alert('Internal server error, please contacts support', 'Error');
                };
            },
            error: function() {
                add_alert('Internal server error, please contacts support', 'Error');
            },
        });
    });
})
