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

    // Transference - Product Quantity
    $(document).on("click", "#btn_search_product_quantity", function(e) {
        e.preventDefault();
        populate_product_list();        
    });

    function populate_product_list() {
        $('#product_list').html('');
        url = 'search_product_quantity';
        $.ajax({
            type : 'POST',
            url : url,
            data : {
                searched : $('#txt_search_product').val(),
                stock_id : 1,
                csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),
            },

            success : function(data){
                const jsonData = JSON.parse(data);


                const output = document.getElementById('product_list');
                output.classList.add("input-group");
                output.classList.add("mb-2");
                // Iterar sobre a lista de dicionários
                for (let i = 0; i < jsonData.length; i++) {
                    const item = jsonData[i];

                    const divItem = document.createElement('div');
                    divItem.classList.add("form-control");
                    divItem.classList.add("w-100");
                    const input = document.createElement('input');
                    input.value = item['id'];
                    input.classList.add('form-check-input');
                    input.style = 'margin-left: -5px;';
                    input.type = 'radio';
                    input.name = 'product-radio'

                    const label_name = document.createElement('label');
                    label_name.classList.add('w-75');
                    label_name.classList.add('p3');
                    label_name.textContent = item['name'];

                    const label_quantity = document.createElement('label');
                    label_quantity.classList.add('w-auto');
                    label_quantity.textContent = item['quantity'];


                    divItem.appendChild(input);
                    divItem.appendChild(label_name);
                    divItem.appendChild(label_quantity);

                    output.appendChild(divItem);
                }
            }
        });
    };
});