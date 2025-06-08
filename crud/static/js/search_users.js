document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const usersTable = document.getElementById('usersTable');
    const tbody = document.getElementById('usersTbody');
    const rows = tbody.getElementsByTagName('tr');

    searchInput.addEventListener('keyup', function () {
        const searchTerm = this.value.toLowerCase();

        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            const cells = row.getElementsByTagName('td');
            let found = false;

            // Skip the last cell (Action column)
            for (let j = 0; j < cells.length - 1; j++) {
                const cellText = cells[j].textContent.toLowerCase();
                if (cellText.includes(searchTerm)) {
                    found = true;
                    break;
                }
            }

            row.style.display = found ? '' : 'none';
        }
    });
}); 