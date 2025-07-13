"""
Step Definitions for Content Generation BDD Tests

This module contains the step definitions for behavior-driven development
scenarios related to content generation and presentation functionality
in the AI-QA Portal.

Author: AI-QA Portal Testing Team
Date: 2024
"""

from behave import given, when, then, step
import json
import sys
import os
from unittest.mock import MagicMock, patch

# Add the parent directory to sys.path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from app import PresentationGenerator


# Background Steps for Content Generation
@given('the presentation generator is initialized')
def step_presentation_generator_initialized(context):
    """
    Initialize the presentation generator with test configuration
    
    Sets up the presentation generator with a comprehensive
    test configuration for content generation testing.
    """
    context.test_config = {
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
            }
        },
        "assessment_criteria": {
            "beginner": {"understanding": 40, "application": 40, "problem_solving": 20},
            "intermediate": {"understanding": 30, "application": 50, "problem_solving": 20},
            "advanced": {"understanding": 25, "application": 45, "problem_solving": 30}
        }
    }
    
    context.generator = PresentationGenerator(context.test_config)
    assert context.generator is not None


@given('the assessment criteria are defined')
def step_assessment_criteria_defined(context):
    """
    Verify that assessment criteria are properly defined
    
    Ensures that all difficulty levels have appropriate
    assessment criteria weightings defined.
    """
    criteria = context.test_config["assessment_criteria"]
    
    # Verify all difficulty levels are present
    assert "beginner" in criteria
    assert "intermediate" in criteria
    assert "advanced" in criteria
    
    # Verify each criteria has required components
    for difficulty, weights in criteria.items():
        assert "understanding" in weights
        assert "application" in weights
        assert "problem_solving" in weights
        
        # Verify weights sum to 100%
        total_weight = sum(weights.values())
        assert total_weight == 100


# Introduction Slide Generation Steps
@given('I am requesting introduction slides')
def step_requesting_introduction_slides(context):
    """
    Set up context for introduction slide generation
    
    Prepares the context for testing introduction
    slide generation functionality.
    """
    context.slide_type = "introduction"
    context.slide_requests = []


@when('I generate the "Welcome to AI-Driven QA" slide')
def step_generate_welcome_slide(context):
    """
    Generate the welcome slide content
    
    Calls the presentation generator to create the
    welcome slide and captures the generated content.
    """
    context.welcome_slide = context.generator.generate_slide("introduction", 0)
    assert context.welcome_slide is not None
    assert len(context.welcome_slide) > 0


@then('the slide should contain a welcoming header')
def step_slide_contains_welcoming_header(context):
    """
    Verify the presence of a welcoming header
    
    Checks that the generated slide contains an
    appropriate welcoming header element.
    """
    slide_content = context.welcome_slide
    assert "Welcome" in slide_content or "🚀" in slide_content
    assert slide_content.startswith("#")  # Markdown header


@then('it should include an overview of benefits')
def step_slide_includes_benefits_overview(context):
    """
    Verify the inclusion of benefits overview
    
    Checks that the slide contains the specified
    benefits listed in the scenario table.
    """
    slide_content = context.welcome_slide
    
    for row in context.table:
        benefit = row['benefit']
        assert benefit in slide_content, f"Benefit '{benefit}' not found in slide"


@then('it should include the learning approach description')
def step_slide_includes_learning_approach(context):
    """
    Verify the inclusion of learning approach description
    
    Checks that the slide describes the learning
    approach and methodology used in the portal.
    """
    slide_content = context.welcome_slide
    approach_keywords = ["approach", "learning", "method", "practice", "theory"]
    
    assert any(keyword.lower() in slide_content.lower() for keyword in approach_keywords)


@then('it should use engaging visual elements like emojis')
def step_slide_uses_engaging_visual_elements(context):
    """
    Verify the use of engaging visual elements
    
    Checks that the slide includes visual elements
    like emojis to enhance engagement.
    """
    slide_content = context.welcome_slide
    common_emojis = ["🚀", "🎯", "🛠️", "📊", "🤖", "🌟", "📚"]
    
    assert any(emoji in slide_content for emoji in common_emojis)


# Module Overview Slide Generation Steps
@given('I have modules with different difficulty levels')
def step_modules_with_different_difficulties(context):
    """
    Set up modules with varying difficulty levels
    
    Creates test modules with beginner, intermediate,
    and advanced difficulty levels for testing.
    """
    context.test_modules = {
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
    }


@when('I generate module overview slides for "{module_name}" ({difficulty})')
def step_generate_module_overview_slides(context, module_name, difficulty):
    """
    Generate module overview slides for specific module
    
    Creates overview slides for the specified module
    and captures the assessment criteria slide.
    """
    # Find the module data
    module_data = None
    for module_id, data in context.test_modules.items():
        if data["title"] == module_name:
            module_data = data
            break
    
    assert module_data is not None, f"Module '{module_name}' not found"
    assert module_data["difficulty"] == difficulty
    
    # Generate the assessment criteria slide (slide index 4)
    context.assessment_slide = context.generator.generate_slide(
        "module_overview", 4, module_data
    )
    context.current_module_difficulty = difficulty


@then('the "Assessment Criteria" slide should show')
def step_assessment_slide_shows_criteria(context):
    """
    Verify assessment criteria slide content
    
    Checks that the assessment criteria slide displays
    the correct weightings for the module difficulty.
    """
    slide_content = context.assessment_slide
    criteria = context.test_config["assessment_criteria"][context.current_module_difficulty]
    
    for row in context.table:
        criteria_name = row['criteria']
        weight = row['weight']
        
        # Verify the weight percentage appears in the slide
        assert weight in slide_content, f"Weight '{weight}' not found for '{criteria_name}'"


# Hands-on Session Content Generation Steps
@given('I am generating hands-on session content')
def step_generating_hands_on_content(context):
    """
    Set up context for hands-on session content generation
    
    Prepares the context for testing hands-on session
    slide generation functionality.
    """
    context.content_type = "hands_on_session"
    context.session_slides = {}


@when('I create the "Setup and Prerequisites" slide')
def step_create_setup_prerequisites_slide(context):
    """
    Generate the setup and prerequisites slide
    
    Creates the setup slide for hands-on sessions
    and captures the generated content.
    """
    context.setup_slide = context.generator.generate_slide("hands_on_session", 0)
    assert context.setup_slide is not None
    assert len(context.setup_slide) > 100  # Should be substantial content


@then('it should include technical requirements')
def step_includes_technical_requirements(context):
    """
    Verify technical requirements inclusion
    
    Checks that the setup slide contains the specified
    technical requirements from the scenario table.
    """
    slide_content = context.setup_slide
    
    for row in context.table:
        requirement = row['requirement']
        details = row['details']
        
        # Check for requirement presence (case-insensitive)
        assert requirement.lower() in slide_content.lower() or \
               details.lower() in slide_content.lower(), \
               f"Requirement '{requirement}' or details '{details}' not found"


@then('it should include required packages installation commands')
def step_includes_installation_commands(context):
    """
    Verify package installation commands inclusion
    
    Checks that the slide provides installation
    commands for required packages.
    """
    slide_content = context.setup_slide
    installation_keywords = ["pip install", "package", "install", "requirements"]
    
    assert any(keyword in slide_content.lower() for keyword in installation_keywords)


@then('it should include API key setup instructions')
def step_includes_api_key_setup(context):
    """
    Verify API key setup instructions inclusion
    
    Checks that the slide provides guidance on
    setting up necessary API keys.
    """
    slide_content = context.setup_slide
    api_keywords = ["api key", "openai", "hugging face", "token", "access"]
    
    assert any(keyword.lower() in slide_content.lower() for keyword in api_keywords)


@then('it should include project structure guidelines')
def step_includes_project_structure(context):
    """
    Verify project structure guidelines inclusion
    
    Checks that the slide provides information about
    recommended project structure and organization.
    """
    slide_content = context.setup_slide
    structure_keywords = ["structure", "folder", "directory", "project", "organize"]
    
    assert any(keyword.lower() in slide_content.lower() for keyword in structure_keywords)


# Dynamic Content Adaptation Steps
@given('I have a module with the following data')
def step_module_with_specific_data(context):
    """
    Set up a module with specific test data
    
    Creates a test module with the data specified
    in the scenario table.
    """
    context.test_module_data = {}
    for row in context.table:
        field = row['field']
        value = row['value']
        
        # Convert specific fields to appropriate types
        if field == 'hands_on':
            value = value.lower() == 'true'
        elif field == 'topics':
            value = [topic.strip() for topic in value.split(',')]
        
        context.test_module_data[field] = value


@when('I generate the "Module Introduction" slide')
def step_generate_module_introduction_slide(context):
    """
    Generate the module introduction slide
    
    Creates the introduction slide using the test
    module data and captures the content.
    """
    context.introduction_slide = context.generator.generate_slide(
        "module_overview", 0, context.test_module_data
    )
    assert context.introduction_slide is not None


@then('the slide should include the module title')
def step_slide_includes_module_title(context):
    """
    Verify module title inclusion
    
    Checks that the generated slide contains the
    specified module title.
    """
    slide_content = context.introduction_slide
    module_title = context.test_module_data.get('title', '')
    assert module_title in slide_content


@then('it should include the module description')
def step_slide_includes_module_description(context):
    """
    Verify module description inclusion
    
    Checks that the slide contains the module
    description text.
    """
    slide_content = context.introduction_slide
    module_description = context.test_module_data.get('description', '')
    assert module_description in slide_content


@then('it should indicate "{difficulty}" difficulty level')
def step_slide_indicates_difficulty(context, difficulty):
    """
    Verify difficulty level indication
    
    Checks that the slide properly indicates the
    module's difficulty level.
    """
    slide_content = context.introduction_slide
    assert difficulty in slide_content


@then('it should show "{hands_on_indicator}" for hands-on component')
def step_slide_shows_hands_on_indicator(context, hands_on_indicator):
    """
    Verify hands-on component indication
    
    Checks that the slide correctly indicates whether
    the module has hands-on components.
    """
    slide_content = context.introduction_slide
    assert hands_on_indicator in slide_content


@then('it should list the module topics')
def step_slide_lists_module_topics(context):
    """
    Verify module topics listing
    
    Checks that the slide includes a list of the
    module's topics or learning areas.
    """
    slide_content = context.introduction_slide
    module_topics = context.test_module_data.get('topics', [])
    
    for topic in module_topics:
        assert topic in slide_content, f"Topic '{topic}' not found in slide"


# Error Handling Steps
@when('I request a slide with an invalid template type')
def step_request_invalid_template_type(context):
    """
    Request a slide with an invalid template type
    
    Tests error handling by requesting a slide with
    a non-existent template type.
    """
    context.error_result = context.generator.generate_slide("invalid_template", 0)


@when('I request a slide with an invalid slide index')
def step_request_invalid_slide_index(context):
    """
    Request a slide with an invalid slide index
    
    Tests error handling by requesting a slide with
    an out-of-range slide index.
    """
    context.error_result = context.generator.generate_slide("introduction", 999)


@when('I request a module overview slide without module data')
def step_request_slide_without_module_data(context):
    """
    Request a module overview slide without module data
    
    Tests error handling by requesting a module slide
    without providing necessary module data.
    """
    context.error_result = context.generator.generate_slide("module_overview", 0, None)


@then('it should return "{error_message}"')
def step_should_return_error_message(context, error_message):
    """
    Verify specific error message return
    
    Checks that the system returns the expected
    error message for invalid requests.
    """
    assert context.error_result == error_message


@then('it should not crash the application')
def step_should_not_crash_application(context):
    """
    Verify application doesn't crash on errors
    
    Ensures that error conditions are handled gracefully
    without causing application crashes.
    """
    # If we got here, the application didn't crash
    assert isinstance(context.error_result, str)
    assert len(context.error_result) > 0


@then('it should handle the error gracefully')
def step_should_handle_error_gracefully(context):
    """
    Verify graceful error handling
    
    Checks that errors are handled in a user-friendly
    manner without exposing system internals.
    """
    assert isinstance(context.error_result, str)
    assert "error" not in context.error_result.lower() or \
           "not found" in context.error_result.lower() or \
           "not available" in context.error_result.lower()


@then('it should provide a meaningful error message')
def step_should_provide_meaningful_error_message(context):
    """
    Verify meaningful error message provision
    
    Ensures that error messages provide helpful
    information to users about what went wrong.
    """
    assert isinstance(context.error_result, str)
    assert len(context.error_result) > 10  # Should be more than just "Error"
    
    # Should contain helpful keywords
    helpful_keywords = ["not", "available", "found", "data", "invalid"]
    assert any(keyword in context.error_result.lower() for keyword in helpful_keywords)


# Content Quality and Consistency Steps
@given('I am generating slides for any module')
def step_generating_slides_for_any_module(context):
    """
    Set up context for general slide generation testing
    
    Prepares the context for testing slide generation
    quality and consistency across modules.
    """
    context.sample_module = {
        "title": "Sample Module",
        "description": "A sample module for testing",
        "topics": ["Topic 1", "Topic 2"],
        "hands_on": True,
        "difficulty": "intermediate"
    }


@when('a slide is created')
def step_slide_is_created(context):
    """
    Generate a sample slide for testing
    
    Creates a slide using the sample module data
    for quality and consistency testing.
    """
    context.test_slide = context.generator.generate_slide(
        "module_overview", 0, context.sample_module
    )


@then('it should have substantial content (at least {min_chars:d} characters)')
def step_should_have_substantial_content(context, min_chars):
    """
    Verify slide has substantial content
    
    Checks that generated slides contain enough
    content to be meaningful and useful.
    """
    slide_content = context.test_slide
    assert len(slide_content) >= min_chars, \
        f"Slide content too short: {len(slide_content)} < {min_chars}"


@then('it should not be excessively long (no more than {max_chars:d} characters)')
def step_should_not_be_excessively_long(context, max_chars):
    """
    Verify slide is not excessively long
    
    Checks that slides don't contain too much content
    that would be overwhelming for presentation format.
    """
    slide_content = context.test_slide
    assert len(slide_content) <= max_chars, \
        f"Slide content too long: {len(slide_content)} > {max_chars}"


@then('it should be appropriate for a presentation slide format')
def step_should_be_appropriate_for_presentation(context):
    """
    Verify slide is appropriate for presentation format
    
    Checks that the slide content is structured
    appropriately for presentation delivery.
    """
    slide_content = context.test_slide
    
    # Should have clear structure
    assert slide_content.startswith("#")  # Header
    assert "\n" in slide_content  # Multiple lines
    
    # Should not be just one long paragraph
    lines = slide_content.split('\n')
    assert len(lines) >= 3  # At least header + content


# Markdown Formatting Consistency Steps
@given('I am generating any type of slide')
def step_generating_any_type_of_slide(context):
    """
    Set up context for markdown formatting testing
    
    Prepares for testing markdown formatting
    consistency across different slide types.
    """
    context.slide_types_to_test = [
        ("introduction", 0, None),
        ("module_overview", 0, context.sample_module if hasattr(context, 'sample_module') else {
            "title": "Test", "description": "Test", "topics": [], "hands_on": False, "difficulty": "beginner"
        })
    ]


@when('the slide content is created')
def step_slide_content_is_created(context):
    """
    Generate slide content for format testing
    
    Creates slide content and captures it for
    markdown formatting validation.
    """
    # Test first slide type
    template_type, slide_index, module_data = context.slide_types_to_test[0]
    context.format_test_slide = context.generator.generate_slide(
        template_type, slide_index, module_data
    )


@then('it should start with a proper markdown header (#)')
def step_should_start_with_markdown_header(context):
    """
    Verify proper markdown header usage
    
    Checks that slides start with appropriate
    markdown header formatting.
    """
    slide_content = context.format_test_slide
    assert slide_content.strip().startswith("#"), "Slide should start with markdown header"


@then('it should use consistent subheader formatting (##)')
def step_should_use_consistent_subheader_formatting(context):
    """
    Verify consistent subheader formatting
    
    Checks that slides use proper markdown
    subheader formatting throughout.
    """
    slide_content = context.format_test_slide
    if "##" in slide_content:
        # If subheaders exist, they should be properly formatted
        lines = slide_content.split('\n')
        subheader_lines = [line for line in lines if line.strip().startswith("##")]
        
        for line in subheader_lines:
            assert line.strip().startswith("## "), f"Improper subheader format: {line}"


@then('it should use proper list formatting (- or *)')
def step_should_use_proper_list_formatting(context):
    """
    Verify proper list formatting
    
    Checks that slides use consistent and proper
    markdown list formatting.
    """
    slide_content = context.format_test_slide
    if "- " in slide_content or "* " in slide_content:
        lines = slide_content.split('\n')
        list_lines = [line for line in lines if line.strip().startswith(("- ", "* "))]
        
        assert len(list_lines) > 0, "Lists should be properly formatted"


@then('it should include appropriate emoji usage for engagement')
def step_should_include_appropriate_emoji_usage(context):
    """
    Verify appropriate emoji usage
    
    Checks that slides include emojis to enhance
    visual appeal and engagement.
    """
    slide_content = context.format_test_slide
    common_emojis = ["🚀", "🎯", "🛠️", "📊", "🤖", "🌟", "📚", "✅", "❌", "🔧", "📈"]
    
    emoji_found = any(emoji in slide_content for emoji in common_emojis)
    assert emoji_found, "Slide should include emojis for engagement"


# Performance and Scalability Steps
@given('I have a configuration with {template_count:d} presentation templates')
def step_configuration_with_many_templates(context, template_count):
    """
    Set up configuration with many templates
    
    Creates a large configuration for performance
    and scalability testing.
    """
    large_config = {
        "presentation_templates": {},
        "assessment_criteria": {
            "beginner": {"understanding": 40, "application": 40, "problem_solving": 20}
        }
    }
    
    # Create many templates
    for i in range(template_count):
        large_config["presentation_templates"][f"template_{i}"] = {
            "slides": [f"Slide {j}" for j in range(10)]
        }
    
    context.large_config = large_config
    context.template_count = template_count


@given('each template has {slide_count:d} slides')
def step_each_template_has_many_slides(context, slide_count):
    """
    Configure templates with many slides
    
    Updates the configuration to have many slides
    per template for scalability testing.
    """
    # Update existing templates to have more slides
    for template_name, template_data in context.large_config["presentation_templates"].items():
        template_data["slides"] = [f"Slide {i}" for i in range(slide_count)]
    
    context.slide_count = slide_count


@when('the presentation generator is initialized')
def step_presentation_generator_initialized_with_large_config(context):
    """
    Initialize generator with large configuration
    
    Creates the presentation generator with the large
    configuration for performance testing.
    """
    import time
    start_time = time.time()
    
    context.large_generator = PresentationGenerator(context.large_config)
    
    context.initialization_time = time.time() - start_time


@then('it should load the configuration without performance issues')
def step_should_load_without_performance_issues(context):
    """
    Verify configuration loads efficiently
    
    Checks that large configurations are loaded
    within acceptable time limits.
    """
    # Should load within 1 second even for large configs
    assert context.initialization_time < 1.0, \
        f"Initialization took too long: {context.initialization_time:.2f}s"


@then('it should be able to generate any slide efficiently')
def step_should_generate_slides_efficiently(context):
    """
    Verify efficient slide generation
    
    Tests that slide generation remains efficient
    even with large configurations.
    """
    import time
    
    # Test generating first slide from first template
    template_name = list(context.large_config["presentation_templates"].keys())[0]
    
    start_time = time.time()
    slide_content = context.large_generator.generate_slide(template_name, 0)
    generation_time = time.time() - start_time
    
    assert generation_time < 0.1, f"Slide generation too slow: {generation_time:.3f}s"
    assert slide_content is not None


@then('memory usage should remain reasonable')
def step_memory_usage_should_remain_reasonable(context):
    """
    Verify reasonable memory usage
    
    Checks that the generator doesn't consume
    excessive memory with large configurations.
    """
    import sys
    
    # Simple memory check - generator should not store excessive data
    generator_size = sys.getsizeof(context.large_generator)
    config_size = sys.getsizeof(context.large_config)
    
    # Generator shouldn't be much larger than the config itself
    assert generator_size < config_size * 2, "Generator using too much memory"
