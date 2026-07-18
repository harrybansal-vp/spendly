// Vanilla JS modal handling for the "See how it works" demo video
// Requirements:
//  - Open modal when the button with class .see-how is clicked
//  - Close modal when clicking the close button or outside the modal content
//  - Stop video playback when modal is closed

document.addEventListener('DOMContentLoaded', function () {
    const openBtn = document.querySelector('.see-how');
    const modalOverlay = document.getElementById('demo-modal');
    const closeBtn = document.getElementById('modal-close-btn');
    const iframe = document.getElementById('demo-video');
    // Preserve the original src to restore when reopening
    const originalSrc = iframe ? iframe.getAttribute('src') : '';

    if (!openBtn || !modalOverlay || !closeBtn || !iframe) {
        // If any element is missing, do nothing – fail silently
        return;
    }

    // Function to open modal
    function openModal(event) {
        event.preventDefault();
        modalOverlay.style.display = 'flex';
        // Restore src to ensure video loads (in case it was cleared)
        iframe.setAttribute('src', originalSrc);
    }

    // Function to close modal and stop video
    function closeModal() {
        modalOverlay.style.display = 'none';
        // Stop video by removing src attribute (or setting to empty)
        iframe.setAttribute('src', '');
    }

    openBtn.addEventListener('click', openModal);
    closeBtn.addEventListener('click', closeModal);

    // Clicking outside the modal content (on overlay) closes it
    modalOverlay.addEventListener('click', function (e) {
        if (e.target === modalOverlay) {
            closeModal();
        }
    });
});