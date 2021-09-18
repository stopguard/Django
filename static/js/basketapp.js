"use strict";

window.onload = function () {
    console.log('Window ready');
    $('input[type="number"]').on('change', function (event) {
        event.preventDefault();
        let quantity = event.target.value;
        let basketItemId = event.target.name.split('-')[1];
        $.ajax({
            url: `/basket/edit/${basketItemId}/${quantity}/`,
            success: function (data) {
                if (data.status) {
                    $('.basketapp-count').text(data.basket_count);
                    if (+data.item_count > 0) {
                        $(`.basketapp-sum-${basketItemId}`).text(data.item_cost);
                        $(`input[name='number-${basketItemId}']`).text(data.item_count);
                    } else {
                        $(`.basketapp-item-${basketItemId}`).remove();
                    }
                    if (+data.basket_cost > 0) {
                        $('.basketapp-total').text(data.basket_cost);
                    } else {
                        $('div.card-footer p').remove();
                        $('.btn-success').remove();
                        $('h4.float-right').text('Здесь пока ничего нет');
                    }
                }
            },
        });
    });
};
