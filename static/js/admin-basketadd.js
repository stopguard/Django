"use strict";

console.log('Window ready');
$('.adminapp-load-products').on('click', function (event) {
    event.preventDefault();
    let buttonName = event.target.textContent;
    if (buttonName === 'Добавить товары') {
        $.ajax({
            url: '/auth/admin/users/profile/show_products/',
            success: function (data) {
                if (data.status) {
                    $('.adminapp-basket-add').html(data.products_all_html);
                    $('.adminapp-load-products').text('Скрыть товары');
                    $('.adminapp-add-to-basket').on('click', addToBasket);
                }
            },
        });
    } else {
        $('.adminapp-add-to-basket').off('click');
        $('.adminapp-basket-add').html('');
        $('.adminapp-load-products').text('Добавить товары');
    }
});

function addToBasket(event) {
    event.preventDefault();
    console.log(`event=`)
    console.log(event)
    let productId = event.target.id;
    let userId = $('.adminapp-basket-add')[0].id
    console.log(`/basket/add/${productId}/${userId}/`)
    $.ajax({
        url: `/basket/add/${productId}/${userId}/`,
        success: function (data) {
            console.log(`data=`)
            console.log(data)
            if (data.status) {
                $('input[type="number"]').off('change')
                $('.basketapp-count').text(data.basket_count);
                $('.basketapp').html(data.basket);
                basketEdit()
            }
        },
    });
}
