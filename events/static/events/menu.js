document.addEventListener('DOMContentLoaded', () => {
    let menu_button = document.getElementById('menubutton');
    let menu_items = document.getElementsByClassName('menu-items')[0]
    menu_button.addEventListener('click', () => {
        menu_items.classList.toggle('active');
    })
});