
class Product {
    constructor(id, count, maxCount, price, basketId) {
        this.id = id;
        this.count = count;
        this.maxCount = maxCount;
        this.price = price;
        this.basketId = basketId;
    }
    changeCount(count) {
        if (this.count + count > this.maxCount) {
            return this.maxCount;
        } else if (this.count + count <= 0) {
            return 1;
        } else {
            this.count += count;
            return this.count;
        }
    }
}

const productsArray = [];

function addProduct(id, count, maxCount, price, basketId) {
    productsArray.push(new Product(id, count, maxCount, price, basketId));
}

function getTotalPrice(){
    let price = 0;
    for (let product of productsArray) {
        price += product.price * product.count;
    }
    return price;
}

function getTotalCount(){
    let count = 0;
    for (let product of productsArray) {
        count += product.count;
    }
    return count;
}

function changeCount(id, count) {
    for (let product of productsArray) {
        if (product.id == id) {
            return product.changeCount(count);
        }
    }
}

function changeCountElement(element, id, count) {
    let elem = element.parentNode.querySelector(".count");
    elem.textContent = changeCount(id, count);
    let totalPriceElem = document.querySelector(".total-price-p");
    totalPriceElem.textContent = `${getTotalPrice()}$`;
    let ordersCountElem = document.querySelector(".orders-count");
    ordersCountElem.textContent = `${getTotalCount()} товари на суму`
}

function deleteProduct(element, id) {
    for (let i = 0; i < productsArray.length; i++) {
        if (productsArray[i].basketId == id) {
            let xhr = new XMLHttpRequest();
            xhr.open('post', `${window.location.href}delete/${id}`);
            xhr.onload = () => {
                console.log(xhr.status)
                if (xhr.status == 200 && xhr.readyState == 4){
                    productsArray.splice(i, 1);
                    element.parentNode.parentNode.parentNode.parentNode.removeChild(element.parentNode.parentNode.parentNode);
                    let totalPriceElem = document.querySelector(".total-price-p");
                    totalPriceElem.textContent = `${getTotalPrice()}$`;
                    let ordersCountElem = document.querySelector(".orders-count");
                    ordersCountElem.textContent = `${getTotalCount()} товари на суму`
                }
            }
            xhr.send();
        }
    }
}

function placeOrder() {
    let xhr = new XMLHttpRequest();
    xhr.open("post", window.location.href);
    xhr.onload = () => {
        if (xhr.status == 200 && xhr.readyState == 4) {
            window.location.href = xhr.responseText;
        }
    }
    const formData = new FormData();
    productsArray.forEach((item, index) => {
        formData.append(`products[${index}]`, JSON.stringify(item));
    });
    xhr.send(formData);
}