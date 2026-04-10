document.querySelectorAll(".product").forEach(pr=>{
pr.addEventListener('click', ()=>{
    console.log(pr.getAttribute("value"))
    window.location.href = pr.getAttribute("value");
})
})