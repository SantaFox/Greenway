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
                    location.reload();
                } else {
                    if (response.message) {
                        add_alert(response.message.text, response.message.level);
                    }
                    console.log(response.errors)
                }
            },
            error:function(){
                console.log('something went wrong here');
            },
        });
    });
});

/*
    Обработчик добавления или редактирования объекта из строки в основной таблице страницы.
    Если у кнопки, вызвавшей обработчик, прописан data-id, то это редактирование указанного объекта (так оформлены
    кнопки в таблице); если не прописан - то это добавление (кнопка в шапке).
    Если это редактирование, то запрашивается список нужных полей для редактирования (так как в таблице могут быть
    не все) через AJAX по адресу, указанному в параметрах формы. Дальше все поля формы заполняются из полученных
    с сервера данных. Для positionsCount и paymentsCount специальные обработчики, указывающие количество
    строк в соответствующих подтаблицах.
    Если это добавление, то используются пустые поля.
*/
$(document).ready(function() {
    $('.editModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var modal = $(this)
        if (typeof button.data('id') !== 'undefined') {
            $(modal).find('.modal-footer input[name="action"]').val('edit');
            var itemId = button.data('id') // Extract info from data-* attributes
            $.ajax({
                url: $(modal).find('form').attr('action'),
                type: 'GET',
                data: {id: itemId},
                dataType: 'json',
                success: function(response) {
                    for (var i in response) {
                        if (i == 'positions_count') {
                            button = $(modal).find('#positionsCount');
                            button.text('('+response[i]+')');
                        } else if (i == 'payments_count') {
                            button = $(modal).find('#paymentsCount');
                            button.text('('+response[i]+')');
                        } else {
                            formElement = $(modal).find('.modal-body [name="' + i + '"],.modal-footer [name="' + i + '"]');
                            if (formElement.attr('type') == 'checkbox'){
                                formElement.prop('checked', response[i]);
                            } else {
                                formElement.val(response[i]);
                            }
                        }
                    }
                },
                error: function() {
                    console.log('something went wrong here');
                },
            });
        } else {
            // TODO: We can ask application to prepare form with some initial values
            $(modal).find('.modal-footer input[name="action"]').val('add');
            $(modal).find('.modal-body input[type="text"]').val('');
            $(modal).find('.modal-body input[type="number"]').val('');
            $(modal).find('.modal-body input[type="checkbox"]').prop('checked', false);
            $(modal).find('.modal-body textarea').val('');
            $(modal).find('.modal-body select').val('');
        };
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
                console.log('something went wrong here');
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
        var button = $(event.relatedTarget); // Button that triggered the modal
        var header = button.data('modal-title');
        var action = button.data('modal-action');
        var itemId = $(button).closest("form").find('input[type="hidden"][name="id"]').val();

        var modal = $(this);
        $(modal).find('form').attr('action', action);
        $(modal).find('form .modal-header h4').text(header);
        $(modal).find('form .modal-footer input[type="hidden"][name="parentId"]').val(itemId); // Child form may need it
        $.ajax({
            url: $(modal).find('form').attr('action'),
            type: 'GET',
            data: {id: itemId},
            dataType: 'json',
            success: function(response) {
                var content = $(modal).find('.modal-body');
                if (response.status == 'ok') {
                    content.empty();
                    $(response.table).appendTo(content);
                    initialize_checkboxes();
                } else {
                    console.log('something went wrong here');
                };
            },
            error: function() {
                console.log('something went wrong here');
            },
        });
    });
})

$(document).ready(function() {
    $('#formModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var header = button.data('modal-title');
        var action = button.data('modal-action');
        var itemId = $(button).closest("form").find('input[type="hidden"][name="id"]').val();
        var parentId = $(button).closest("form").find('input[type="hidden"][name="parentId"]').val();
        //var parentId = 175

        var modal = $(this);
        $(modal).find('form').attr('action', action);
        $(modal).find('form .modal-header h4').text(header);
        $.ajax({
            url: $(modal).find('form').attr('action'),
            type: 'GET',
            data: {id: itemId, parent_id:parentId},
            dataType: 'json',
            success: function(response) {
                var content = $(modal).find('.modal-body');
                if (response.status == 'ok') {
                    content.empty();
                    $(response.form).appendTo(content);
                    $(modal).find('input[type="hidden"][name="action"]').val(response.hidden.action)
                    $(modal).find('input[type="hidden"][name="parentId"]').val(response.hidden.parent)
                } else {
                    console.log('something went wrong here');
                };
            },
            error: function() {
                console.log('something went wrong here');
            },
        });
    });
})
