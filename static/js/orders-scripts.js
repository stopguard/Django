'use strict';

let orderItemNum, orderItemQuantity, deltaQuantity, deltaCost;
let productPrices, quantityArr, priceArr;

let totalForms, orderTotalQuantity, orderTotalCost;

let $orderTotalQuantityDOM, $orderTotalCost, $orderForm;

let API_PATH = '/products/price/'

function parseOrderForm() {
    quantityArr = [];
    priceArr = [];
    for (let i = 0; i < totalForms; i++) {
        const $quantity = document.querySelector(`input[name="items-${i}-count"]`);
        let quantity = parseInt($quantity.value);
        const $row = $quantity.parentNode.parentNode
        const $price = $row.querySelector('span.item-price');
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
        orderTotalCost += el * priceArr[idx];
    });
    renderSummary();
}

function orderCountUpdate(orderItemPrice) {
    orderTotalQuantity += deltaQuantity;
    deltaCost = orderItemPrice * deltaQuantity;
    orderTotalCost += deltaCost;
    renderSummary();
}

function deleteOrderItem(row) {
    let targetName = row[0].querySelector('input[type="number"]').name;
    orderItemNum = numExtractor(targetName);
    let quantity = quantityArr[orderItemNum];
    deltaQuantity = -quantity;
    orderCountUpdate(priceArr[orderItemNum]);
}

function getItemNumber(e) {
    return numExtractor(e.target.name);
}

function numExtractor(str) {
    return parseInt(str.match(/\d+/)[0]);
}

function onCountCorrection(e) {
    orderItemNum = getItemNumber(e);
    let price = priceArr[orderItemNum];
    if (price) {
        orderItemQuantity = e.target.value;
        deltaQuantity = orderItemQuantity - quantityArr[orderItemNum];
        quantityArr[orderItemNum] = orderItemQuantity
        orderCountUpdate(price);
    }
}

function onSelectChange(e) {
    let target = e.target;
    let product_id = target.value;
    let itemNumber = getItemNumber(e);
    fetch(`${API_PATH}${product_id}/`,
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
                "X-Requested-With": "XMLHttpRequest",
            },
        })
        .then((response) => {
            return response.json();
        })
        .then((request) => {
            let $row = target.parentNode.parentNode
            let $itemPrice = $row.querySelector('span.item-price');
            let newPrice = request.price || '0';
            newPrice = isNaN(newPrice) ? '0' : newPrice;
            $itemPrice.textContent = newPrice.replace('.', ',');
            newPrice = parseFloat(newPrice)
            let oldPrice = priceArr[itemNumber];
            let count = quantityArr[itemNumber];
            deltaCost = newPrice * count - oldPrice * count;
            orderTotalCost += deltaCost;
            priceArr[itemNumber] = newPrice;
            renderSummary();
        });
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
        if (e.target.type === 'number') {
            onCountCorrection(e);
        } else if (e.target.tagName === 'SELECT') {
            onSelectChange(e);
        }
    });

    $('.formset-row').formset({
        addText: 'Добавить продукт',
        deleteText: 'Удалить',
        prefix: 'items',
        removed: deleteOrderItem
    });

    let $addButton = document.querySelector('a.add-row');
    $addButton.addEventListener('click', () => {
        quantityArr.push(0);
        priceArr.push(0);
    })

}

window.onload = onLoad
