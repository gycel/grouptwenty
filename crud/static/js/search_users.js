document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const usersTable = document.getElementById('usersTable');
    const tbody = document.getElementById('usersTbody');
    const rows = tbody.getElementsByTagName('tr');

    searchInput.addEventListener('keyup', function() {
        const searchTerm = this.value.toLowerCase();

        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            const nameCell = row.getElementsByTagName('td')[0]; 

            const nameText = nameCell ? nameCell.textContent.toLowerCase() : '';

            if (nameText.includes(searchTerm)) {
                row.style.display = ''; 
            } else {
                row.style.display = 'none'; 
            }
        }
    });
}); 