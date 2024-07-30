
function Download_DFR() {
    let table = document.getElementsByClassName("hidden-table");
    TableToExcel.convert(table[0], {
        name: `energy_diesel_filling_download_data.xlsx`,
        sheet: {
            name: 'Diesel Filling'
        }
    });
}

