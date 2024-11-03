// Select all star icons within the modal body
let reviewStars;
document.addEventListener('DOMContentLoaded', () => {
    reviewStars = document.querySelectorAll('.modal-body i.fa-star, .modal-body i.fa-star-half-alt');

    reviewStars.forEach((star, index) => {
        // Add hover event listener

        star.addEventListener('mouseenter', () => {
            highlightStars(index);
        });

        // Remove highlight when mouse leaves
        star.addEventListener('mouseleave', resetStars);
    });
})

// Function to highlight stars up to the hovered index
function highlightStars(index) {

    reviewStars.forEach((star, i) => {
        if (i <= index) {
            star.classList.remove('far');
            star.classList.add('fas');  // Add a highlight class for styling
        } else {
            star.classList.remove('fas');
            star.classList.add('far'); // Remove highlight for stars beyond the hovered one
        }


    });
}

// Function to reset the stars (removes all highlights)
function resetStars() {
    reviewStars.forEach(star => {
        // star.classList.remove('far');
        // star.classList.add('fas'); // Remove highlight for stars beyond the hovered one
    });
}