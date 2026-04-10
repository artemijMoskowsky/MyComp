const categorySelect = document.querySelector("#category-filter");
const priceSelect = document.querySelector("#price-filter");
const searchInput = document.querySelector("#search");
const url = new URL(window.location.href);

if (url.searchParams.has("category")){
    categorySelect.value = url.searchParams.get("category");
}

if (url.searchParams.has("price")){
    priceSelect.value = url.searchParams.get("price");
}

if (url.searchParams.has("search")){
    searchInput.value = url.searchParams.get("search");
}

categorySelect.addEventListener("change", (event) => {
    url.searchParams.set("category", event.target.value);
    window.location = url;
})

priceSelect.addEventListener("change", (event) => {
    url.searchParams.set("price", event.target.value);
    window.location = url;
})

document.querySelectorAll(".product").forEach(pr=>{
pr.addEventListener('click', ()=>{
    console.log(pr.getAttribute("value"))
    window.location.href = pr.getAttribute("value");
})
})

searchInput.addEventListener("change", (event) => {
    url.searchParams.set("search", event.target.value);
    window.location = url;
})