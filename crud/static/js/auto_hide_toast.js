setTimeout(() => {
    // Hide all success toasts
    document.querySelectorAll('[id^="toast-success"]').forEach(el => {
        el.style.display = 'none';
    });
    // Hide all warning toasts
    document.querySelectorAll('#toast-warning').forEach(el => {
        el.style.display = 'none';
    });
}, 3000);