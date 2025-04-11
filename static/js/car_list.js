document.addEventListener('DOMContentLoaded', function() {
    // Для каждой карточки
    document.querySelectorAll('.card-body').forEach(function(cardBody) {
        const shortDescription = cardBody.querySelector('.short-description');
        const fullDescription = cardBody.querySelector('.full-description');
        const showMoreButton = cardBody.querySelector('.show-more');

        // Проверяем, если длина полного описания больше 100 символов
        if (fullDescription.textContent.length > 100) {
            showMoreButton.style.display = 'inline'; // Показываем кнопку "Показать целиком"
        }

        // Добавляем обработчик для кнопки
        showMoreButton.addEventListener('click', function() {
            // Переключаем между показом сокращенного и полного описания
            if (shortDescription.style.display === 'none') {
                shortDescription.style.display = 'inline';  // Показываем сокращенное описание
                fullDescription.style.display = 'none';    // Скрываем полное описание
                this.textContent = 'Показать целиком';      // Меняем текст кнопки
            } else {
                shortDescription.style.display = 'none';   // Скрываем сокращенное описание
                fullDescription.style.display = 'inline';  // Показываем полное описание
                this.textContent = 'Скрыть описание';      // Меняем текст кнопки
            }
        });
    });
});
