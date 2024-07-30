

document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');

    fileInput.addEventListener('change', function () {
        const files = fileInput.files;

        Array.from(files).forEach(file => {
            const listItem = document.createElement('div');
            listItem.classList.add('file-item');

            const fileName = document.createElement('div');
            fileName.classList.add('file-name');
            fileName.textContent = file.name;

            const deleteButton = document.createElement('button');
            deleteButton.classList.add('delete-button');
            deleteButton.textContent = 'Delete';
            deleteButton.addEventListener('click', function () {
                listItem.remove();
            });

            listItem.appendChild(fileName);
            listItem.appendChild(deleteButton);
            fileList.appendChild(listItem);
        });

        fileInput.value = ''; // Clear selected files from input
    });
});