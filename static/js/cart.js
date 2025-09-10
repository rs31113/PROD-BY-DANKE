document.addEventListener("DOMContentLoaded", function() {
    var deliveryRadios = document.querySelectorAll('input[type="radio"][name="delivery"]');

    function updateTotalPrice() {
        var selectedDeliveryPrice = 0;
        var selectedDeliveryLabel = document.querySelector('input[type="radio"][name="delivery"]:checked + label');
        if (selectedDeliveryLabel) {
            var selectedDeliveryName = selectedDeliveryLabel.textContent.trim();
            selectedDeliveryPrice = parseFloat(selectedDeliveryName.split('-')[1]);
        }

        var basePrice = parseFloat(document.getElementById('total-price').getAttribute('data-base-price'));
        var totalPrice = basePrice + selectedDeliveryPrice;
        document.getElementById('total-price').textContent = Math.round(totalPrice);
    }

    deliveryRadios.forEach(function(radio) {
        radio.addEventListener("change", function() {
            updateTotalPrice();
        });
    });
    updateTotalPrice();
});


function redirectToProductPage(article) {
    window.location.href = "/shop/" + article + "/";
}
