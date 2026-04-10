// thumbs -> main image
if (document.querySelectorAll(".thumb").length){
    document.getElementById('mainImage').src = document.querySelectorAll(".thumb")[0].dataset.full;
    document.querySelectorAll(".thumb")[0].classList.add("active");
}

document.querySelectorAll('.thumb').forEach(t=>{
t.addEventListener('click', ()=> {
    document.querySelectorAll('.thumb').forEach(x=>x.classList.remove('active'));
    t.classList.add('active');
    document.getElementById('mainImage').src = t.dataset.full;
});
});

// tabs
document.querySelectorAll('.tab-btn').forEach(btn=>{
btn.addEventListener('click', ()=>{
    document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    const tab = btn.dataset.tab;
    document.querySelectorAll('[data-panel]').forEach(p=>p.style.display = p.dataset.panel===tab ? 'block' : 'none');
});
});

// add to cart simple feedback
const btn = document.getElementById('addCart');
btn.addEventListener('click', ()=>{
    let xhr = new XMLHttpRequest();
    xhr.open("post", btn.getAttribute("value"));
    xhr.onload = ()=>{
        if (xhr.status == 200 && xhr.readyState == 4) {
            btn.textContent = 'Додано ✓';
            btn.style.opacity = '0.9';
        }
    }
    xhr.send();
    setTimeout(()=>{ btn.textContent = 'Добавити до кошику'; btn.style.opacity = '1'}, 1500);
});

document.querySelectorAll('.card').forEach(card=>{
card.addEventListener('click', ()=>{
    window.location.href = card.getAttribute("value");
});
});