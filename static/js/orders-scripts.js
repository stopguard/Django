'use strict';

let orderItemNum;
let orderItemQuantity;
let deltaQuantity;
let deltaCost;
let productPrices;
let quantityArr;
let priceArr;

let totalForms;
let orderTotalQuantity;
let orderTotalCost;

let $orderTotalQuantityDOM;
let $orderTotalCost;
let $orderForm;

function parseOrderForm() {
    quantityArr = [];
    priceArr = [];
    for (let i = 0; i < totalForms; i++) {
        const $quantity = document.querySelector(`input[name="items-${i}-count"]`);
        let quantity = parseInt($quantity.value);
        const $price = document.querySelector(`.item-${i}-price`);
        let price = parseFloat($price.textContent.replace(',', '.'));
        price = price ? price : 0;
        quantityArr.push(quantity);
        priceArr.push(price);
    }
}

function renderSummary() {
    $orderTotalQuantityDOM.textContent = orderTotalQuantity.toString();
    let totalCostStr = orderTotalCost.toFixed(2).toString();
    $orderTotalCost.textContent = totalCostStr.replace('.', ',');
}

function updateTotalQuantity() {
    orderTotalQuantity = 0;
    orderTotalCost = 0;
    quantityArr.forEach((el, idx) => {
        orderTotalQuantity += el;
        orderTotalCost += el * priceArr(idx);
    });
    renderSummary();
}

function orderSummaryUpdate(orderItemPrice) {
    orderTotalQuantity += deltaQuantity;
    deltaCost = orderItemPrice * deltaQuantity;
    orderTotalCost += deltaCost;
    renderSummary();
}

function deleteOrderItem(row) {
    let targetName = row[0].querySelector('input[type="number"]').name;
    orderItemNum = parseInt(targetName.match(/\d+/)[0]);
    let quantity = quantityArr[orderItemNum];
    deltaQuantity = -quantity;
    orderSummaryUpdate(quantity);
}

function getItemNumber(e) {
    return parseInt(e.target.name.match(/\d+/)[0]);
}

function onLoad() {
    console.log('DOM loaded');

    const $totalForms = document.querySelector('input[name="items-TOTAL_FORMS"]');
    totalForms = parseInt($totalForms.value);

    $orderTotalQuantityDOM = document.querySelector('.orderitems-total-count');
    orderTotalQuantity = parseInt($orderTotalQuantityDOM.textContent);

    $orderTotalCost = document.querySelector('.order-total-cost');
    let totalCostValue = $orderTotalCost.textContent;
    orderTotalCost = parseFloat(totalCostValue.replace(',', '.'));

    parseOrderForm();

    if (!orderTotalQuantity) {
        updateTotalQuantity();
    }

    $orderForm = document.querySelector('.order-form');
    $orderForm.addEventListener('change', function countSet(e) {
        let targetType = e.target.type;
        if (targetType === 'number') {
            orderItemNum = getItemNumber(e);
            let price = priceArr[orderItemNum];
            if (price) {
                orderItemQuantity = e.target.value;
                deltaQuantity = orderItemQuantity - quantityArr[orderItemNum];
                quantityArr[orderItemNum] = orderItemQuantity
                orderSummaryUpdate(price);
            }
        }
    });

    $('.formset-row').formset({
        addText: 'Добавить продукт',
        deleteText: 'Удалить',
        prefix: 'items',
        removed: deleteOrderItem
    });

}

window.onload = onLoad
