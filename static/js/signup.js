const checkbox = document.getElementById('consent-checkbox');
const submitBtn = document.querySelector('.btn');
checkbox.addEventListener('change', () => {
     submitBtn.disabled = !checkbox.checked;
});
