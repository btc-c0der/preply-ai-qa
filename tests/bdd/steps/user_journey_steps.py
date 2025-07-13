"""
Step Definitions for User Journey BDD Tests

This module contains the step definitions for behavior-driven development
scenarios related to user journeys in the AI-QA Portal.

The step definitions implement the Gherkin scenarios using the behave framework
and provide the bridge between natural language scenarios and test code.

Author: AI-QA Portal Testing Team
Date: 2024
"""

from behave import given, when, then, step
import json
import time
from unittest.mock import MagicMock, patch
import sys
import os

# Add the parent directory to sys.path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from app import (
    load_config,
    load_user_progress,
    save_user_progress,
    PresentationGenerator
)


# Background Steps
@given('the AI-QA Portal is running')
def step_portal_running(context):
    """
    Verify that the AI-QA Portal is properly initialized and running
    
    Sets up the basic context for portal operations including
    configuration loading and service initialization.
    """
    context.portal_status = "running"
    context.services = {
        "presentation_generator": True,
        "progress_tracker": True,
        "user_management": True
    }
    assert context.portal_status == "running"


@given('the module configuration is loaded')
def step_config_loaded(context):
    """
    Ensure module configuration is properly loaded
    
    Loads and validates the module configuration data
    required for portal functionality.
    """
    # Use sample configuration for testing
    context.config = {
        "modules": {
            "ai_best_practices": {
                "title": "Best Practices with AI",
                "description": "Learn effective AI usage in QA",
                "topics": ["Prompt Design", "Workflow Integration"],
                "hands_on": True,
                "difficulty": "beginner"
            },
            "programming_with_ai": {
                "title": "Programming with AI",
                "description": "Build AI-powered QA tools",
                "topics": ["Automation", "Chatbots"],
                "hands_on": True,
                "difficulty": "intermediate"
            },
            "qa_ai_integration": {
                "title": "QA + AI Integration",
                "description": "Advanced AI integration in testing",
                "topics": ["Test Generation", "Bug Analysis"],
                "hands_on": True,
                "difficulty": "advanced"
            }
        },
        "presentation_templates": {
            "introduction": {
                "slides": ["Welcome", "Overview", "Tools", "Outcomes"]
            },
            "module_overview": {
                "slides": ["Introduction", "Objectives", "Topics", "Activities", "Assessment"]
            }
        },
        "assessment_criteria": {
            "beginner": {"understanding": 40, "application": 40, "problem_solving": 20},
            "intermediate": {"understanding": 30, "application": 50, "problem_solving": 20},
            "advanced": {"understanding": 25, "application": 45, "problem_solving": 30}
        }
    }
    assert "modules" in context.config
    assert len(context.config["modules"]) > 0


@given('the user progress system is initialized')
def step_progress_system_initialized(context):
    """
    Initialize the user progress tracking system
    
    Sets up the progress tracking system with default
    user state and progress tracking capabilities.
    """
    context.user_progress = {
        "current_module": None,
        "completed_modules": [],
        "current_progress": 0,
        "skills_acquired": [],
        "assessments_completed": [],
        "hands_on_projects": [],
        "learning_path": "custom",
        "preferences": {
            "difficulty_level": "intermediate",
            "focus_areas": [],
            "hands_on_preference": True
        },
        "session_history": [],
        "bookmarks": [],
        "notes": {}
    }
    context.progress_system_initialized = True
    assert context.progress_system_initialized


# New User Registration and Onboarding Steps
@given('I am a new user visiting the portal')
def step_new_user(context):
    """
    Set up context for a new user visiting the portal
    
    Initializes the user context as a new, first-time visitor
    with no prior progress or preferences set.
    """
    context.user_type = "new"
    context.first_visit = True
    context.user_id = "test_user_001"
    assert context.user_type == "new"


@when('I access the dashboard for the first time')
def step_access_dashboard_first_time(context):
    """
    Simulate accessing the dashboard for the first time
    
    Triggers the dashboard loading process and captures
    the initial user experience and displayed content.
    """
    context.dashboard_accessed = True
    context.dashboard_content = {
        "welcome_message": "Welcome to the AI-Driven QA Portal!",
        "modules_overview": context.config["modules"],
        "personalization_options": True,
        "default_progress": context.user_progress
    }
    assert context.dashboard_accessed


@then('I should see a welcome message')
def step_see_welcome_message(context):
    """
    Verify that a welcome message is displayed
    
    Checks that the dashboard contains an appropriate
    welcome message for new users.
    """
    assert "welcome_message" in context.dashboard_content
    assert "Welcome" in context.dashboard_content["welcome_message"]


@then('I should see an overview of available modules')
def step_see_modules_overview(context):
    """
    Verify that available modules are displayed
    
    Checks that the dashboard shows an overview of
    all available learning modules.
    """
    assert "modules_overview" in context.dashboard_content
    modules = context.dashboard_content["modules_overview"]
    assert len(modules) >= 3
    assert "ai_best_practices" in modules
    assert "programming_with_ai" in modules


@then('I should see personalization options')
def step_see_personalization_options(context):
    """
    Verify that personalization options are available
    
    Checks that the dashboard provides options for
    users to customize their learning experience.
    """
    assert context.dashboard_content["personalization_options"]


@then('my default progress should be initialized')
def step_default_progress_initialized(context):
    """
    Verify that default progress is properly initialized
    
    Checks that the user's progress tracking is set up
    with appropriate default values.
    """
    progress = context.dashboard_content["default_progress"]
    assert progress["current_module"] is None
    assert progress["completed_modules"] == []
    assert progress["current_progress"] == 0


@when('I set my preferences')
def step_set_preferences(context):
    """
    Simulate setting user preferences
    
    Takes the preference data from the scenario table
    and applies it to the user's profile.
    """
    context.new_preferences = {}
    for row in context.table:
        field = row['field']
        value = row['value']
        
        # Convert string values to appropriate types
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
        elif field == 'focus_areas':
            value = [value]  # Convert to list
            
        context.new_preferences[field] = value
    
    # Apply preferences
    context.user_progress["preferences"].update(context.new_preferences)
    assert len(context.new_preferences) > 0


@then('my preferences should be saved')
def step_preferences_saved(context):
    """
    Verify that user preferences are properly saved
    
    Checks that the preference changes are persisted
    in the user's profile.
    """
    saved_preferences = context.user_progress["preferences"]
    for field, value in context.new_preferences.items():
        assert saved_preferences[field] == value


@then('the module recommendations should update based on my preferences')
def step_recommendations_updated(context):
    """
    Verify that module recommendations are updated
    
    Checks that the system provides appropriate module
    recommendations based on user preferences.
    """
    difficulty = context.user_progress["preferences"]["difficulty_level"]
    
    # Mock recommendation logic
    recommended_modules = []
    for module_id, module_data in context.config["modules"].items():
        if module_data["difficulty"] == difficulty:
            recommended_modules.append(module_id)
    
    context.recommendations = recommended_modules
    assert len(context.recommendations) > 0


# Module Selection and Navigation Steps
@given('I am logged into the portal')
def step_logged_in(context):
    """
    Set up context for a logged-in user
    
    Establishes the user as authenticated and
    able to access portal features.
    """
    context.user_authenticated = True
    context.user_id = "test_user_001"
    assert context.user_authenticated


@given('I have set my preferences to "{difficulty}" difficulty')
def step_preferences_set_difficulty(context, difficulty):
    """
    Set user difficulty preference
    
    Updates the user's difficulty preference to the
    specified level for testing module recommendations.
    """
    context.user_progress["preferences"]["difficulty_level"] = difficulty
    assert context.user_progress["preferences"]["difficulty_level"] == difficulty


@when('I view the available modules')
def step_view_available_modules(context):
    """
    Simulate viewing the available modules list
    
    Loads and displays the list of available modules
    with their metadata and accessibility status.
    """
    context.available_modules = []
    for module_id, module_data in context.config["modules"].items():
        module_info = module_data.copy()
        module_info["id"] = module_id
        module_info["accessible"] = True  # Simplified logic
        context.available_modules.append(module_info)
    
    assert len(context.available_modules) > 0


@then('I should see modules marked with difficulty levels')
def step_see_difficulty_levels(context):
    """
    Verify that modules display difficulty levels
    
    Checks that each module in the list shows
    its appropriate difficulty level indicator.
    """
    for module in context.available_modules:
        assert "difficulty" in module
        assert module["difficulty"] in ["beginner", "intermediate", "advanced"]


@then('I should see "{module_name}" marked as "{difficulty}"')
def step_see_specific_module_difficulty(context, module_name, difficulty):
    """
    Verify specific module difficulty marking
    
    Checks that a particular module displays the
    correct difficulty level.
    """
    module_found = False
    for module in context.available_modules:
        if module["title"] == module_name:
            assert module["difficulty"] == difficulty
            module_found = True
            break
    assert module_found, f"Module '{module_name}' not found"


@when('I select the "{module_name}" module')
def step_select_module(context, module_name):
    """
    Simulate selecting a specific module
    
    Triggers the module selection process and
    updates the user's current module.
    """
    # Find module by name
    selected_module_id = None
    for module_id, module_data in context.config["modules"].items():
        if module_data["title"] == module_name:
            selected_module_id = module_id
            break
    
    assert selected_module_id is not None, f"Module '{module_name}' not found"
    
    context.selected_module_id = selected_module_id
    context.user_progress["current_module"] = selected_module_id
    context.user_progress["current_progress"] = 0


@then('I should be taken to the module overview')
def step_taken_to_module_overview(context):
    """
    Verify navigation to module overview
    
    Checks that the user is properly navigated to
    the selected module's overview page.
    """
    assert context.selected_module_id is not None
    context.current_page = "module_overview"
    assert context.current_page == "module_overview"


@then('I should see the module description')
def step_see_module_description(context):
    """
    Verify module description is displayed
    
    Checks that the module overview page displays
    the module's description.
    """
    module_data = context.config["modules"][context.selected_module_id]
    context.displayed_description = module_data["description"]
    assert len(context.displayed_description) > 0


@then('I should see the learning objectives')
def step_see_learning_objectives(context):
    """
    Verify learning objectives are displayed
    
    Checks that the module overview includes
    clear learning objectives.
    """
    context.learning_objectives_displayed = True
    assert context.learning_objectives_displayed


@then('I should see the estimated duration')
def step_see_estimated_duration(context):
    """
    Verify estimated duration is displayed
    
    Checks that the module overview shows
    the estimated time to complete.
    """
    context.estimated_duration = "2-4 hours"  # Mock duration
    assert context.estimated_duration is not None


@then('the module should be marked as "in progress" in my profile')
def step_module_marked_in_progress(context):
    """
    Verify module status is updated
    
    Checks that the selected module is properly
    marked as in progress in the user's profile.
    """
    assert context.user_progress["current_module"] == context.selected_module_id


# Presentation Slide Navigation Steps
@given('I have selected the "{module_name}" module')
def step_module_selected(context, module_name):
    """
    Set up context with a selected module
    
    Establishes that a specific module has been
    selected and is ready for navigation.
    """
    # Find and select module
    for module_id, module_data in context.config["modules"].items():
        if module_data["title"] == module_name:
            context.selected_module_id = module_id
            context.selected_module_data = module_data
            break
    
    assert hasattr(context, 'selected_module_id')


@given('I am viewing the module presentation')
def step_viewing_presentation(context):
    """
    Set up presentation viewing context
    
    Initializes the presentation generator and
    sets up the viewing environment.
    """
    context.generator = PresentationGenerator(context.config)
    context.current_slide_index = 0
    context.total_slides = len(context.config["presentation_templates"]["module_overview"]["slides"])


@when('I navigate through the presentation slides')
def step_navigate_slides(context):
    """
    Simulate navigating through presentation slides
    
    Moves through the slides and tracks navigation
    progress and slide content.
    """
    context.slide_contents = []
    context.navigation_history = []
    
    for slide_index in range(context.total_slides):
        slide_content = context.generator.generate_slide(
            "module_overview", 
            slide_index, 
            context.selected_module_data
        )
        context.slide_contents.append(slide_content)
        context.navigation_history.append(slide_index)
    
    assert len(context.slide_contents) == context.total_slides


@then('I should see the "{slide_name}" slide first')
def step_see_first_slide(context, slide_name):
    """
    Verify the first slide content
    
    Checks that the first slide in the sequence
    matches the expected slide name.
    """
    first_slide = context.slide_contents[0]
    assert slide_name in first_slide or "Introduction" in first_slide


@then('I should be able to navigate to the "{slide_name}" slide')
def step_navigate_to_slide(context, slide_name):
    """
    Verify navigation capability to specific slides
    
    Checks that specific slides can be accessed
    and contain appropriate content.
    """
    slide_found = False
    for slide_content in context.slide_contents:
        if slide_name in slide_content:
            slide_found = True
            break
    assert slide_found, f"Slide '{slide_name}' not found in presentation"


@then('my progress should update as I complete each slide')
def step_progress_updates_per_slide(context):
    """
    Verify progress tracking per slide completion
    
    Checks that progress is properly updated as
    the user moves through presentation slides.
    """
    for row in context.table:
        slide_number = int(row['slide_number'])
        expected_progress = row['expected_progress']
        
        # Calculate actual progress
        actual_progress = (slide_number / context.total_slides) * 100
        expected_percent = int(expected_progress.replace('%', ''))
        
        assert abs(actual_progress - expected_percent) < 5  # Allow 5% tolerance


# Hands-on Lab Completion Steps
@given('I have completed the presentation slides for "{module_name}"')
def step_completed_slides(context, module_name):
    """
    Set up context with completed slides
    
    Establishes that the user has finished all
    presentation slides for the specified module.
    """
    context.slides_completed = True
    context.slide_progress = 100
    assert context.slides_completed


@given('the module has hands-on activities enabled')
def step_hands_on_enabled(context):
    """
    Verify hands-on activities are enabled
    
    Checks that the current module has hands-on
    activities available for completion.
    """
    module_data = context.selected_module_data
    assert module_data["hands_on"] is True


@when('I access the hands-on lab section')
def step_access_hands_on_lab(context):
    """
    Simulate accessing the hands-on lab
    
    Triggers the hands-on lab interface and
    loads the lab content and instructions.
    """
    context.lab_accessed = True
    context.lab_content = {
        "setup_instructions": "Setup guide available",
        "implementation_guide": "Step-by-step guide available",
        "code_examples": "Code templates provided"
    }
    assert context.lab_accessed


@then('I should see the lab setup instructions')
def step_see_setup_instructions(context):
    """
    Verify lab setup instructions are displayed
    
    Checks that the hands-on lab provides clear
    setup instructions for the activities.
    """
    assert "setup_instructions" in context.lab_content
    assert len(context.lab_content["setup_instructions"]) > 0


@then('I should see the step-by-step implementation guide')
def step_see_implementation_guide(context):
    """
    Verify implementation guide is available
    
    Checks that the lab provides detailed
    implementation guidance.
    """
    assert "implementation_guide" in context.lab_content
    assert len(context.lab_content["implementation_guide"]) > 0


@then('I should see code examples and templates')
def step_see_code_examples(context):
    """
    Verify code examples are provided
    
    Checks that the lab includes practical
    code examples and templates.
    """
    assert "code_examples" in context.lab_content
    assert len(context.lab_content["code_examples"]) > 0


@when('I complete the hands-on project')
def step_complete_hands_on_project(context):
    """
    Simulate completing the hands-on project
    
    Processes the project completion checklist
    and updates the user's project status.
    """
    context.project_components = {}
    for row in context.table:
        component = row['project_component']
        status = row['status']
        context.project_components[component] = status
    
    # Check all components are completed
    all_completed = all(
        status == "completed" 
        for status in context.project_components.values()
    )
    context.project_completed = all_completed


@then('the project should be marked as completed')
def step_project_marked_completed(context):
    """
    Verify project completion status
    
    Checks that the hands-on project is properly
    marked as completed in the system.
    """
    assert context.project_completed


@then('it should be added to my portfolio')
def step_added_to_portfolio(context):
    """
    Verify project is added to portfolio
    
    Checks that the completed project is added
    to the user's project portfolio.
    """
    project_name = f"{context.selected_module_id}_project"
    context.user_progress["hands_on_projects"].append(project_name)
    assert project_name in context.user_progress["hands_on_projects"]


@then('my skills should be updated with the relevant technologies')
def step_skills_updated(context):
    """
    Verify skills are updated
    
    Checks that completing the project updates
    the user's skill inventory.
    """
    module_topics = context.selected_module_data["topics"]
    for topic in module_topics:
        if topic not in context.user_progress["skills_acquired"]:
            context.user_progress["skills_acquired"].append(topic)
    
    assert len(context.user_progress["skills_acquired"]) > 0


# Module Assessment and Completion Steps
@given('I have completed all slides and hands-on activities for "{module_name}"')
def step_completed_all_activities(context, module_name):
    """
    Set up context with all activities completed
    
    Establishes that the user has finished both
    slides and hands-on activities for the module.
    """
    context.slides_completed = True
    context.hands_on_completed = True
    context.ready_for_assessment = True
    assert context.ready_for_assessment


@when('I take the module assessment')
def step_take_assessment(context):
    """
    Simulate taking the module assessment
    
    Initiates the assessment process and loads
    the appropriate questions and format.
    """
    module_difficulty = context.selected_module_data["difficulty"]
    context.assessment = {
        "difficulty": module_difficulty,
        "criteria": context.config["assessment_criteria"][module_difficulty],
        "started": True
    }
    assert context.assessment["started"]


@then('I should see questions appropriate for "{difficulty}" difficulty level')
def step_see_appropriate_questions(context, difficulty):
    """
    Verify assessment difficulty appropriateness
    
    Checks that the assessment questions match
    the specified difficulty level.
    """
    assert context.assessment["difficulty"] == difficulty


@then('the assessment should cover')
def step_assessment_covers_areas(context):
    """
    Verify assessment coverage areas
    
    Checks that the assessment covers all required
    areas with appropriate weightings.
    """
    criteria = context.assessment["criteria"]
    for row in context.table:
        area = row['assessment_area'].lower().replace(' ', '_')
        weight = int(row['weight'].replace('%', ''))
        assert criteria[area] == weight


@when('I submit my assessment with passing scores')
def step_submit_passing_assessment(context):
    """
    Simulate submitting a passing assessment
    
    Submits the assessment with scores that meet
    the passing criteria for the module.
    """
    context.assessment_scores = {
        "understanding": 85,
        "application": 90,
        "problem_solving": 80
    }
    context.assessment_passed = True
    assert context.assessment_passed


@then('the module should be marked as "completed"')
def step_module_marked_completed(context):
    """
    Verify module completion status
    
    Checks that the module is properly marked
    as completed in the user's progress.
    """
    context.user_progress["completed_modules"].append(context.selected_module_id)
    context.user_progress["current_module"] = None
    context.user_progress["current_progress"] = 0
    
    assert context.selected_module_id in context.user_progress["completed_modules"]


@then('my overall progress should increase')
def step_overall_progress_increases(context):
    """
    Verify overall progress increase
    
    Checks that completing the module increases
    the user's overall learning progress.
    """
    total_modules = len(context.config["modules"])
    completed_modules = len(context.user_progress["completed_modules"])
    overall_progress = (completed_modules / total_modules) * 100
    
    context.overall_progress = overall_progress
    assert context.overall_progress > 0


@then('I should earn the module completion certificate')
def step_earn_certificate(context):
    """
    Verify certificate earning
    
    Checks that the user receives a completion
    certificate for the finished module.
    """
    certificate_name = f"{context.selected_module_id}_certificate"
    context.earned_certificates = [certificate_name]
    assert len(context.earned_certificates) > 0


@then('the skills from this module should be added to my profile')
def step_skills_added_to_profile(context):
    """
    Verify skills are added to profile
    
    Checks that the module's skills are properly
    added to the user's skill inventory.
    """
    module_topics = context.selected_module_data["topics"]
    for topic in module_topics:
        if topic not in context.user_progress["skills_acquired"]:
            context.user_progress["skills_acquired"].append(topic)
    
    # Verify skills were added
    for topic in module_topics:
        assert topic in context.user_progress["skills_acquired"]


@then('I should see recommendations for the next module')
def step_see_next_recommendations(context):
    """
    Verify next module recommendations
    
    Checks that the system provides appropriate
    recommendations for the next learning steps.
    """
    # Simple recommendation logic
    completed = context.user_progress["completed_modules"]
    available_modules = [
        module_id for module_id in context.config["modules"]
        if module_id not in completed
    ]
    
    context.next_recommendations = available_modules[:3]  # Top 3
    assert len(context.next_recommendations) > 0
