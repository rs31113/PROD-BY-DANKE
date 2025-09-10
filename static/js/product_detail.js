const carousel = document.getElementById('productCarousel');
let maxQuantity = 1;
const carouselItems = carousel.getElementsByClassName('carousel-item');
let currentSlideIndex = 0;

const thumbnails = Array.from(document.querySelectorAll('.thumbnail'));
function updateThumbActive(index) {
    thumbnails.forEach((t, i) => {
        if (i === index) {
            t.classList.add('thumb-active');
        } else {
            t.classList.remove('thumb-active');
        }
    });
}

function changeCarouselSlide(index) {
    if (index === currentSlideIndex) return;
    carouselItems[currentSlideIndex].classList.remove('active');
    currentSlideIndex = index;
    carouselItems[currentSlideIndex].classList.add('active');
    updateThumbActive(currentSlideIndex);
}

function nextSlide() {
    let nextIndex = currentSlideIndex + 1;
    if (nextIndex >= carouselItems.length) nextIndex = 0;
    changeCarouselSlide(nextIndex);
}

function prevSlide() {
    let prevIndex = currentSlideIndex - 1;
    if (prevIndex < 0) prevIndex = carouselItems.length - 1;
    changeCarouselSlide(prevIndex);
}

/* клики по превью */
thumbnails.forEach((thumbnail, index) => {
    thumbnail.addEventListener('click', () => changeCarouselSlide(index));
});

document.addEventListener('DOMContentLoaded', () => {
    const items = [...document.querySelectorAll('#productCarousel .carousel-item img')];
    const lb = document.getElementById('lightbox');
    const lbImg = document.getElementById('lightbox-img');
    const lbCap = document.getElementById('lb-caption');
    const lbLeft = document.querySelector('.lb-left');
    const lbPrevBtn = document.getElementById('lb-prev');
    const lbNextBtn = document.getElementById('lb-next');

    let currentIndex = -1;
    let isAnimating = false;
    const FADE_MS = 320;

    function openLightbox(index) {
        currentIndex = index;
        const img = items[index];

        isAnimating = false;
        lbImg.classList.remove('transition-out');
        lbImg.onload = null;

        lbImg.src = img.src;
        lbCap.textContent = img.dataset.caption || "";
        lbLeft.textContent = img.dataset.date || "";

        const reveal = () => {
            lb.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
            document.body.classList.add('lightbox-open');
        };
        if (lbImg.complete) reveal();
        else lbImg.onload = reveal;
    }

    function closeLightbox() {
        lb.classList.add('hidden');
        lbImg.src = "";
        lbCap.textContent = "";
        currentIndex = -1;
        isAnimating = false;
        document.body.style.overflow = '';
        document.body.classList.remove('lightbox-open');
    }

    function switchTo(newIndex) {
        if (isAnimating || newIndex === currentIndex || lb.classList.contains('hidden')) return;
        isAnimating = true;

        const target = items[newIndex];
        const nextSrc = target.src;
        const nextCap = target.dataset.caption || "";
        const nextDate = target.dataset.date || "";

        const pre = new Image();
        let loaded = false;
        let faded = false;
        let fadeTimer;

        pre.onload = () => { loaded = true; maybeSwap(); };
        pre.onerror = () => { isAnimating = false; };
        pre.src = nextSrc;

        lbImg.classList.add('transition-out');

        const onFade = () => {
            lbImg.removeEventListener('transitionend', onFade);
            clearTimeout(fadeTimer);
            faded = true; maybeSwap();
        };
        lbImg.addEventListener('transitionend', onFade, { once: true });

        fadeTimer = setTimeout(() => {
            lbImg.removeEventListener('transitionend', onFade);
            faded = true; maybeSwap();
        }, FADE_MS + 60);

        function maybeSwap() {
            if (!loaded || !faded) return;

            lbCap.textContent = nextCap;
            lbLeft.textContent = nextDate;

            lbImg.onload = null;
            lbImg.src = nextSrc;

            requestAnimationFrame(() => {
                void lbImg.offsetWidth;
                lbImg.classList.remove('transition-out');
                currentIndex = newIndex;

                lbImg.addEventListener('transitionend', () => {
                    isAnimating = false;
                }, { once: true });

                setTimeout(() => { isAnimating = false; }, FADE_MS + 80);
            });
        }
    }

    function showPrev() {
        const newIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
        switchTo(newIndex);
    }

    function showNext() {
        const newIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
        switchTo(newIndex);
    }

    items.forEach((img, i) => {
        img.style.cursor = 'zoom-in';
        img.addEventListener('click', () => openLightbox(i));
    });

    lbPrevBtn.addEventListener('click', showPrev);
    lbNextBtn.addEventListener('click', showNext);

    lb.addEventListener('click', (e) => {
        if (e.target === lb) closeLightbox();
    });

    document.addEventListener('keydown', (e) => {
        if (lb.classList.contains('hidden')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') showPrev();
        if (e.key === 'ArrowRight') showNext();
    });

    window.closeLightboxFromHeader = function () {
        if (!lb.classList.contains('hidden')) closeLightbox();
    };
});

function selectSize(option) {
    let options = document.querySelectorAll('.size-option');
    options.forEach(function(item) {
        item.classList.remove('selected');
    });

    option.classList.add('selected');

    document.getElementById('selected-size').value = option.textContent;

    document.querySelector('.quantity-input').value = 1;
    document.querySelector('.quantity-display').textContent = 1;
    maxQuantity = parseInt(option.getAttribute('data-quantity'));

    const decreaseButton = document.querySelector('.decrease-quantity');
    const increaseButton = document.querySelector('.increase-quantity');

    decreaseButton.disabled = (1 <= 1);
    increaseButton.disabled = (1 >= maxQuantity);
}

const decreaseButton = document.querySelector('.decrease-quantity');
const increaseButton = document.querySelector('.increase-quantity');
const quantityDisplay = document.querySelector('.quantity-display');
const quantityInput = document.querySelector('.quantity-input');

function updateQuantity(newQuantity) {
    if (newQuantity < 1) newQuantity = 1;
    else if (newQuantity > maxQuantity) newQuantity = maxQuantity;

    quantityDisplay.textContent = newQuantity;
    quantityInput.value = newQuantity;

    increaseButton.disabled = (newQuantity >= maxQuantity);
    decreaseButton.disabled = (newQuantity <= 1);
}

decreaseButton.addEventListener('click', () => {
    let currentQuantity = parseInt(quantityDisplay.textContent, 10);
    if (currentQuantity > 1) updateQuantity(currentQuantity - 1);
});

increaseButton.addEventListener('click', () => {
    let currentQuantity = parseInt(quantityDisplay.textContent, 10);
    if (currentQuantity < maxQuantity) updateQuantity(currentQuantity + 1);
});

document.addEventListener('DOMContentLoaded', function() {
    const sizeOptions = document.querySelectorAll('.size-option');
    for (let i = 0; i < sizeOptions.length; i++) {
        const option = sizeOptions[i];
        if (!option.classList.contains('disabled')) {
            selectSize(option);
            option.classList.add('selected');
            document.getElementById('selected-size').value = option.textContent;
            break;
        }
    }

    updateThumbActive(0);
});

const notification = document.getElementById("notification");
if (notification) {
    setTimeout(() => { notification.classList.add('show-notification'); }, 100);
    setTimeout(() => { notification.classList.remove('show-notification'); }, 5000);
}
