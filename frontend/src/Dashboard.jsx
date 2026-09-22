import React from "react";
import "./Dashboard.css";
import dashboardData from "./dashboardData";

function Dashboard() {
  return (
    <div className="dashboard">

      {/* Header */}
      <div className="dashboard-header">
        <div>
          <h1>Employee Dashboard</h1>
          <p>Welcome back! Continue your personalized learning journey.</p>
        </div>

        <div className="dashboard-profile">
          <div className="profile-avatar">S</div>
          <div>
            <strong>Student</strong>
            <span>Learner</span>
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="dashboard-cards">

        <div className="dashboard-card">
          <div className="card-icon">📈</div>
          <div>
            <p>Overall Progress</p>
            <h2>72%</h2>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-icon">📝</div>
          <div>
            <p>Quiz Score</p>
            <h2>78%</h2>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-icon">⏱️</div>
          <div>
            <p>Learning Hours</p>
            <h2>12.5 hrs</h2>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-icon">🔥</div>
          <div>
            <p>Study Streak</p>
            <h2>6 Days</h2>
          </div>
        </div>

      </div>

      {/* Competency Overview */}
      <section className="dashboard-section">

        <div className="section-title">
          <h2>Competency Overview</h2>
          <span>Current learning status</span>
        </div>

        <div className="competency-grid">

          <div className="competency-box strong">
            <h3>🟢 Strong Skills</h3>

            <div className="skill-item">
              <span>Python</span>
              <strong>85%</strong>
            </div>

            <div className="skill-item">
              <span>Communication</span>
              <strong>82%</strong>
            </div>

            <div className="skill-item">
              <span>Survey Design</span>
              <strong>80%</strong>
            </div>
          </div>

          <div className="competency-box developing">
            <h3>🟡 Developing Skills</h3>

            <div className="skill-item">
              <span>SQL</span>
              <strong>65%</strong>
            </div>

            <div className="skill-item">
              <span>Data Visualization</span>
              <strong>60%</strong>
            </div>

            <div className="skill-item">
              <span>Statistics</span>
              <strong>58%</strong>
            </div>
          </div>

          <div className="competency-box weak">
            <h3>🔴 Skill Gaps</h3>

            <div className="skill-item">
              <span>GIS</span>
              <strong>35%</strong>
            </div>

            <div className="skill-item">
              <span>AI / ML</span>
              <strong>30%</strong>
            </div>

            <div className="skill-item">
              <span>Cloud Computing</span>
              <strong>25%</strong>
            </div>
          </div>

        </div>
      </section>

      {/* Learning Path + Next Action */}
      <div className="dashboard-two-column">

        {/* Learning Path */}
        <section className="dashboard-panel">
          <div className="section-title">
            <h2>Personalized Learning Path</h2>
            <span>Recommended for you</span>
          </div>

          <div className="learning-step">
            <div className="step-number high">1</div>

            <div className="step-content">
              <h3>Cloud Computing</h3>
              <p>High priority skill gap</p>
            </div>

            <span className="priority high-text">High</span>
          </div>

          <div className="learning-step">
            <div className="step-number medium">2</div>

            <div className="step-content">
              <h3>AI / Machine Learning</h3>
              <p>Develop technical competency</p>
            </div>

            <span className="priority medium-text">Medium</span>
          </div>

          <div className="learning-step">
            <div className="step-number low">3</div>

            <div className="step-content">
              <h3>SQL Advanced</h3>
              <p>Strengthen existing knowledge</p>
            </div>

            <span className="priority low-text">Low</span>
          </div>

        </section>

        {/* Next Action */}
        <section className="dashboard-panel next-action">

          <div className="section-title">
            <h2>Recommended Next Action</h2>
            <span>AI recommendation</span>
          </div>

          <div className="recommendation-icon">
            🎯
          </div>

          <h3>Improve Cloud Computing</h3>

          <p>
            Your current competency in Cloud Computing is below
            the required level. Start a focused learning module
            to improve this skill.
          </p>

          <button className="start-learning-btn">
            Start Learning →
          </button>

        </section>

      </div>

      {/* Recent Quiz Performance */}
      <section className="dashboard-section">

        <div className="section-title">
          <h2>Recent Quiz Performance</h2>
          <span>Your latest learning activity</span>
        </div>

        <div className="quiz-table">

          <div className="quiz-row quiz-header">
            <span>Quiz</span>
            <span>Topic</span>
            <span>Score</span>
            <span>Status</span>
          </div>

          <div className="quiz-row">
            <span>Quiz 1</span>
            <span>Python Basics</span>
            <strong>60%</strong>
            <span className="status developing-status">
              Developing
            </span>
          </div>

          <div className="quiz-row">
            <span>Quiz 2</span>
            <span>SQL Fundamentals</span>
            <strong>68%</strong>
            <span className="status developing-status">
              Developing
            </span>
          </div>

          <div className="quiz-row">
            <span>Quiz 3</span>
            <span>Python Functions</span>
            <strong>85%</strong>
            <span className="status strong-status">
              Strong
            </span>
          </div>

        </div>

      </section>

    </div>
  );
}

export default Dashboard;