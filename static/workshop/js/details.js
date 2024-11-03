let currentFocusedElement;
let possibleImages;

function getFocusedElement() {
    currentFocusedElement = document.getElementById('focused-image');
    return currentFocusedElement;
}

function addClickEventListenerToImages() {
    possibleImages = document.querySelectorAll('#thumbnailCarousel .img-thumbnail.rounded.img-fluid')
    console.log(possibleImages)
    for (const i of possibleImages) {
        i.addEventListener('click', (event) => {
            const clickedImg = i.getAttribute('src');
            const currentImg = currentFocusedElement.getAttribute('src');

            currentFocusedElement.setAttribute('src', clickedImg);
            i.setAttribute('src', currentImg);

        });
    }

}

document.addEventListener('DOMContentLoaded', addClickEventListenerToImages)
document.addEventListener('DOMContentLoaded', getFocusedElement);
