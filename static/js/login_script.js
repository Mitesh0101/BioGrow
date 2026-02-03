lucide.createIcons();

const tabLogin = document.getElementById("tab-login");
const tabRegister = document.getElementById("tab-register");
const formLogin = document.getElementById("form-login");
const formRegister = document.getElementById("form-register");

tabRegister.addEventListener("click", () => {
    tabRegister.classList.add("active-tab", "text-success");
    tabRegister.classList.remove("text-secondary");
    tabLogin.classList.remove("active-tab");
    tabLogin.classList.add("text-secondary");

    formLogin.classList.add("d-none");
    formRegister.classList.remove("d-none");

    lucide.createIcons();
});

tabLogin.addEventListener("click", () => {
    tabLogin.classList.add("active-tab");
    tabLogin.classList.remove("text-secondary");
    tabRegister.classList.remove("active-tab", "text-success");
    tabRegister.classList.add("text-secondary");

    formRegister.classList.add("d-none");
    formLogin.classList.remove("d-none");

    lucide.createIcons();
});


const regFullname = document.getElementById("reg-fullname");
const errFullname = document.getElementById("err-fullname");

const regEmail = document.getElementById("reg-email");
const errEmail = document.getElementById("err-email");

const regPassword = document.getElementById("reg-password");
const errPassword = document.getElementById("err-password");

const regConfirm = document.getElementById("reg-confirm");
const errConfirm = document.getElementById("err-confirm");

const regLocation = document.getElementById("reg-location");
const errLocation = document.getElementById("err-location");

const regDob = document.getElementById("reg-dob");
const errDob = document.getElementById("err-dob");

const regMobile = document.getElementById("reg-mobile");
const errMobile = document.getElementById("err-mobile");

const registerBtn = document.getElementById("registerBtn");



function validateFullname() {
    if (regFullname.value.trim().length < 3) {
        errFullname.classList.remove("d-none");
        return false;
    }
    errFullname.classList.add("d-none");
    return true;
}

const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
function validateEmail() {
    const email = regEmail.value.trim();

    if (email === "") {
        errEmail.classList.add("d-none");
        return false;
    }

    if (!emailRegex.test(email)) {
        errEmail.classList.remove("d-none");
        return false;
    }

    errEmail.classList.add("d-none");
    return true;
}

const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/;
function validatePassword() {
    const pwd = regPassword.value;

    if (pwd === "") {
        errPassword.classList.add("d-none");
        return false;
    }

    if (!passwordRegex.test(pwd)) {
        errPassword.classList.remove("d-none");
        return false;
    }

    errPassword.classList.add("d-none");
    return true;
}

function validateConfirmPassword() {
    if (regConfirm.value === "") {
        errConfirm.classList.add("d-none");
        return false;
    }

    if (regConfirm.value !== regPassword.value) {
        errConfirm.classList.remove("d-none");
        return false;
    }

    errConfirm.classList.add("d-none");
    return true;
}

function validateLocation() {
    if (regLocation.value === "") {
        errLocation.classList.add("d-none");
        return false;
    }

    if (regLocation.value.trim().length < 2) {
        errLocation.classList.remove("d-none");
        return false;
    }

    errLocation.classList.add("d-none");
    return true;
}

function validateDOB() {
    if (!regDob.value) {
        errDob.classList.add("d-none");
        return false;
    }

    const dob = new Date(regDob.value);
    const today = new Date();

    if (dob > today) {
        errDob.classList.remove("d-none");
        errDob.innerText = "Date of birth cannot be in future";
        return false;
    }

    let age = today.getFullYear() - dob.getFullYear();
    const m = today.getMonth() - dob.getMonth();

    if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
        age--;
    }

    if (age < 13) {
        errDob.classList.remove("d-none");
        return false;
    }

    errDob.classList.add("d-none");
    return true;
}

function validateMobile() {
    const mobile = regMobile.value.trim();

    if (mobile === "") {
        errMobile.classList.add("d-none");
        return false;
    }

    if (!/^[6-9]\d{9}$/.test(mobile)) {
        errMobile.classList.remove("d-none");
        return false;
    }

    errMobile.classList.add("d-none");
    return true;
}


function checkRegisterForm() {
    if (
        validateFullname() &&
        validateEmail() &&
        validatePassword() &&
        validateConfirmPassword() &&
        validateLocation() &&
        validateDOB() &&
        validateMobile()
    ) {
        registerBtn.disabled = false;
    } else {
        registerBtn.disabled = true;
    }
}
