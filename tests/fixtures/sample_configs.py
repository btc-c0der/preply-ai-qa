"""
Sample configuration data for testing the AI-QA Studies Portal.

This module contains realistic test data that mimics the actual
configuration structures used in the application.
"""

from typing import Dict, Any

# Sample module configuration matching the actual app structure
SAMPLE_MODULE_CONFIG: Dict[str, Any] = {
    "modules": {
        "programming_with_ai": {
            "title": "Programming/Building Projects with AI",
            "description": "Practical AI-driven development for QA professionals",
            "topics": [
                "Automation Tools Development",
                "Chatbot Integration for QA",
                "Personal QA Assistants",
                "Test Data Generation",
                "API Testing Automation"
            ],
            "hands_on": True,
            "difficulty": "intermediate"
        },
        "ai_best_practices": {
            "title": "Best Practices with AI",
            "description": "Effective and safe AI usage in QA workflows",
            "topics": [
                "Prompt Design for QA",
                "Workflow Integration",
                "Smart Decision Making",
                "AI Model Selection",
                "Quality Metrics"
            ],
            "hands_on": True,
            "difficulty": "beginner"
        },
        "qa_ai_integration": {
            "title": "QA + AI Integration",
            "description": "Advanced AI integration in testing processes",
            "topics": [
                "Automated Test Case Generation",
                "AI-Driven Bug Analysis",
                "LLM Integration in Testing",
                "Visual Testing with AI",
                "Performance Testing Automation"
            ],
            "hands_on": True,
            "difficulty": "advanced"
        }
    },
    "presentation_templates": {
        "introduction": {
            "slides": [
                "Welcome to AI-Driven QA",
                "Your Learning Journey",
                "Tools and Resources",
                "Expected Outcomes"
            ]
        },
        "module_overview": {
            "slides": [
                "Module Introduction",
                "Learning Objectives",
                "Key Topics",
                "Hands-on Activities",
                "Assessment Criteria"
            ]
        },
        "hands_on_session": {
            "slides": [
                "Setup and Prerequisites",
                "Step-by-Step Implementation",
                "Common Challenges",
                "Best Practices",
                "Next Steps"
            ]
        },
        "conclusion": {
            "slides": [
                "Key Takeaways",
                "Further Resources",
                "Community and Support",
                "Certification Path"
            ]
        }
    },
    "assessment_criteria": {
        "beginner": {
            "understanding": 40,
            "application": 30,
            "problem_solving": 30
        },
        "intermediate": {
            "understanding": 30,
            "application": 40,
            "problem_solving": 30
        },
        "advanced": {
            "understanding": 20,
            "application": 40,
            "problem_solving": 40
        }
    }
}

# Sample user progress data
SAMPLE_USER_PROGRESS: Dict[str, Any] = {
    "current_module": "programming_with_ai",
    "completed_modules": ["ai_best_practices"],
    "current_progress": 25.5,
    "skills_acquired": [
        "Prompt Design for QA",
        "Workflow Integration",
        "Smart Decision Making"
    ],
    "assessments_completed": [
        {
            "module": "ai_best_practices",
            "score": 85,
            "completed_date": "2025-07-10T14:30:00Z",
            "areas": {
                "understanding": 90,
                "application": 80,
                "problem_solving": 85
            }
        }
    ],
    "hands_on_projects": [
        {
            "project_id": "chatbot_integration_basic",
            "module": "ai_best_practices",
            "status": "completed",
            "completion_date": "2025-07-09T16:45:00Z",
            "feedback": "Excellent implementation of basic chatbot features"
        }
    ],
    "learning_path": "intermediate",
    "preferences": {
        "difficulty_level": "intermediate",
        "focus_areas": ["automation", "integration"],
        "hands_on_preference": True
    },
    "session_history": [
        {
            "timestamp": "2025-07-13T10:00:00Z",
            "module": "ai_best_practices",
            "action": "complete",
            "session_duration": 3600
        },
        {
            "timestamp": "2025-07-13T11:00:00Z",
            "module": "programming_with_ai",
            "action": "start",
            "session_duration": 0
        }
    ],
    "bookmarks": [
        {
            "module": "programming_with_ai",
            "slide": "Automation Tools Development",
            "notes": "Important for current project"
        }
    ],
    "notes": {
        "programming_with_ai": "Focus on API testing automation",
        "general": "Need to practice more with prompt engineering"
    }
}

# Additional test configurations for edge cases
EMPTY_MODULE_CONFIG: Dict[str, Any] = {
    "modules": {},
    "presentation_templates": {},
    "assessment_criteria": {}
}

MINIMAL_MODULE_CONFIG: Dict[str, Any] = {
    "modules": {
        "test_module": {
            "title": "Test Module",
            "description": "A test module",
            "topics": ["Topic 1"],
            "hands_on": False,
            "difficulty": "beginner"
        }
    },
    "presentation_templates": {
        "introduction": {
            "slides": ["Welcome"]
        }
    },
    "assessment_criteria": {
        "beginner": {
            "understanding": 100,
            "application": 0,
            "problem_solving": 0
        }
    }
}

INVALID_MODULE_CONFIG: Dict[str, Any] = {
    "modules": {
        "invalid_module": {
            "title": "Invalid Module",
            # Missing required fields: description, topics, hands_on, difficulty
        }
    }
}

# Test data for different user scenarios
NEW_USER_PROGRESS: Dict[str, Any] = {
    "current_module": None,
    "completed_modules": [],
    "current_progress": 0,
    "skills_acquired": [],
    "assessments_completed": [],
    "hands_on_projects": [],
    "learning_path": "custom",
    "preferences": {
        "difficulty_level": "beginner",
        "focus_areas": [],
        "hands_on_preference": True
    },
    "session_history": [],
    "bookmarks": [],
    "notes": {}
}

ADVANCED_USER_PROGRESS: Dict[str, Any] = {
    "current_module": "qa_ai_integration",
    "completed_modules": ["ai_best_practices", "programming_with_ai"],
    "current_progress": 75.0,
    "skills_acquired": [
        "Prompt Design for QA",
        "Workflow Integration",
        "Smart Decision Making",
        "Automation Tools Development",
        "Chatbot Integration for QA",
        "Personal QA Assistants"
    ],
    "assessments_completed": [
        {
            "module": "ai_best_practices",
            "score": 95,
            "completed_date": "2025-07-01T14:30:00Z",
            "areas": {"understanding": 95, "application": 95, "problem_solving": 95}
        },
        {
            "module": "programming_with_ai",
            "score": 88,
            "completed_date": "2025-07-08T16:20:00Z",
            "areas": {"understanding": 85, "application": 90, "problem_solving": 90}
        }
    ],
    "hands_on_projects": [
        {
            "project_id": "advanced_automation_suite",
            "module": "programming_with_ai",
            "status": "completed",
            "completion_date": "2025-07-08T18:00:00Z",
            "feedback": "Outstanding implementation with innovative approaches"
        }
    ],
    "learning_path": "advanced",
    "preferences": {
        "difficulty_level": "advanced",
        "focus_areas": ["integration", "automation", "ai_models"],
        "hands_on_preference": True
    },
    "session_history": [
        {
            "timestamp": "2025-07-13T09:00:00Z",
            "module": "qa_ai_integration",
            "action": "start",
            "session_duration": 0
        }
    ],
    "bookmarks": [
        {
            "module": "qa_ai_integration",
            "slide": "LLM Integration in Testing",
            "notes": "Key for enterprise implementation"
        }
    ],
    "notes": {
        "qa_ai_integration": "Focus on enterprise-scale solutions",
        "general": "Ready for certification path"
    }
}
