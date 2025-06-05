document.addEventListener('DOMContentLoaded', function() {

    const paginationLinks = document.querySelectorAll('.pagination-link');
    const currentPageSpan = document.querySelector('.current-page');
    const totalPagesSpan = document.querySelector('.total-pages');
    
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const pageNumber = this.getAttribute('data-page');
            const currentUrl = new URL(window.location.href);
            
            currentUrl.searchParams.set('page', pageNumber);
            
            const categorySelect = document.querySelector('select[name="category"]');
            if (categorySelect && categorySelect.value) {
                currentUrl.searchParams.set('category', categorySelect.value);
            }
            
            window.location.href = currentUrl.toString();
        });
    });

    if (currentPageSpan && totalPagesSpan) {
        const urlParams = new URLSearchParams(window.location.search);
        const currentPage = urlParams.get('page') || '1';
        currentPageSpan.textContent = currentPage;
    }

    const categoryForm = document.querySelector('form[method="get"]');
    if (categoryForm) {
        categoryForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const categorySelect = this.querySelector('select[name="category"]');
            const currentUrl = new URL(window.location.href);
            
            if (categorySelect.value) {
                currentUrl.searchParams.set('category', categorySelect.value);
            } else {
                currentUrl.searchParams.delete('category');
            }
            
            currentUrl.searchParams.set('page', '1');
            
            window.location.href = currentUrl.toString();
        });
    }
}); 