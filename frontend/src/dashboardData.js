const dashboardData = {
  employee: {
    name: "Student",
    role: "Learner",
  },

  summary: {
    overallProgress: 72,
    quizScore: 78,
    learningHours: 12.5,
    studyStreak: 6,
  },

  competencies: {
    strong: [
      {
        name: "Python",
        score: 85,
      },
      {
        name: "Communication",
        score: 82,
      },
      {
        name: "Survey Design",
        score: 80,
      },
    ],

    developing: [
      {
        name: "SQL",
        score: 65,
      },
      {
        name: "Data Visualization",
        score: 60,
      },
      {
        name: "Statistics",
        score: 58,
      },
    ],

    gaps: [
      {
        name: "GIS",
        score: 35,
      },
      {
        name: "AI / ML",
        score: 30,
      },
      {
        name: "Cloud Computing",
        score: 25,
      },
    ],
  },

  learningPath: [
    {
      position: 1,
      name: "Cloud Computing",
      description: "High priority skill gap",
      priority: "High",
    },
    {
      position: 2,
      name: "AI / Machine Learning",
      description: "Develop technical competency",
      priority: "Medium",
    },
    {
      position: 3,
      name: "SQL Advanced",
      description: "Strengthen existing knowledge",
      priority: "Low",
    },
  ],

  recommendation: {
    title: "Improve Cloud Computing",
    description:
      "Your current competency in Cloud Computing is below the required level. Start a focused learning module to improve this skill.",
  },

  recentQuizzes: [
    {
      name: "Quiz 1",
      topic: "Python Basics",
      score: 60,
      status: "Developing",
    },
    {
      name: "Quiz 2",
      topic: "SQL Fundamentals",
      score: 68,
      status: "Developing",
    },
    {
      name: "Quiz 3",
      topic: "Python Functions",
      score: 85,
      status: "Strong",
    },
  ],
};

export default dashboardData;