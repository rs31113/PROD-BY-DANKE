document.addEventListener("DOMContentLoaded", function () {
    // Берём сам контейнер с текстом оферты
    const source = document.querySelector(".container");
    if (!source) {
        console.warn("terms.js: .container not found");
        return;
    }

    // Забираем чистый текст без тегов
    let text = source.innerText || source.textContent || "";
    text = text.trim();

    if (!text) {
        console.warn("terms.js: no text found in .container");
        return;
    }

    // Разбиваем на строки по переносам
    const lines = text.split(/\r?\n/).map(line => line.trim()).filter(line => line.length > 0);

    if (lines.length === 0) {
        console.warn("terms.js: no non-empty lines after split");
        return;
    }

    // Очищаем контейнер и создаём анимируемые строки
    source.innerHTML = lines.map(line => `<div class="offer-line">${line}</div>`).join("");

    // Запускаем анимацию "лестницей"
    const elems = source.querySelectorAll(".offer-line");
    elems.forEach((el, idx) => {
        setTimeout(() => {
            el.classList.add("visible");
        }, idx * 200);
    });

    console.log(`terms.js: animated ${elems.length} lines`);
});
