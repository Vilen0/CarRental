document.addEventListener('DOMContentLoaded', function () {
    const pricePerDay = parseFloat(document.getElementById('pricePerDayValue').value);
    const endInput = document.querySelector('input[name="end_date"]');
    const totalPriceInput = document.getElementById('totalPrice');

    // Получаем сегодняшнюю дату (без времени)
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // Устанавливаем минимально допустимую дату окончания — завтра
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    endInput.min = tomorrow.toISOString().split('T')[0];

    function calculateTotalPrice() {
        const endDate = new Date(endInput.value);
        endDate.setHours(0, 0, 0, 0); // сравниваем только даты без времени

        if (endDate > today) {
            const days = Math.ceil((endDate - today) / (1000 * 3600 * 24));
            const totalPrice = days * pricePerDay;
            totalPriceInput.value = totalPrice.toFixed(2) + ' ₽';
        } else {
            totalPriceInput.value = '';
        }
    }

    endInput.addEventListener('change', calculateTotalPrice);
});
