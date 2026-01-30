// Initialize Icons 
lucide.createIcons();

// Select DOM Elements 
const tabLogin = document.getElementById('tab-login'); 
const tabRegister = document.getElementById('tab-register'); 
const formLogin = document.getElementById('form-login'); 
const formRegister = document.getElementById('form-register');

// Switch to Register Form 
tabRegister.addEventListener('click', () => { 
    // Update Button Styles 
    tabRegister.classList.add('active-tab', 'text-success'); 
    tabRegister.classList.remove('text-secondary');
    tabLogin.classList.remove('active-tab');
    tabLogin.classList.add('text-secondary');

    // Switch Forms with Animation
    formLogin.classList.add('d-none');
    formRegister.classList.remove('d-none');

    // Refresh icons just in case specific icons are only in one form
    lucide.createIcons();
});

// Switch to Login Form 
tabLogin.addEventListener('click', () => { 
    // Update Button Styles 
    tabLogin.classList.add('active-tab'); 
    tabLogin.classList.remove('text-secondary');
    tabRegister.classList.remove('active-tab', 'text-success');
    tabRegister.classList.add('text-secondary');

    // Switch Forms
    formRegister.classList.add('d-none');
    formLogin.classList.remove('d-none');

    lucide.createIcons();
});

// Prevent default form submission for demo purposes 
document.querySelectorAll('form').forEach(form => { 
    form.addEventListener('submit', (e) => { 
        e.preventDefault(); 
        const btn = form.querySelector('button[type="submit"]'); 
        const originalText = btn.innerHTML;
        // Show loading state
        btn.innerHTML = 'Processing...';
        btn.disabled = true;

        setTimeout(() => {
            alert('Form submitted successfully!');
            btn.innerHTML = originalText;
            btn.disabled = false;
            // Here you would typically redirect to dashboard or home
            window.location.href = 'index.html';
        }, 1500);
    });
});