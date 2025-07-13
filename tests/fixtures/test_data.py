"""
Test data and mock responses for AI-QA Studies Portal testing.

This module contains mock data for presentations, charts, API responses,
and other components used in testing.
"""

from typing import Dict, Any, List

# Mock presentation data
MOCK_PRESENTATION_DATA: Dict[str, Any] = {
    "sample_slide": """# 🚀 Welcome to AI-Driven QA

Welcome to the **AI-Driven Quality Assurance Professional Development Portal**!

## What You'll Experience:
- 🎯 **Practical AI Integration** in QA workflows
- 🛠️ **Hands-on Projects** with real-world applications
- 📊 **Template-driven Learning** with structured presentations
- 🤖 **AI Tools and Techniques** specific to QA professionals

## Our Approach:
- **Theory + Practice**: Balance conceptual understanding with practical implementation
- **Personalized Learning**: Adapt to your experience level and interests
- **Community Focus**: Connect with fellow QA professionals exploring AI

Ready to transform your QA practice with AI? Let's begin! 🌟""",
    
    "module_overview_slide": """# 📖 Module Introduction: Programming with AI

## Module Overview
Practical AI-driven development for QA professionals

### 🎯 Target Audience:
- **Difficulty Level**: Intermediate
- **Hands-on Component**: ✅ Yes
- **Prerequisites**: Basic understanding of QA processes

### 📊 Module Structure:
- **Duration**: 2-4 hours (flexible pacing)
- **Format**: Interactive presentations + practical exercises
- **Assessment**: Hands-on projects and knowledge checks
- **Certification**: Module completion certificate""",
    
    "hands_on_slide": """# 🛠️ Hands-on Activities

## Interactive Exercises:
- **Live Coding Sessions** - Build AI tools together
- **Problem-Solving Challenges** - Real QA scenarios
- **Peer Collaboration** - Group projects and discussions
- **Tool Exploration** - Hands-on with latest AI platforms

## Practical Projects:
1. **Mini-Project**: Quick implementation (30 minutes)
2. **Main Project**: Comprehensive solution (90 minutes)
3. **Extension Challenge**: Advanced features (optional)""",
    
    "invalid_slide": "",
    "empty_slide": None
}

# Mock chart data for visualization testing
MOCK_CHART_DATA: Dict[str, Any] = {
    "progress_data": {
        "modules": ["AI Best Practices", "Programming with AI", "QA Integration"],
        "completion": [1, 0.5, 0],
        "colors": ["green", "orange", "lightgray"]
    },
    "skills_data": {
        "skills": ["AI Integration", "Prompt Engineering", "Automation", "Analysis", "Innovation"],
        "values": [0.8, 0.6, 0.9, 0.7, 0.5]
    },
    "sample_data": [
        {"module": "AI Best Practices", "progress": 100, "score": 95},
        {"module": "Programming with AI", "progress": 50, "score": 0},
        {"module": "QA Integration", "progress": 0, "score": 0}
    ],
    "html_output": """<div id="plotly-chart">
        <script>
            // Mock Plotly chart HTML
            var data = [{x: ['Module 1', 'Module 2'], y: [1, 0.5]}];
            Plotly.newPlot('chart', data);
        </script>
    </div>""",
    "json_data": {
        "data": [{"x": ["Module 1", "Module 2"], "y": [1, 0.5], "type": "bar"}],
        "layout": {"title": "Learning Progress"}
    }
}

# Mock API responses
MOCK_API_RESPONSES: Dict[str, Any] = {
    "module_list": {
        "status": "success",
        "data": [
            {"id": "ai_best_practices", "title": "Best Practices with AI"},
            {"id": "programming_with_ai", "title": "Programming with AI"},
            {"id": "qa_ai_integration", "title": "QA + AI Integration"}
        ]
    },
    "progress_update": {
        "status": "success",
        "message": "Progress updated successfully",
        "data": {
            "current_progress": 33.3,
            "modules_completed": 1,
            "total_modules": 3
        }
    },
    "slide_generation": {
        "status": "success",
        "data": {
            "slide_content": MOCK_PRESENTATION_DATA["sample_slide"],
            "slide_number": 1,
            "total_slides": 4,
            "template_type": "introduction"
        }
    },
    "error_response": {
        "status": "error",
        "message": "Module not found",
        "error_code": "MODULE_NOT_FOUND"
    },
    "validation_error": {
        "status": "error",
        "message": "Invalid input parameters",
        "errors": [
            {"field": "module_id", "message": "Module ID is required"},
            {"field": "slide_index", "message": "Slide index must be a positive integer"}
        ]
    }
}

# Mock user interaction data
MOCK_USER_INTERACTIONS: Dict[str, List[Dict[str, Any]]] = {
    "button_clicks": [
        {"element": "start_module_btn", "module": "ai_best_practices", "timestamp": "2025-07-13T10:00:00Z"},
        {"element": "generate_slide_btn", "template": "introduction", "timestamp": "2025-07-13T10:01:00Z"},
        {"element": "complete_module_btn", "module": "ai_best_practices", "timestamp": "2025-07-13T12:00:00Z"}
    ],
    "form_submissions": [
        {
            "form": "progress_update",
            "data": {"module_id": "ai_best_practices", "action": "complete"},
            "timestamp": "2025-07-13T12:00:00Z"
        }
    ],
    "navigation": [
        {"from": "dashboard", "to": "presentations", "timestamp": "2025-07-13T10:00:00Z"},
        {"from": "presentations", "to": "hands_on_lab", "timestamp": "2025-07-13T11:00:00Z"},
        {"from": "hands_on_lab", "to": "resources", "timestamp": "2025-07-13T11:30:00Z"}
    ]
}

# Mock chatbot responses
MOCK_CHATBOT_RESPONSES: Dict[str, str] = {
    "greeting": "Hi! I'm your AI QA assistant. How can I help you today?",
    "help_request": "I can help you with QA automation, AI integration, testing strategies, and learning resources. What specific topic interests you?",
    "automation_question": "For QA automation with AI, I recommend starting with test case generation using LLMs. Would you like me to show you an example?",
    "integration_question": "AI integration in QA can be approached through several methods: automated test generation, intelligent bug analysis, and performance prediction. Which area would you like to explore?",
    "error_response": "I'm sorry, I didn't understand that. Could you please rephrase your question or ask about QA, testing, or AI topics?",
    "learning_guidance": "Based on your current progress, I suggest focusing on practical automation projects. The Programming with AI module would be perfect for your next step!"
}

# Mock file system data
MOCK_FILE_SYSTEM: Dict[str, Any] = {
    "config_files": {
        "module_config.json": MOCK_PRESENTATION_DATA,
        "user_progress.json": {"current_progress": 25.5},
        "settings.json": {"theme": "default", "language": "en"}
    },
    "report_files": {
        "progress_report.html": "<html><body>Progress Report</body></html>",
        "test_results.json": {"tests_passed": 45, "tests_failed": 2, "coverage": 95.5}
    },
    "temp_files": {
        "session_data.tmp": {"session_id": "test_session_123", "timestamp": "2025-07-13T10:00:00Z"}
    }
}

# Mock external service responses
MOCK_EXTERNAL_SERVICES: Dict[str, Any] = {
    "openai_api": {
        "valid_response": {
            "choices": [
                {
                    "message": {
                        "content": "Here's a comprehensive test case for your QA scenario..."
                    }
                }
            ],
            "usage": {"total_tokens": 150}
        },
        "error_response": {
            "error": {
                "message": "Rate limit exceeded",
                "type": "rate_limit_error",
                "code": "rate_limit_exceeded"
            }
        }
    },
    "analytics_service": {
        "user_metrics": {
            "active_users": 45,
            "completion_rate": 78.5,
            "average_session_time": 3600,
            "popular_modules": ["ai_best_practices", "programming_with_ai"]
        }
    }
}

# Mock performance data
MOCK_PERFORMANCE_DATA: Dict[str, Any] = {
    "response_times": {
        "dashboard_load": 250,  # milliseconds
        "slide_generation": 180,
        "progress_update": 95,
        "chart_rendering": 320
    },
    "memory_usage": {
        "baseline": 45.2,  # MB
        "peak": 78.9,
        "average": 52.1
    },
    "concurrent_users": {
        "max_supported": 100,
        "current_active": 23,
        "peak_today": 67
    }
}

# Mock security test data
MOCK_SECURITY_DATA: Dict[str, Any] = {
    "xss_payloads": [
        "<script>alert('xss')</script>",
        "javascript:alert('xss')",
        "<img src=x onerror=alert('xss')>",
        "';alert('xss');//"
    ],
    "sql_injection_payloads": [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT * FROM users --"
    ],
    "csrf_test_data": {
        "valid_token": "abc123def456ghi789",
        "invalid_token": "invalid_token_123",
        "missing_token": None
    },
    "authentication_test_data": {
        "valid_credentials": {"username": "test_user", "password": "Test123!"},
        "invalid_credentials": {"username": "test_user", "password": "wrong_password"},
        "malformed_credentials": {"username": "", "password": ""}
    }
}

# Test scenarios for BDD tests
BDD_TEST_SCENARIOS: Dict[str, List[Dict[str, Any]]] = {
    "learning_progress": [
        {
            "scenario": "Starting a new module",
            "given": "User is on dashboard",
            "when": "User selects a module and clicks start",
            "then": "Progress is updated and module shows as in progress"
        },
        {
            "scenario": "Completing a module",
            "given": "User has started a module",
            "when": "User completes all requirements and clicks complete",
            "then": "Progress shows 100% and certificate is available"
        }
    ],
    "presentation_generation": [
        {
            "scenario": "Generating module overview",
            "given": "User has selected a learning module",
            "when": "User chooses module overview template",
            "then": "Relevant module introduction is displayed"
        }
    ]
}

# Mock error conditions for testing
MOCK_ERROR_CONDITIONS: Dict[str, Any] = {
    "network_errors": {
        "timeout": {"code": "TIMEOUT", "message": "Request timed out"},
        "connection_refused": {"code": "CONNECTION_REFUSED", "message": "Connection refused"},
        "dns_error": {"code": "DNS_ERROR", "message": "DNS resolution failed"}
    },
    "application_errors": {
        "module_not_found": {"code": "MODULE_NOT_FOUND", "message": "Requested module does not exist"},
        "invalid_config": {"code": "INVALID_CONFIG", "message": "Configuration file is malformed"},
        "permission_denied": {"code": "PERMISSION_DENIED", "message": "Access denied"}
    },
    "validation_errors": {
        "missing_parameter": {"code": "MISSING_PARAMETER", "message": "Required parameter is missing"},
        "invalid_format": {"code": "INVALID_FORMAT", "message": "Parameter format is invalid"},
        "out_of_range": {"code": "OUT_OF_RANGE", "message": "Parameter value is out of acceptable range"}
    }
}
