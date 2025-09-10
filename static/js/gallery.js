document.addEventListener('DOMContentLoaded', () => {
    const items = [...document.querySelectorAll('.ph-item img')];
    const lb = document.getElementById('lightbox');
    const lbImg = document.getElementById('lightbox-img');
    const lbCap = document.getElementById('lb-caption');
    const lbLeft = document.querySelector('.lb-left');
    const lbPrev = document.getElementById('lb-prev');
    const lbNext = document.getElementById('lb-next');

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

        pre.onload = () => {
            loaded = true;
            maybeSwap();
        };
        pre.onerror = () => {
            isAnimating = false;
        };
        pre.src = nextSrc;

        lbImg.classList.add('transition-out');

        const onFade = () => {
            lbImg.removeEventListener('transitionend', onFade);
            clearTimeout(fadeTimer);
            faded = true;
            maybeSwap();
        };
        lbImg.addEventListener('transitionend', onFade, { once: true });

        fadeTimer = setTimeout(() => {
            lbImg.removeEventListener('transitionend', onFade);
            faded = true;
            maybeSwap();
        }, FADE_MS + 60);

        function maybeSwap() {
            if (!loaded || !faded) return;

            lbCap.textContent = nextCap;
            lbLeft.textContent = nextDate;

            lbImg.onload = null;
            lbImg.src = nextSrc;

            requestAnimationFrame(() => {
                void lbImg.offsetWidth;
                lbImg.classList.remove('transition-out');  // плавный вход
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
        img.addEventListener('click', () => openLightbox(i));
    });

    lbPrev.addEventListener('click', showPrev);
    lbNext.addEventListener('click', showNext);

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

window.addEventListener('load', () => {
    document.getElementById('container').classList.add('ready');
});
