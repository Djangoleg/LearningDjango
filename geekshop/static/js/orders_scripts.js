window.addEventListener("load", () => {

    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;

    let quantity_arr = [];
    let price_arr = [];

    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());

    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_price = parseInt($('.order_total_cost').text().replace(',', '.')) || 0;

    for (let i = 0; i < total_forms; i++) {
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity').val());
        _price = parseInt($('.orderitems-' + i + '-price').text().replace(',', '.'));

        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }

    $('.order_form').on('click', 'input[type=number]', (e) => {
        let target = e.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummerUpdate(price_arr[orderitem_num], delta_quantity);
        }

        e.preventDefault();
    });

    $('.order_form').on('click', 'input[type=checkbox]', (e) => {
        let target = e.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            delta_quantity = quantity_arr[orderitem_num];
        }
        orderSummerUpdate(price_arr[orderitem_num], delta_quantity);

        e.preventDefault();
    });

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
    });

    $(document).on('change', '.order_form select', (e) => {
    // $('.order_form select').on('change', (e) => {
        let target = e.target;
        let orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));

        $('input[name=orderitems-' + orderitem_num + '-quantity').val(0);
        // Пересчитать.
        if (quantity_arr[orderitem_num] === undefined) {
            quantity_arr[orderitem_num] = 0;
        }
        if (price_arr[orderitem_num] === undefined) {
            price_arr[orderitem_num] = 0;
        }
        orderSummerUpdate(price_arr[orderitem_num], -quantity_arr[orderitem_num]);
        quantity_arr[orderitem_num] = 0;

        if (target.value) {
            $.ajax({
                url: '/orders/get_product_price/' + target.value + '/',
                success: (data) => {
                    if (data) {
                        // $('.orderitems-' + orderitem_num + '-price').text(data.price + ' руб');
                        let price_html = '<span class="orderitems-' + orderitem_num + '-price">' + data.price.toString().replace('.', ',') + '</span> руб';
                        let current_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                        current_tr.find('td:eq(2)').html(price_html);

                        price_arr[orderitem_num] = parseFloat(data.price);
                    }
                },
            });
        } else {
            price_arr.splice(orderitem_num, 1);
            quantity_arr.splice(orderitem_num, 1);
            $('.orderitems-' + orderitem_num + '-price').text('');
        }

        e.preventDefault();
    });

    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummerUpdate(price_arr[orderitem_num], delta_quantity);
    }


    function orderSummerUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;
        order_total_price = Number((order_total_price + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(order_total_price.toString() + ',00');
    }

}, false);
