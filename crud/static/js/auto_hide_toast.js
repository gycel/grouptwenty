setTimeout(() => {
    const successToastMessage = document.getElementById('toast-success')
    const warningToastMessage = document.getElementById('toast-warning')

    if(successToastMessage) {
        successToastMessage.style.display = 'none'
    }
    else {
        warningToastMessage.style.display = 'none'
    }
}, 3000)