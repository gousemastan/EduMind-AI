import { useRef, useState, useEffect } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const fileInputRef = useRef(null);

    // Prevent duplicate PDF processing
  const processingFileRef = useRef(false);

  const [aiNotes, setAiNotes] = useState(null);
  const [notesLoading, setNotesLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(() => {
  return localStorage.getItem("edumind_theme") === "dark";
});



  


  // ============================================================
  // STATE
  // ============================================================

  const [selectedFile, setSelectedFile] = useState(null);
  // ============================================================
// MULTILINGUAL SUPPORT
// ============================================================

const [selectedLanguage, setSelectedLanguage] = useState(() => {
  return localStorage.getItem("edumind_language") || "English";
});


const handleLanguageChange = (event) => {
  const language = event.target.value;

  setSelectedLanguage(language);
  localStorage.setItem("edumind_language", language);

  console.log("🌐 Selected language:", language);
};



  // Authentication
  const [showLogin, setShowLogin] = useState(false);
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");

  const [flashcards, setFlashcards] = useState([]);
const [flashcardIndex, setFlashcardIndex] = useState(0);
const [flashcardFlipped, setFlashcardFlipped] = useState(false);
const [flashcardsLoading, setFlashcardsLoading] = useState(false);

  const [showRegister, setShowRegister] = useState(false);
  const [registerName, setRegisterName] = useState("");
  const [registerEmail, setRegisterEmail] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");
  const [registerConfirmPassword, setRegisterConfirmPassword] =
    useState("");

  const [registerDesignation, setRegisterDesignation] = useState("");
  const [registerDepartment, setRegisterDepartment] = useState("");
  const [registerJobRole, setRegisterJobRole] = useState("");
  const [registerEducation, setRegisterEducation] = useState("");
  const [registerExperience, setRegisterExperience] = useState("");
  const [registerPreviousTraining, setRegisterPreviousTraining] =
    useState("");

  const [currentUser, setCurrentUser] = useState(null);
  // ============================================================
// EMPLOYEE PROFILE EDIT
// ============================================================

const [editingProfile, setEditingProfile] = useState(false);
const [profileSaving, setProfileSaving] = useState(false);

const [profileForm, setProfileForm] = useState({
  designation: "",
  department: "",
  job_role: "",
  current_assignment: "",
  education: "",
  experience: "",
  previous_training: "",
});


useEffect(() => {
  if (!currentUser) {
    return;
  }

  setProfileForm({
    designation: currentUser.designation || "",
    department: currentUser.department || "",
    job_role: currentUser.job_role || "",
    education: currentUser.education || "",
    experience: currentUser.experience || "",
    previous_training:
      Array.isArray(currentUser.previous_training)
        ? currentUser.previous_training.join(", ")
        : currentUser.previous_training || "",
  });
}, [currentUser]);


const handleSaveProfile = async () => {
  const token = localStorage.getItem("edumind_token");

  if (!token) {
    alert("Please login first.");
    return;
  }

  if (!profileForm.job_role) {
    alert("Please select a Job Role.");
    return;
  }

  setProfileSaving(true);

  try {
    const response = await fetch(
      `${API_URL}/api/auth/profile`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          designation: profileForm.designation,
          department: profileForm.department,
          job_role: profileForm.job_role,
          current_assignment: profileForm.current_assignment,
          education: profileForm.education,
          experience: profileForm.experience,
          previous_training: JSON.stringify(
            profileForm.previous_training
              .split(",")
              .map((item) => item.trim())
              .filter(Boolean)
          ),
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Failed to update profile."
      );
    }

    // Update current user
    setCurrentUser(data.user);

    // Save updated user locally
    localStorage.setItem(
      "edumind_user",
      JSON.stringify(data.user)
    );

    setEditingProfile(false);

    alert("Profile updated successfully!");

    console.log(
      "✅ Updated profile:",
      data.user
    );

  } catch (error) {
    console.error(
      "Profile update error:",
      error
    );

    alert(
      `Profile update failed: ${error.message}`
    );

  } finally {
    setProfileSaving(false);
  }
};

// STEP 25.1 — ADMIN ACCESS CONTROL
const [showAdminAccess, setShowAdminAccess] = useState(false);

  // ============================================================
  // STEP 25.3 — ADMINISTRATOR DASHBOARD
  // ============================================================
  const [adminDashboard, setAdminDashboard] = useState(null);
  const [adminDashboardLoading, setAdminDashboardLoading] = useState(false);
  const [adminDashboardError, setAdminDashboardError] = useState("");
  const [authLoading, setAuthLoading] = useState(false);

  const [assessmentSkill, setAssessmentSkill] = useState("");
const [assessmentCategory, setAssessmentCategory] = useState("");
const [assessmentQuestions, setAssessmentQuestions] = useState([]);
const [assessmentAnswers, setAssessmentAnswers] = useState([]);
const [assessmentIndex, setAssessmentIndex] = useState(0);
const [assessmentResult, setAssessmentResult] = useState(null);
const [assessmentLoading, setAssessmentLoading] = useState(false);
const [assessmentSubmitting, setAssessmentSubmitting] = useState(false);
const [showAssessment, setShowAssessment] = useState(false);

  // Upload
  const [uploadStatus, setUploadStatus] = useState("");
  const [uploading, setUploading] = useState(false);

  // Quiz
  const [quiz, setQuiz] = useState([]);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [score, setScore] = useState(null);
  const [questionStartTimes, setQuestionStartTimes] = useState({});
  const [questionTimes, setQuestionTimes] = useState({});
  const [studyWasteAnalysis, setStudyWasteAnalysis] = useState(null);
  const [studyWasteLoading, setStudyWasteLoading] = useState(false);
  // ============================================================
// QUESTION INTELLIGENCE
// ============================================================

  const [questionIntelligence, setQuestionIntelligence] = useState(null);
  const [questionIntelligenceLoading, setQuestionIntelligenceLoading] =
    useState(false);
  // ============================================================
// RECOVERY MODE
// ============================================================

  const [recoveryAnalysis, setRecoveryAnalysis] = useState(null);
  const [recoveryLoading, setRecoveryLoading] = useState(false);
  // ============================================================
// EXPLAIN-TO-LEARN AI
// ============================================================

  const [explainAnalysis, setExplainAnalysis] = useState(null);
  const [explainLoading, setExplainLoading] = useState(false);

  

  // ============================================================
// CONFUSION DETECTOR
// ============================================================

  const [confusionAnalysis, setConfusionAnalysis] = useState({});
  const [confusionLoading, setConfusionLoading] = useState({});

  // AI Tutor
  const [tutorQuestion, setTutorQuestion] = useState("");
  const [tutorAnswer, setTutorAnswer] = useState("");
  const [askingTutor, setAskingTutor] = useState(false);
  const [tutorHistory, setTutorHistory] = useState([]);

  // Learning analysis
  const [learningAnalysis, setLearningAnalysis] = useState(null);
  const [loadingLearningPath, setLoadingLearningPath] =
    useState(false);
  // ============================================================
// ADAPTIVE LEARNING
// ============================================================

  const [adaptiveAnalysis, setAdaptiveAnalysis] = useState(null);
  const [adaptiveLoading, setAdaptiveLoading] = useState(false);
  

  // Topics
  const [detectedTopics, setDetectedTopics] = useState([]);
  
  const [detectingTopics, setDetectingTopics] = useState(false);
  // ============================================================
// INTERACTIVE LEARNING MODULES
// ============================================================

  const [activeLearningModule, setActiveLearningModule] =
    useState(null);

  const [completedLearningModules, setCompletedLearningModules] =
    useState([]);

  // ============================================================
// VIRTUAL LABS - STEP 23.1
// ============================================================

  const [selectedVirtualLab, setSelectedVirtualLab] =
    useState(null);

  const [activeVirtualLab, setActiveVirtualLab] =
    useState(null);

  const [completedVirtualLabs, setCompletedVirtualLabs] =
    useState([]);
  const [virtualLabActivityIndex, setVirtualLabActivityIndex] =
    useState(0);

  // Skill gaps
  const [skillGaps, setSkillGaps] = useState([]);
  const [detectingSkillGaps, setDetectingSkillGaps] =
    useState(false);
  const [igotCourses, setIgotCourses] = useState([]);
  const [igotEnrollments, setIgotEnrollments] = useState([]);
  const [revisionQuestions, setRevisionQuestions] = useState([]);
  const [loadingRevision, setLoadingRevision] = useState(false);
  const [revisionTopics, setRevisionTopics] = useState([]);
  const [revisionAnswers, setRevisionAnswers] = useState({});
  const [revisionSubmitted, setRevisionSubmitted] = useState(false);
  const [revisionScore, setRevisionScore] = useState(0);

  const [igotRecommendations, setIgotRecommendations] = useState([]);
  const [loadingIgot, setLoadingIgot] = useState(false);
  const [nsstaTrainings, setNsstaTrainings] = useState([]);
  const [nsstaRecommendations, setNsstaRecommendations] = useState([]);
  const [loadingNssta, setLoadingNssta] = useState(false);

  // ============================================================
// INTERACTIVE LEARNING MODULES
// ============================================================

const createInteractiveLearningModules = () => {
  const topics = Array.isArray(detectedTopics)
    ? detectedTopics
    : [];

  return topics.map((topic, index) => {
    const topicName =
      typeof topic === "string"
        ? topic
        : topic?.topic ||
          topic?.name ||
          topic?.title ||
          `Topic ${index + 1}`;

    return {
      id: `module-${index}-${topicName}`,
      title: topicName,
      description:
        `Interactive learning module for ${topicName}.`,
      lessons: [
        {
          id: "learn",
          title: "Learn",
          description:
            `Understand the important concepts of ${topicName}.`,
        },
        {
          id: "practice",
          title: "Practice",
          description:
            `Apply your knowledge of ${topicName} through practice activities.`,
        },
        {
          id: "checkpoint",
          title: "Checkpoint",
          description:
            `Check your understanding of ${topicName}.`,
        },
      ],
    };
  });
};
// ============================================================
// VIRTUAL LAB CATALOGUE - STEP 23.1
// ============================================================

const virtualLabCatalogue = [
  {
    id: "ai-lab",
    technology: "Artificial Intelligence",
    title: "AI Fundamentals Virtual Lab",
    description:
      "Explore basic Artificial Intelligence concepts through guided hands-on activities.",
    level: "Beginner",
    activities: [
      "Understand AI concepts",
      "Explore a simple AI workflow",
      "Check AI knowledge",
    ],
  },

  {
    id: "data-science-lab",
    technology: "Data Science",
    title: "Data Science Virtual Lab",
    description:
      "Practice basic data analysis concepts using structured learning activities.",
    level: "Beginner",
    activities: [
      "Understand datasets",
      "Explore data analysis",
      "Check data interpretation",
    ],
  },

  {
    id: "cloud-lab",
    technology: "Cloud Computing",
    title: "Cloud Computing Virtual Lab",
    description:
      "Learn fundamental cloud computing concepts through guided activities.",
    level: "Beginner",
    activities: [
      "Understand cloud concepts",
      "Explore cloud services",
      "Check cloud knowledge",
    ],
  },

  {
    id: "cybersecurity-lab",
    technology: "Cybersecurity",
    title: "Cybersecurity Virtual Lab",
    description:
      "Learn essential cybersecurity concepts through practical guided activities.",
    level: "Beginner",
    activities: [
      "Understand security concepts",
      "Identify common security risks",
      "Check cybersecurity knowledge",
    ],
  },

  {
    id: "automation-lab",
    technology: "Automation",
    title: "Automation Virtual Lab",
    description:
      "Explore automation concepts through structured hands-on learning activities.",
    level: "Beginner",
    activities: [
      "Understand automation",
      "Explore an automation workflow",
      "Check automation knowledge",
    ],
  },
];

// ============================================================
// VIRTUAL LAB SELECTION - STEP 23.1
// ============================================================

const handleSelectVirtualLab = (lab) => {
  setSelectedVirtualLab(lab);
};

// ============================================================
// VIRTUAL LAB HANDS-ON INTERACTION - STEP 23.4
// ============================================================

const handleStartVirtualLab = (lab) => {
  setActiveVirtualLab(lab);
  setVirtualLabActivityIndex(0);
};

const handleNextVirtualLabActivity = () => {
  if (!activeVirtualLab?.activities) {
    return;
  }

  setVirtualLabActivityIndex((previous) => {
    if (previous < activeVirtualLab.activities.length - 1) {
      return previous + 1;
    }

    return previous;
  });
};

const handlePreviousVirtualLabActivity = () => {
  setVirtualLabActivityIndex((previous) => {
    if (previous > 0) {
      return previous - 1;
    }

    return previous;
  });
};

const handleExitVirtualLab = () => {
  setActiveVirtualLab(null);
  setVirtualLabActivityIndex(0);
};
// ============================================================
// VIRTUAL LAB COMPLETION - STEP 23.5
// ============================================================

const handleCompleteVirtualLab = (lab) => {
  if (!lab) {
    return;
  }

  setCompletedVirtualLabs((previous) => {
    if (previous.includes(lab.id)) {
      return previous;
    }

    return [...previous, lab.id];
  });

  setActiveVirtualLab(null);
  setSelectedVirtualLab(null);
  setVirtualLabActivityIndex(0);
};

const handleOpenLearningModule = (module) => {
  setActiveLearningModule({
    ...module,
    activeLesson: module.lessons?.[0] || null,
  });
};

// Step 22.4 - Handle Learning Module Lessons
const handleModuleLesson = (module, lesson) => {
  setActiveLearningModule({
    ...module,
    activeLesson: lesson,
  });
};

const handleCompleteLearningModule = (moduleId) => {
  setCompletedLearningModules((previous) => {
    if (previous.includes(moduleId)) {
      return previous;
    }

    return [...previous, moduleId];
  });
};

const handleCloseLearningModule = () => {
  setActiveLearningModule(null);
};

  const handleLoadIgotCourses = async () => {
  const token = localStorage.getItem("edumind_token");

  if (!token) {
    console.warn("No login token found.");
    return;
  }

  setLoadingIgot(true);

  try {
    const response = await fetch(
      `${API_URL}/api/igot/courses`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.detail || "Failed to load iGoT courses"
      );
    }

    const data = await response.json();

    setIgotCourses(data.courses || []);

    console.log("iGoT courses loaded:", data.courses);
  } catch (error) {
    console.error("iGoT courses error:", error);
  } finally {
    setLoadingIgot(false);
  }
};

// ============================================================
// iGoT COURSE ENROLLMENT
// ============================================================

const handleIgotEnroll = async (course) => {
  const token = localStorage.getItem("edumind_token");

  if (!token) {
    alert("Please login first.");
    return;
  }

  try {
    const response = await fetch(
      `${API_URL}/api/igot/enroll`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          course_id: course.id,
          course_title:
            course.title ||
            course.course_name ||
            "Training Course",
          skill: course.skill || "",
          duration: course.duration || "",
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Failed to enroll in course"
      );
    }

    alert(
      `Successfully enrolled in ${
        course.title ||
        course.course_name ||
        "the course"
      }`
    );

    console.log(
      "✅ iGoT enrollment:",
      data
    );

  } catch (error) {
    console.error(
      "❌ iGoT enrollment error:",
      error
    );

    alert(error.message);
  }
};



// ============================================================
// LOAD MY ENROLLED iGoT COURSES
// ============================================================

const handleLoadIgotEnrollments = async () => {
  const token = localStorage.getItem("edumind_token");

  if (!token) {
    alert("Please login first.");
    return;
  }

  try {
    const response = await fetch(
      `${API_URL}/api/igot/enrollments`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Failed to load enrolled courses"
      );
    }

    setIgotEnrollments(data.enrollments || []);

    console.log(
      "✅ My iGoT enrollments:",
      data.enrollments
    );
  } catch (error) {
    console.error(
      "❌ iGoT enrollment loading error:",
      error
    );

    alert(error.message);
  }
};
const handleUpdateIgotProgress = async (enrollmentId, progress) => {
  const token = localStorage.getItem("edumind_token");

  if (!token) {
    alert("Please login again.");
    return;
  }

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/api/igot/progress",
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          enrollment_id: enrollmentId,
          progress: progress,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Failed to update course progress"
      );
    }

    console.log("✅ iGoT progress updated:", data);

    // Refresh enrolled courses
    await handleLoadIgotEnrollments();

  } catch (error) {
    console.error("❌ iGoT progress update error:", error);
    alert(error.message);
  }
};

const handleLoadIgotRecommendations = async (gaps = skillGaps) => {
  const token = localStorage.getItem("edumind_token");

  if (!token) {
    console.warn("No login token found.");
    return;
  }

  const normalizedGaps = (gaps || []).map((gap) => {
    if (typeof gap === "string") {
      return { skill: gap };
    }

    return gap;
  });

  if (!normalizedGaps.length) {
    setIgotRecommendations([]);
    return;
  }

  setLoadingIgot(true);

  try {
    const response = await fetch(
      `${API_URL}/api/igot/recommendations`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(normalizedGaps),
      }
    );

    if (!response.ok) {
      const errorData = await response.json();

      throw new Error(
        errorData.detail || "Failed to load iGoT recommendations"
      );
    }

    const data = await response.json();

    setIgotRecommendations(
      data.recommendations || []
    );

    console.log(
      "iGoT recommendations loaded:",
      data.recommendations
    );
  } catch (error) {
    console.error(
      "iGoT recommendations error:",
      error
    );
  } finally {
    setLoadingIgot(false);
  }
};

  const handleLoadNsstaRecommendations = async (gaps = skillGaps) => {
  try {
    setLoadingNssta(true);

    const token =
      localStorage.getItem("token") ||
      localStorage.getItem("access_token");

    if (!token) {
      console.error("No authentication token found.");
      setNsstaRecommendations([]);
      return;
    }

    const normalizedGaps = (gaps || [])
      .map((gap) => {
        if (typeof gap === "string") {
          return {
            skill: gap,
            level: "Needs Practice",
          };
        }

        return {
          skill:
            gap.skill ||
            gap.topic ||
            gap.name ||
            "",
          level:
            gap.level ||
            "Needs Practice",
        };
      })
      .filter((gap) => gap.skill);

    if (normalizedGaps.length === 0) {
      setNsstaRecommendations([]);
      return;
    }

    const response = await fetch(
      "http://127.0.0.1:8000/api/nssta/recommendations",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(normalizedGaps),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail ||
          "Failed to load NSSTA recommendations"
      );
    }

    setNsstaRecommendations(
      data.recommendations || []
    );

    console.log(
      "NSSTA recommendations:",
      data.recommendations
    );
  } catch (error) {
    console.error(
      "NSSTA recommendation error:",
      error
    );
    setNsstaRecommendations([]);
  } finally {
    setLoadingNssta(false);
  }
};
  // Personalized learning path
  const [personalizedPath, setPersonalizedPath] =
    useState(null);
  const [creatingLearningPath, setCreatingLearningPath] =
    useState(false);

  const [practiceTopic, setPracticeTopic] = useState("");
  // ============================================================
// COMPETENCY PROFILE
// ============================================================

const defaultCompetencyCategories = {
  Statistical: [],
  Technical: [],
  "Digital Governance": [],
  "Behavioural / Managerial": [],
};

const [competencyCategories, setCompetencyCategories] = useState(
  defaultCompetencyCategories
);

const [frameworkLoading, setFrameworkLoading] = useState(false);

const [competencyProfile, setCompetencyProfile] = useState(() => {
  const saved = localStorage.getItem("edumind_competency_profile");

  if (saved) {
    try {
      return JSON.parse(saved);
    } catch {
      return {};
    }
  }

  return {};
});

 // PASTE THE NEW useEffect HERE
  useEffect(() => {
    if (!currentUser?.id) {
      return;
    }

    const token = localStorage.getItem("edumind_token");

    if (!token) {
      return;
    }

    const loadCompetencies = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/competencies",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error(
            "Failed to load competency profile"
          );
        }

        const data = await response.json();

        if (data.competencies) {
          setCompetencyProfile(data.competencies);

          localStorage.setItem(
            "edumind_competency_profile",
            JSON.stringify(data.competencies)
          );
        }
      } catch (error) {
        console.error(
          "Competency loading error:",
          error
        );
      }
    };

    loadCompetencies();
    handleLoadIgotEnrollments();
  }, [currentUser?.id]);


  
  const loadCompetencyFramework = async (jobRole) => {
  const token = localStorage.getItem("edumind_token");

  if (!token || !jobRole) {
    return;
  }

  setFrameworkLoading(true);

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/competencies/framework/${encodeURIComponent(
        jobRole
      )}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Failed to load competency framework"
      );
    }

    setCompetencyCategories(
      data.framework || defaultCompetencyCategories
    );

    const framework = data.framework || {};

setCompetencyProfile((previousProfile) => {
  const updatedProfile = { ...previousProfile };

  Object.entries(framework).forEach(
    ([category, skills]) => {
      if (!updatedProfile[category]) {
        updatedProfile[category] = {};
      }

      Object.keys(skills).forEach((skill) => {
        if (!updatedProfile[category][skill]) {
          updatedProfile[category][skill] = "Beginner";
        }
      });
    }
  );

  localStorage.setItem(
    "edumind_competency_profile",
    JSON.stringify(updatedProfile)
  );

  return updatedProfile;
});

    console.log(
      "✅ Competency framework loaded:",
      data.framework
    );
  } catch (error) {
    console.error(
      "❌ Competency framework error:",
      error
    );
  } finally {
    setFrameworkLoading(false);
  }
};

useEffect(() => {
  if (!currentUser?.job_role) {
    return;
  }

  loadCompetencyFramework(currentUser.job_role);
}, [currentUser?.job_role]);
  useEffect(() => {

  if (!currentUser) {
    return;
  }

  handleLoadIgotCourses();
}, [currentUser]);


// ============================================================
// COMPETENCY GAP ANALYSIS
// ============================================================

const [competencyGapAnalysis, setCompetencyGapAnalysis] =
  useState(null);

const [gapAnalysisLoading, setGapAnalysisLoading] =
  useState(false);

const loadCompetencyGapAnalysis = async () => {
  const token = localStorage.getItem("edumind_token");

  if (!token) {
    console.warn("No login token found.");
    return;
  }

  setGapAnalysisLoading(true);

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/api/competencies/gap-analysis",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Failed to load competency gap analysis"
      );
    }

    setCompetencyGapAnalysis(data);

    console.log(
      "✅ Competency gap analysis loaded:",
      data
    );

  } catch (error) {
    console.error(
      "Competency gap analysis error:",
      error
    );
  } finally {
    setGapAnalysisLoading(false);
  }
};

const handleCompetencyChange = async (category, skill, level) => {
  const updatedProfile = {
    ...competencyProfile,
    [category]: {
      ...(competencyProfile[category] || {}),
      [skill]: level,
    },
  };

  // Update screen immediately
  setCompetencyProfile(updatedProfile);

  // Keep local fallback
  localStorage.setItem(
    "edumind_competency_profile",
    JSON.stringify(updatedProfile)
  );

  const token = localStorage.getItem("edumind_token");

  if (!token) {
    console.warn("No login token found.");
    return;
  }

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/api/competencies",
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          category,
          skill,
          level,
        }),
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.detail || "Failed to save competency"
      );
    }

    console.log(
      `Saved: ${category} → ${skill} → ${level}`
    );
    await loadCompetencyGapAnalysis();
    console.log(
  `Saved: ${category} → ${skill} → ${level}`
);

await loadCompetencyGapAnalysis();

  } catch (error) {
    console.error(
      "Competency save error:",
      error
    );
  }
};
const startCompetencyAssessment = async (category, skill) => {
  const token = localStorage.getItem("edumind_token");

  if (!token) {
    alert("Please login first.");
    return;
  }

  setAssessmentLoading(true);
  setAssessmentResult(null);
  setAssessmentQuestions([]);
  setAssessmentAnswers([]);
  setAssessmentIndex(0);

  try {
    const currentLevel =
      competencyProfile?.[category]?.[skill] || "Beginner";

    const response = await fetch(
      "http://127.0.0.1:8000/api/competencies/assessment/generate",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          category,
          skill,
          current_level: currentLevel,
          target_level: "Advanced",
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Failed to generate assessment"
      );
    }

    const questions = data.assessment?.questions || [];

    if (questions.length === 0) {
      throw new Error("No assessment questions received.");
    }

    setAssessmentCategory(category);
    setAssessmentSkill(skill);
    setAssessmentQuestions(questions);
    setAssessmentAnswers(
      Array(questions.length).fill("")
    );
    setAssessmentIndex(0);
    setShowAssessment(true);

  } catch (error) {
    console.error(
      "Competency assessment error:",
      error
    );

    alert(
      error.message ||
      "Failed to generate competency assessment."
    );

  } finally {
    setAssessmentLoading(false);
  }
};
const submitCompetencyAssessment = async () => {
  const token = localStorage.getItem("edumind_token");

  if (!token) {
    alert("Please login first.");
    return;
  }

  if (
    assessmentAnswers.length !==
    assessmentQuestions.length
  ) {
    alert("Please answer all questions.");
    return;
  }

  if (assessmentAnswers.some((answer) => !answer)) {
    alert("Please answer all questions.");
    return;
  }

  setAssessmentSubmitting(true);

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/api/competencies/assessment/submit",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          category: assessmentCategory,
          skill: assessmentSkill,
          questions: assessmentQuestions,
          answers: assessmentAnswers,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail ||
        "Failed to submit assessment"
      );
    }

    setAssessmentResult(data.result);
setShowAssessment(false);

// Refresh competency profile after assessment
try {
  const competencyResponse = await fetch(
    "http://127.0.0.1:8000/api/competencies",
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (competencyResponse.ok) {
    const competencyData = await competencyResponse.json();

    setCompetencyProfile(
      competencyData.competencies || {}
    );

    console.log(
      "✅ Competency profile refreshed:",
      competencyData.competencies
    );
  }
} catch (refreshError) {
  console.error(
    "⚠️ Failed to refresh competency profile:",
    refreshError
  );
}

// Refresh gap analysis
await loadCompetencyGapAnalysis();

alert("AI competency assessment completed.");

  } catch (error) {
    console.error(
      "Assessment submission error:",
      error
    );

    alert(
      error.message ||
      "Failed to submit assessment."
    );

  } finally {
    setAssessmentSubmitting(false);
  }
};

  const [generatingPracticeQuiz, setGeneratingPracticeQuiz] = useState(false);

  // ============================================================
  // API HELPER
  // ============================================================

  const apiRequest = async (url, options = {}) => {
    try {
      const response = await fetch(url, options);

      let data = {};

      try {
        data = await response.json();
      } catch {
        data = {};
      }

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.message ||
            `Request failed with status ${response.status}`
        );
      }

      return data;
    } catch (error) {
      if (error instanceof TypeError) {
        throw new Error(
          "Cannot connect to EduMind AI backend. Make sure FastAPI is running on port 8000."
        );
      }

      throw error;
    }
  };

  // ============================================================
  // STEP 25.1 — ADMIN ACCESS CONTROL
  // ============================================================

  const isAdminUser =
    String(currentUser?.role || "")
      .trim()
      .toLowerCase() === "admin";

  const handleOpenAdminDashboard = () => {
    if (!currentUser) {
      alert("Please login first.");
      return;
    }

    if (!isAdminUser) {
      alert("Admin access is restricted to Administrator users.");
      return;
    }

    setShowAdminAccess(true);
  };

  const handleCloseAdminAccess = () => {
    setShowAdminAccess(false);
    setAdminDashboardError("");
  };

  // ============================================================
  // STEP 25.3 — LOAD ADMINISTRATOR DASHBOARD
  // ============================================================
  const handleLoadAdminDashboard = async () => {
    const token = localStorage.getItem("edumind_token");

    if (!token) {
      alert("Please login first.");
      return;
    }

    if (!isAdminUser) {
      alert("Administrator access required.");
      return;
    }

    setAdminDashboardLoading(true);
    setAdminDashboardError("");

    try {
      const data = await apiRequest(
        `${API_URL}/api/admin/dashboard`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setAdminDashboard(data.dashboard || null);
    } catch (error) {
      console.error("Admin dashboard error:", error);
      setAdminDashboardError(
        error.message ||
          "Failed to load administrator dashboard."
      );
    } finally {
      setAdminDashboardLoading(false);
    }
  };

  // ============================================================
  // LOGIN
  // ============================================================

  const handleLogin = async (event) => {
    event.preventDefault();

    if (!loginEmail.trim() || !loginPassword.trim()) {
      alert("Please enter your email and password.");
      return;
    }

    try {
      setAuthLoading(true);

      const data = await apiRequest(
        `${API_URL}/api/auth/login`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: loginEmail.trim(),
            password: loginPassword,
          }),
        }
      );

      // Save JWT token
      const token = data.access_token;
      localStorage.setItem(
        "edumind_token",
        token
      );

      // The current login response does not always include the user's role.
      // Resolve the role from the authenticated administrator endpoint.
      // Admin -> 200, normal learner -> 403.
      let loggedInUser = data.user || {};

      if (!loggedInUser.role) {
        try {
          const adminCheckResponse = await fetch(
            `${API_URL}/api/admin/dashboard`,
            {
              method: "GET",
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );

          loggedInUser = {
            ...loggedInUser,
            role: adminCheckResponse.ok
              ? "admin"
              : "learner",
          };
        } catch (roleError) {
          console.warn(
            "Role check failed. Defaulting to learner.",
            roleError
          );

          loggedInUser = {
            ...loggedInUser,
            role: "learner",
          };
        }
      }

      // Save the complete user object, including role.
      localStorage.setItem(
        "edumind_user",
        JSON.stringify(loggedInUser)
      );

      setCurrentUser(loggedInUser);

      // Clear login form
      setLoginEmail("");
      setLoginPassword("");

      // Close modal
      setShowLogin(false);

      alert(`Welcome back, ${data.user.name}!`);

      console.log("Login successful:", data.user);
    } catch (error) {
      console.error("Login error:", error);

      alert(`Login failed: ${error.message}`);
    } finally {
      setAuthLoading(false);
    }
  };

  // ============================================================
  // REGISTER
  // ============================================================

  const handleRegister = async (event) => {
    event.preventDefault();

    if (
      !registerName.trim() ||
      !registerEmail.trim() ||
      !registerPassword ||
      !registerConfirmPassword
    ) {
      alert("Please fill in all fields.");
      return;
    }

    if (registerPassword !== registerConfirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    if (registerPassword.length < 6) {
      alert("Password must be at least 6 characters.");
      return;
    }

    try {
      setAuthLoading(true);

      const data = await apiRequest(
        `${API_URL}/api/auth/register`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: registerName.trim(),
            email: registerEmail.trim(),
            password: registerPassword,
              designation: registerDesignation.trim(),

  department: registerDepartment.trim(),

  job_role: registerJobRole.trim(),

  education: registerEducation.trim(),

  experience: registerExperience.trim(),

  previous_training: registerPreviousTraining
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean),



          }),
        }
      );

      console.log("Registration successful:", data);

      // Clear register form
      setRegisterName("");
      setRegisterEmail("");
      setRegisterPassword("");
      setRegisterConfirmPassword("");
      setRegisterDesignation("");
setRegisterDepartment("");
setRegisterJobRole("");
setRegisterEducation("");
setRegisterExperience("");
setRegisterPreviousTraining("");

      // Close register
      setShowRegister(false);

      // Open login
      setShowLogin(true);

      alert(
        "Account created successfully! Please login."
      );
    } catch (error) {
      console.error("Registration error:", error);

      alert(`Registration failed: ${error.message}`);
    } finally {
      setAuthLoading(false);
    }
  };

  // ============================================================
  // START LEARNING
  // ============================================================

  const handleStartLearning = () => {
    fileInputRef.current?.click();
  };

  // ============================================================
  // SCROLL TO AI TUTOR
  // ============================================================

  const handleAITutor = () => {
    document
      .getElementById("ai-tutor-section")
      ?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
  };

  // ============================================================
  // HANDLE FILE
  // ============================================================

 // ============================================================
// HANDLE FILE
// ============================================================

const handleFileChange = async (event) => {
  const file = event.target.files?.[0];

  if (!file) {
    return;
  }

  // ------------------------------------------------------------
  // PREVENT DUPLICATE PROCESSING
  // ------------------------------------------------------------

  if (processingFileRef.current) {
    console.log(
      "⏳ A PDF is already being processed. Please wait."
    );

    return;
  }

  // ------------------------------------------------------------
  // PDF VALIDATION
  // ------------------------------------------------------------

  const isPDF =
    file.type === "application/pdf" ||
    file.name.toLowerCase().endsWith(".pdf");

  if (!isPDF) {
    setUploadStatus(
      "❌ Please select a PDF file."
    );

    setSelectedFile(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }

    return;
  }

  // ------------------------------------------------------------
  // LOCK PROCESSING
  // ------------------------------------------------------------

  processingFileRef.current = true;

  console.log(
    "🚀 Starting PDF processing:",
    file.name
  );

  // ------------------------------------------------------------
  // SET FILE
  // ------------------------------------------------------------

  setSelectedFile(file);

  setUploadStatus(
    "⏳ Uploading PDF..."
  );

  setUploading(true);

  // ------------------------------------------------------------
  // RESET PREVIOUS RESULTS
  // ------------------------------------------------------------
  setQuiz([]);
setSelectedAnswers({});
setScore(null);
setConfusionAnalysis({});
setConfusionLoading({});
setQuestionStartTimes({});
setQuestionTimes({});
setStudyWasteAnalysis(null);


setLearningAnalysis(null);

setDetectedTopics([]);
setActiveLearningModule(null);
setCompletedLearningModules([]);

setSkillGaps([]);

setPersonalizedPath(null);


// Reset previous AI Notes
setAiNotes(null);

setFlashcards([]);
setFlashcardIndex(0);
setFlashcardFlipped(false);

  try {
    // ==========================================================
    // STEP 1: UPLOAD PDF
    // ==========================================================

    console.log(
      "📤 STEP 1: Uploading PDF..."
    );

    const formData = new FormData();

    formData.append(
      "file",
      file
    );

    const uploadData =
      await apiRequest(
        `${API_URL}/api/upload`,
        {
          method: "POST",
          body: formData,
        }
      );

    console.log(
      "✅ PDF upload completed:",
      uploadData
    );

    setUploadStatus(
  `🧠 PDF uploaded successfully. Generating quiz in ${selectedLanguage}...`
);



    // ==========================================================
    // STEP 2: GENERATE QUIZ
    // ==========================================================

    console.log(
      "📝 STEP 2: Generating AI quiz..."
    );

  const quizData =
  await apiRequest(
    `${API_URL}/api/generate-quiz?filename=${encodeURIComponent(
      file.name
    )}&number_of_questions=5&language=${encodeURIComponent(
      selectedLanguage
    )}`,
    {
      method: "POST",
    }
  );

    console.log(
      "✅ Quiz generation completed:",
      quizData
    );

    // ----------------------------------------------------------
    // GET QUESTIONS
    // ----------------------------------------------------------

    const generatedQuestions =
      Array.isArray(
        quizData.questions
      )
        ? quizData.questions
        : [];

    // ----------------------------------------------------------
    // VALIDATE QUIZ
    // ----------------------------------------------------------

    if (
      generatedQuestions.length === 0
    ) {
      setQuiz([]);

      setUploadStatus(
        "⚠️ PDF uploaded, but no quiz questions were generated."
      );

      return;
    }

    // ----------------------------------------------------------
    // SAVE QUIZ
    // ----------------------------------------------------------

    setQuiz(
      generatedQuestions
    );

    setSelectedAnswers({});
    setScore(null);

    // ----------------------------------------------------------
    // SUCCESS
    // ----------------------------------------------------------

    setUploadStatus(
      `✅ PDF processed successfully! ${generatedQuestions.length} questions generated.`
    );

    console.log(
      `🎯 SUCCESS: ${generatedQuestions.length} quiz questions ready.`
    );

    // ----------------------------------------------------------
    // SCROLL TO QUIZ
    // ----------------------------------------------------------

    setTimeout(() => {
      document
        .getElementById(
          "quiz-section"
        )
        ?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
    }, 300);

  } catch (error) {
    console.error(
      "❌ PDF processing error:",
      error
    );

    setUploadStatus(
      `❌ ${error.message}`
    );

  } finally {
    // ----------------------------------------------------------
    // UNLOCK PROCESSING
    // ----------------------------------------------------------

    processingFileRef.current = false;

    setUploading(false);

    // ----------------------------------------------------------
    // RESET FILE INPUT
    // ----------------------------------------------------------

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }

    console.log(
      "🔓 PDF processing lock released."
    );
  }
};

  // ============================================================
  // QUESTION KEY
  // ============================================================

  const getQuestionKey = (item, index) => {
    return item.id ?? `question-${index}`;
  };

  // ============================================================
// GENERATE AI NOTES
// ============================================================

const handleGenerateNotes = async () => {
  if (!selectedFile) {
    alert("Please upload a PDF first.");
    return;
  }

  try {
    setNotesLoading(true);

    setUploadStatus(
      "🧠 Gemini AI is generating study notes from your PDF..."
    );

    console.log(
      "📚 Generating AI Notes for:",
      selectedFile.name
    );

    const data = await apiRequest(
  `${API_URL}/api/generate-notes?filename=${encodeURIComponent(
    selectedFile.name
  )}&language=${encodeURIComponent(
    selectedLanguage
  )}`,
  {
    method: "POST",
  }
);

    console.log(
      "✅ AI Notes generated:",
      data
    );

    if (!data.notes) {
      throw new Error(
        "AI notes were not returned by the backend."
      );
    }

    setAiNotes(data.notes);

    setUploadStatus(
      "✅ AI study notes generated successfully!"
    );

    // Scroll to notes
    setTimeout(() => {
      document
        .getElementById("ai-notes-section")
        ?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
    }, 300);

  } catch (error) {
    console.error(
      "❌ AI Notes Error:",
      error
    );

    setUploadStatus(
      `❌ Failed to generate AI notes: ${error.message}`
    );

    alert(
      `AI Notes generation failed: ${error.message}`
    );

  } finally {
    setNotesLoading(false);
  }
};

// ============================================================
// GENERATE AI FLASHCARDS
// ============================================================

const handleGenerateFlashcards = async () => {
  if (!selectedFile) {
    alert("Please upload a PDF first.");
    return;
  }

  try {
    setFlashcardsLoading(true);

    setUploadStatus(
      "🧠 Gemini AI is generating flashcards from your PDF..."
    );

    console.log(
      "🗂️ Generating AI Flashcards for:",
      selectedFile.name
    );

    const data = await apiRequest(
      `${API_URL}/api/generate-flashcards?filename=${encodeURIComponent(
        selectedFile.name
      )}&number_of_cards=10`,
      {
        method: "POST",
      }
    );

    console.log(
      "✅ Flashcards generated:",
      data
    );

    if (
      !data.flashcards ||
      data.flashcards.length === 0
    ) {
      throw new Error(
        "No flashcards were generated."
      );
    }

    setFlashcards(data.flashcards);
    setFlashcardIndex(0);
    setFlashcardFlipped(false);

    setUploadStatus(
      "✅ AI flashcards generated successfully!"
    );

    setTimeout(() => {
      document
        .getElementById("flashcards-section")
        ?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
    }, 300);

  } catch (error) {
    console.error(
      "❌ Flashcard Error:",
      error
    );

    setUploadStatus(
      `❌ Failed to generate flashcards: ${error.message}`
    );

    alert(
      `Flashcard generation failed: ${error.message}`
    );

  } finally {
    setFlashcardsLoading(false);
  }
};


// ============================================================
// FLASHCARD NAVIGATION
// ============================================================

const handleNextFlashcard = () => {
  if (
    flashcardIndex <
    flashcards.length - 1
  ) {
    setFlashcardIndex(
      (previous) => previous + 1
    );

    setFlashcardFlipped(false);
  }
};

const handlePreviousFlashcard = () => {
  if (flashcardIndex > 0) {
    setFlashcardIndex(
      (previous) => previous - 1
    );

    setFlashcardFlipped(false);
  }
};

const handleShuffleFlashcards = () => {
  const shuffled = [...flashcards].sort(
    () => Math.random() - 0.5
  );

  setFlashcards(shuffled);
  setFlashcardIndex(0);
  setFlashcardFlipped(false);
};



  // ============================================================
  // HANDLE ANSWER
  // ============================================================

  const handleAnswerChange = (questionId, answer) => {
  const now = Date.now();

  setSelectedAnswers((previous) => ({
    ...previous,
    [questionId]: answer,
  }));
  



  setQuestionTimes((previous) => {
    if (previous[questionId]) {
      return previous;
    }

    const startTime = questionStartTimes[questionId];

    if (!startTime) {
      return previous;
    }

    const seconds = Math.max(
      1,
      Math.round((now - startTime) / 1000)
    );

    return {
      ...previous,
      [questionId]: seconds,
    };
  });

  if (score !== null) {
    setScore(null);
  }

  if (learningAnalysis !== null) {
    setLearningAnalysis(null);
  }

  if (personalizedPath !== null) {
    setPersonalizedPath(null);
  }

  if (studyWasteAnalysis !== null) {
    setStudyWasteAnalysis(null);
  }
  if (recoveryAnalysis !== null) {
  setRecoveryAnalysis(null);
}
if (explainAnalysis !== null) {
  setExplainAnalysis(null);
}
};

useEffect(() => {
  if (!quiz || quiz.length === 0) {
    return;
  }

  const now = Date.now();

  setQuestionStartTimes((previous) => {
    const updated = { ...previous };

    quiz.forEach((item, index) => {
      const questionId = item.id ?? `question-${index}`;

      if (!updated[questionId]) {
        updated[questionId] = now;
      }
    });

    return updated;
  });
}, [quiz]);

  // ============================================================
  // NORMALIZE TEXT
  // ============================================================

  const normalizeText = (text) => {
    return String(text || "")
      .toLowerCase()
      .replace(/[^\w\s]/g, "")
      .replace(/\s+/g, " ")
      .trim();
  };

  // ============================================================
// CONFUSION DETECTOR
// ============================================================

const handleDetectConfusion = async (item, index) => {
  const questionId = getQuestionKey(item, index);

  const studentAnswer =
    selectedAnswers[questionId] || "";

  const correctAnswer =
    item.correct_answer ??
    item.answer ??
    "";

  if (!studentAnswer.trim()) {
    alert("Please answer this question first.");
    return;
  }

  try {
    setConfusionLoading((previous) => ({
      ...previous,
      [questionId]: true,
    }));

    const data = await apiRequest(
      `${API_URL}/api/confusion-detector`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          question: item.question || "",

          correct_answer:
            correctAnswer,

          student_answer:
            studentAnswer,

          explanation:
            item.explanation ||
            "Review the learning material.",

          topic:
            item.topic ||
            "General",
        }),
      }
    );

    console.log(
      "🧠 Confusion Detector:",
      data
    );

    setConfusionAnalysis((previous) => ({
      ...previous,
      [questionId]: data,
    }));

  } catch (error) {
    console.error(
      "❌ Confusion Detector Error:",
      error
    );

    alert(
      `Confusion analysis failed: ${error.message}`
    );

  } finally {
    setConfusionLoading((previous) => ({
      ...previous,
      [questionId]: false,
    }));
  }
};

  // ============================================================
  // BUILD ANALYZED QUESTIONS
  // ============================================================

  const buildAnalyzedQuestions = () => {
    return quiz.map((item, index) => {
      const questionId =
        getQuestionKey(item, index);

      const userAnswer =
        selectedAnswers[questionId] || "";

      // Gemini may return correct_answer.
      // answer is kept as fallback.
      const correctAnswer =
        item.correct_answer ??
        item.answer ??
        "";

      const correct =
        normalizeText(userAnswer) ===
        normalizeText(correctAnswer);

      return {
        id: item.id ?? questionId,

        question: item.question || "",

        options: Array.isArray(item.options)
          ? item.options
          : [],

        answer: correctAnswer,

        correct_answer: correctAnswer,

        explanation:
          item.explanation ||
          "Review the learning material and try this question again.",

        topic: item.topic || "General",

        user_answer: userAnswer,

        is_correct: correct,
      };
    });
  };

  // ============================================================
  // ANSWERED COUNT
  // ============================================================

  const answeredCount = Object.keys(
    selectedAnswers
  ).filter(
    (id) =>
      selectedAnswers[id]?.trim()
  ).length;

  // ============================================================
  // PROGRESS
  // ============================================================

  const progress =
    quiz.length > 0
      ? Math.round(
          (answeredCount / quiz.length) * 100
        )
      : 0;

      // ============================================================
// EXPLAIN-TO-LEARN AI
// ============================================================

const handleExplainToLearn = async (item) => {
  try {
    setExplainLoading(true);
    setExplainAnalysis(null);

    console.log("🧠 Explain item:", item);

    const question =
      item.question ||
      "";

    const topic =
      item.topic ||
      "General";

    const studentAnswer =
      item.student_answer ||
      item.studentAnswer ||
      "";

    const correctAnswer =
      item.correct_answer ??
      item.correctAnswer ??
      item.answer ??
      item.expected_answer ??
      item.expectedAnswer ??
      "";

    console.log("📤 Explain-to-Learn Payload:", {
      question,
      topic,
      student_answer: studentAnswer,
      correct_answer: correctAnswer,
    });

    if (!question) {
      throw new Error("Question data is missing.");
    }

    if (!correctAnswer) {
      throw new Error(
        "Correct answer data is missing for this recovery question."
      );
    }

    const response = await apiRequest(
      `${API_URL}/api/explain-to-learn`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          question: question,
          topic: topic,
          student_answer: studentAnswer,
          correct_answer: correctAnswer,
        }),
      }
    );

    console.log(
      "🧠 Explain-to-Learn Response:",
      response
    );

    setExplainAnalysis(response);

  } catch (error) {

    console.error(
      "❌ Explain-to-Learn Error:",
      error
    );

    setUploadStatus(
      `❌ ${error.message}`
    );

  } finally {

    setExplainLoading(false);

  }
};

  // ============================================================
  // SUBMIT QUIZ
  // ============================================================

  const calculateScore = async () => {
    if (quiz.length === 0) {
      alert("Please generate a quiz first.");
      return;
    }

    // ==========================================
// ⏱️ STUDY WASTE DETECTOR
// ==========================================

try {
  setStudyWasteLoading(true);

  const questionTimesData = quiz.map((item, index) => {
    const questionId = getQuestionKey(item, index);

    const correctAnswer =
      item.correct_answer ?? item.answer ?? "";

    const studentAnswer =
      selectedAnswers[questionId] ?? "";

    const isCorrect =
      studentAnswer.trim().toLowerCase() ===
      correctAnswer.trim().toLowerCase();

    return {
  question: item.question || "",
  topic: item.topic || "General",
  student_answer: studentAnswer,
  correct_answer: correctAnswer,
  time_spent: questionTimes[questionId] || 0,
  is_correct: isCorrect,
};
  });

  const wasteResponse = await apiRequest(
    `${API_URL}/api/study-waste-detector`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question_times: questionTimesData,
        total_session_time: questionTimesData.reduce(
          (total, item) => total + item.time_spent,
          0
        ),
      }),
    }
  );

  console.log(
    "⏱️ Study Waste Detector:",
    wasteResponse
  );

  setStudyWasteAnalysis(wasteResponse);
  // ============================================================
// QUESTION INTELLIGENCE
// ============================================================

try {
  setQuestionIntelligenceLoading(true);

  const intelligenceResponse = await apiRequest(
    `${API_URL}/api/question-intelligence`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        questions: questionTimesData,
      }),
    }
  );

  console.log(
    "🧠 Question Intelligence:",
    intelligenceResponse
  );

  setQuestionIntelligence(intelligenceResponse);


  // ============================================================
// RECOVERY MODE
// ============================================================

try {
  setRecoveryLoading(true);

  // questionTimesData already contains:
  // question, topic, student_answer, correct_answer,
  // time_spent, and is_correct.
  // Reuse it instead of creating a second recovery payload.
  const recoveryQuestions = questionTimesData.map((item) => ({
    question: item.question || "",
    topic: item.topic || "General",
    student_answer: item.student_answer || "",
    correct_answer: item.correct_answer || "",
    time_spent: item.time_spent || 0,
    is_correct: Boolean(item.is_correct),
  }));

  console.log(
    "🔄 Recovery Mode Request:",
    recoveryQuestions
  );

  const recoveryResponse = await apiRequest(
    `${API_URL}/api/recovery-mode`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        questions: recoveryQuestions,
      }),
    }
  );

  console.log(
    "🔄 Recovery Mode Response:",
    recoveryResponse
  );

  setRecoveryAnalysis(recoveryResponse);

} catch (error) {
  console.error(
    "❌ Recovery Mode Error:",
    error
  );
} finally {
  setRecoveryLoading(false);
}



} catch (error) {
  console.error(
    "❌ Question Intelligence Error:",
    error
  );
} finally {
  setQuestionIntelligenceLoading(false);
}

} catch (error) {
  console.error(
    "❌ Study Waste Detector Error:",
    error
  );
} finally {
  setStudyWasteLoading(false);
}

    // IMPORTANT:
    // User must answer every question.
    if (answeredCount < quiz.length) {
      alert(
        `Please answer all ${quiz.length} questions before submitting.`
      );
      return;
    }

    let correct = 0;

    const analyzedQuestions =
      buildAnalyzedQuestions();

    analyzedQuestions.forEach((question) => {
      if (question.is_correct) {
        correct++;
      }
    });

    // Set score
    setScore(correct);


// ==========================================================
// SAVE QUIZ HISTORY
// ==========================================================

try {
  const token = localStorage.getItem("edumind_token");

  if (token) {
    const topic =
      detectedTopics.length > 0
        ? detectedTopics[0]
        : selectedFile
        ? selectedFile.name.replace(/\.pdf$/i, "")
        : "Uploaded Material";

    const quizHistoryData = {
      quiz_title: selectedFile
        ? selectedFile.name.replace(/\.pdf$/i, "")
        : "Generated Quiz",

      topic: topic,

      score: correct,

      total_questions: quiz.length,

      percentage:
        quiz.length > 0
          ? Number(((correct / quiz.length) * 100).toFixed(2))
          : 0,

      result:
        correct === quiz.length
          ? "Excellent"
          : correct >= quiz.length * 0.6
          ? "Passed"
          : "Needs Improvement",
    };

    await apiRequest(
      `${API_URL}/api/history/quiz`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },

        body: JSON.stringify(quizHistoryData),
      }
    );

    console.log(
      "Quiz history saved successfully:",
      quizHistoryData
    );
  } else {
    console.log(
      "No login token found. Quiz history was not saved."
    );
  }
} catch (error) {
  console.error(
    "Quiz history save error:",
    error
  );

  // History failure should not stop quiz evaluation.
}
    // ==========================================================
// ADAPTIVE LEARNING
// ==========================================================

await handleAnalyzeAdaptiveLearning(
  analyzedQuestions,
  correct,
  quiz.length
);

    setUploadStatus(
      `🎯 Quiz evaluated! You scored ${correct}/${quiz.length}.`
    );

    // ==========================================================
    // SAVE PROGRESS TO DATABASE
    // ==========================================================

    try {
      const token =
        localStorage.getItem("edumind_token");

      if (token) {
        const topic =
          detectedTopics.length > 0
            ? detectedTopics[0]
            : selectedFile
            ? selectedFile.name.replace(
                /\.pdf$/i,
                ""
              )
            : "Uploaded Material";

        const progressData = {
          topic: topic,
          score: correct,
          total_questions: quiz.length,
          completed: true,
        };

        await apiRequest(
          `${API_URL}/api/progress/save`,
          {
            method: "POST",

            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },

            body: JSON.stringify(
              progressData
            ),
          }
        );

        console.log(
          "Progress saved successfully:",
          progressData
        );
      } else {
        console.log(
          "No login token found. Progress was not saved."
        );
      }
    } catch (error) {
      console.error(
        "Progress save error:",
        error
      );

      // Do not stop quiz results if progress saving fails.
      setUploadStatus(
        `🎯 Quiz completed! Score: ${correct}/${quiz.length}. Progress could not be saved.`
      );
    }

    // ==========================================================
    // LEARNING ANALYSIS
    // ==========================================================

    try {
      setLoadingLearningPath(true);

      const data = await apiRequest(
        `${API_URL}/api/learning-path`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            score: correct,
            total_questions: quiz.length,
            questions: analyzedQuestions,
          }),
        }
      );

      console.log(
        "Learning Analysis:",
        data
      );

      setLearningAnalysis(data);

      setUploadStatus(
        "✅ Quiz analyzed and learning recommendations generated."
      );

      setTimeout(() => {
        document
          .getElementById("quiz-result")
          ?.scrollIntoView({
            behavior: "smooth",
            block: "center",
          });
      }, 300);
    } catch (error) {
      console.error(
        "Learning analysis error:",
        error
      );

      setUploadStatus(
        `⚠️ Quiz completed, but learning analysis failed: ${error.message}`
      );
    } finally {
      setLoadingLearningPath(false);
    }
  };

  // ============================================================
  // DETECT TOPICS
  // ============================================================

  const handleDetectTopics = async () => {
    if (!selectedFile) {
      alert("Please upload a PDF first.");
      return;
    }

    try {
      setDetectingTopics(true);

      setUploadStatus(
        "🧠 Detecting topics from your learning material..."
      );

      const data = await apiRequest(
        `${API_URL}/api/detect-topics?filename=${encodeURIComponent(
          selectedFile.name
        )}`,
        {
          method: "POST",
        }
      );

      console.log(
        "Detected Topics:",
        data
      );

      const rawTopics = Array.isArray(
        data.topics
      )
        ? data.topics
        : [];

      const topics = rawTopics.map(
        (topic) => {
          if (typeof topic === "string") {
            return topic;
          }

          if (
            typeof topic === "object" &&
            topic !== null
          ) {
            return (
              topic.topic ||
              topic.name ||
              topic.title ||
              "Unknown Topic"
            );
          }

          return String(topic);
        }
      );

      setDetectedTopics(topics);

      if (topics.length === 0) {
        setUploadStatus(
          "⚠️ No topics were detected."
        );
        return;
      }

      setUploadStatus(
        `✅ ${topics.length} topics detected successfully!`
      );

      setTimeout(() => {
        document
          .getElementById("topics-section")
          ?.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
      }, 300);
    } catch (error) {
      console.error(
        "Topic detection error:",
        error
      );

      setUploadStatus(
        `❌ ${error.message}`
      );
    } finally {
      setDetectingTopics(false);
    }
  };

  // ============================================================
  // DETECT SKILL GAPS
  // ============================================================

  // ============================================================
// DETECT SKILL GAPS
// ============================================================

const handleDetectSkillGaps = async () => {

  // ----------------------------------------------------------
  // 1. CHECK PDF
  // ----------------------------------------------------------

  if (!selectedFile) {
    alert("Please upload a PDF first.");
    return;
  }


  // ----------------------------------------------------------
  // 2. CHECK QUIZ
  // ----------------------------------------------------------

  if (quiz.length === 0) {
    alert(
      "Please generate and complete the quiz first."
    );
    return;
  }


  // ----------------------------------------------------------
  // 3. CHECK SCORE
  // ----------------------------------------------------------

  if (score === null) {
    alert(
      "Please submit the quiz first."
    );
    return;
  }


  try {

    setDetectingSkillGaps(true);

    setUploadStatus(
      "🧠 AI is preparing your skill gap analysis..."
    );


    // --------------------------------------------------------
    // 4. GET TOPICS
    // --------------------------------------------------------

    let topics = detectedTopics || [];


    // If topics were already detected, use them.
    // Otherwise automatically detect them now.
    if (topics.length === 0) {

      setUploadStatus(
        "🏷️ Detecting topics from your learning material..."
      );

      console.log(
        "🏷️ Topics not detected yet. Detecting automatically..."
      );


      const topicData = await apiRequest(
        `${API_URL}/api/detect-topics?filename=${encodeURIComponent(
          selectedFile.name
        )}`,
        {
          method: "POST",
        }
      );


      console.log(
        "🏷️ Automatic Topic Detection:",
        topicData
      );


      const rawTopics = Array.isArray(
        topicData.topics
      )
        ? topicData.topics
        : [];


      topics = rawTopics.map((topic) => {

        if (typeof topic === "string") {
          return topic;
        }


        if (
          typeof topic === "object" &&
          topic !== null
        ) {
          return (
            topic.topic ||
            topic.name ||
            topic.title ||
            "Unknown Topic"
          );
        }


        return String(topic);

      });


      // Save topics into React state
      setDetectedTopics(topics);


      // If still no topics were found
      if (topics.length === 0) {

        setUploadStatus(
          "⚠️ No topics could be detected from this PDF."
        );

        alert(
          "No topics could be detected from this learning material."
        );

        return;
      }

    }


    // --------------------------------------------------------
    // 5. BUILD QUESTION ANALYSIS
    // --------------------------------------------------------

    const questions =
      buildAnalyzedQuestions();


    console.log(
      "📊 Skill Gap Input:",
      {
        filename: selectedFile.name,
        topics: topics,
        score: score,
        total_questions: quiz.length,
        questions: questions,
      }
    );


    // --------------------------------------------------------
    // 6. CALL SKILL GAP API
    // --------------------------------------------------------

    setUploadStatus(
      "🧠 AI is analyzing your skill gaps..."
    );


    const data = await apiRequest(
      `${API_URL}/api/skill-gaps`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({

          filename:
            selectedFile.name,

          topics:
            topics,

          score:
            score,

          total_questions:
            quiz.length,

          questions:
            questions,

        }),
      }
    );


    console.log(
      "🎯 Skill Gap Analysis:",
      data
    );


    // --------------------------------------------------------
    // 7. SAVE RESULTS
    // --------------------------------------------------------

    const gaps =
      data.skill_gaps || [];


    setSkillGaps(gaps);
    await handleLoadNsstaRecommendations(gaps);



    // --------------------------------------------------------
    // 8. LOAD iGoT RECOMMENDATIONS
    // --------------------------------------------------------

    if (
      typeof handleLoadIgotRecommendations ===
      "function"
    ) {

      
      await handleLoadIgotRecommendations(
        gaps
      );


    }
    


    // --------------------------------------------------------
    // 9. SUCCESS MESSAGE
    // --------------------------------------------------------

    setUploadStatus(
      `✅ Skill gap analysis completed! ${gaps.length} areas need attention.`
    );


    // --------------------------------------------------------
    // 10. SCROLL TO RESULTS
    // --------------------------------------------------------

    setTimeout(() => {

      document
        .getElementById(
          "skill-gap-section"
        )
        ?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });

    }, 300);


  } catch (error) {

    console.error(
      "❌ Skill gap analysis error:",
      error
    );


    setUploadStatus(
      `❌ ${error.message}`
    );


    alert(
      `Skill gap analysis failed: ${error.message}`
    );


  } finally {

    setDetectingSkillGaps(false);

  }

};

 // ============================================================
// STEP 21 - AI REVISION
// ============================================================

const handleGenerateRevision = async (topics = []) => {
  try {
    setLoadingRevision(true);

    console.log("🔄 Starting AI Revision...");
    console.log("📚 Revision topics received:", topics);

    const token =
      localStorage.getItem("token") ||
      localStorage.getItem("access_token") ||
      localStorage.getItem("edumind_token");

    if (!token) {
      console.error("❌ No authentication token found.");
      alert("Please login again.");
      return;
    }

    const normalizedTopics = (topics || [])
      .map((topic) => {
        if (typeof topic === "string") {
          return topic.trim();
        }

        if (typeof topic === "object" && topic !== null) {
          return (
            topic.topic ||
            topic.skill ||
            topic.name ||
            ""
          ).toString().trim();
        }

        return "";
      })
      .filter(Boolean);

    console.log(
      "📚 Normalized revision topics:",
      normalizedTopics
    );

    if (normalizedTopics.length === 0) {
      console.warn("⚠️ No topics available for revision.");
      alert(
        "No revision topics are available. Please analyze your skill gaps first."
      );
      setRevisionQuestions([]);
      return;
    }

    setRevisionTopics(normalizedTopics);

    console.log(
      "📡 Sending request to AI Revision API..."
    );

    const response = await fetch(
      "http://127.0.0.1:8000/api/revision/practice",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(normalizedTopics),
      }
    );

    console.log(
      "📡 AI Revision response status:",
      response.status
    );

    const data = await response.json();

    console.log("📦 AI Revision response:", data);

    if (!response.ok) {
      throw new Error(
        data.detail ||
          "Failed to generate AI revision"
      );
    }

    const questions =
      data.revision?.questions || [];

    console.log(
      "✅ Revision questions received:",
      questions
    );

    setRevisionQuestions(questions);

  } catch (error) {
    console.error(
      "❌ AI Revision error:",
      error
    );

    alert(
      "AI Revision generation failed. Please try again."
    );

    setRevisionQuestions([]);

  } finally {
    setLoadingRevision(false);
  }
}; 

// ============================================================
// AI REVISION - HANDLE ANSWER
// ============================================================

const handleRevisionAnswer = (questionIndex, answer) => {
  setRevisionAnswers((previous) => ({
    ...previous,
    [questionIndex]: answer,
  }));

  console.log(
    "📝 Revision answer stored:",
    questionIndex,
    answer
  );
};
// ============================================================
// AI REVISION - SUBMIT
// ============================================================

const handleSubmitRevision = () => {
  if (revisionQuestions.length === 0) {
    alert("No revision questions available.");
    return;
  }

  const unanswered = revisionQuestions.filter(
    (_, index) =>
      !revisionAnswers[index]
  );

  if (unanswered.length > 0) {
    alert(
      `Please answer all ${revisionQuestions.length} revision questions before submitting.`
    );
    return;
  }

  let correctCount = 0;

  revisionQuestions.forEach(
    (question, index) => {
      const userAnswer =
        revisionAnswers[index] || "";

      const correctAnswer =
        question.correct_answer ??
        question.answer ??
        "";

      if (
        normalizeText(userAnswer) ===
        normalizeText(correctAnswer)
      ) {
        correctCount++;
      }
    }
  );

  setRevisionScore(correctCount);
  setRevisionSubmitted(true);

  console.log(
    "🎯 AI Revision Score:",
    correctCount,
    "/",
    revisionQuestions.length
  );
};

  

// ============================================================
  // STEP 20 - PRACTICE WEAK SKILL
  // ============================================================

const handlePracticeWeakTopic = async (topic) => {
  if (!topic) {
    alert("Invalid weak skill.");
    return;
  }

  try {
    setGeneratingPracticeQuiz(true);
    setPracticeTopic(topic);

    setUploadStatus(
      `🧠 Generating weak-skill practice for "${topic}"...`
    );

    const token =
      localStorage.getItem("edumind_token") ||
      localStorage.getItem("token") ||
      localStorage.getItem("access_token");

    if (!token) {
      alert("Please login again.");
      return;
    }

    const response = await fetch(
      `${API_URL}/api/weak-skill/practice`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },

        body: JSON.stringify([
          {
            skill: topic,
            level: "Needs Practice",
          },
        ]),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail ||
          data.message ||
          `Request failed with status ${response.status}`
      );
    }

    console.log(
      "🧠 Weak Skill Practice Response:",
      data
    );

    const newQuestions =
      data?.practice?.questions || [];

    if (!Array.isArray(newQuestions) || newQuestions.length === 0) {
      setUploadStatus(
        `⚠️ No practice questions were generated for "${topic}".`
      );
      return;
    }

    // Load generated questions into the existing quiz UI
    setQuiz(newQuestions);

    // Reset quiz state
    setSelectedAnswers({});
    setScore(null);

    // Clear old analysis
    setLearningAnalysis(null);
    setPersonalizedPath(null);

    setUploadStatus(
      `✅ ${newQuestions.length} weak-skill practice questions generated for "${topic}"!`
    );

    // Scroll to existing quiz section
    setTimeout(() => {
      document
        .getElementById("quiz-section")
        ?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
    }, 300);

  } catch (error) {
    console.error(
      "❌ Weak Skill Practice Error:",
      error
    );

    setUploadStatus(
      `❌ ${error.message}`
    );

  } finally {
    setGeneratingPracticeQuiz(false);
  }
};


// ============================================================
// ADAPTIVE LEARNING ANALYSIS
// ============================================================

const handleAnalyzeAdaptiveLearning = async (
  analyzedQuestions,
  quizScore,
  totalQuestions
) => {
  if (
    !Array.isArray(analyzedQuestions) ||
    analyzedQuestions.length === 0
  ) {
    console.warn(
      "No analyzed questions available for adaptive learning."
    );
    return;
  }

  try {
    setAdaptiveLoading(true);

    const token =
      localStorage.getItem("edumind_token") ||
      localStorage.getItem("token") ||
      localStorage.getItem("access_token");

    if (!token) {
      console.warn(
        "No authentication token found for adaptive learning."
      );
      return;
    }

    const response = await fetch(
      `${API_URL}/api/adaptive/analyze`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },

        body: JSON.stringify({
          score: quizScore,
          total_questions: totalQuestions,
          questions: analyzedQuestions,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail ||
          "Failed to analyze adaptive learning."
      );
    }

    console.log(
      "🧠 Adaptive Learning Analysis:",
      data
    );

    setAdaptiveAnalysis(
      data.adaptive_analysis || null
    );

  } catch (error) {
    console.error(
      "❌ Adaptive Learning Error:",
      error
    );

    setAdaptiveAnalysis(null);

  } finally {
    setAdaptiveLoading(false);
  }
};

  // ============================================================
  // CREATE PERSONALIZED LEARNING PATH
  // ============================================================

  const handleCreateLearningPath =
    async () => {
      if (quiz.length === 0) {
        alert(
          "Please complete the quiz first."
        );
        return;
      }

      if (score === null) {
        alert(
          "Please submit the quiz first."
        );
        return;
      }

      try {
        setCreatingLearningPath(
          true
        );

        setUploadStatus(
          "🚀 Creating your personalized learning path..."
        );

        const analyzedQuestions =
          buildAnalyzedQuestions();

        const data = await apiRequest(
          `${API_URL}/api/learning-path`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({
              score: score,

              total_questions:
                quiz.length,

              questions:
                analyzedQuestions,
            }),
          }
        );

        console.log(
          "Personalized Learning Path:",
          data
        );

        setPersonalizedPath(data);

        setUploadStatus(
          "✅ Personalized learning path created successfully!"
        );

        setTimeout(() => {
          document
            .getElementById(
              "personalized-path-section"
            )
            ?.scrollIntoView({
              behavior: "smooth",
              block: "start",
            });
        }, 300);
      } catch (error) {
        console.error(
          "Personalized learning path error:",
          error
        );

        setUploadStatus(
          `❌ ${error.message}`
        );
      } finally {
        setCreatingLearningPath(
          false
        );
      }
    };

  // ============================================================
  // RETAKE QUIZ
  // ============================================================

  const retakeQuiz = () => {
    setSelectedAnswers({});
    setScore(null);
    setLearningAnalysis(null);
    setAdaptiveAnalysis(null);
    setSkillGaps([]);
    setPersonalizedPath(null);
    setAdaptiveAnalysis(null);
    setRecoveryAnalysis(null);
    setExplainAnalysis(null);
    setConfusionAnalysis({});
    setConfusionLoading({});

    setUploadStatus(
      "🔄 Quiz reset. Try again!"
    );

    setTimeout(() => {
      document
        .getElementById("quiz-section")
        ?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
    }, 200);
  };

  // ============================================================
  // AI TUTOR
  // ============================================================

  // ============================================================
// AI TUTOR
// ============================================================

const handleAskTutor = async () => {
  const question =
    tutorQuestion.trim();

  if (!question) {
    alert(
      "Please enter your question."
    );

    return;
  }

  try {
    setAskingTutor(true);

    const data = await apiRequest(
      `${API_URL}/ai-tutor`,
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json",
        },

        body: JSON.stringify({
          question: question,

          language: selectedLanguage,

          context: selectedFile
            ? `Learning material: ${selectedFile.name}`
            : "",

          topic:
            detectedTopics.length > 0
              ? detectedTopics.join(", ")
              : "General",
        }),
      }
    );

    console.log(
      "🤖 AI Tutor response:",
      data
    );

    console.log(
      "🌐 Tutor Language:",
      selectedLanguage
    );

    const answer =
      data.answer ||
      data.response ||
      "No answer received from AI Tutor.";

    setTutorHistory(
      (previous) => [
        ...previous,

        {
          question: question,
          answer: answer,
        },
      ]
    );

    setTutorAnswer(answer);
    setTutorQuestion("");

  } catch (error) {
    console.error(
      "❌ AI Tutor error:",
      error
    );

    setTutorAnswer(
      `❌ ${error.message}`
    );

  } finally {
    setAskingTutor(false);
  }
};

  // ============================================================
  // CLEAR TUTOR CHAT
  // ============================================================

  const clearTutorChat = () => {
    setTutorHistory([]);
    setTutorAnswer("");
    setTutorQuestion("");
  };

  // ============================================================
  // RESTORE LOGIN SESSION
  // ============================================================




  // STEP 25.1 — RESTORE LOGIN SESSION
  useEffect(() => {
    const savedUser = localStorage.getItem("edumind_user");
    const token = localStorage.getItem("edumind_token");

    if (!savedUser || !token) {
      return;
    }

    try {
      const parsedUser = JSON.parse(savedUser);

      // Restore the saved session immediately.
      setCurrentUser(parsedUser);

      // Refresh the role from the backend when the saved user object
      // comes from an older login response that did not contain role.
      if (!parsedUser?.role) {
        fetch(`${API_URL}/api/admin/dashboard`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
          .then((response) => {
            const role = response.ok ? "admin" : "learner";
            const updatedUser = {
              ...parsedUser,
              role,
            };
            setCurrentUser(updatedUser);
            localStorage.setItem(
              "edumind_user",
              JSON.stringify(updatedUser)
            );
          })
          .catch((error) => {
            console.warn("Could not refresh user role:", error);
            const updatedUser = {
              ...parsedUser,
              role: "learner",
            };
            setCurrentUser(updatedUser);
            localStorage.setItem(
              "edumind_user",
              JSON.stringify(updatedUser)
            );
          });
      }
    } catch (error) {
      console.error("Failed to restore login session:", error);
      localStorage.removeItem("edumind_user");
      localStorage.removeItem("edumind_token");
    }
  }, []);

  useEffect(() => {
  localStorage.setItem(
    "edumind_theme",
    darkMode ? "dark" : "light"
  );
}, [darkMode]);

// ============================================================
// ⏱️ START QUESTION TIMERS
// ============================================================

useEffect(() => {
  if (!quiz || quiz.length === 0) {
    return;
  }

  const now = Date.now();

  setQuestionStartTimes((previous) => {
    const updated = { ...previous };

    quiz.forEach((item, index) => {
      const questionId = getQuestionKey(item, index);

      if (!updated[questionId]) {
        updated[questionId] = now;
      }
    });

    return updated;
  });
}, [quiz]);



  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div className={`app ${darkMode ? "dark-mode" : ""}`}>

      {/* ======================================================
          LOGIN MODAL
      ====================================================== */}

      {showLogin && (
        <div
          className="login-overlay"
          onClick={() =>
            setShowLogin(false)
          }
        >
          <div
            className="login-card"
            onClick={(e) =>
              e.stopPropagation()
            }
          >

            <button
              className="login-close"
              onClick={() =>
                setShowLogin(false)
              }
              aria-label="Close login"
            >
              ✕
            </button>

            <div className="login-icon">
              🎓
            </div>

            <h2>
              Welcome Back
            </h2>

            <p>
              Login to continue learning
              with EduMind AI.
            </p>

            <form
              onSubmit={handleLogin}
            >

              <div className="login-field">
                <label>
                  Email Address
                </label>

                <input
                  type="email"
                  value={loginEmail}
                  onChange={(e) =>
                    setLoginEmail(
                      e.target.value
                    )
                  }
                  placeholder="Enter your email"
                  autoComplete="email"
                  required
                />
              </div>

              <div className="login-field">
                <label>
                  Password
                </label>

                <input
                  type="password"
                  value={loginPassword}
                  onChange={(e) =>
                    setLoginPassword(
                      e.target.value
                    )
                  }
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  required
                />
              </div>

              <button
                type="submit"
                className="login-submit-btn"
                disabled={authLoading}
              >
                {authLoading
                  ? "⏳ Logging in..."
                  : "🔐 Login"}
              </button>

            </form>

            <div className="login-register">

              <span>
                Don't have an account?
              </span>

              <button
                type="button"
                onClick={() => {
                  setShowLogin(false);
                  setShowRegister(true);
                }}
              >
                Create Account
              </button>

            </div>

          </div>
        </div>
      )}

      {/* ======================================================
          REGISTER MODAL
      ====================================================== */}

      {showRegister && (
        <div
          className="login-overlay"
          onClick={() =>
            setShowRegister(false)
          }
        >
          <div
            className="login-card"
            onClick={(e) =>
              e.stopPropagation()
            }
          >

            <button
              className="login-close"
              onClick={() =>
                setShowRegister(false)
              }
              aria-label="Close register"
            >
              ✕
            </button>

            <div className="login-icon">
              📝
            </div>

            <h2>
              Create Account
            </h2>

            <p>
              Create your EduMind AI
              learning account.
            </p>

            <form
              onSubmit={handleRegister}
            >

              <div className="login-field">

                <label>
                  Full Name
                </label>

                <input
                  type="text"
                  value={registerName}
                  onChange={(e) =>
                    setRegisterName(
                      e.target.value
                    )
                  }
                  placeholder="Enter your full name"
                  autoComplete="name"
                  required
                />

              </div>

              <div className="login-field">

                <label>
                  Email Address
                </label>

                <input
                  type="email"
                  value={registerEmail}
                  onChange={(e) =>
                    setRegisterEmail(
                      e.target.value
                    )
                  }
                  placeholder="Enter your email"
                  autoComplete="email"
                  required
                />

              </div>

              <div className="login-field">

                <label>
                  Password
                </label>

                <input
                  type="password"
                  value={registerPassword}
                  onChange={(e) =>
                    setRegisterPassword(
                      e.target.value
                    )
                  }
                  placeholder="Create a password"
                  autoComplete="new-password"
                  required
                />

              </div>

              <div className="login-field">

                <label>
                  Confirm Password
                </label>

                <input
                  type="password"
                  value={
                    registerConfirmPassword
                  }
                  onChange={(e) =>
                    setRegisterConfirmPassword(
                      e.target.value
                    )
                  }
                  placeholder="Confirm your password"
                  autoComplete="new-password"
                  required
                />

              </div>

              {/* ONLY ONE REGISTER SUBMIT BUTTON */}

              <button
                type="submit"
                className="login-submit-btn"
                disabled={authLoading}
              >
                {authLoading
                  ? "⏳ Creating Account..."
                  : "🚀 Create Account"}
              </button>

            </form>

            <div className="login-register">

              <span>
                Already have an account?
              </span>

              <button
                type="button"
                onClick={() => {
                  setShowRegister(false);
                  setShowLogin(true);
                }}
              >
                Login
              </button>

            </div>

          </div>
        </div>
      )}

      {/* ======================================================
          HIDDEN FILE INPUT
      ====================================================== */}

      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,application/pdf"
        onChange={handleFileChange}
        hidden
      />

      {/* ======================================================
          NAVBAR
      ====================================================== */}

      <nav className="navbar">

        <div className="logo">

          <div className="logo-icon">
            🎓
          </div>

          <div className="logo-text">

            <h2>
              EduMind AI
            </h2>

            <span>
              Personalized Learning
            </span>

          </div>

        </div>

        <div className="nav-links">

          <a href="#home">
            Home
          </a>

          <a href="#features">
            Features
          </a>

          <a href="#about">
            About
          </a>
          <a href="#dashboard">Dashboard</a>

          {isAdminUser && (
            <button
              className="secondary-btn"
              type="button"
              onClick={handleOpenAdminDashboard}
              style={{
                padding: "8px 14px",
                fontSize: "13px",
                margin: 0,
              }}
            >
              🛡️ Administrator
            </button>
          )}

          {currentUser ? (
            <>
              <div
                className="user-session-badge"
                style={{
                  padding: "8px 14px",
                  borderRadius: "10px",
                  background: "rgba(124, 58, 237, 0.14)",
                  border: "1px solid rgba(124, 58, 237, 0.30)",
                  color: "#e2e8f0",
                  fontSize: "13px",
                  fontWeight: 600,
                  whiteSpace: "nowrap",
                }}
              >
                👤 {currentUser?.name || "User"}
              </div>

              <button
                className="login-btn"
                type="button"
                onClick={() => {
                  localStorage.removeItem("edumind_token");
                  localStorage.removeItem("edumind_user");
                  setCurrentUser(null);
                  setShowAdminAccess(false);
                  setAdminDashboard(null);
                  setAdminDashboardError("");
                }}
              >
                🚪 Logout
              </button>
            </>
          ) : (
            <button
              className="login-btn"
              type="button"
              onClick={() => setShowLogin(true)}
            >
              🔐 Login
            </button>
          )}

          {/* 🌐 LANGUAGE SELECTOR */}
<div className="language-selector">
  <span>🌐</span>

  <select
    value={selectedLanguage}
    onChange={handleLanguageChange}
  >
    <option value="English">English</option>
    <option value="Telugu">తెలుగు</option>
    <option value="Hindi">हिन्दी</option>
    <option value="Tamil">தமிழ்</option>
    <option value="Kannada">ಕನ್ನಡ</option>
  </select>
</div>


<button
  className="theme-toggle"
  onClick={() => setDarkMode((prev) => !prev)}
  title={darkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
  aria-label={darkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
>
  <span>{darkMode ? "☀️" : "🌙"}</span>
  <span>{darkMode ? "Light" : "Dark"}</span>
</button>

        </div>

      </nav>

      {/* ======================================================
          MAIN
      ====================================================== */}

      <main id="home">

        {/* ======================================================
            STEP 25.3 — ADMINISTRATOR DASHBOARD
        ====================================================== */}
        {showAdminAccess && isAdminUser && (
          <section
            id="admin-dashboard"
            className="admin-dashboard-section"
            style={{
              maxWidth: "1200px",
              margin: "0 auto",
              padding: "32px 20px 20px",
            }}
          >
            <div
              className="admin-dashboard-container"
              style={{
                background: "rgba(15, 23, 42, 0.92)",
                border: "1px solid rgba(124, 92, 255, 0.35)",
                borderRadius: "20px",
                padding: "24px",
                boxShadow: "0 20px 60px rgba(0,0,0,0.25)",
              }}
            >
              <div
                className="admin-dashboard-header"
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  gap: "16px",
                  flexWrap: "wrap",
                  marginBottom: "24px",
                }}
              >
                <div>
                  <div
                    style={{
                      fontSize: "12px",
                      fontWeight: 700,
                      letterSpacing: "1px",
                      color: "#a78bfa",
                      textTransform: "uppercase",
                      marginBottom: "8px",
                    }}
                  >
                    🛡️ ADMINISTRATOR ACCESS
                  </div>
                  <h2
                    style={{
                      margin: 0,
                      fontSize: "28px",
                      color: "#ffffff",
                    }}
                  >
                    Administrator Dashboard
                  </h2>
                  <p
                    style={{
                      margin: "8px 0 0",
                      color: "#a9b7d0",
                    }}
                  >
                    Organization-wide learning, competency, and training insights.
                  </p>
                </div>

                <div
                  style={{
                    display: "flex",
                    gap: "10px",
                    flexWrap: "wrap",
                  }}
                >
                  <button
                    className="secondary-btn"
                    type="button"
                    onClick={handleLoadAdminDashboard}
                    disabled={adminDashboardLoading}
                  >
                    {adminDashboardLoading
                      ? "⏳ Loading..."
                      : "🔄 Refresh Dashboard"}
                  </button>
                  <button
                    className="secondary-btn"
                    type="button"
                    onClick={handleCloseAdminAccess}
                  >
                    ✕ Close
                  </button>
                </div>
              </div>

              {!adminDashboard && !adminDashboardLoading && !adminDashboardError && (
                <div
                  style={{
                    textAlign: "center",
                    padding: "44px 20px",
                    borderRadius: "16px",
                    background: "rgba(255,255,255,0.035)",
                    border: "1px dashed rgba(255,255,255,0.12)",
                  }}
                >
                  <div style={{ fontSize: "42px", marginBottom: "12px" }}>📊</div>
                  <h3 style={{ margin: "0 0 8px", color: "#ffffff" }}>
                    Load Administrator Dashboard
                  </h3>
                  <p style={{ margin: "0 0 20px", color: "#a9b7d0" }}>
                    Retrieve the latest organization-wide analytics from the EduMind AI backend.
                  </p>
                  <button
                    className="primary-btn"
                    type="button"
                    onClick={handleLoadAdminDashboard}
                  >
                    📊 Load Dashboard
                  </button>
                </div>
              )}

              {adminDashboardLoading && (
                <div
                  style={{
                    textAlign: "center",
                    padding: "44px 20px",
                    color: "#cbd5e1",
                  }}
                >
                  <div style={{ fontSize: "34px", marginBottom: "10px" }}>⏳</div>
                  <p style={{ margin: 0 }}>Loading administrator analytics...</p>
                </div>
              )}

              {adminDashboardError && (
                <div
                  style={{
                    padding: "16px",
                    marginBottom: "20px",
                    borderRadius: "12px",
                    background: "rgba(239,68,68,0.10)",
                    border: "1px solid rgba(239,68,68,0.30)",
                    color: "#fecaca",
                  }}
                >
                  ⚠️ {adminDashboardError}
                </div>
              )}

              {adminDashboard && !adminDashboardLoading && (
                <>
                  <div
                    className="admin-summary-grid"
                    style={{
                      display: "grid",
                      gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
                      gap: "14px",
                      marginBottom: "22px",
                    }}
                  >
                    {[
                      ["👥", "Total Users", adminDashboard.total_users ?? 0],
                      ["🎓", "Total Learners", adminDashboard.total_learners ?? 0],
                      ["🛡️", "Total Admins", adminDashboard.total_admins ?? 0],
                      ["⚡", "Active Learners", adminDashboard.active_learners ?? 0],
                      ["📈", "Average Progress", `${adminDashboard.average_progress ?? 0}%`],
                      ["⏱️", "Learning Hours", adminDashboard.total_learning_hours ?? 0],
                    ].map(([icon, label, value]) => (
                      <div
                        key={label}
                        className="admin-stat-card"
                        style={{
                          padding: "18px",
                          borderRadius: "15px",
                          background: "rgba(30,41,59,0.88)",
                          border: "1px solid rgba(148,163,184,0.13)",
                        }}
                      >
                        <div style={{ fontSize: "22px", marginBottom: "8px" }}>{icon}</div>
                        <div style={{ color: "#94a3b8", fontSize: "13px" }}>{label}</div>
                        <strong
                          style={{
                            display: "block",
                            marginTop: "6px",
                            fontSize: "26px",
                            color: "#ffffff",
                          }}
                        >
                          {value}
                        </strong>
                      </div>
                    ))}
                  </div>

                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
                      gap: "18px",
                    }}
                  >
                    <div className="admin-dashboard-card" style={{ padding: "18px", borderRadius: "15px", background: "rgba(30,41,59,0.65)" }}>
                      <h3 style={{ marginTop: 0, color: "#ffffff" }}>📚 Training Activity</h3>
                      {Array.isArray(adminDashboard.training_activity) && adminDashboard.training_activity.length > 0 ? (
                        <div style={{ overflowX: "auto" }}>
                          <table style={{ width: "100%", borderCollapse: "collapse", color: "#dbeafe" }}>
                            <thead>
                              <tr>
                                <th style={{ textAlign: "left", padding: "10px 6px" }}>Topic</th>
                                <th style={{ padding: "10px 6px" }}>Activities</th>
                                <th style={{ padding: "10px 6px" }}>Completed</th>
                                <th style={{ padding: "10px 6px" }}>Avg. Score</th>
                              </tr>
                            </thead>
                            <tbody>
                              {adminDashboard.training_activity.map((item, index) => (
                                <tr key={`${item.topic}-${index}`}>
                                  <td style={{ padding: "9px 6px" }}>{item.topic}</td>
                                  <td style={{ textAlign: "center", padding: "9px 6px" }}>{item.activity_count ?? 0}</td>
                                  <td style={{ textAlign: "center", padding: "9px 6px" }}>{item.completed_count ?? 0}</td>
                                  <td style={{ textAlign: "center", padding: "9px 6px" }}>{item.average_score ?? 0}%</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      ) : (
                        <p style={{ color: "#94a3b8" }}>No training activity data available yet.</p>
                      )}
                    </div>

                    <div className="admin-dashboard-card" style={{ padding: "18px", borderRadius: "15px", background: "rgba(30,41,59,0.65)" }}>
                      <h3 style={{ marginTop: 0, color: "#ffffff" }}>🎯 Competency Overview</h3>
                      {Array.isArray(adminDashboard.competency_overview) && adminDashboard.competency_overview.length > 0 ? (
                        <div style={{ overflowX: "auto" }}>
                          <table style={{ width: "100%", borderCollapse: "collapse", color: "#dbeafe" }}>
                            <thead>
                              <tr>
                                <th style={{ textAlign: "left", padding: "10px 6px" }}>Category</th>
                                <th style={{ textAlign: "left", padding: "10px 6px" }}>Skill</th>
                                <th style={{ padding: "10px 6px" }}>Learners</th>
                                <th style={{ padding: "10px 6px" }}>Avg. Score</th>
                              </tr>
                            </thead>
                            <tbody>
                              {adminDashboard.competency_overview.map((item, index) => (
                                <tr key={`${item.category}-${item.skill}-${index}`}>
                                  <td style={{ padding: "9px 6px" }}>{item.category}</td>
                                  <td style={{ padding: "9px 6px" }}>{item.skill}</td>
                                  <td style={{ textAlign: "center", padding: "9px 6px" }}>{item.learner_count ?? 0}</td>
                                  <td style={{ textAlign: "center", padding: "9px 6px" }}>{item.average_score ?? 0}%</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      ) : (
                        <p style={{ color: "#94a3b8" }}>No competency assessment data available yet.</p>
                      )}
                    </div>

                    <div className="admin-dashboard-card" style={{ padding: "18px", borderRadius: "15px", background: "rgba(30,41,59,0.65)" }}>
                      <h3 style={{ marginTop: 0, color: "#ffffff" }}>📊 Competency Distribution</h3>
                      {Array.isArray(adminDashboard.competency_distribution) && adminDashboard.competency_distribution.length > 0 ? (
                        <div style={{ display: "grid", gap: "10px" }}>
                          {adminDashboard.competency_distribution.map((item, index) => (
                            <div
                              key={`${item.level}-${index}`}
                              style={{
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                padding: "12px 14px",
                                borderRadius: "10px",
                                background: "rgba(255,255,255,0.04)",
                              }}
                            >
                              <span style={{ color: "#cbd5e1" }}>{item.level}</span>
                              <strong style={{ color: "#ffffff" }}>{item.count ?? 0}</strong>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p style={{ color: "#94a3b8" }}>No competency distribution data available yet.</p>
                      )}
                    </div>

                    <div className="admin-dashboard-card" style={{ padding: "18px", borderRadius: "15px", background: "rgba(30,41,59,0.65)" }}>
                      <h3 style={{ marginTop: 0, color: "#ffffff" }}>📈 Training Effectiveness</h3>
                      {Array.isArray(adminDashboard.training_effectiveness) && adminDashboard.training_effectiveness.length > 0 ? (
                        <div style={{ display: "grid", gap: "10px" }}>
                          {adminDashboard.training_effectiveness.map((item, index) => (
                            <div key={`${item.skill}-${index}`} style={{ padding: "12px 14px", borderRadius: "10px", background: "rgba(255,255,255,0.04)" }}>
                              <div style={{ display: "flex", justifyContent: "space-between", gap: "10px" }}>
                                <strong style={{ color: "#ffffff" }}>{item.skill}</strong>
                                <span style={{ color: "#a78bfa" }}>{item.effectiveness_score ?? 0}%</span>
                              </div>
                              <small style={{ color: "#94a3b8" }}>Assessments: {item.assessment_count ?? 0}</small>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p style={{ color: "#94a3b8" }}>No training effectiveness data available yet.</p>
                      )}
                    </div>

                    <div className="admin-dashboard-card" style={{ padding: "18px", borderRadius: "15px", background: "rgba(30,41,59,0.65)" }}>
                      <h3 style={{ marginTop: 0, color: "#ffffff" }}>🚀 Emerging Skills</h3>
                      {Array.isArray(adminDashboard.emerging_skills) && adminDashboard.emerging_skills.length > 0 ? (
                        <ul style={{ margin: 0, paddingLeft: "20px", color: "#cbd5e1" }}>
                          {adminDashboard.emerging_skills.map((item, index) => (
                            <li key={index} style={{ marginBottom: "8px" }}>
                              {typeof item === "string" ? item : item.skill || item.name || JSON.stringify(item)}
                            </li>
                          ))}
                        </ul>
                      ) : (
                        <p style={{ color: "#94a3b8" }}>Emerging skill analytics will be populated in Step 27.</p>
                      )}
                    </div>

                      <div
  className="admin-dashboard-card"
  style={{
    padding: "18px",
    borderRadius: "15px",
    background: "rgba(30,41,59,0.65)"
  }}
>
  <h3
    style={{
      marginTop: 0,
      color: "#ffffff"
    }}
  >
    🔮 Predictive Skill Requirements
  </h3>

  {Array.isArray(
    adminDashboard.predictive_skill_requirements
  ) &&
  adminDashboard.predictive_skill_requirements.length > 0 ? (

    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "12px"
      }}
    >

      {adminDashboard.predictive_skill_requirements.map(
        (item, index) => (

          <div
            key={index}
            style={{
              padding: "14px",
              borderRadius: "10px",
              background: "rgba(15,23,42,0.75)",
              border: "1px solid rgba(148,163,184,0.15)"
            }}
          >

            {/* Skill Name */}

            <div
              style={{
                color: "#ffffff",
                fontSize: "16px",
                fontWeight: "600",
                marginBottom: "6px"
              }}
            >
              {typeof item === "string"
                ? item
                : item.skill || item.name || "Unknown Skill"}
            </div>

            {typeof item !== "string" && (
              <>

                {/* Category */}

                {item.category && (
                  <div
                    style={{
                      color: "#94a3b8",
                      fontSize: "13px",
                      marginBottom: "5px"
                    }}
                  >
                    📂 Category: {item.category}
                  </div>
                )}

                {/* Target Level */}

                {item.target_level && (
                  <div
                    style={{
                      color: "#94a3b8",
                      fontSize: "13px",
                      marginBottom: "5px"
                    }}
                  >
                    🎯 Required Level: {item.target_level}
                  </div>
                )}

                {/* Learner Count */}

                {item.learner_count !== undefined && (
                  <div
                    style={{
                      color: "#94a3b8",
                      fontSize: "13px"
                    }}
                  >
                    👥 Learners Requiring Skill:{" "}
                    {item.learner_count}
                  </div>
                )}

              </>
            )}

          </div>

        )
      )}

    </div>

  ) : (

    <p
      style={{
        color: "#94a3b8",
        margin: 0
      }}
    >
      No predictive skill requirements identified yet.
    </p>

  )}
</div>
                  </div>
                </>
              )}
            </div>
          </section>
        )}

        {/* ====================================================
            HERO
        ==================================================== */}

        <section className="hero">

          <div className="hero-content">

            <div className="badge">
              ✨ AI-Powered Learning Platform
            </div>

            <h1>
              Learn Smarter.
              <br />

              <span>
                Grow Faster.
              </span>
            </h1>

            <p>
              EduMind AI analyzes your
              learning materials, identifies
              competency gaps, generates
              personalized quizzes, and
              creates a learning path
              designed for you.
            </p>

            <div className="hero-buttons">

              <button
                className="primary-btn"
                onClick={
                  handleStartLearning
                }
                disabled={uploading}
              >
                {uploading
                  ? "⏳ Processing..."
                  : "📚 Start Learning"}
              </button>

              <button
                className="secondary-btn"
                onClick={handleAITutor}
              >
                🤖 Meet AI Tutor
              </button>
              

            </div>

            {selectedFile && (
              <div className="upload-status">

                <div className="file-name">
                  📄{" "}
                  {selectedFile.name}
                </div>

                <div className="upload-message">
                  {uploadStatus}
                </div>

              </div>
            )}

          </div>

          {/* ==================================================
              DASHBOARD PREVIEW
          ================================================== */}

          <div className="dashboard-preview">

            <div className="preview-header">

              <div>

                <span>
                  Welcome back 👋
                </span>

                <h3>
                  Your Learning Dashboard
                </h3>

              </div>

              <div className="profile-circle">
                {currentUser?.name
                  ? currentUser.name
                      .charAt(0)
                      .toUpperCase()
                  : "S"}
              </div>

            </div>

            <div className="progress-card">

              <div className="progress-info">

                <div>

                  <span>
                    Overall Progress
                  </span>

                  <strong>
                    {progress}%
                  </strong>

                </div>

              </div>

              <div className="progress-bar">

                <div
                  className="progress-value"
                  style={{
                    width: `${progress}%`,
                  }}
                />

              </div>

              <small>
                Keep learning 🚀
              </small>

            </div>

            <div className="mini-cards">

              <div className="mini-card">

                <div className="mini-icon">
                  📚
                </div>

                <span>
                  Courses
                </span>

                <strong>
                  06
                </strong>

              </div>

              <div className="mini-card">

                <div className="mini-icon">
                  📝
                </div>

                <span>
                  Quizzes
                </span>

                <strong>
                  24
                </strong>

              </div>

              <div className="mini-card">

                <div className="mini-icon">
                  🎯
                </div>

                <span>
                  Skills
                </span>

                <strong>
                  18
                </strong>

              </div>

            </div>

          </div>

        </section>

        {/* ====================================================
            QUIZ SECTION
        ==================================================== */}

        {quiz.length > 0 && (

          <section
            id="quiz-section"
            className="quiz-section"
          >

            <div className="quiz-header">

              <div className="quiz-label">
                📄 AI GENERATED QUIZ
              </div>

              <h2>
                Test Your Knowledge
              </h2>

              <p>
                Answer each multiple-choice
                question based on your
                uploaded learning material.
              </p>

              <div className="quiz-progress-info">

                <div>

                  <span>
                    {quiz.length} Questions
                  </span>

                  <strong>
                    {answeredCount}/
                    {quiz.length} Answered
                  </strong>

                </div>

                <span>
                  {progress}%
                </span>

              </div>

              <div className="quiz-progress-bar">

                <div
                  className="quiz-progress-value"
                  style={{
                    width: `${progress}%`,
                  }}
                />

              </div>

            </div>

            <div className="quiz-container">

              {quiz.map(
                (item, index) => {

                  const questionId =
                    getQuestionKey(
                      item,
                      index
                    );

                  const userAnswer =
                    selectedAnswers[
                      questionId
                    ] || "";

                  const answered =
                    userAnswer.trim()
                      .length > 0;

                  const correctAnswer =
                    item.correct_answer ??
                    item.answer ??
                    "";

                  const correct =
                    score !== null &&
                    normalizeText(
                      userAnswer
                    ) ===
                      normalizeText(
                        correctAnswer
                      );

                  return (

                    <div
                      className={`question-card ${
                        score !== null
                          ? correct
                            ? "question-correct"
                            : "question-wrong"
                          : ""
                      }`}
                      key={questionId}
                    >

                      <div className="question-top">

                        <span className="question-number">
                          Question{" "}
                          {index + 1}
                        </span>

                        <span className="question-badge">
                          ✨ AI Generated
                        </span>

                      </div>

                      <h3>
                        {item.question}
                      </h3>

                      {/* OPTIONS */}

                      <div className="answer-area">

                        <label>
                          Select Your Answer
                        </label>

                      <div className="quiz-options">
  {Array.isArray(item.options) &&
    item.options.map((option, optionIndex) => {
      const optionText =
        typeof option === "string"
          ? option
          : option?.label ??
            option?.text ??
            option?.value ??
            "";

      const optionLetter =
        String.fromCharCode(65 + optionIndex);

      const isSelected =
        userAnswer === optionText;

      return (
        <button
          key={optionIndex}
          type="button"
          className={`quiz-option ${
            isSelected ? "selected" : ""
          }`}
          onClick={() =>
            handleAnswerChange(
              questionId,
              optionText
            )
          }
          disabled={score !== null}
        >
          <span className="option-letter">
            {optionLetter}
          </span>

          <span className="option-text">
            {optionText}
          </span>

          <span className="option-check">
            {isSelected ? "✓" : ""}
          </span>
        </button>
      );
    })}
</div>

                      </div>

                      {/* ==================================================
                          ANSWER + EXPLANATION
                          SHOWN ONLY AFTER SUBMISSION
                      ================================================== */}

                      {score !== null && (

                        <div className="answer-feedback">

                          <div className="feedback-answer">

                            <strong>
                              {correct
                                ? "✓ Correct Answer"
                                : "✗ Incorrect Answer"}
                            </strong>

                            <p>
                              Correct answer:{" "}
                              {correctAnswer}
                            </p>

                            {!answered && (
                              <p>
                                Your answer:
                                Not answered
                              </p>
                            )}

                            {answered &&
                              !correct && (
                                <p>
                                  Your answer:{" "}
                                  {userAnswer}
                                </p>
                              )}

                          </div>

                          <div className="feedback-explanation">

                            <strong>
                              💡 Explanation
                            </strong>

                            <p>
                              {item.explanation ||
                                "Review the learning material to understand this concept."}
                            </p>

                          </div>

                          {/* ==================================================
    CONFUSION DETECTOR
================================================== */}

{answered && (
  <div className="confusion-detector-wrapper">

    <button
      type="button"
      className="confusion-detector-btn"
      onClick={() =>
        handleDetectConfusion(item, index)
      }
      disabled={
        confusionLoading[questionId]
      }
    >
      {confusionLoading[questionId]
        ? "🧠 Analyzing Understanding..."
        : "🧠 Check My Understanding"}
    </button>

    {confusionAnalysis[questionId] && (
      <div className="confusion-detector">

        {/* HEADER */}

        <div className="confusion-header">

          <div>
            <span className="confusion-label">
              🧠 CONFUSION DETECTOR
            </span>

            <h4>
              Understanding Analysis
            </h4>
          </div>

          <div className="confusion-score">
            <strong>
              {confusionAnalysis[questionId]
                .understanding_score ?? 0}
            </strong>

            <span>
              /100
            </span>
          </div>

        </div>


        {/* CONFUSION LEVEL */}

        <div className="confusion-level-row">

          <span>
            Confusion Level
          </span>

          <strong
            className={`confusion-level ${
              String(
                confusionAnalysis[questionId]
                  .confusion_level || "Medium"
              ).toLowerCase()
            }`}
          >
            {
              confusionAnalysis[questionId]
                .confusion_level ||
              "Medium"
            }
          </strong>

        </div>


        {/* WHAT STUDENT UNDERSTOOD */}

        {Array.isArray(
          confusionAnalysis[questionId]
            .understood
        ) &&
          confusionAnalysis[questionId]
            .understood.length > 0 && (

          <div className="confusion-block understood">

            <h5>
              ✅ What You Understood
            </h5>

            <ul>
              {confusionAnalysis[
                questionId
              ].understood.map(
                (point, pointIndex) => (
                  <li key={pointIndex}>
                    {point}
                  </li>
                )
              )}
            </ul>

          </div>
        )}


        {/* MISSING CONCEPTS */}

        {Array.isArray(
          confusionAnalysis[questionId]
            .missing_concepts
        ) &&
          confusionAnalysis[questionId]
            .missing_concepts.length > 0 && (

          <div className="confusion-block missing">

            <h5>
              ⚠️ Concepts You May Be Missing
            </h5>

            <ul>
              {confusionAnalysis[
                questionId
              ].missing_concepts.map(
                (point, pointIndex) => (
                  <li key={pointIndex}>
                    {point}
                  </li>
                )
              )}
            </ul>

          </div>
        )}


        {/* TARGETED EXPLANATION */}

        {confusionAnalysis[questionId]
          .targeted_explanation && (

          <div className="confusion-targeted">

            <h5>
              🎯 Targeted Explanation
            </h5>

            <p>
              {
                confusionAnalysis[
                  questionId
                ].targeted_explanation
              }
            </p>

          </div>
        )}


        {/* PRACTICE QUESTIONS */}

        {Array.isArray(
          confusionAnalysis[questionId]
            .practice_questions
        ) &&
          confusionAnalysis[questionId]
            .practice_questions.length > 0 && (

          <div className="confusion-practice">

            <h5>
              📝 Practice These Questions
            </h5>

            <ol>
              {confusionAnalysis[
                questionId
              ].practice_questions.map(
                (practiceQuestion, practiceIndex) => (
                  <li key={practiceIndex}>
                    {practiceQuestion}
                  </li>
                )
              )}
            </ol>

          </div>
        )}


        {/* PROVIDER */}

        {confusionAnalysis[questionId]
          .provider && (

          <div className="confusion-provider">

            Analysis provider:
            <strong>
              {" "}
              {
                confusionAnalysis[
                  questionId
                ].provider
              }
            </strong>

          </div>
        )}

      </div>
    )}

  </div>
)}

                        </div>

                      )}

                    </div>

                  );
                }
              )}

              {/* ==================================================
                  QUIZ SUBMIT
              ================================================== */}

              <div className="quiz-submit">

                <div className="submit-info">

                  <span>
                    📝 {answeredCount} of{" "}
                    {quiz.length} answered
                  </span>

                  <small>
                    {answeredCount <
                    quiz.length
                      ? `Answer all ${quiz.length} questions before submitting.`
                      : "All questions answered. Review your answers before submitting."}
                  </small>

                </div>

                <button
                  className="submit-quiz-btn"
                  onClick={
                    calculateScore
                  }
                  disabled={
                    loadingLearningPath ||
                    score !== null ||
                    answeredCount <
                      quiz.length
                  }
                >
                  {loadingLearningPath
                    ? "🧠 Analyzing..."
                    : score !== null
                    ? "✅ Quiz Submitted"
                    : "🎯 Submit Quiz"}
                </button>

              </div>

              {/* ==================================================
                  SCORE CARD
              ================================================== */}

              {score !== null && (

                <div
                  id="quiz-result"
                  className="score-card"
                >

                  <div className="score-icon">

                    {score ===
                    quiz.length
                      ? "🏆"
                      : score >=
                        quiz.length / 2
                      ? "🎉"
                      : "💪"}

                  </div>

                  <div className="score-content">

                    <span className="score-label">
                      QUIZ COMPLETED
                    </span>

                    <h2>
                      Great job!
                    </h2>

                    <p>
                      You scored
                    </p>

                    <div className="score-number">

                      {score}

                      <span>
                        / {quiz.length}
                      </span>

                    </div>

                    <div className="score-message">

                      {score ===
                      quiz.length
                        ? "Excellent work! You mastered this material. 🎉"
                        : score >=
                          quiz.length / 2
                        ? "Good effort! Review the incorrect answers and try again. 🚀"
                        : "Keep practicing! Review the material and try the quiz again. 💪"}

                    </div>

                    <div className="result-actions">

  <button
    className="retake-btn"
    onClick={retakeQuiz}
  >
    🔄 Retake Quiz
  </button>

  <button
    className="next-btn"
    onClick={handleDetectTopics}
    disabled={detectingTopics}
  >
    {detectingTopics
      ? "⏳ Detecting..."
      : "🚀 Detect Topics"}
  </button>

  <button
    className="ai-notes-btn"
    onClick={handleGenerateNotes}
    disabled={notesLoading || !selectedFile}
  >
    {notesLoading
      ? "⏳ Generating Notes..."
      : "📚 Generate AI Notes"}
  </button>

  <button
    className="flashcards-btn"
    onClick={handleGenerateFlashcards}
    disabled={flashcardsLoading || !selectedFile}
  >
    {flashcardsLoading
      ? "🧠 Generating..."
      : "🗂️ Generate AI Flashcards"}
  </button>

</div>





                  </div>

                </div>

              )}

              {/* ==================================================
                  LEARNING ANALYSIS
              ================================================== */}

              {learningAnalysis && (

                <div className="learning-analysis">

                  <div className="analysis-label">
                    🎯 PERSONALIZED LEARNING
                  </div>

                  <h2>
                    Your Learning Analysis
                  </h2>

                  <p>
                    AI analyzed your quiz
                    performance and created
                    personalized
                    recommendations.
                  </p>

                  {learningAnalysis.weak_topics &&
                    learningAnalysis
                      .weak_topics.length >
                      0 && (

                      <div className="analysis-box">

                        <h3>
                          📚 Topics to Improve
                        </h3>

                        <ul>

                          {learningAnalysis
                            .weak_topics
                            .map(
                              (
                                topic,
                                index
                              ) => (

                                <li
                                  key={
                                    index
                                  }
                                >
                                  {topic}
                                </li>

                              )
                            )}

                        </ul>

                      </div>

                    )}

                  {learningAnalysis.strong_topics &&
                    learningAnalysis
                      .strong_topics.length >
                      0 && (

                      <div className="analysis-box">

                        <h3>
                          🏆 Strong Topics
                        </h3>

                        <ul>

                          {learningAnalysis
                            .strong_topics
                            .map(
                              (
                                topic,
                                index
                              ) => (

                                <li
                                  key={
                                    index
                                  }
                                >
                                  {topic}
                                </li>

                              )
                            )}

                        </ul>

                      </div>

                    )}

                </div>

              )}

              

              {/* ============================================================
    PERSONALIZED LEARNING PATH
============================================================ */}

{personalizedPath && (
  <div
    id="personalized-path-section"
    className="dashboard-card personalized-path-section"
  >
    <div className="personalized-path-header">
      <div>
        <span className="igot-badge">
          🤖 EduMind AI
        </span>

        <h2>Personalized Learning Path</h2>

        <p>
          Your learning path is generated from your quiz performance.
        </p>
      </div>

      <div className="personalized-score-card">
        <span>Overall Score</span>
        <strong>
          {personalizedPath.percentage}%
        </strong>
      </div>
    </div>

    {/* Topic Summary */}

    <div className="learning-topic-summary">

      <div className="learning-summary-card weak">
        <span>🔴</span>
        <div>
          <strong>Weak Topics</strong>
          <p>
            {personalizedPath.weak_topics?.length || 0}
          </p>
        </div>
      </div>

      <div className="learning-summary-card developing">
        <span>🟡</span>
        <div>
          <strong>Developing</strong>
          <p>
            {personalizedPath.developing_topics?.length || 0}
          </p>
        </div>
      </div>

      <div className="learning-summary-card strong">
        <span>🟢</span>
        <div>
          <strong>Strong Topics</strong>
          <p>
            {personalizedPath.strong_topics?.length || 0}
          </p>
        </div>
      </div>

    </div>

    {/* Weak Topics */}

    {personalizedPath.weak_topics?.length > 0 && (
      <div className="learning-path-topic-box weak-box">
        <h3>🔴 Topics Needing Attention</h3>

        <div className="learning-topic-list">
          {personalizedPath.weak_topics.map((topic, index) => (
            <span key={index}>
              {topic}
            </span>
          ))}
        </div>
      </div>
    )}

    {/* Developing Topics */}

    {personalizedPath.developing_topics?.length > 0 && (
      <div className="learning-path-topic-box developing-box">
        <h3>🟡 Developing Topics</h3>

        <div className="learning-topic-list">
          {personalizedPath.developing_topics.map((topic, index) => (
            <span key={index}>
              {topic}
            </span>
          ))}
        </div>
      </div>
    )}

    {/* Strong Topics */}

    {personalizedPath.strong_topics?.length > 0 && (
      <div className="learning-path-topic-box strong-box">
        <h3>🟢 Strong Topics</h3>

        <div className="learning-topic-list">
          {personalizedPath.strong_topics.map((topic, index) => (
            <span key={index}>
              {topic}
            </span>
          ))}
        </div>
      </div>
    )}

    {/* Learning Path */}

    {personalizedPath.learning_path?.length > 0 && (
      <div className="learning-path-steps">

        <h3>📚 Your Learning Path</h3>

        <div className="learning-path-step-list">

          {personalizedPath.learning_path.map((step) => (

            <div
              className="learning-path-step"
              key={step.step}
            >

              <div className="learning-step-number">
                {step.step}
              </div>

              <div className="learning-step-content">

                <div className="learning-step-top">

                  <h4>
                    {step.topic}
                  </h4>

                  <span
                    className={`learning-priority ${String(
                      step.priority
                    ).toLowerCase()}`}
                  >
                    {step.priority} Priority
                  </span>

                </div>

                <p>
                  {step.description}
                </p>

                <div className="learning-step-meta">
                  <span>
                    Level: {step.level}
                  </span>

                  <span>
                    Score: {step.score_percentage}%
                  </span>

                  <span>
                    Action: {step.action}
                  </span>
                </div>

              </div>

            </div>

          ))}

        </div>
      </div>
    )}

    {/* Next Topic */}

    {personalizedPath.next_topic && (
      <div className="learning-next-topic">

        <div>
          <span>🎯 Next Topic</span>

          <strong>
            {personalizedPath.next_topic}
          </strong>
        </div>

        <p>
          {personalizedPath.next_action}
        </p>

      </div>
    )}

    {/* Recommendation */}

    {personalizedPath.recommendation && (
      <div className="learning-recommendation">

        <span>💡</span>

        <div>
          <strong>AI Recommendation</strong>

          <p>
            {personalizedPath.recommendation}
          </p>
        </div>

      </div>
    )}

  </div>
)}

{/* ==================================================
    ADAPTIVE LEARNING
================================================== */}

{adaptiveLoading && (
  <div className="adaptive-loading">

    <h3>
      🧠 Adaptive Learning
    </h3>

    <p>
      Analyzing your performance and adjusting your learning path...
    </p>

  </div>
)}

{adaptiveAnalysis && (

  <div className="adaptive-learning-panel">

    {/* HEADER */}

    <div className="adaptive-learning-header">

      <h3>
        🧠 Adaptive Learning
      </h3>

      <p>
        Your learning path has been automatically adjusted based on your performance.
      </p>

    </div>


    {/* PERFORMANCE */}

    <div className="adaptive-stat-grid">

      <div className="adaptive-stat-card">

        <span>
          Overall Performance
        </span>

        <strong>
          {adaptiveAnalysis.performance || "No Data"}
        </strong>

      </div>


      <div className="adaptive-stat-card">

        <span>
          Next Difficulty
        </span>

        <strong>
          {adaptiveAnalysis.next_difficulty || "Beginner"}
        </strong>

      </div>


      <div className="adaptive-stat-card">

        <span>
          Practice Mode
        </span>

        <strong>
          {adaptiveAnalysis.practice_mode ||
            "Fundamental Practice"}
        </strong>

      </div>

    </div>


    {/* RECOMMENDATION */}

    {adaptiveAnalysis.recommendation && (

      <div className="adaptive-recommendation">

        <h4>
          🎯 Adaptive Recommendation
        </h4>

        <p>
          {adaptiveAnalysis.recommendation}
        </p>

      </div>

    )}


    {/* LEARNING PATH */}

    {adaptiveAnalysis.topic_adaptations &&
      adaptiveAnalysis.topic_adaptations.length > 0 && (

      <div>

        <h4 className="adaptive-path-title">
          📚 Your Adaptive Learning Path
        </h4>


        {adaptiveAnalysis.topic_adaptations.map(
          (topic, index) => (

            <div
              key={`${topic.topic}-${index}`}
              className="adaptive-topic-card"
            >

              <div className="adaptive-topic-header">

                <h4 className="adaptive-topic-name">
                  {index + 1}. {topic.topic}
                </h4>

                <span className="adaptive-priority">
                  {index === 0
                    ? "⭐ Start Here"
                    : `Priority ${index + 1}`}
                </span>

              </div>


              <div className="adaptive-topic-info">

                <p>
                  <strong>Score:</strong>{" "}
                  {topic.percentage}%
                </p>

                <p>
                  <strong>Performance:</strong>{" "}
                  {topic.performance}
                </p>

                <p>
                  <strong>Next Difficulty:</strong>{" "}
                  {topic.next_difficulty}
                </p>

                <p>
                  <strong>Practice Mode:</strong>{" "}
                  {topic.practice_mode}
                </p>

                <p>
                  <strong>Action:</strong>{" "}
                  {topic.action}
                </p>

              </div>

            </div>

          )
        )}

      </div>

    )}

  </div>

)}

            </div>

          </section>

        )}
        {/* ====================================================
    CENTRAL EMPLOYEE DASHBOARD
==================================================== */}
<section
  id="dashboard"
  className="central-dashboard-section"
>
  <div className="dashboard-container">

    {/* HEADER */}
    <div className="dashboard-main-header">
      <div>
        <span className="dashboard-label">
          📊 EMPLOYEE DASHBOARD
        </span>

        <h2>
          Your Learning Dashboard
        </h2>

        <p>
          Track your competency, skill gaps,
          learning progress and personalized
          recommendations in one place.
        </p>
      </div>

      <div className="dashboard-user-badge">
        <div className="dashboard-avatar">
          {currentUser?.name
            ? currentUser.name
                .charAt(0)
                .toUpperCase()
            : "S"}
        </div>

        <div>
          <strong>
            {currentUser?.name || "Student"}
          </strong>

          <span>
            {currentUser?.role || "Learner"}
          </span>
        </div>
      </div>
    </div>


    {/* ==================================================
        1. EMPLOYEE PROFILE
    ================================================== */}
    <div className="dashboard-card profile-dashboard-card">

  <div className="dashboard-card-title">
    <span>👤</span>

    <div>
      <h3>Employee Profile</h3>
      <p>Your professional learning profile</p>
    </div>

    <button
      type="button"
      className="profile-edit-button"
      onClick={() => setEditingProfile(!editingProfile)}
    >
      {editingProfile ? "✕ Cancel" : "✏️ Edit Profile"}
    </button>
  </div>

  {!editingProfile ? (

    <div className="profile-grid">

      <div className="profile-item">
        <span>Name</span>
        <strong>
          {currentUser?.name || "Not provided"}
        </strong>
      </div>

      <div className="profile-item">
        <span>Designation</span>
        <strong>
          {currentUser?.designation || "Not provided"}
        </strong>
      </div>

      <div className="profile-item">
        <span>Department</span>
        <strong>
          {currentUser?.department || "Not provided"}
        </strong>
      </div>

      <div className="profile-item">
        <span>Job Role</span>
        <strong>
          {currentUser?.job_role || "Not provided"}
        </strong>
      </div>

      <div className="profile-item">
        <span>Education</span>
        <strong>
          {currentUser?.education || "Not provided"}
        </strong>
      </div>

      <div className="profile-item">
        <span>Experience</span>
        <strong>
          {currentUser?.experience || "Not provided"}
        </strong>
      </div>

    </div>

  ) : (

    <div className="profile-edit-form">

      <div className="profile-form-grid">

        <div className="login-field">
          <label>Designation</label>

          <input
            type="text"
            value={profileForm.designation}
            onChange={(e) =>
              setProfileForm({
                ...profileForm,
                designation: e.target.value,
              })
            }
            placeholder="Example: Data Analyst"
          />
        </div>

        <div className="login-field">
          <label>Department</label>

          <input
            type="text"
            value={profileForm.department}
            onChange={(e) =>
              setProfileForm({
                ...profileForm,
                department: e.target.value,
              })
            }
            placeholder="Example: Statistics Department"
          />
        </div>

        <div className="login-field">
          <label>Job Role *</label>

          <select
            value={profileForm.job_role}
            onChange={(e) =>
              setProfileForm({
                ...profileForm,
                job_role: e.target.value,
              })
            }
          >
            <option value="">
              Select Job Role
            </option>

            <option value="Data Analyst">
              Data Analyst
            </option>

            <option value="Data Scientist">
              Data Scientist
            </option>

            <option value="IT / Technical Officer">
              IT / Technical Officer
            </option>

            <option value="Manager / Team Lead">
              Manager / Team Lead
            </option>

            <option value="Statistical Officer">
              Statistical Officer
            </option>
          </select>
        </div>

        <div className="login-field">
  <label>Current Assignment *</label>

  <input
    type="text"
    value={profileForm.current_assignment}
    onChange={(e) =>
      setProfileForm({
        ...profileForm,
        current_assignment: e.target.value,
      })
    }
    placeholder="Enter your current assignment"
  />
</div>

        <div className="login-field">
          <label>Education</label>

          <input
            type="text"
            value={profileForm.education}
            onChange={(e) =>
              setProfileForm({
                ...profileForm,
                education: e.target.value,
              })
            }
            placeholder="Example: B.Tech CSE"
          />
        </div>

        <div className="login-field">
          <label>Experience</label>

          <input
            type="text"
            value={profileForm.experience}
            onChange={(e) =>
              setProfileForm({
                ...profileForm,
                experience: e.target.value,
              })
            }
            placeholder="Example: 0-2 years"
          />
        </div>

        <div className="login-field">
          <label>Previous Training</label>

          <input
            type="text"
            value={profileForm.previous_training}
            onChange={(e) =>
              setProfileForm({
                ...profileForm,
                previous_training: e.target.value,
              })
            }
            placeholder="Example: Python, SQL, AI"
          />
        </div>

      </div>

      <button
        type="button"
        className="login-submit-btn"
        onClick={handleSaveProfile}
        disabled={profileSaving}
      >
        {profileSaving
          ? "⏳ Saving..."
          : "💾 Save Profile"}
      </button>

    </div>

  )}

</div>


    {/* ==================================================
        2. OVERALL PROGRESS
    ================================================== */}
    <div className="dashboard-card">

      <div className="dashboard-card-title">
        <span>📈</span>

        <div>
          <h3>Overall Progress</h3>
          <p>Your current learning performance</p>
        </div>
      </div>

      <div className="dashboard-stat-grid">

        <div className="dashboard-stat-card">
          <span>Overall Progress</span>

          <strong>
            {progress || 0}%
          </strong>

          <div className="dashboard-progress-bar">
            <div
              style={{
                width: `${Math.min(
                  Math.max(progress || 0, 0),
                  100
                )}%`,
              }}
            />
          </div>
        </div>


        <div className="dashboard-stat-card">
          <span>Quiz Questions</span>

          <strong>
            {quiz?.length || 0}
          </strong>

          <small>
            Questions generated
          </small>
        </div>


        <div className="dashboard-stat-card">
          <span>Quiz Score</span>

          <strong>
            {score !== null
              ? `${score}/${quiz.length}`
              : "—"}
          </strong>

          <small>
            Latest assessment
          </small>
        </div>


        <div className="dashboard-stat-card">
          <span>Topics Detected</span>

          <strong>
            {detectedTopics?.length || 0}
          </strong>

          <small>
            Learning areas
          </small>
        </div>

      </div>
    </div>


  {/* ============================================================
    COMPETENCY PROFILE
============================================================ */}

<section className="dashboard-card competency-profile-card">

  <div className="dashboard-card-title">
    <span>🧠</span>

    <div>
      <h3>Competency Profile</h3>

      <p>
        Tell EduMind AI about your current competency level.
        This information will be used for AI skill-gap analysis.
      </p>
    </div>
  </div>


  <div className="competency-profile-grid">

    {Object.entries(competencyCategories).map(
      ([category, skills]) => (

        <div
          className="competency-profile-category"
          key={category}
        >

          <div className="competency-profile-category-header">

            <div className="competency-profile-category-icon">
              {category === "Statistical"
                ? "📊"
                : category === "Technical"
                ? "💻"
                : category === "Digital Governance"
                ? "🔐"
                : "👥"}
            </div>

            <div>
              <h4>{category}</h4>

<span>
  {Object.keys(skills).length} competencies
</span>
            </div>

          </div>


          <div className="competency-profile-skills">

            {Object.keys(skills).map((skill) => (

              <div
                className="competency-profile-skill"
                key={skill}
              >

                <div className="competency-skill-name">
                  <span>{skill}</span>
                </div>


                <select
                  value={
                    competencyProfile?.[category]?.[skill] ||
                    "Beginner"
                  }
                  onChange={(event) =>
                    handleCompetencyChange(
                      category,
                      skill,
                      event.target.value
                    )
                  }
                >

                  <option value="Beginner">
                    Beginner
                  </option>

                  <option value="Intermediate">
                    Intermediate
                  </option>

                  <option value="Advanced">
                    Advanced
                  </option>

                  <option value="Expert">
                    Expert
                  </option>

                </select>
                <button
  className="ai-assess-btn"
  onClick={() =>
    startCompetencyAssessment(category, skill)
  }
  disabled={assessmentLoading}
>
  {assessmentLoading
    ? "Generating..."
    : "AI Assess"}
</button>

              </div>

            ))}

          </div>

        </div>

      )
    )}

  </div>
  {/* ============================================================
      AI COMPETENCY GAP ANALYSIS
      ============================================================ */}

  <div className="competency-gap-analysis">

    <div className="competency-gap-header">

      <div>
        <h3>🎯 AI Competency Gap Analysis</h3>

        <p>
          EduMind AI compares your current competency levels
          with the required competency framework for your job role.
        </p>
      </div>

      <button
        className="gap-analysis-refresh-btn"
        onClick={loadCompetencyGapAnalysis}
        disabled={gapAnalysisLoading}
      >
        {gapAnalysisLoading
          ? "Analyzing..."
          : "🔄 Analyze Gaps"}
      </button>

    </div>


    {gapAnalysisLoading && (
      <div className="competency-gap-loading">
        <p>🤖 AI is analyzing your competency profile...</p>
      </div>
    )}


    {!gapAnalysisLoading &&
      competencyGapAnalysis?.summary && (

        <>

          {/* SUMMARY CARDS */}

          <div className="competency-gap-summary">

            <div className="gap-summary-card">

              <span className="gap-summary-icon">
                🎯
              </span>

              <div>
                <span className="gap-summary-label">
                  Coverage
                </span>

                <strong>
                  {competencyGapAnalysis.summary
                    .competency_coverage}%
                </strong>
              </div>

            </div>


            <div className="gap-summary-card">

              <span className="gap-summary-icon">
                📋
              </span>

              <div>
                <span className="gap-summary-label">
                  Required
                </span>

                <strong>
                  {competencyGapAnalysis.summary
                    .total_required_competencies}
                </strong>
              </div>

            </div>


            <div className="gap-summary-card">

              <span className="gap-summary-icon">
                ✅
              </span>

              <div>
                <span className="gap-summary-label">
                  Achieved
                </span>

                <strong>
                  {competencyGapAnalysis.summary
                    .competencies_achieved}
                </strong>
              </div>

            </div>


            <div className="gap-summary-card">

              <span className="gap-summary-icon">
                ⚠️
              </span>

              <div>
                <span className="gap-summary-label">
                  Skill Gaps
                </span>

                <strong>
                  {competencyGapAnalysis.summary
                    .total_skill_gaps}
                </strong>
              </div>

            </div>

          </div>


          {/* SKILL GAPS */}

          <div className="competency-gap-section">

            <h4>
              ⚠️ Identified Skill Gaps
            </h4>

            <div className="competency-gap-list">

              {competencyGapAnalysis.skill_gaps?.map(
                (gap, index) => (

                  <div
                    className="competency-gap-card"
                    key={`${gap.category}-${gap.skill}-${index}`}
                  >

                    <div className="competency-gap-card-top">

                      <div>

                        <span className="competency-gap-category">
                          {gap.category}
                        </span>

                        <h5>
                          {gap.skill}
                        </h5>

                      </div>

                      <span
                        className={`competency-gap-priority ${
                          gap.priority === "High"
                            ? "high"
                            : "medium"
                        }`}
                      >
                        {gap.priority} Priority
                      </span>

                    </div>


                    <div className="competency-gap-levels">

                      <div>
                        <span>Current Level</span>
                        <strong>
                          {gap.current_level}
                        </strong>
                      </div>

                      <span className="competency-gap-arrow">
                        →
                      </span>

                      <div>
                        <span>Target Level</span>
                        <strong>
                          {gap.target_level}
                        </strong>
                      </div>

                    </div>


                    <div className="competency-gap-status">
                      {gap.status}
                    </div>

                  </div>

                )
              )}

            </div>

          </div>


          {/* AI RECOMMENDATIONS */}

          <div className="competency-gap-section">

            <h4>
              🤖 AI Development Recommendations
            </h4>

            <div className="competency-recommendation-list">

              {competencyGapAnalysis.recommendations?.map(
                (recommendation, index) => (

                  <div
                    className="competency-recommendation-card"
                    key={`${recommendation.skill}-${index}`}
                  >

                    <div className="recommendation-number">
                      {index + 1}
                    </div>

                    <div>

                      <strong>
                        {recommendation.skill}
                      </strong>

                      <p>
                        {recommendation.action}
                      </p>

                    </div>

                    <span
                      className={`recommendation-priority ${
                        recommendation.priority === "High"
                          ? "high"
                          : "medium"
                      }`}
                    >
                      {recommendation.priority}
                    </span>

                  </div>

                )
              )}

            </div>

          </div>

        </>

      )}


    {!gapAnalysisLoading &&
      !competencyGapAnalysis?.summary && (

        <div className="competency-gap-empty">

          <p>
            Complete your employee profile and competency
            levels to generate an AI competency gap analysis.
          </p>

          <button
            className="gap-analysis-refresh-btn"
            onClick={loadCompetencyGapAnalysis}
          >
            Generate Analysis
          </button>

        </div>

      )}

  </div>





  <div className="competency-profile-footer">

    <div>

      <strong>
        🤖 AI Competency Analysis
      </strong>

      <p>
        Your selected competency levels will help EduMind AI
        identify skill gaps and recommend personalized training.
      </p>

    </div>

    <span className="competency-profile-status">
      ✓ Profile saved automatically
    </span>

  </div>

</section>

{showAssessment &&
  assessmentQuestions.length > 0 && (
    <section className="assessment-panel">

      <div className="assessment-header">
        <div>
          <h2>AI Competency Assessment</h2>

          <p>
            {assessmentCategory} → {assessmentSkill}
          </p>
        </div>

        <button
          className="assessment-close-btn"
          onClick={() => setShowAssessment(false)}
        >
          ✕
        </button>
      </div>

      <div className="assessment-progress">
        Question {assessmentIndex + 1} of{" "}
        {assessmentQuestions.length}
      </div>

      <div className="assessment-question-card">

        <h3>
          {assessmentQuestions[
            assessmentIndex
          ]?.question}
        </h3>

        <div className="assessment-options">

          {assessmentQuestions[
            assessmentIndex
          ]?.options?.map(
            (option, optionIndex) => (
              <label
                key={optionIndex}
                className={`assessment-option ${
                  assessmentAnswers[
                    assessmentIndex
                  ] === option
                    ? "selected"
                    : ""
                }`}
              >

                <input
                  type="radio"
                  name={`assessment-${assessmentIndex}`}
                  value={option}
                  checked={
                    assessmentAnswers[
                      assessmentIndex
                    ] === option
                  }
                  onChange={() => {

                    const updatedAnswers = [
                      ...assessmentAnswers,
                    ];

                    updatedAnswers[
                      assessmentIndex
                    ] = option;

                    setAssessmentAnswers(
                      updatedAnswers
                    );
                  }}
                />

                <span>{option}</span>

              </label>
            )
          )}

        </div>

      </div>

      <div className="assessment-actions">

        <button
          className="assessment-secondary-btn"
          disabled={assessmentIndex === 0}
          onClick={() =>
            setAssessmentIndex(
              assessmentIndex - 1
            )
          }
        >
          Previous
        </button>

        {assessmentIndex <
        assessmentQuestions.length - 1 ? (
          <button
            className="assessment-primary-btn"
            onClick={() => {

              if (
                !assessmentAnswers[
                  assessmentIndex
                ]
              ) {
                alert(
                  "Please select an answer."
                );
                return;
              }

              setAssessmentIndex(
                assessmentIndex + 1
              );
            }}
          >
            Next
          </button>
        ) : (
          <button
            className="assessment-primary-btn"
            onClick={submitCompetencyAssessment}
            disabled={assessmentSubmitting}
          >
            {assessmentSubmitting
              ? "Submitting..."
              : "Submit Assessment"}
          </button>
        )}

      </div>

    </section>
  )}
  {assessmentResult && (
  <section className="assessment-result-card">

    <h2>AI Assessment Result</h2>

    <div className="assessment-score">
      <strong>
        {assessmentResult.score}
      </strong>
      <span>
        / {assessmentResult.total_questions}
      </span>
    </div>

    <p className="assessment-percentage">
      Score: {assessmentResult.percentage}%
    </p>

    <div className="assessment-level">
      Assessed Level:{" "}
      <strong>
        {assessmentResult.assessed_level}
      </strong>
    </div>

    {assessmentResult.analysis && (
      <div className="assessment-analysis">

        <h3>Competency Summary</h3>
        <p>
          {assessmentResult.analysis.summary}
        </p>

        <h3>Strengths</h3>
        <ul>
          {assessmentResult.analysis.strengths?.map(
            (strength, index) => (
              <li key={index}>
                {strength}
              </li>
            )
          )}
        </ul>

        <h3>Weaknesses</h3>
        <ul>
          {assessmentResult.analysis.weaknesses?.map(
            (weakness, index) => (
              <li key={index}>
                {weakness}
              </li>
            )
          )}
        </ul>

        <h3>Recommended Next Action</h3>
        <p>
          {assessmentResult.analysis.next_action}
        </p>

      </div>
    )}

  </section>
)}


    {/* ==================================================
        4. SKILL GAP SUMMARY
    ================================================== */}
    <div className="dashboard-card">

      <div className="dashboard-card-title">
        <span>🎯</span>

        <div>
          <h3>Skill Gap Summary</h3>

          <p>
            AI-identified areas requiring
            additional learning
          </p>
        </div>
      </div>

      {skillGaps?.length > 0 ? (

        <div className="dashboard-skill-gap-list">

          {skillGaps.map((gap, index) => {
            <button
  className="primary-button"
  onClick={() =>
    handlePracticeWeakTopic(
      typeof gap === "string"
        ? gap
        : gap.skill ||
          gap.topic ||
          gap.name ||
          ""
    )
  }
  disabled={generatingPracticeQuiz}
>
  {generatingPracticeQuiz &&
  practiceTopic ===
    (typeof gap === "string"
      ? gap
      : gap.skill ||
        gap.topic ||
        gap.name ||
        "") ? (
    "Generating..."
  ) : (
    "Practice Weak Skill"
  )}
</button>

            const topic =
              typeof gap === "string"
                ? gap
                : gap.topic ||
                  gap.name ||
                  "Unknown Topic";

            const level =
              typeof gap === "object"
                ? gap.level ||
                  "Needs Practice"
                : "Needs Practice";

            return (
              <div
                className="dashboard-skill-gap-item"
                key={index}
              >

                <div className="skill-gap-index">
                  {String(index + 1).padStart(2, "0")}
                </div>

                <div className="skill-gap-content">

                  <strong>
                    {topic}
                  </strong>

                  <span>
                    {level}
                  </span>

                </div>

                <div className="skill-gap-action">
                  🎯 Practice
                </div>

              </div>
            );
          })}

        </div>

      ) : (

        <div className="dashboard-empty-state">
          <span>🎉</span>

          <h4>
            No skill gaps detected yet
          </h4>

          <p>
            Complete a quiz and run Skill Gap
            Analysis to generate competency insights.
          </p>

        </div>

      )}
    </div>



          {/* ==================================================
        5. iGoT KARMAYOGI RECOMMENDATIONS
    ================================================== */}
    <div className="dashboard-card">

      <div className="dashboard-card-title">
        <span>🎓</span>

        <div>
          <h3>iGoT Karmayogi Recommendations</h3>

          <p>
            Personalized training courses based on your skill gaps
          </p>
        </div>
      </div>

      {loadingIgot ? (

        <div className="dashboard-empty-state">
          <span>⏳</span>

          <h4>
            Loading iGoT courses...
          </h4>

          <p>
            Finding relevant training opportunities for you.
          </p>
        </div>

      ) : igotCourses?.length > 0 ? (

        <div className="igot-course-grid">

          {igotCourses.map((course, index) => (

            <div
              className="igot-course-card"
              key={course.id || index}
            >

              <span className="igot-badge">
                iGoT Karmayogi
              </span>

              <h4>
                {course.title ||
                  course.course_name ||
                  "Training Course"}
              </h4>

              <p>
                {course.description ||
                  "Recommended learning course for competency development."}
              </p>

              {course.skill && (
                <div className="igot-skill">
                  Skill:
                  <strong>{course.skill}</strong>
                </div>
              )}

              {course.duration && (
  <div className="igot-duration">
    Duration: {course.duration}
  </div>
)}

{/* iGoT Enrollment */}
<div style={{ marginTop: "16px" }}>

  <button
    className="primary-button"
    onClick={() => handleIgotEnroll(course)}
  >
    Enroll in Course
  </button>

</div>

</div>

          ))}

        </div>

      ) : (

        <div className="dashboard-empty-state">

          <span>🎓</span>

          <h4>
            No iGoT courses available
          </h4>

          <p>
            Complete your competency and skill-gap analysis
            to receive personalized training recommendations.
          </p>

        </div>

      )}

    </div>
    {/* ==================================================
    MY ENROLLED iGoT COURSES
================================================== */}

<div className="dashboard-card igot-enrollment-section">

  <div className="igot-enrollment-header">

    <span className="igot-enrollment-header-icon">
      🎓
    </span>

    <div>
      <h2>My Enrolled iGoT Courses</h2>

      <p>
        Track your enrolled training courses and learning progress.
      </p>
    </div>

  </div>


  {/* Load Enrollments Button */}

  <div className="igot-enrollment-actions">

    <button
      className="primary-button"
      onClick={handleLoadIgotEnrollments}
    >
      🔄 Load My Enrolled Courses
    </button>

  </div>


  {/* No Enrollments */}

  {igotEnrollments.length === 0 ? (

    <div className="igot-enrollment-empty">

      <div className="igot-enrollment-empty-icon">
        📚
      </div>

      <h4>
        No enrolled courses yet
      </h4>

      <p>
        Enroll in an iGoT course to start your personalized
        learning journey.
      </p>

    </div>

  ) : (

    /* Enrolled Courses */

    <div className="igot-enrollment-grid">

      {igotEnrollments.map((enrollment) => (

        <div
          className="igot-enrollment-card"
          key={enrollment.id}
        >

          <span className="igot-badge">
            iGoT Karmayogi
          </span>


          <h4>
            {enrollment.course_title}
          </h4>


          {/* Skill */}

          {enrollment.skill && (

            <div className="igot-enrollment-skill">

              Skill:
              <strong>
                {enrollment.skill}
              </strong>

            </div>

          )}


          {/* Duration */}

          {enrollment.duration && (

            <div className="igot-enrollment-duration">

              Duration: {enrollment.duration}

            </div>

          )}


          {/* Progress */}

          <div className="igot-progress-section">

            <div className="igot-progress-header">

              <span>
                Course Progress
              </span>

              <span className="igot-progress-percentage">
                {enrollment.progress}%
              </span>

            </div>


            <div className="igot-progress-bar">

              <div
                className="igot-progress-fill"
                style={{
                  width: `${enrollment.progress}%`,
                }}
              />

            </div>

          </div>


          {/* ==================================================
              UPDATE COURSE PROGRESS
          ================================================== */}

          <div style={{ marginTop: "18px" }}>

            <label
              style={{
                display: "block",
                marginBottom: "8px",
                fontWeight: 600,
              }}
            >
              Update Progress
            </label>

              <select
  value={enrollment.progress}
  onChange={(event) =>
    handleUpdateIgotProgress(
      enrollment.id,
      Number(event.target.value)
    )
  }
  disabled={enrollment.status === "completed"}
  style={{
    width: "100%",
    padding: "10px",
    borderRadius: "8px",
    border: "1px solid #475569",
    background: "#1e293b",
    color: "inherit",
  }}
>
  <option value={0}>0%</option>
  <option value={25}>25%</option>
  <option value={50}>50%</option>
  <option value={75}>75%</option>
  <option value={100}>100% - Complete</option>
</select>

          </div>


          {/* Status */}

          <div className="igot-enrollment-status">

            {enrollment.status === "completed" ? (

              <span className="igot-status-completed">
                ✅ Course Completed
              </span>

            ) : (

              <span className="igot-status-progress">
                📖 In Progress
              </span>

            )}

          </div>

        </div>

      ))}

    </div>

  )}

</div>

    <div className="dashboard-card">
  <h2>NSSTA / TPAC Training Recommendations</h2>

  {loadingNssta ? (
    <p>Loading personalized training recommendations...</p>
  ) : nsstaRecommendations.length === 0 ? (
    <p>No NSSTA / TPAC recommendations available yet.</p>
  ) : (
    <div className="training-list">
      {nsstaRecommendations.map((training, index) => (
        <div className="training-item" key={training.id || index}>
          <h3>{training.title}</h3>

          <p>
            <strong>Skill:</strong>{" "}
            {training.skill || training.skill_gap || "N/A"}
          </p>

          <p>
            <strong>Level:</strong>{" "}
            {training.level || "Intermediate"}
          </p>

          <p>
            <strong>Duration:</strong>{" "}
            {training.duration || "N/A"}
          </p>

          {training.reason && (
            <p>
              <strong>Why recommended:</strong> {training.reason}
            </p>
          )}
        </div>
      ))}
    </div>
  )}
</div>


    {/* ==================================================
        5.5 INTERACTIVE LEARNING MODULES
    ================================================== */}

    <div className="dashboard-card">

      <div className="dashboard-card-title">
        <span>📚</span>

        <div>
          <h3>Interactive Learning Modules</h3>

          <p>
            Learn concepts through interactive lessons,
            practice and checkpoints.
          </p>
        </div>
      </div>

      {detectedTopics?.length > 0 ? (

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(250px, 1fr))",
            gap: "16px",
          }}
        >

          {createInteractiveLearningModules().map(
            (module, index) => {

              const completed =
                completedLearningModules.includes(
                  module.id
                );

              return (
                <div
                  key={module.id}
                  style={{
                    border: "1px solid #334155",
                    borderRadius: "16px",
                    padding: "20px",
                    background:
                      "rgba(30, 41, 59, 0.65)",
                  }}
                >

                  <div
                    style={{
                      fontSize: "13px",
                      opacity: 0.7,
                      marginBottom: "8px",
                    }}
                  >
                    MODULE {index + 1}
                  </div>

                  <h3>{module.title}</h3>

                  <p>{module.description}</p>

                  <div
                    style={{
                      display: "flex",
                      gap: "8px",
                      flexWrap: "wrap",
                      margin: "14px 0",
                    }}
                  >
                    {module.lessons.map((lesson) => (
                      <span
                        key={lesson.id}
                        style={{
                          padding: "6px 10px",
                          borderRadius: "20px",
                          border: "1px solid #475569",
                          fontSize: "12px",
                        }}
                      >
                        {lesson.title}
                      </span>
                    ))}
                  </div>

                  <button
                    className="primary-button"
                    onClick={() =>
                      handleOpenLearningModule(module)
                    }
                  >
                    {completed
                      ? "✓ Review Module"
                      : "▶ Start Module"}
                  </button>

                  {completed && (
                    <div
                      style={{
                        marginTop: "10px",
                        color: "#4ade80",
                        fontWeight: 600,
                      }}
                    >
                      ✓ Module Completed
                    </div>
                  )}

                </div>
              );
            }
          )}

        </div>

      ) : (

        <div className="dashboard-empty-state">

          <span>📚</span>

          <h4>
            No learning modules available yet
          </h4>

          <p>
            Upload learning material and detect
            topics to create interactive modules.
          </p>

        </div>

      )}

    </div>

    {/* ==================================================
        ACTIVE INTERACTIVE MODULE
    ================================================== */}

    {activeLearningModule && (

      <div className="dashboard-card">

        <div className="dashboard-card-title">

          <span>🎓</span>

          <div>
            <h3>
              {activeLearningModule.title}
            </h3>

            <p>
              Interactive Learning Module
            </p>
          </div>

        </div>

        <div
          style={{
            display: "flex",
            gap: "10px",
            flexWrap: "wrap",
            marginBottom: "18px",
          }}
        >

          {activeLearningModule.lessons.map(
            (lesson) => (

              <button
                key={lesson.id}
                className={
                  activeLearningModule.activeLesson?.id ===
                  lesson.id
                    ? "primary-button"
                    : "secondary-button"
                }
                onClick={() =>
                  handleModuleLesson(
                    activeLearningModule,
                    lesson
                  )
                }
              >
                {lesson.title}
              </button>

            )
          )}

        </div>

        {activeLearningModule.activeLesson && (

          <div
            style={{
              padding: "20px",
              border: "1px solid #334155",
              borderRadius: "14px",
              marginBottom: "16px",
            }}
          >

            <h4>
              {activeLearningModule.activeLesson.title}
            </h4>

            <p>
              {activeLearningModule.activeLesson.description}
            </p>

            {activeLearningModule.activeLesson.id ===
              "learn" && (
              <div
                style={{
                  padding: "14px",
                  borderRadius: "10px",
                  background:
                    "rgba(59, 130, 246, 0.08)",
                  marginTop: "12px",
                }}
              >
                📖 Study the key concepts and
                understand the fundamentals before
                moving to practice.
              </div>
            )}

            {activeLearningModule.activeLesson.id ===
              "practice" && (
              <div
                style={{
                  padding: "14px",
                  borderRadius: "10px",
                  background:
                    "rgba(168, 85, 247, 0.08)",
                  marginTop: "12px",
                }}
              >
                🧩 Apply what you learned through
                practical examples and activities.
              </div>
            )}

            {activeLearningModule.activeLesson.id ===
              "checkpoint" && (
              <div
                style={{
                  padding: "14px",
                  borderRadius: "10px",
                  background:
                    "rgba(34, 197, 94, 0.08)",
                  marginTop: "12px",
                }}
              >
                🎯 Check your understanding before
                completing the module.
              </div>
            )}

          </div>

        )}

        <div
          style={{
            display: "flex",
            gap: "10px",
          }}
        >

          <button
            className="primary-button"
            onClick={() =>
              handleCompleteLearningModule(
                activeLearningModule.id
              )
            }
          >
            ✓ Complete Module
          </button>

          <button
            className="secondary-button"
            onClick={handleCloseLearningModule}
          >
            Close
          </button>

        </div>

      </div>

    )}

    {/* ==================================================
    23. VIRTUAL LABS
================================================== */}

<section className="virtual-labs-section">

  <div className="section-header">
    <h2>Virtual Labs</h2>

    <p>
      Practice real-world technologies through guided
      hands-on virtual learning environments.
    </p>
  </div>

  <div className="virtual-labs-grid">

    {virtualLabCatalogue.map((lab) => (
      <div
        key={lab.id}
        className={`virtual-lab-card ${
          selectedVirtualLab?.id === lab.id
            ? "virtual-lab-card-active"
            : ""
        }`}
      >

        <div className="virtual-lab-card-header">

  <div>
    <span className="virtual-lab-badge">
      {lab.level}
    </span>

    {completedVirtualLabs.includes(lab.id) && (
      <span className="virtual-lab-completed-badge">
        ✓ Completed
      </span>
    )}
  </div>

  <span className="virtual-lab-technology">
    {lab.technology}
  </span>

</div>

        <h3>{lab.title}</h3>

        <p>{lab.description}</p>

        <div className="virtual-lab-card-progress">

  <div className="virtual-lab-card-progress-header">
    <span>Progress</span>

    <strong>
      {completedVirtualLabs.includes(lab.id)
        ? "100%"
        : "0%"}
    </strong>
  </div>

  <div className="virtual-lab-card-progress-track">
    <div
      className="virtual-lab-card-progress-fill"
      style={{
        width: completedVirtualLabs.includes(lab.id)
          ? "100%"
          : "0%",
      }}
    />
  </div>

</div>

        <div className="virtual-lab-activities">

          <h4>Lab Activities</h4>

          <ul>
            {lab.activities.map((activity, index) => (
              <li key={index}>
                {activity}
              </li>
            ))}
          </ul>

        </div>

            <button
  className="primary-button"
  onClick={() => handleSelectVirtualLab(lab)}
>
  {completedVirtualLabs.includes(lab.id)
    ? "Review Virtual Lab"
    : "Open Virtual Lab"}
</button>

      </div>
    ))}

  </div>

  {selectedVirtualLab && (
    <div className="selected-virtual-lab">

      <div className="selected-virtual-lab-header">

        <div>
          <span className="virtual-lab-badge">
            {selectedVirtualLab.level}
          </span>

          <h3>{selectedVirtualLab.title}</h3>

          <p>
            {selectedVirtualLab.description}
          </p>
        </div>

      </div>

      <div className="selected-virtual-lab-info">

        <h4>Available Activities</h4>

        <div className="virtual-lab-activity-list">

          {selectedVirtualLab.activities.map(
            (activity, index) => (
              <div
                key={index}
                className="virtual-lab-activity-item"
              >
                <span>{index + 1}</span>
                <p>{activity}</p>
              </div>
            )
          )}

        </div>

      </div>

      <div className="virtual-lab-ui-actions">

          <button
  className="primary-button"
  onClick={() =>
    handleStartVirtualLab(selectedVirtualLab)
  }
>
  Start Lab
</button>

        <button
          className="secondary-button"
          onClick={() => setSelectedVirtualLab(null)}
        >
          Close
        </button>

      </div>

    </div>
  )}
  {activeVirtualLab && (
  <div className="virtual-lab-workspace">

    <div className="virtual-lab-workspace-header">

      <div>
        <span className="virtual-lab-badge">
          Hands-on Lab
        </span>

        <h3>{activeVirtualLab.title}</h3>

        <p>
          Activity {virtualLabActivityIndex + 1} of{" "}
          {activeVirtualLab.activities.length}
        </p>
      </div>

    </div>

    <div className="virtual-lab-progress-info">
      <div className="virtual-lab-progress-track">
        <div
          className="virtual-lab-progress-fill"
          style={{
            width: `${
              ((virtualLabActivityIndex + 1) /
                activeVirtualLab.activities.length) *
              100
            }%`,
          }}
        />
      </div>
    </div>

    <div className="virtual-lab-current-activity">

      <span className="virtual-lab-activity-number">
        {virtualLabActivityIndex + 1}
      </span>

      <div>
        <h4>
          {activeVirtualLab.activities[
            virtualLabActivityIndex
          ]}
        </h4>

        <p>
          Complete this hands-on learning activity before
          moving to the next activity.
        </p>
      </div>

    </div>
    
    <div className="virtual-lab-workspace-actions">

  <button
    className="secondary-button"
    onClick={handlePreviousVirtualLabActivity}
    disabled={virtualLabActivityIndex === 0}
  >
    Previous
  </button>

  {virtualLabActivityIndex <
  activeVirtualLab.activities.length - 1 ? (

    <button
      className="primary-button"
      onClick={handleNextVirtualLabActivity}
    >
      Next Activity
    </button>

  ) : (

    <button
      className="primary-button"
      onClick={() =>
        handleCompleteVirtualLab(activeVirtualLab)
      }
    >
      ✓ Complete Lab
    </button>

  )}

  <button
    className="secondary-button"
    onClick={handleExitVirtualLab}
  >
    Exit Lab
  </button>

</div>

  </div>
)}

</section>



    {/* ==================================================
        6. LEARNING PATH
    ================================================== */}
    
    <div className="dashboard-card">

      <div className="dashboard-card-title">
        <span>🛣️</span>

        <div>
          <h3>Personalized Learning Path</h3>

          <p>
            AI-generated learning recommendations
          </p>
        </div>
      </div>


      {personalizedPath ? (

        <div className="dashboard-learning-path">

          {personalizedPath.weak_topics?.length > 0 && (

            <div className="dashboard-path-box high-priority">

              <div className="path-box-icon">
                🔴
              </div>

              <div>
                <h4>
                  High Priority
                </h4>

                <p>
                  Focus on your weak topics first.
                </p>

                <div className="dashboard-topic-tags">

                  {personalizedPath.weak_topics.map(
                    (topic, index) => (
                      <span key={index}>
                        {topic}
                      </span>
                    )
                  )}

                </div>
              </div>

            </div>

          )}


          {personalizedPath.strong_topics?.length > 0 && (

            <div className="dashboard-path-box strong-priority">

              <div className="path-box-icon">
                🟢
              </div>

              <div>
                <h4>
                  Strong Areas
                </h4>

                <p>
                  Continue advanced learning
                  in these areas.
                </p>

                <div className="dashboard-topic-tags">

                  {personalizedPath.strong_topics.map(
                    (topic, index) => (
                      <span key={index}>
                        {topic}
                      </span>
                    )
                  )}

                </div>
              </div>

            </div>

          )}


          {personalizedPath.recommendation && (

            <div className="dashboard-ai-recommendation">

              <span>
                🤖
              </span>

              <div>
                <h4>
                  AI Recommendation
                </h4>

                <p>
                  {personalizedPath.recommendation}
                </p>
              </div>

            </div>

          )}

        </div>

      ) : (

  <div className="dashboard-empty-state">

    <span>🎯</span>

    <h4>
      No skill gaps detected yet
    </h4>

    <p>
      Complete a quiz and analyze your performance
      to identify competency gaps.
    </p>

    <button
      className="learning-path-btn"
      onClick={handleDetectSkillGaps}
      disabled={detectingSkillGaps}
    >
      {detectingSkillGaps
        ? "⏳ Analyzing Skill Gaps..."
        : "🎯 Analyze My Skill Gaps"}
    </button>

  </div>

)}

    </div>


    {/* ==================================================
        6. LEARNING ACTIVITY
    ================================================== */}
    <div className="dashboard-card">

      <div className="dashboard-card-title">
        <span>📝</span>

        <div>
          <h3>Learning Activity</h3>

          <p>
            Your recent learning activities
          </p>
        </div>
      </div>

      <div className="activity-grid">

        <div className="activity-card">
          <span>📄</span>
          <strong>
            {selectedFile
              ? selectedFile.name
              : "No material uploaded"}
          </strong>
          <small>
            Study Material
          </small>
        </div>


        <div className="activity-card">
          <span>🧠</span>
          <strong>
            {detectedTopics?.length || 0}
          </strong>
          <small>
            Topics Identified
          </small>
        </div>


        <div className="activity-card">
          <span>📝</span>
          <strong>
            {quiz?.length || 0}
          </strong>
          <small>
            Questions Generated
          </small>
        </div>


        <div className="activity-card">
          <span>🎯</span>
          <strong>
            {skillGaps?.length || 0}
          </strong>
          <small>
            Skill Gaps
          </small>
        </div>

      </div>
    </div>


    {/* ==================================================
        7. AI NEXT ACTION
    ================================================== */}
    <div className="dashboard-ai-next-action">

      <div className="next-action-icon">
        🤖
      </div>

      <div className="next-action-content">

        <span>
          AI NEXT ACTION
        </span>

        <h3>
          Continue your personalized learning
        </h3>

        <p>
          EduMind AI continuously analyzes your
          learning performance and recommends the
          next best learning activity.
        </p>

      </div>

      <button
        onClick={() => {
          document
            .getElementById("skill-gap-section")
            ?.scrollIntoView({
              behavior: "smooth",
            });
        }}
      >
        🎯 View Skill Gaps
      </button>

    </div>

  </div>
</section>


        {/* ====================================================
    STUDY WASTE DETECTOR
==================================================== */}

{studyWasteAnalysis && (
  <section
    id="study-waste-section"
    className="study-waste-card"
  >

    <div className="study-waste-header">

      <span className="analysis-label">
        ⏱️ STUDY BEHAVIOR ANALYSIS
      </span>

      <h2>
        Where Did You Spend Your Time?
      </h2>

      <p>
        EduMind AI analyzed how much time you
        spent on each quiz question.
      </p>

    </div>


    {/* STATS */}

    <div className="study-waste-stats">

      <div className="study-waste-stat">

        <strong>
          {studyWasteAnalysis.average_time ??
            studyWasteAnalysis.average_time_per_question ??
            0}s
        </strong>

        <span>
          Avg. Time / Question
        </span>

      </div>


      <div className="study-waste-stat">

        <strong>
          {studyWasteAnalysis.efficiency_percentage ??
            studyWasteAnalysis.efficiency ??
            0}%
        </strong>

        <span>
          Study Efficiency
        </span>

      </div>


      <div className="study-waste-stat">

        <strong>
          {studyWasteAnalysis.wasted_time ?? 0}s
        </strong>

        <span>
          Potentially Wasted Time
        </span>

      </div>

    </div>


    {/* WASTE LEVEL */}

    {studyWasteAnalysis.waste_level && (

      <div className="study-waste-level">

        <strong>
          ⚡ Time Waste Level
        </strong>

        <span
          className={`waste-level ${String(
            studyWasteAnalysis.waste_level
          ).toLowerCase()}`}
        >
          {studyWasteAnalysis.waste_level}
        </span>

      </div>

    )}


    {/* MOST TIME CONSUMING TOPIC */}

    {studyWasteAnalysis.most_time_consuming_topic && (

      <div className="study-waste-focus">

        <strong>
          🎯 Most Time-Consuming Topic
        </strong>

        <p>
          {studyWasteAnalysis.most_time_consuming_topic}
        </p>

      </div>

    )}


    {/* AI RECOMMENDATION */}

    {studyWasteAnalysis.recommendation && (

      <div className="study-waste-recommendation">

        <strong>
          💡 AI Recommendation
        </strong>

        <p>
          {studyWasteAnalysis.recommendation}
        </p>

      </div>

    )}


    {/* TIME-CONSUMING QUESTIONS */}

    {Array.isArray(
      studyWasteAnalysis.waste_questions
    ) &&
      studyWasteAnalysis.waste_questions.length > 0 && (

        <div className="study-waste-questions">

          <h3>
            ⏱️ Questions That Took the Most Time
          </h3>

          <ul>

            {studyWasteAnalysis.waste_questions.map(
              (item, index) => (

                <li key={index}>

                  <span>
                    {item.question ||
                      `Question ${index + 1}`}
                  </span>

                  <strong>
                    {item.time_spent ?? 0}s
                  </strong>

                </li>

              )
            )}

          </ul>

        </div>

      )}

  </section>
)}

{/* ============================================================
    QUESTION INTELLIGENCE
============================================================ */}

{questionIntelligence && (
  <section className="question-intelligence-card">

    <div className="question-intelligence-header">
      <span className="analysis-label">
        🧠 QUESTION INTELLIGENCE
      </span>

      <h2>How Did You Perform?</h2>

      <p>
        EduMind AI analyzed your accuracy, response time,
        and performance for each question.
      </p>
    </div>

    {/* Main Statistics */}
    <div className="question-intelligence-stats">

      <div className="question-intelligence-stat">
        <strong>
          {questionIntelligence.total_questions ?? 0}
        </strong>
        <span>Total Questions</span>
      </div>

      <div className="question-intelligence-stat">
        <strong>
          {questionIntelligence.correct_questions ?? 0}
        </strong>
        <span>Correct</span>
      </div>

      <div className="question-intelligence-stat">
        <strong>
          {questionIntelligence.incorrect_questions ?? 0}
        </strong>
        <span>Incorrect</span>
      </div>

      <div className="question-intelligence-stat">
        <strong>
          {questionIntelligence.average_time ?? 0}s
        </strong>
        <span>Average Time</span>
      </div>

    </div>

    {/* Overall Insight */}
    {questionIntelligence.overall_insight && (
      <div className="question-intelligence-insight">

        <strong>💡 Overall Insight</strong>

        <p>
          {questionIntelligence.overall_insight}
        </p>

      </div>
    )}

    {/* Most Time Consuming Question */}
    {questionIntelligence.most_time_consuming_question && (
      <div className="question-intelligence-focus">

        <strong>
          ⏱️ Most Time-Consuming Question
        </strong>

        <p>
          Question{" "}
          {questionIntelligence.most_time_consuming_question.question_number}
          :{" "}
          {questionIntelligence.most_time_consuming_question.question}
        </p>

        <span>
          Time:{" "}
          {questionIntelligence.most_time_consuming_question.time_spent}
          s
        </span>

        <span>
          Difficulty:{" "}
          {questionIntelligence.most_time_consuming_question.difficulty}
        </span>

        <span>
          Performance:{" "}
          {questionIntelligence.most_time_consuming_question.performance}
        </span>

      </div>
    )}

    {/* Strong Questions */}
    <div className="question-intelligence-strong">

      <strong>⭐ Strong Questions</strong>

      <p>
        You answered{" "}
        {questionIntelligence.strong_questions ?? 0}{" "}
        question(s) quickly and correctly.
      </p>

    </div>

    {/* Question-by-Question Analysis */}
    {Array.isArray(questionIntelligence.questions) &&
      questionIntelligence.questions.length > 0 && (

        <div className="question-intelligence-list">

          <h3>📊 Question-by-Question Analysis</h3>

          {questionIntelligence.questions.map(
            (item, index) => (

              <div
                className="question-intelligence-item"
                key={index}
              >

                <div className="question-intelligence-item-header">

                  <strong>
                    Question {item.question_number}
                  </strong>

                  <span>
                    {item.time_spent}s
                  </span>

                </div>

                <p>
                  {item.question}
                </p>
                <button
                  className="explain-learn-button"
                  onClick={() => {
                    const sourceQuizItem = quiz[index];

                    const correctAnswer =
                      sourceQuizItem?.correct_answer ??
                      sourceQuizItem?.answer ??
                      item.correct_answer ??
                      item.answer ??
                      "";

                    const questionId = sourceQuizItem
                      ? getQuestionKey(sourceQuizItem, index)
                      : null;

                    const studentAnswer = questionId
                      ? selectedAnswers[questionId] ?? ""
                      : "";

                    handleExplainToLearn({
                      question: item.question || sourceQuizItem?.question || "",
                      topic: item.topic || sourceQuizItem?.topic || "General",
                      student_answer: studentAnswer,
                      correct_answer: correctAnswer,
                    });
                  }}
                  disabled={explainLoading}
                >
                  {explainLoading
                    ? "🧠 Explaining..."
                    : "🧠 Explain This Concept"}
                </button>

                <div className="question-intelligence-tags">

                  <span>
                    Topic: {item.topic}
                  </span>

                  <span>
                    Difficulty: {item.difficulty}
                  </span>

                  <span>
                    Performance: {item.performance}
                  </span>

                  <span>
                    {item.is_correct
                      ? "✅ Correct"
                      : "❌ Incorrect"}
                  </span>

                </div>

                {item.insight && (
                  <small>
                    💡 {item.insight}
                  </small>
                )}

              </div>

            )
          )}

        </div>
      )}

  </section>
)}

{/* ============================================================
    RECOVERY MODE
============================================================ */}

{recoveryAnalysis && (
  <section className="recovery-mode-card">

    <div className="recovery-mode-header">
      <span className="analysis-label">
        🔄 RECOVERY MODE
      </span>

      <h2>Let's Strengthen Your Weak Areas</h2>

      <p>
        EduMind AI identified the questions that need more
        practice and created a recovery plan for you.
      </p>
    </div>

    {!recoveryAnalysis.recovery_required ? (
      <div className="recovery-success">
        <h3>🎉 Excellent Performance!</h3>
        <p>
          No recovery is required. You answered all questions correctly.
        </p>
      </div>
    ) : (
      <>
        <div className="recovery-stats">

          <div className="recovery-stat">
            <strong>
              {recoveryAnalysis.weak_question_count ?? 0}
            </strong>
            <span>Weak Questions</span>
          </div>

          <div className="recovery-stat">
            <strong>
              {recoveryAnalysis.weak_topics?.length ?? 0}
            </strong>
            <span>Weak Topics</span>
          </div>

        </div>

        {Array.isArray(recoveryAnalysis.weak_topics) &&
          recoveryAnalysis.weak_topics.length > 0 && (
            <div className="recovery-topics">

              <h3>📚 Topics to Review</h3>

              <div className="recovery-topic-list">
                {recoveryAnalysis.weak_topics.map(
                  (topic, index) => (
                    <span key={index}>
                      {topic}
                    </span>
                  )
                )}
              </div>

            </div>
          )}

        {Array.isArray(recoveryAnalysis.recovery_plan) &&
          recoveryAnalysis.recovery_plan.length > 0 && (
            <div className="recovery-plan">

              <h3>🔄 Recovery Plan</h3>

              {recoveryAnalysis.recovery_plan.map(
                (item, index) => (
                  <div
                    className="recovery-plan-item"
                    key={index}
                  >

                    <div className="recovery-plan-header">
                      <strong>
                        Recovery {item.recovery_number}
                      </strong>

                      <span>
                        {item.priority} Priority
                      </span>
                    </div>

                    <p>
                      {item.question}
                    </p>

                    <div className="recovery-plan-tags">
                      <span>
                        Topic: {item.topic}
                      </span>

                      <span>
                        Reason: {item.reason}
                      </span>
                    </div>
                    <button
  className="explain-learn-button"
  onClick={() => handleExplainToLearn(item)}
  disabled={explainLoading}
>
  {explainLoading
    ? "🧠 Explaining..."
    : "🧠 Explain This Concept"}
</button>

                    <small>
                      💡 {item.action}
                    </small>

                  </div>
                )
              )}

            </div>
          )}

        {recoveryAnalysis.recommendation && (
          <div className="recovery-recommendation">

            <strong>💡 Recommendation</strong>

            <p>
              {recoveryAnalysis.recommendation}
            </p>

          </div>
        )}
      </>
    )}

  </section>
)}
{/* ============================================================
    EXPLAIN-TO-LEARN RESULT
============================================================ */}

{explainAnalysis && (
  <section className="explain-learn-card">

    <div className="explain-learn-header">
      <span className="analysis-label">
        🧠 EXPLAIN-TO-LEARN AI
      </span>

      <h2>Understand the Concept</h2>

      <p>
        EduMind AI analyzed your answer and created a
        personalized explanation using Gemini.
      </p>
    </div>

    <div className="explain-learn-topic">
      <strong>📚 Topic</strong>
      <p>{explainAnalysis.topic}</p>
    </div>

    <div className="explain-learn-wrong">
      <strong>❌ Why Your Answer Needs Improvement</strong>
      <p>
        {explainAnalysis.why_student_wrong}
      </p>
    </div>

    <div className="explain-learn-explanation">
      <strong>💡 Concept Explanation</strong>
      <p>
        {explainAnalysis.explanation}
      </p>
    </div>

    <div className="explain-learn-example">
      <strong>📝 Simple Example</strong>
      <p>
        {explainAnalysis.example}
      </p>
    </div>

    <div className="explain-learn-memory">
      <strong>🧠 Memory Tip</strong>
      <p>
        {explainAnalysis.memory_tip}
      </p>
    </div>

    <div className="explain-learn-next">
      <strong>🎯 What to Do Next</strong>
      <p>
        {explainAnalysis.next_step}
      </p>
    </div>

    <div className="explain-learn-practice">
      <strong>❓ Practice Question</strong>
      <p>
        {explainAnalysis.practice_question}
      </p>
    </div>

  </section>
)}






        {/* ====================================================
    AI GENERATED STUDY NOTES
==================================================== */}

{aiNotes && (

  <section
    id="ai-notes-section"
    className="ai-notes-section"
  >

    <div className="ai-notes-header">

      <div className="topics-label">
        📚 AI STUDY MATERIAL
      </div>

      <h2>
        {aiNotes.title || "AI Study Notes"}
      </h2>

      <p>
        Gemini AI generated these personalized
        study notes from your uploaded PDF.
      </p>

    </div>


    {/* ==================================================
        SUMMARY
    ================================================== */}

    {aiNotes.summary && (

      <div className="notes-card">

        <div className="notes-card-icon">
          📝
        </div>

        <div className="notes-card-content">

          <h3>
            Summary
          </h3>

          <p>
            {aiNotes.summary}
          </p>

        </div>

      </div>

    )}


    {/* ==================================================
        KEY POINTS
    ================================================== */}

    {Array.isArray(aiNotes.key_points) &&
      aiNotes.key_points.length > 0 && (

        <div className="notes-card">

          <div className="notes-card-icon">
            🎯
          </div>

          <div className="notes-card-content">

            <h3>
              Key Points
            </h3>

            <ul className="notes-key-points">

              {aiNotes.key_points.map(
                (point, index) => (

                  <li key={index}>
                    <span className="key-point-number">
                      {index + 1}
                    </span>

                    <span>
                      {point}
                    </span>
                  </li>

                )
              )}

            </ul>

          </div>

        </div>

      )}


    {/* ==================================================
        DEFINITIONS
    ================================================== */}

    {Array.isArray(aiNotes.definitions) &&
      aiNotes.definitions.length > 0 && (

        <div className="notes-card">

          <div className="notes-card-icon">
            📖
          </div>

          <div className="notes-card-content">

            <h3>
              Important Definitions
            </h3>

            <div className="definitions-list">

              {aiNotes.definitions.map(
                (item, index) => (

                  <div
                    className="definition-item"
                    key={index}
                  >

                    <h4>
                      {item.term}
                    </h4>

                    <p>
                      {item.definition}
                    </p>

                  </div>

                )
              )}

            </div>

          </div>

        </div>

      )}


    {/* ==================================================
        DETAILED NOTES
    ================================================== */}

    {Array.isArray(aiNotes.notes) &&
      aiNotes.notes.length > 0 && (

        <div className="notes-card">

          <div className="notes-card-icon">
            📚
          </div>

          <div className="notes-card-content">

            <h3>
              Detailed Notes
            </h3>

            <div className="detailed-notes-list">

              {aiNotes.notes.map(
                (item, index) => (

                  <div
                    className="detailed-note"
                    key={index}
                  >

                    <div className="detailed-note-number">
                      {index + 1}
                    </div>

                    <div>

                      <h4>
                        {item.heading}
                      </h4>

                      <p>
                        {item.content}
                      </p>

                    </div>

                  </div>

                )
              )}

            </div>

          </div>

        </div>

      )}


    {/* ==================================================
        GENERATE AGAIN
    ================================================== */}

    <div className="notes-footer">

      <div>

        <strong>
          💡 Study Tip
        </strong>

        <p>
          Review these notes before taking
          the quiz again to improve your score.
        </p>

      </div>

      <button
        className="ai-notes-btn"
        onClick={handleGenerateNotes}
        disabled={notesLoading}
      >
        {notesLoading
          ? "⏳ Generating..."
          : "🔄 Regenerate Notes"}
      </button>

    </div>

  </section>

)}

{/* ====================================================
    AI FLASHCARDS
==================================================== */}

{flashcards.length > 0 && (
  <section
    id="flashcards-section"
    className="flashcards-section"
  >
    <div className="flashcards-header">
      <div>
        <span className="section-badge">AI LEARNING</span>

        <h2>🗂️ AI Flashcards</h2>

        <p>
          Review important concepts from your uploaded study
          material.
        </p>
      </div>

      <button
        className="shuffle-btn"
        onClick={handleShuffleFlashcards}
      >
        🔀 Shuffle
      </button>
    </div>

    <div className="flashcard-progress">
      Card {flashcardIndex + 1} of {flashcards.length}
    </div>

    <div
      className={`flashcard-container ${
        flashcardFlipped ? "flipped" : ""
      }`}
      onClick={() =>
        setFlashcardFlipped((prev) => !prev)
      }
    >
      <div className="flashcard-inner">

        {/* QUESTION */}
        <div className="flashcard-face flashcard-front">
          <span className="flashcard-label">
            QUESTION
          </span>

          <h3>
            {flashcards[flashcardIndex]?.question}
          </h3>

          <p>
            👆 Click to reveal answer
          </p>
        </div>

        {/* ANSWER */}
        <div className="flashcard-face flashcard-back">
          <span className="flashcard-label">
            ANSWER
          </span>

          <p>
            {flashcards[flashcardIndex]?.answer}
          </p>

          <small>
            👆 Click to see question
          </small>
        </div>

      </div>
    </div>

    {/* CONTROLS */}
    <div className="flashcard-controls">

      <button
        onClick={handlePreviousFlashcard}
        disabled={flashcardIndex === 0}
      >
        ← Previous
      </button>

      <button
        className="flip-btn"
        onClick={() =>
          setFlashcardFlipped((prev) => !prev)
        }
      >
        🔄 Flip Card
      </button>

      <button
        onClick={handleNextFlashcard}
        disabled={
          flashcardIndex === flashcards.length - 1
        }
      >
        Next →
      </button>

    </div>
  </section>
)}

        {/* ====================================================
            DETECTED TOPICS
        ==================================================== */}

        {detectedTopics.length >
          0 && (

          <section
            id="topics-section"
            className="topics-section"
          >

            <div className="topics-header">

              <div className="topics-label">
                🧠 AI TOPIC ANALYSIS
              </div>

              <h2>
                Topics Detected
              </h2>

              <p>
                EduMind AI analyzed your
                learning material and
                identified these topics.
              </p>

            </div>

            <div className="topics-grid">

              {detectedTopics.map(
                (
                  topic,
                  index
                ) => (

                  <div
                    className="topic-card"
                    key={index}
                  >

                    <div className="topic-number">
                      {String(
                        index + 1
                      ).padStart(
                        2,
                        "0"
                      )}
                    </div>

                    <div className="topic-icon">
                      🧠
                    </div>

                    <div className="topic-content">

                      <h3>
                        {topic}
                      </h3>

                      <span>
                        Detected from your PDF
                      </span>

                    </div>

                  </div>

                )
              )}

            </div>

            <div className="topics-next">

              <div>

                <strong>
                  🎯 What's next?
                </strong>

                <p>
                  We'll use these topics
                  to identify your skill
                  gaps and create a
                  personalized learning
                  path.
                </p>

              </div>

              <button
                className="learning-path-btn"
                onClick={
                  handleDetectSkillGaps
                }
                disabled={
                  detectingSkillGaps
                }
              >
                {detectingSkillGaps
                  ? "⏳ Analyzing..."
                  : "🚀 Detect Skill Gaps"}
              </button>

            </div>

          </section>

        )}

        {/* ====================================================
            SKILL GAPS
        ==================================================== */}

        {skillGaps.length > 0 && (

          <section
            id="skill-gap-section"
            className="skill-gap-section"
          >

            <div className="skill-gap-header">

              <div className="topics-label">
                🎯 AI SKILL GAP ANALYSIS
              </div>

              <h2>
                Your Skill Gaps
              </h2>

              <p>
                EduMind AI identified
                the areas where you
                need additional practice.
              </p>

            </div>

            <div className="skill-gap-grid">

              {skillGaps.map(
                (
                  gap,
                  index
                ) => {

                  const topic =
                    typeof gap ===
                    "string"
                      ? gap
                      : gap.topic ||
                        gap.name ||
                        "Unknown Topic";

                  const level =
                    typeof gap ===
                    "object"
                      ? gap.level ||
                        gap.difficulty ||
                        "Needs Practice"
                      : "Needs Practice";

                  const recommendation =
                    typeof gap ===
                    "object"
                      ? gap.recommendation ||
                        gap.message ||
                        "Review this topic and practice more questions."
                      : "Review this topic and practice more questions.";

                  return (

                    <div
  className="skill-gap-card"
  key={index}
>
  <div className="skill-gap-number">
    {String(index + 1).padStart(2, "0")}
  </div>

  <div className="skill-gap-icon">
    🎯
  </div>

  <h3>
    {topic}
  </h3>

  <span className="skill-level">
    {level}
  </span>

  <p>
    {recommendation}
  </p>

  {/* ====================================================
      STEP 20 - PRACTICE WEAK SKILL BUTTON
  ==================================================== */}

  <button
    className="learning-path-btn"
    onClick={() =>
      handlePracticeWeakTopic(topic)
    }
    disabled={generatingPracticeQuiz}
  >
    {generatingPracticeQuiz &&
    practiceTopic === topic
      ? "⏳ Generating..."
      : "🧠 Practice Weak Skill"}
  </button>
</div>

                  );
                }
              )}

            </div>

            <div className="learning-path-next">

              <div>

                <strong>
                  🚀 Ready for the next step?
                </strong>

                <p>
                  Based on your performance
                  and skill gaps, create your
                  personalized learning path.
                </p>

              </div>

              <button
                className="learning-path-btn"
                onClick={
                  handleCreateLearningPath
                }
                disabled={
                  creatingLearningPath
                }
              >
                {creatingLearningPath
                  ? "⏳ Creating..."
                  : "🚀 Create Learning Path"}
              </button>

            </div>



{/* ============================================================
    STEP 21 - AI REVISION
============================================================ */}

{/* ============================================================
    STEP 21 - AI REVISION
============================================================ */}

<div className="revision-section">

  <div className="revision-header">

    <div className="topics-label">
      🔄 AI REVISION
    </div>

    <h2>
      Revise Your Weak Topics
    </h2>

    <p>
      Strengthen your weak skills with AI-generated
      revision questions based on your learning gaps.
    </p>

  </div>


  {/* START AI REVISION */}

  <button
    type="button"
    className="learning-path-btn"
    onClick={() => {

      setRevisionAnswers({});
      setRevisionSubmitted(false);
      setRevisionScore(0);

      handleGenerateRevision(
        skillGaps.length > 0
          ? skillGaps
          : revisionTopics
      );

    }}
    disabled={
      loadingRevision ||
      (
        skillGaps.length === 0 &&
        revisionTopics.length === 0
      )
    }
  >
    {loadingRevision
      ? "⏳ Generating Revision..."
      : "🔄 Start AI Revision"}
  </button>


  {/* ==========================================================
      REVISION QUESTIONS
  ========================================================== */}

  {revisionQuestions.length > 0 && (

    <div className="revision-questions">

      <h3>
        AI Revision Questions
      </h3>


      {revisionQuestions.map(
        (question, index) => {

          const selectedAnswer =
            revisionAnswers[index] || "";

          const correctAnswer =
            question.correct_answer ??
            question.answer ??
            "";

          const correct =
            revisionSubmitted &&
            normalizeText(
              selectedAnswer
            ) ===
            normalizeText(
              correctAnswer
            );


          return (

            <div
              className={`question-card ${
                revisionSubmitted
                  ? correct
                    ? "question-correct"
                    : "question-wrong"
                  : ""
              }`}
              key={index}
            >


              {/* QUESTION TOP */}

              <div className="question-top">

                <span className="question-number">
                  Question{" "}
                  {index + 1}
                </span>

                <span className="question-badge">
                  ✨ AI Revision
                </span>

              </div>


              {/* QUESTION */}

              <h3>
                {question.question ||
                  question.text ||
                  question.prompt ||
                  "Revision Question"}
              </h3>


              {/* ANSWER AREA */}

              <div className="answer-area">

                <label>
                  Select Your Answer
                </label>


                {/* OPTIONS */}

                <div className="quiz-options">

                  {Array.isArray(
                    question.options
                  ) &&
                    question.options.map(
                      (
                        option,
                        optionIndex
                      ) => {

                        const optionText =
                          typeof option ===
                          "string"
                            ? option
                            : option?.label ??
                              option?.text ??
                              option?.value ??
                              option?.option ??
                              "";

                        const isSelected =
                          normalizeText(
                            selectedAnswer
                          ) ===
                          normalizeText(
                            optionText
                          );

                        const isCorrectOption =
                          revisionSubmitted &&
                          normalizeText(
                            optionText
                          ) ===
                          normalizeText(
                            correctAnswer
                          );

                        const isWrongOption =
                          revisionSubmitted &&
                          isSelected &&
                          !isCorrectOption;


                        return (

                          <button
                            key={
                              optionIndex
                            }
                            type="button"
                            className={`quiz-option ${
                              isSelected
                                ? "selected"
                                : ""
                            } ${
                              isCorrectOption
                                ? "correct"
                                : ""
                            } ${
                              isWrongOption
                                ? "wrong"
                                : ""
                            }`}
                            onClick={() =>
                              handleRevisionAnswer(
                                index,
                                optionText
                              )
                            }
                            disabled={
                              revisionSubmitted
                            }
                          >

                            <span className="option-letter">
                              {String.fromCharCode(
                                65 +
                                  optionIndex
                              )}
                            </span>


                            <span className="option-text">
                              {optionText}
                            </span>


                            <span className="option-check">

                              {revisionSubmitted &&
                              isCorrectOption
                                ? "✓"
                                : revisionSubmitted &&
                                  isWrongOption
                                ? "✗"
                                : isSelected
                                ? "✓"
                                : ""}

                            </span>

                          </button>

                        );

                      }
                    )}

                </div>

              </div>


              {/* ==================================================
                  FEEDBACK
              ================================================== */}

              {revisionSubmitted && (

                <div className="answer-feedback">

                  <div className="feedback-answer">

                    <strong>

                      {correct
                        ? "✓ Correct Answer"
                        : "✗ Incorrect Answer"}

                    </strong>


                    <p>

                      Correct answer:{" "}

                      {correctAnswer ||
                        "Not available"}

                    </p>


                    {!correct &&
                      selectedAnswer && (

                        <p>

                          Your answer:{" "}

                          {selectedAnswer}

                        </p>

                      )}

                  </div>


                  <div className="feedback-explanation">

                    <strong>
                      💡 Explanation
                    </strong>


                    <p>

                      {question.explanation ||
                        "Review the learning material to understand this concept."}

                    </p>

                  </div>

                </div>

              )}

            </div>

          );

        }
      )}


      {/* ==========================================================
          SUBMIT / RESULT
      ========================================================== */}

      <div className="revision-submit-area">

        {!revisionSubmitted ? (

          <button
            type="button"
            className="submit-revision-btn"
            onClick={
              handleSubmitRevision
            }
          >
            🎯 Submit Revision
          </button>

        ) : (

          <div className="revision-result">

            <div className="revision-result-icon">

              {revisionScore ===
              revisionQuestions.length
                ? "🏆"
                : revisionScore >=
                  revisionQuestions.length / 2
                ? "🎉"
                : "💪"}

            </div>


            <h3>
              AI Revision Completed
            </h3>


            <div className="revision-score">

              {revisionScore}

              <span>
                / {revisionQuestions.length}
              </span>

            </div>


            <p>

              {revisionScore ===
              revisionQuestions.length
                ? "Excellent! You mastered these weak topics."
                : revisionScore >=
                  revisionQuestions.length / 2
                ? "Good work! Review the incorrect answers."
                : "Keep practicing these topics and try again."}

            </p>


            <button
              type="button"
              className="retake-revision-btn"
              onClick={() => {

                setRevisionAnswers({});
                setRevisionSubmitted(false);
                setRevisionScore(0);

              }}
            >
              🔄 Retry Revision
            </button>

          </div>

        )}

      </div>

    </div>

  )}

</div>

            

          </section>

        )}

        {/* ====================================================
            PERSONALIZED PATH
        ==================================================== */}

        {personalizedPath && (

          <section
            id="personalized-path-section"
            className="personalized-path-section"
          >

            <div className="section-heading">

              <span>
                🚀 PERSONALIZED PLAN
              </span>

              <h2>
                Your Learning Path
              </h2>

              <p>
                EduMind AI created a
                learning plan based on
                your quiz performance.
              </p>

            </div>

            {personalizedPath.weak_topics &&
              personalizedPath
                .weak_topics.length >
                0 && (

                <div className="path-card">

                  <div className="path-icon">
                    📚
                  </div>

                  <div>

                    <h3>
                      Focus Areas
                    </h3>

                    <ul>

                      {personalizedPath
                        .weak_topics
                        .map(
                          (
                            topic,
                            index
                          ) => (

                            <li
                              key={
                                index
                              }
                            >
                              {topic}
                            </li>

                          )
                        )}

                    </ul>

                  </div>

                </div>

              )}

            {personalizedPath.strong_topics &&
              personalizedPath
                .strong_topics.length >
                0 && (

                <div className="path-card">

                  <div className="path-icon">
                    🏆
                  </div>

                  <div>

                    <h3>
                      Your Strengths
                    </h3>

                    <ul>

                      {personalizedPath
                        .strong_topics
                        .map(
                          (
                            topic,
                            index
                          ) => (

                            <li
                              key={
                                index
                              }
                            >
                              {topic}
                            </li>

                          )
                        )}

                    </ul>

                  </div>

                </div>

              )}

            {personalizedPath.recommendation && (

              <div className="path-card">

                <div className="path-icon">
                  💡
                </div>

                <div>

                  <h3>
                    AI Recommendation
                  </h3>

                  <p>
                    {
                      personalizedPath
                        .recommendation
                    }
                  </p>

                </div>

              </div>

            )}

            {personalizedPath.message && (

              <div className="path-card">

                <div className="path-icon">
                  🎯
                </div>

                <div>

                  <h3>
                    Next Step
                  </h3>

                  <p>
                    {
                      personalizedPath
                        .message
                    }
                  </p>

                </div>

              </div>

            )}

          </section>

        )}

        {/* ====================================================
            AI TUTOR
        ==================================================== */}

        <section
          id="ai-tutor-section"
          className="ai-tutor-section"
        >

          <div className="section-heading">

            <span>
              🤖 AI TUTOR
            </span>

            <h2>
              Ask Your AI Tutor
            </h2>

            <p>
              Get personalized explanations
              and guidance from your AI
              learning assistant.
            </p>

          </div>

          <div className="ai-tutor-container">

            {/* TUTOR HEADER */}

            <div className="tutor-header">

              <div className="tutor-avatar">
                🤖
              </div>

              <div className="tutor-title">

                <h3>
                  EduMind AI Tutor
                </h3>

                <span>
                  Gemini AI
                </span>

              </div>

              <div className="tutor-online">

                <span className="online-dot"></span>

                AI Online

              </div>

              {tutorHistory.length >
                0 && (

                <button
                  className="clear-chat-btn"
                  onClick={
                    clearTutorChat
                  }
                >
                  🗑 Clear
                </button>

              )}

            </div>

            {/* CHAT */}

            <div className="tutor-chat">

              {tutorHistory.length ===
                0 &&
                !askingTutor && (

                  <div className="tutor-welcome">

                    <div className="welcome-icon">
                      🧠
                    </div>

                    <h3>
                      Hello! I'm your AI Tutor 👋
                    </h3>

                    <p>
                      Ask me anything about
                      your learning material.
                    </p>

                    <div className="quick-questions">

                      <button
                        onClick={() =>
                          setTutorQuestion(
                            "Explain photosynthesis in simple words."
                          )
                        }
                      >
                        🌱 Explain a topic
                      </button>

                      <button
                        onClick={() =>
                          setTutorQuestion(
                            "Give me an example to understand this concept."
                          )
                        }
                      >
                        💡 Give an example
                      </button>

                      <button
                        onClick={() =>
                          setTutorQuestion(
                            "Give me a short quiz about this topic."
                          )
                        }
                      >
                        📝 Test me
                      </button>

                    </div>

                  </div>

                )}

              {tutorHistory.map(
                (
                  chat,
                  index
                ) => (

                  <div
                    className="tutor-conversation"
                    key={index}
                  >

                    {/* USER */}

                    <div className="user-message">

                      <div className="user-message-avatar">
                        👤
                      </div>

                      <div className="user-message-content">

                        <div className="message-label">
                          You
                        </div>

                        <p>
                          {chat.question}
                        </p>

                      </div>

                    </div>

                    {/* AI */}

                    <div className="tutor-message">

                      <div className="tutor-message-avatar">
                        🤖
                      </div>

                      <div className="tutor-message-content">

                        <div className="tutor-message-header">

                          <strong>
                            EduMind AI Tutor
                          </strong>

                          <span>
                            Gemini AI
                          </span>

                        </div>

                        <div className="ai-answer">
                          {chat.answer}
                        </div>

                      </div>

                    </div>

                  </div>

                )
              )}

              {askingTutor && (

                <div className="tutor-loading">

                  <div className="loading-icon">
                    🧠
                  </div>

                  <div>

                    <strong>
                      AI Tutor is thinking...
                    </strong>

                    <span>
                      Gemini is generating your answer
                    </span>

                  </div>

                  <div className="typing-dots">

                    <span></span>
                    <span></span>
                    <span></span>

                  </div>

                </div>

              )}

            </div>

            {/* INPUT */}

            <div className="tutor-input-area">

              <textarea
                value={
                  tutorQuestion
                }
                onChange={(e) =>
                  setTutorQuestion(
                    e.target.value
                  )
                }
                placeholder="Ask anything about your learning material..."
                rows={3}
                disabled={
                  askingTutor
                }
                onKeyDown={(e) => {

                  if (
                    e.key ===
                      "Enter" &&
                    !e.shiftKey
                  ) {
                    e.preventDefault();

                    handleAskTutor();
                  }

                }}
              />

              <div className="tutor-input-bottom">

                <span>
                  💡 Enter = Ask&nbsp;&nbsp;
                  • &nbsp;&nbsp;Shift + Enter = New line
                </span>

                <button
                  className="tutor-ask-btn"
                  onClick={
                    handleAskTutor
                  }
                  disabled={
                    askingTutor ||
                    !tutorQuestion.trim()
                  }
                >
                  {askingTutor
                    ? "🧠 Thinking..."
                    : "🚀 Ask AI Tutor"}
                </button>

              </div>

            </div>

          </div>

        </section>

        {/* ====================================================
            FEATURES
        ==================================================== */}

        <section
          id="features"
          className="features-section"
        >

          <div className="section-heading">

            <span>
              POWERFUL FEATURES
            </span>

            <h2>
              Everything you need
              to learn better
            </h2>

            <p>
              One intelligent platform
              for personalized learning,
              assessment and progress
              tracking.
            </p>

          </div>

          <div className="features-grid">

            <div className="feature-card">

              <div className="feature-icon">
                📄
              </div>

              <h3>
                Upload Materials
              </h3>

              <p>
                Upload PDFs and learning
                materials for AI-powered
                analysis.
              </p>

            </div>

            <div className="feature-card">

              <div className="feature-icon">
                🧠
              </div>

              <h3>
                Topic Detection
              </h3>

              <p>
                Automatically identify
                important topics from
                your learning material.
              </p>

            </div>

            <div className="feature-card">

              <div className="feature-icon">
                📝
              </div>

              <h3>
                AI Quiz Generator
              </h3>

              <p>
                Automatically generate
                quizzes from your
                learning materials.
              </p>

            </div>

            <div className="feature-card">

              <div className="feature-icon">
                🎯
              </div>

              <h3>
                Skill Gap Detection
              </h3>

              <p>
                Discover topics where
                you need additional
                practice.
              </p>

            </div>

            <div className="feature-card">

              <div className="feature-icon">
                🤖
              </div>

              <h3>
                AI Tutor
              </h3>

              <p>
                Ask questions and receive
                AI-powered explanations
                from Gemini AI.
              </p>

            </div>

            <div className="feature-card">

              <div className="feature-icon">
                📊
              </div>

              <h3>
                Progress Dashboard
              </h3>

              <p>
                Track quiz scores and
                learning progress.
              </p>

            </div>

          </div>

        </section>

        {/* ====================================================
            ABOUT
        ==================================================== */}

        <section
          id="about"
          className="about-section"
        >

          <div className="section-heading">

            <span>
              ABOUT EDUMIND AI
            </span>

            <h2>
              Learn according to
              your strengths
            </h2>

            <p>
              EduMind AI transforms
              traditional learning into
              an intelligent, personalized
              experience. Upload your
              material, take an AI-generated
              quiz, discover your skill gaps,
              and follow a personalized
              learning path.
            </p>

          </div>

        </section>

      </main>

      {/* ======================================================
          FOOTER
      ====================================================== */}

      <footer>

        <div className="footer-logo">

          🎓

          <strong>
            EduMind AI
          </strong>

        </div>

        <p>
          AI-powered personalized
          learning for everyone.
        </p>

        <span>
          © 2026 EduMind AI
        </span>

      </footer>

    </div>
  );
}

export default App;