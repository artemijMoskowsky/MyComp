const selectedMeta = document.querySelector("meta[name='selected']");

if (selectedMeta){
    const pageElement = document.querySelector(`#${selectedMeta.content}`);

    if (pageElement) {
        pageElement.classList.add("selected");
    }
}
