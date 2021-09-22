"use strict";

window.onload = function () {
    console.log('Window ready');
    $('.add-to-basket').on('click', function (event) {
        let productId = event.target.id;
        const isAuthorised = $('.userprofile').length != 0;
        if (isAuthorised) {
            event.preventDefault();
            const link = `/basket/add/${productId}/0/`;
            $.ajax({
                url: link,
                // success: function (data) {
                //     if (data.status) {
                //     }
                // },
            });
        }
    });
};
