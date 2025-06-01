document.addEventListener('DOMContentLoaded', () =>{
    const checkboxElement = document.querySelectorAll('input[type="checkbox"].show-element');

    checkboxElement.forEach(checkbox => {
        const forWhatElements = checkbox.dataset.forWhatElements;

        checkbox.addEventListener('change', () => {
            const hiddenElements = document.querySelectorAll(`.${forWhatElements}`);

            hiddenElements.forEach(element => {
                element.classList.toggle(`${forWhatElements}-showed`);
            });
        });
    });
});