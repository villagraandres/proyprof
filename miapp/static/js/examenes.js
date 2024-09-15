document.addEventListener("DOMContentLoaded", function() {
    const numQuestionsInput = document.getElementById('numQuestions');
    const createExamForm = document.getElementById('createExamForm');
    const questionContainer = document.getElementById('questionContainer');

    // Escuchar cuando se cambia la cantidad de preguntas
    numQuestionsInput.addEventListener('input', function() {
        // Elimina los bloques de preguntas anteriores, si los hay
        clearPreviousQuestions();

        // Generar los bloques de respuestas correctas dinámicamente
        const numQuestions = parseInt(numQuestionsInput.value);
        for (let i = 1; i <= numQuestions; i++) {
            createAnswerBlock(i);
        }
    });

    // Función para crear un bloque de respuesta correcta
    function createAnswerBlock(questionNum) {
        // Crear un nuevo div contenedor para la respuesta
        const newAnswerBlock = document.createElement('div');
        newAnswerBlock.classList.add('answer-block');

        // Etiqueta para la respuesta correcta
        const correctAnswerLabel = document.createElement('label');
        correctAnswerLabel.setAttribute('for', `correctAnswer${questionNum}`);
        correctAnswerLabel.textContent = `Respuesta Correcta ${questionNum}:`;
        newAnswerBlock.appendChild(correctAnswerLabel);

        // Input para la respuesta correcta
        const correctAnswerInput = document.createElement('input');
        correctAnswerInput.type = 'text';
        correctAnswerInput.id = `correctAnswer${questionNum}`;
        correctAnswerInput.name = `correctAnswer${questionNum}`;
        correctAnswerInput.placeholder = 'Escribe la respuesta correcta';
        correctAnswerInput.required = true;
        newAnswerBlock.appendChild(correctAnswerInput);

        // Insertar el nuevo bloque en el contenedor de respuestas
        questionContainer.appendChild(newAnswerBlock);
    }

    // Función para limpiar las respuestas generadas previamente
    function clearPreviousQuestions() {
        questionContainer.innerHTML = '';
    }

    // Función para cambiar el botón "Subir" al seleccionar un archivo de examen
    const photoUpload = document.getElementById('photoUpload');
    const uploadForm = document.getElementById('uploadGradesForm');
    const submitButton = uploadForm.querySelector('button');

    photoUpload.addEventListener('change', function() {
        if (photoUpload.files.length > 0) {
            submitButton.textContent = 'Subir y Calificar';
        } else {
            submitButton.textContent = 'Subir';
        }
    });
});
