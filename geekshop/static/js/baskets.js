window.addEventListener("load", () => {

    $('.basket_list').on('click', 'input[type="number"]', (e) => {
        let t_href = e.target;

        $.ajax({
            url: '/baskets/edit/' + t_href.name + '/' + t_href.value + '/',
            success: (data) => {
                if (data) {
                    $('.basket_list').html(data.result);
                }
            },
        });

        e.preventDefault();
    });


    $(document).on('click', '.product_add', (e) => {

        let t_href = e.target;
        let csrf_token = $('meta[name="csrf-token"]').attr('content');

        let page_id = t_href.value;

        $.ajaxSetup({
            headers: {
                "X-CSRFToken": csrf_token
            }
        });

        $.ajax({
            type: 'POST',
            url: '/baskets/add/' + t_href.name + '/',
            data: {'page_id': page_id},
            success: (data) => {
                if (data) {
                    $('.product_items').html(data.result);
                }
            },
        });

        e.preventDefault();
    });

}, false);


