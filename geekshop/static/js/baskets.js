window.onload = () => {

    $('.basket_list').on('click', 'input[type="number"]', (e) => {
        let t_href = e.target;

        $.ajax({
            url: '../../baskets/edit/' + t_href.name + '/' + t_href.value + '/',
            success: (data) => {
                if (data) {
                    $('.basket_list').html(data.result);
                }
            },
        });

        e.preventDefault();
    });
}