document.addEventListener("DOMContentLoaded", function () {
    // Load sound effects
    const correctSound = new Audio("/static/correct.mp3");
    const wrongSound = new Audio("/static/wrong.mp3");

    document.getElementById("quizForm")?.addEventListener("submit", async function (event) {
        event.preventDefault();

        let topic = document.getElementById("topic").value;
        const customTopic = document.getElementById("custom_topic").value.trim();

        if (topic === "Other") {
            topic = customTopic || "General Knowledge";
        }

        const difficulty = document.getElementById("difficulty").value;
        const num_questions = document.getElementById("num_questions").value;
        const question_type = document.getElementById("question_type").value;

        const requestData = {
            topic: topic,
            difficulty: difficulty,
            num_questions: num_questions,
            question_type: question_type
        };

        try {
            const response = await fetch("/generate_quiz", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();

            if (data.quiz) {
                localStorage.setItem("quizData", JSON.stringify(data.quiz));
                window.location.href = "/quiz";
            } else {
                alert(`⚠️ Failed to generate quiz: ${data.error || "Unknown error"}`);
            }
        } catch (error) {
            console.error("❌ Error:", error);
            alert("An error occurred while generating the quiz.");
        }
    });

    document.getElementById("topic")?.addEventListener("change", function () {
        var customTopicInput = document.getElementById("custom_topic");
        customTopicInput.style.display = (this.value === "Other") ? "block" : "none";
    });

    function displayQuiz() {
        const quizData = JSON.parse(localStorage.getItem("quizData")) || [];
        const quizOutput = document.getElementById("quizOutput");
        quizOutput.innerHTML = quizData.length === 0 ? "<p>No questions found.</p>" : "";

        const optionLetters = ["A", "B", "C", "D", "E", "F"];

        quizData.forEach((q, index) => {
            const questionDiv = document.createElement("div");
            questionDiv.classList.add("question-container");
            questionDiv.innerHTML = `
                <p><strong>Q${index + 1}:</strong> ${q.question}</p>
                <ul id="options-${index}">
                    ${q.options.map((option, i) => `
                        <li class="option" onclick="selectOption(this, ${index}, '${option.replace(/'/g, "\\'")}', '${q.answer.replace(/'/g, "\\'")}')">
                            <span class="option-label">${optionLetters[i] || ''}.</span> ${option}
                        </li>
                    `).join('')}
                </ul>
                <p class="answer" id="answer-${index}"><strong>Answer:</strong> ${q.answer}</p>
                <hr>
            `;
            quizOutput.appendChild(questionDiv);
        });
    }

    window.selectOption = function (selectedOption, questionIndex, selectedAnswer, correctAnswer) {
        const answerElement = document.getElementById(`answer-${questionIndex}`);
        const optionsList = document.getElementById(`options-${questionIndex}`).getElementsByTagName("li");

        for (let option of optionsList) {
            option.style.pointerEvents = "none";
            if (option.textContent.trim().toLowerCase().includes(correctAnswer.trim().toLowerCase())) {
                option.classList.add("correct");
            } else if (option.textContent.trim().toLowerCase().includes(selectedAnswer.trim().toLowerCase())) {
                option.classList.add("incorrect");
            }
        }

        if (selectedAnswer.trim().toLowerCase() === correctAnswer.trim().toLowerCase()) {
            correctSound.play();
        } else {
            wrongSound.play();
        }

        answerElement.classList.add("show");
    };

    window.onload = displayQuiz;
});
