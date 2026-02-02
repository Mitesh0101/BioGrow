lucide.createIcons();

const tabLogin = document.getElementById('tab-login');
const tabRegister = document.getElementById('tab-register');
const formLogin = document.getElementById('form-login');
const formRegister = document.getElementById('form-register');

tabRegister.addEventListener('click', () => {
    tabRegister.classList.add('active-tab', 'text-success');
    tabRegister.classList.remove('text-secondary');
    tabLogin.classList.remove('active-tab');
    tabLogin.classList.add('text-secondary');

    formLogin.classList.add('d-none');
    formRegister.classList.remove('d-none');

    lucide.createIcons();
});

tabLogin.addEventListener('click', () => {
    tabLogin.classList.add('active-tab');
    tabLogin.classList.remove('text-secondary');
    tabRegister.classList.remove('active-tab', 'text-success');
    tabRegister.classList.add('text-secondary');

    formRegister.classList.add('d-none');
    formLogin.classList.remove('d-none');

    lucide.createIcons();
});
