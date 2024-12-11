$(document).ready(function() {
    $(document).on("click", "#btn_search_product", function(e) {
        e.preventDefault();
        $('#product_list').html('');
        url = 'search_product';
        $.ajax({
            type : 'POST',
            url : url,
            data : {
                searched : $('#txt_search_product').val(),
                csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),
            },

            success : function(data){
                let options = ''
                for (let key in data) {
                    let product_option = '<option value="' +key+ '">' + data[key] + '</option>';
                    options = options + product_option
                    $('#product_list').html(options);
                }
            }
        });
    });

    $(document).on("click", "#btn_add_product", function() {
        let product_option = $('#product_list option:selected');

        if(product_option.text()) {
            $('#id_choosed_product').attr('value', product_option.val());
            $('#txt_choosed_product').attr('value', product_option.text());
            $('#staticBackdrop').modal('toggle');
        }
    });
});