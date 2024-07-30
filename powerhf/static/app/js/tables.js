

$("#btn-download-id").click(function () {
    let table = document.getElementById("table");
    TableToExcel.convert(table[0], {
        name: `energy_diesel_filling_download_data.xlsx`,
        sheet: {
            name: 'Diesel Filling'
        }
    });
});