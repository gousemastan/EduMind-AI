import { useEffect, useState } from "react";
import "../quiz.css";

const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function Quiz() {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);

  const filename = "AI_QB_Answers_Unit 1.pdf";

  // ============================================================
  // LOAD QUIZ
  // ============================================================

  useEffect(() => {
    loadQuiz();
  }, []);

  async function loadQuiz() {
    try {
      setLoading(true);
      setError("");
      setSubmitted(false);
      setAnswers({});
      setCurrentQuestion(0);
      setScore(0);

      const response = await fetch(
  `${API_URL}/api/generate-quiz?filename=${encodeURIComponent(
    filename
  )}&number_of_questions=5`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        let errorMessage = "Failed to generate quiz";

        try {
          const errorData = await response.json();

          if (errorData.detail) {
            errorMessage = errorData.detail;
          } else if (errorData.message) {
            errorMessage = errorData.message;
          }
        } catch {
          // Ignore JSON parsing error
        }

        throw new Error(errorMessage);
      }

      const data = await response.json();

      console.log("================================");
      console.log("QUIZ RESPONSE");
      console.log(data);
      console.log("================================");

      const generatedQuestions = Array.isArray(data.questions)
        ? data.questions
        : [];

      // ----------------------------------------------------------
      // Validate questions
      // ----------------------------------------------------------

      const validQuestions = generatedQuestions
        .filter((question) => {
          return (
            question &&
            question.question &&
            Array.isArray(question.options) &&
            question.options.length === 4 &&
            question.answer
          );
        })
        .map((question, index) => ({
          id: question.id || index + 1,
          question: question.question,
          options: question.options,
          answer: question.answer,
          topic: question.topic || "General",
        }));

      console.log("VALID QUESTIONS:", validQuestions);

      if (validQuestions.length === 0) {
        throw new Error(
          "The AI returned no valid multiple-choice questions."
        );
      }

      setQuestions(validQuestions);
    } catch (err) {
      console.error("Quiz error:", err);

      setError(
        err.message ||
          "Unable to load the quiz. Make sure the FastAPI server is running."
      );
    } finally {
      setLoading(false);
    }
  }

  // ============================================================
  // SELECT ANSWER
  // ============================================================

  function handleAnswerChange(option) {
    setAnswers((previousAnswers) => ({
      ...previousAnswers,
      [currentQuestion]: option,
    }));
  }

  // ============================================================
  // NEXT QUESTION
  // ============================================================

  function nextQuestion() {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion((previous) => previous + 1);
    }
  }

  // ============================================================
  // PREVIOUS QUESTION
  // ============================================================

  function previousQuestion() {
    if (currentQuestion > 0) {
      setCurrentQuestion((previous) => previous - 1);
    }
  }

  // ============================================================
  // SUBMIT QUIZ
  // ============================================================

  function submitQuiz() {
    let calculatedScore = 0;

    questions.forEach((question, index) => {
      const selectedAnswer = answers[index];

      if (!selectedAnswer) {
        return;
      }

      const correctAnswer = String(question.answer)
        .trim()
        .toLowerCase();

      const givenAnswer = String(selectedAnswer)
        .trim()
        .toLowerCase();

      if (givenAnswer === correctAnswer) {
        calculatedScore++;
      }
    });

    console.log("QUIZ SCORE:", calculatedScore);

    setScore(calculatedScore);
    setSubmitted(true);
  }

  // ============================================================
  // RETAKE QUIZ
  // ============================================================

  function restartQuiz() {
    setCurrentQuestion(0);
    setAnswers({});
    setSubmitted(false);
    setScore(0);
  }

  // ============================================================
  // LOADING SCREEN
  // ============================================================

  if (loading) {
    return (
      <div className="quiz-container">
        <div className="quiz-card quiz-loading-card">
          <div className="quiz-loading">
            <div className="spinner"></div>

            <h2>Generating your quiz...</h2>

            <p>
              EduMind AI is preparing multiple-choice questions
              from your learning material.
            </p>
          </div>
        </div>
      </div>
    );
  }

  // ============================================================
  // ERROR SCREEN
  // ============================================================

  if (error) {
    return (
      <div className="quiz-container">
        <div className="quiz-card error-card">
          <div className="error-icon">⚠️</div>

          <h2>Something went wrong</h2>

          <p>{error}</p>

          <button
            className="quiz-button"
            onClick={loadQuiz}
          >
            🔄 Try Again
          </button>
        </div>
      </div>
    );
  }

  // ============================================================
  // NO QUESTIONS
  // ============================================================

  if (questions.length === 0) {
    return (
      <div className="quiz-container">
        <div className="quiz-card">
          <div className="error-icon">📚</div>

          <h2>No questions found</h2>

          <p>
            EduMind AI could not generate questions from this
            learning material.
          </p>

          <button
            className="quiz-button"
            onClick={loadQuiz}
          >
            🔄 Generate Again
          </button>
        </div>
      </div>
    );
  }

  // ============================================================
  // RESULT SCREEN
  // ============================================================

  if (submitted) {
    const percentage = Math.round(
      (score / questions.length) * 100
    );

    let resultTitle = "";
    let resultMessage = "";

    if (percentage === 100) {
      resultTitle = "Excellent Work! 🎉";
      resultMessage =
        "Amazing! You mastered this learning material.";
    } else if (percentage >= 70) {
      resultTitle = "Great Job! 🚀";
      resultMessage =
        "You have a strong understanding of the material.";
    } else if (percentage >= 50) {
      resultTitle = "Good Effort! 💪";
      resultMessage =
        "Review the topics you missed and try again.";
    } else {
      resultTitle = "Keep Practicing! 📚";
      resultMessage =
        "Review your learning material and attempt the quiz again.";
    }

    return (
      <div className="quiz-container">
        <div className="quiz-card result-card">

          <div className="result-icon">
            {percentage === 100
              ? "🏆"
              : percentage >= 70
              ? "🎉"
              : "💪"}
          </div>

          <h1>{resultTitle}</h1>

          <p className="result-message">
            {resultMessage}
          </p>

          {/* SCORE */}

          <div className="score-circle">
            <strong>{percentage}%</strong>
            <span>Score</span>
          </div>

          {/* SCORE DETAILS */}

          <div className="score-details">

            <div className="score-detail">
              <strong>{score}</strong>
              <span>Correct</span>
            </div>

            <div className="score-detail">
              <strong>
                {questions.length - score}
              </strong>
              <span>Need Practice</span>
            </div>

            <div className="score-detail">
              <strong>{questions.length}</strong>
              <span>Total</span>
            </div>

          </div>

          {/* ANSWER REVIEW */}

          <div className="answer-review">

            <h3>📋 Answer Review</h3>

            {questions.map((question, index) => {

              const studentAnswer = answers[index];

              const isCorrect =
                studentAnswer &&
                studentAnswer.trim().toLowerCase() ===
                  question.answer.trim().toLowerCase();

              return (
                <div
                  key={question.id}
                  className={`review-item ${
                    isCorrect
                      ? "review-correct"
                      : "review-wrong"
                  }`}
                >

                  <div className="review-question">

                    <span>
                      Question {index + 1}
                    </span>

                    <span>
                      {isCorrect ? "✅" : "❌"}
                    </span>

                  </div>

                  <p>
                    {question.question}
                  </p>

                  <div className="review-answer">

                    <strong>
                      Your answer:
                    </strong>

                    <span>
                      {studentAnswer || "Not answered"}
                    </span>

                  </div>

                  {!isCorrect && (
                    <div className="review-correct-answer">

                      <strong>
                        Correct answer:
                      </strong>

                      <span>
                        {question.answer}
                      </span>

                    </div>
                  )}

                </div>
              );
            })}

          </div>

          <button
            className="quiz-button"
            onClick={restartQuiz}
          >
            🔄 Take Quiz Again
          </button>

          <button
            className="secondary-button"
            onClick={loadQuiz}
          >
            🤖 Generate New Quiz
          </button>

        </div>
      </div>
    );
  }

  // ============================================================
  // CURRENT QUESTION
  // ============================================================

  const question = questions[currentQuestion];

  const selectedAnswer = answers[currentQuestion];

  const progress =
    ((currentQuestion + 1) / questions.length) * 100;

  // ============================================================
  // QUIZ UI
  // ============================================================

  return (
    <div className="quiz-container">

      <div className="quiz-card">

        {/* ======================================================
            HEADER
        ====================================================== */}

        <div className="quiz-header">

          <div>

            <span className="quiz-label">
              🧠 EduMind AI
            </span>

            <h1>
              Learning Quiz
            </h1>

            <p className="quiz-subtitle">
              Test your understanding of the learning material
            </p>

          </div>

          <div className="question-count">
            {currentQuestion + 1}
            <span> / {questions.length}</span>
          </div>

        </div>

        {/* ======================================================
            PROGRESS BAR
        ====================================================== */}

        <div className="quiz-progress">

          <div
            className="quiz-progress-fill"
            style={{
              width: `${progress}%`,
            }}
          ></div>

        </div>

        {/* ======================================================
            TOPIC
        ====================================================== */}

        <div className="question-topic">

          <span>
            📚 Topic
          </span>

          <strong>
            {question.topic}
          </strong>

        </div>

        {/* ======================================================
            QUESTION
        ====================================================== */}

        <div className="question-section">

          <span className="question-number">
            Question {currentQuestion + 1}
          </span>

          <h2>
            {question.question}
          </h2>

        </div>

        {/* ======================================================
            OPTIONS
        ====================================================== */}

        <div className="options-container">

          {question.options.map(
            (option, index) => {

              const optionLetter =
                String.fromCharCode(65 + index);

              const isSelected =
                selectedAnswer === option;

              return (
                <button
                  key={index}
                  type="button"
                  className={`option-button ${
                    isSelected
                      ? "selected"
                      : ""
                  }`}
                  onClick={() =>
                    handleAnswerChange(option)
                  }
                >

                  <span className="option-letter">
                    {optionLetter}
                  </span>

                  <span className="option-text">
                    {option}
                  </span>

                  <span className="option-check">
                    {isSelected ? "✓" : ""}
                  </span>

                </button>
              );
            }
          )}

        </div>

        {/* ======================================================
            ANSWER STATUS
        ====================================================== */}

        <div className="answer-status">

          {selectedAnswer ? (
            <span className="answer-selected">
              ✓ Answer selected
            </span>
          ) : (
            <span className="answer-not-selected">
              Select one answer to continue
            </span>
          )}

        </div>

        {/* ======================================================
            NAVIGATION
        ====================================================== */}

        <div className="quiz-navigation">

          <button
            className="secondary-button"
            onClick={previousQuestion}
            disabled={currentQuestion === 0}
          >
            ← Previous
          </button>

          {currentQuestion <
          questions.length - 1 ? (
            <button
              className="quiz-button"
              onClick={nextQuestion}
              disabled={!selectedAnswer}
            >
              Next Question →
            </button>
          ) : (
            <button
              className="submit-button"
              onClick={submitQuiz}
              disabled={!selectedAnswer}
            >
              🎯 Submit Quiz
            </button>
          )}

        </div>

        {/* ======================================================
            QUESTION INDICATORS
        ====================================================== */}

        <div className="question-indicators">

          {questions.map(
            (item, index) => {

              const answered =
                answers[index];

              const active =
                index === currentQuestion;

              return (
                <button
                  key={item.id}
                  type="button"
                  className={`question-indicator ${
                    active ? "active" : ""
                  } ${
                    answered ? "answered" : ""
                  }`}
                  onClick={() =>
                    setCurrentQuestion(index)
                  }
                >
                  {index + 1}
                </button>
              );
            }
          )}

        </div>

      </div>

    </div>
  );
}

export default Quiz;