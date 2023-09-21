// const togglePassword = document.querySelector('#togglePassword');
// const toggleCPassword = document.querySelector('#toggleCPassword');
// const password = document.querySelector('#password');
// const cpassword = document.querySelector('#cPassword');

// togglePassword.addEventListener('click', function (e) {
//     // toggle the type attribute
//     const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
//     password.setAttribute('type', type);
//     // toggle the eye slash icon
//     this.classList.toggle('bxs-show');
// });

// toggleCPassword.addEventListener('click', function (e) {
//     // toggle the type attribute
//     const type = cpassword.getAttribute('type') === 'password' ? 'text' : 'password';
//     cpassword.setAttribute('type', type);
//     // toggle the eye slash icon
//     this.classList.toggle('bxs-show');
// });

//Hide and Show User Pwd 
function togglePasswordVisibility(targetId) {
    const passwordInput = document.querySelector(`#${targetId}`);
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);

    const icon = document.querySelector(`[data-target="${targetId}"]`);
    icon.classList.toggle('fa-eye');
    icon.classList.toggle('fa-eye-slash');
}

const togglePasswordIcons = document.querySelectorAll('.toggle-password');

togglePasswordIcons.forEach(icon => {
    icon.addEventListener('click', function (e) {
        const targetId = this.getAttribute('data-target');
        togglePasswordVisibility(targetId);
    });
});

// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
    'use strict';

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation');

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms).forEach((form) => {
        form.addEventListener('submit', (event) => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
})();

