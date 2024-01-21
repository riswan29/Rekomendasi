let dropdown = document.querySelector('.dropdown');

dropdown.addEventListener('mouseover', function () {
    let dropdownMenu = dropdown.querySelector('.dropdown-menu');
    dropdownMenu.style.display = 'block';
});

dropdown.addEventListener('mouseout', function () {
    let dropdownMenu = dropdown.querySelector('.dropdown-menu');
    dropdownMenu.style.display = 'none';
});
