$(document).ready(function(){
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
});

$(document).ready(function(){
    $('.modal form').on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type:'POST',
            data: $(this).serialize(),  // $(this).serializeObject(),
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrfcookie());
            },
            success:function(response){
                console.log(response);
                let result = response.status;
                if (result == 'success') {
                    $('.modal').each(function(){
                        $(this).modal('hide');
                    });
                    location.reload();
                } else {
                    console.log(response.errors)
                }
            },
            error:function(){
                console.log('something went wrong here');
            },
        });
    });
});

var csrfcookie = function() {
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