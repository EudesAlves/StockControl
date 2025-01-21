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

    // Transference - Product Quantity //
    $(document).on("click", "#btn_search_product_quantity", function(e) {
        e.preventDefault();
        let stock_id = $('#stockOriginSelect option:selected').val();
        console.log(stock_id);
        if(stock_id <= 0) {
            $('#staticBackdrop').modal('hide');

            const div_error = document.getElementById('div_message_error');
            div_error.innerHTML = '';
            const span_error = document.createElement('span');
            span_error.classList.add('message_error');
            span_error.textContent = 'Selecione um Estoque de Origem';
            div_error.appendChild(span_error);
        }
        else {
            request_product_data(stock_id);
        }
        
    });
    
    function request_product_data(stock_id) {
        $('#tb_product_quantity').html('');
        url = 'search_product_quantity';
        $.ajax({
            type : 'POST',
            url : url,
            data : {
                searched : $('#txt_search_product').val(),
                stock_id : stock_id,
                csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),
            },

            success : function(data){
                const jsonData = JSON.parse(data);

                // Create Table for Product Data
                populate_product_list(jsonData);                
            }
        });
    }

    function populate_product_list(jsonData) {
        const table = document.getElementById('tb_product_quantity');
        const tbody = document.createElement('tbody');
        tbody.classList.add("w-100");

        // Iterar sobre a lista de dicionários
        for (let i = 0; i < jsonData.length; i++) {
            const item = jsonData[i];

            const row = document.createElement('tr');

            const col_id = document.createElement('td');
            col_id.classList.add('text-dark');
            col_id.textContent = item['id'];

            const col_name = document.createElement('td');
            col_name.classList.add('text-dark');
            col_name.classList.add('w-75');
            col_name.textContent = item['name'];

            const col_quantity = document.createElement('td');
            col_quantity.classList.add('text-dark');
            col_quantity.textContent = item['quantity'];
            
            row.appendChild(col_id);
            row.appendChild(col_name);
            row.appendChild(col_quantity);
            row.addEventListener("click", tb_product_row_click_event);

            tbody.appendChild(row);
        }
        table.appendChild(tbody);
        clear_product_temp_data();
    }

    function tb_product_row_click_event() {
        let rows = $('#tb_product_quantity > tbody > tr');
        // Clear tb Product rows background
        Array.from(rows).forEach(function(element) {
            element.classList.remove('bg-primary');
        });

        this.classList.add('bg-primary');
        let cells = this.cells;
        let product_id = cells[0].textContent;
        let product_name = cells[1].textContent;
        let product_quantity = cells[2].textContent;

        $('#temp_product_id').attr('value', product_id);
        $('#temp_product_name').attr('value', product_name);
        $('#temp_product_quantity').attr('value', product_quantity);
    }

    function clear_product_temp_data() { 
        $('#temp_product_id').attr('value', null);
        $('#temp_product_name').attr('value', null);
        $('#temp_product_quantity').attr('value', null);        
    }

    $(document).on("click", "#btn_add_product_quantity", function() {
        let temp_product_id = $('#temp_product_id').val();
        let temp_product_name = $('#temp_product_name').val();
        let temp_product_quantity = $('#temp_product_quantity').val();

        if(temp_product_id) {
            $('#id_choosed_product').attr('value', temp_product_id);
            $('#txt_choosed_product').attr('value', temp_product_name);
            $('#quantity_choosed_product').attr('value', temp_product_quantity);
            $('#staticBackdrop').modal('toggle');
        }
    });

    $('#stockOriginSelect').change(function() {
        clear_product_choosed_data()        
        clear_product_temp_data();
    });

    function clear_product_choosed_data() {
        $('#id_choosed_product').attr('value', null);
        $('#quantity_choosed_product').attr('value', null);
        $('#txt_choosed_product').attr('value', '');
        $('#tb_product_quantity').html('');
    }
});