document.addEventListener("DOMContentLoaded", function() {
    const numQuestionsInput = document.getElementById('numQuestions');
    const createExamForm = document.getElementById('createExamForm');
    const questionContainer = document.getElementById('questionContainer');

    // Escuchar cuando se cambia la cantidad de preguntas
    numQuestionsInput.addEventListener('input', function() {
        // Elimina los bloques de preguntas anteriores, si los hay
        clearPreviousQuestions();

        // Generar los bloques de preguntas dinámicamente
        const numQuestions = parseInt(numQuestionsInput.value);
        for (let i = 1; i <= numQuestions; i++) {
            createQuestionBlock(i);
        }
    });

    // Función para crear un bloque de preguntas y respuestas correctas
    function createQuestionBlock(questionNum) {
        // Crear un nuevo div contenedor para la pregunta
        const newQuestionBlock = document.createElement('div');
        newQuestionBlock.classList.add('question-block');

        // Etiqueta de la pregunta
        const questionLabel = document.createElement('label');
        questionLabel.setAttribute('for', `question${questionNum}`);
        questionLabel.textContent = `Pregunta ${questionNum}:`;
        newQuestionBlock.appendChild(questionLabel);

        // Input para la pregunta
        const questionInput = document.createElement('input');
        questionInput.type = 'text';
        questionInput.id = `question${questionNum}`;
        questionInput.name = `question${questionNum}`;
        questionInput.placeholder = `Escribe la pregunta ${questionNum}`;
        questionInput.required = true;
        newQuestionBlock.appendChild(questionInput);

        // Etiqueta para la respuesta correcta
        const correctAnswerLabel = document.createElement('label');
        correctAnswerLabel.setAttribute('for', `correctAnswer${questionNum}`);
        correctAnswerLabel.textContent = 'Respuesta Correcta:';
        newQuestionBlock.appendChild(correctAnswerLabel);

        // Input para la respuesta correcta
        const correctAnswerInput = document.createElement('input');
        correctAnswerInput.type = 'text';
        correctAnswerInput.id = `correctAnswer${questionNum}`;
        correctAnswerInput.name = `correctAnswer${questionNum}`;
        correctAnswerInput.placeholder = 'Escribe la respuesta correcta';
        correctAnswerInput.required = true;
        newQuestionBlock.appendChild(correctAnswerInput);

        // Insertar el nuevo bloque en el contenedor de preguntas
        questionContainer.appendChild(newQuestionBlock);
    }

    // Función para limpiar las preguntas generadas previamente
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
