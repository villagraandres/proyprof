function openModal() {
    document.getElementById('classModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('classModal').style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == document.getElementById('classModal')) {
        closeModal();
    }
}

document.getElementById('crearClase').addEventListener('click', function() {
    const className = document.getElementById('className').value;
    console.log(className)
    
    fetch(crearClaseUrl, {
        method: 'POST',
        body: JSON.stringify({
            name: className,
            user_id: usuarioId
        })
    })
    .then(response => {
        if (!response.ok) {
            console.log(response)
            throw new Error('Network response was not ok');
        }   
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        closeModal();
        window.location.reload(); 
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});