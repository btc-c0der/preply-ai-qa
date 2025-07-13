"""
BDD Test Runner for Content Generation scenarios

This module executes the behavior-driven development scenarios
for content generation using pytest-bdd.

Author: AI-QA Portal Testing Team
Date: 2024
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import json
import time
from unittest.mock import MagicMock, patch
import sys
import os

# Add the parent directory to sys.path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app import (
    load_config,
    PresentationGenerator
)

# Load all scenarios from the feature file
scenarios('features/basic_content_generation.feature')


# Background Steps
@given('the presentation system is initialized')
def step_presentation_system_initialized():
    """
    Initialize the presentation generation system
    
    Sets up the PresentationGenerator with proper configuration
    and validates it's ready for content generation.
    """
    config = load_config()
    generator = PresentationGenerator(config)
    assert generator is not None
    return {"generator": generator, "config": config}


@given('module configuration data is available')
def step_module_config_available():
    """
    Verify module configuration data is properly loaded
    
    Ensures that all required module data is available
    for content generation operations.
    """
    config = load_config()
    assert "modules" in config
    assert len(config["modules"]) > 0
    return config


# Scenario: Generate Introduction Slide
@given('I want to generate an introduction slide')
def step_want_introduction_slide():
    """Set intention to generate introduction slide"""
    slide_type = "introduction"
    return {"slide_type": slide_type}


@when('I request slide generation with no specific module')
def step_request_general_slide():
    """Simulate requesting general slide generation"""
    config = load_config()
    generator = PresentationGenerator(config)
    slide_content = generator.generate_slide("introduction", 0)
    return {"slide_content": slide_content}


@then('I should receive a general introduction slide')
def step_receive_general_introduction():
    """Verify general introduction slide is generated"""
    config = load_config()
    generator = PresentationGenerator(config)
    slide_content = generator.generate_slide("introduction", 0)
    
    assert slide_content is not None
    assert len(slide_content) > 50
    assert "AI-Driven QA" in slide_content or "Welcome" in slide_content


@then('the slide should contain welcome information')
def step_slide_contains_welcome():
    """Verify slide contains welcome information"""
    config = load_config()
    generator = PresentationGenerator(config)
    slide_content = generator.generate_slide("introduction", 0)
    assert "Welcome" in slide_content or "welcome" in slide_content.lower()


@then('the slide should be properly formatted in Markdown')
def step_slide_markdown_formatted():
    """Verify slide is properly formatted in Markdown"""
    config = load_config()
    generator = PresentationGenerator(config)
    slide_content = generator.generate_slide("introduction", 0)
    assert slide_content.startswith("#")
    assert "##" in slide_content or "###" in slide_content


# Scenario: Generate Module Overview Slide
@given('I have a specific module selected')
def step_specific_module_selected():
    """Select a specific module for content generation"""
    config = load_config()
    module_name = list(config["modules"].keys())[0]  # Get first module
    module_data = config["modules"][module_name]
    return {"module_name": module_name, "module_data": module_data}


@when('I request a module overview slide')
def step_request_module_overview():
    """Request module overview slide generation"""
    config = load_config()
    generator = PresentationGenerator(config)
    module_name = list(config["modules"].keys())[0]  # Get first module
    module_data = config["modules"][module_name]
    
    slide_content = generator.generate_slide("module_overview", 0, module_data)
    # Store in a module-level variable for other steps to access
    global _test_slide_content, _test_module_data
    _test_slide_content = slide_content
    _test_module_data = module_data


@then('I should receive a slide with module-specific content')
def step_receive_module_specific_content():
    """Verify module-specific content is generated"""
    global _test_slide_content, _test_module_data
    
    assert _test_slide_content is not None
    assert len(_test_slide_content) > 50
    assert _test_module_data["title"] in _test_slide_content or any(
        topic in _test_slide_content for topic in _test_module_data["topics"][:2]
    )


@then('the slide should include learning objectives')
def step_slide_includes_objectives():
    """Verify slide includes learning objectives"""
    global _test_slide_content
    assert "objectives" in _test_slide_content.lower() or "learn" in _test_slide_content.lower()


@then('the slide should include module topics')
def step_slide_includes_topics():
    """Verify slide includes module topics"""
    global _test_slide_content, _test_module_data
    
    # Check if at least one topic is mentioned in the slide
    topics_mentioned = any(topic.lower() in _test_slide_content.lower() 
                          for topic in _test_module_data["topics"])
    assert topics_mentioned or "topics" in _test_slide_content.lower()


# Module-level variables to store test data between steps
_test_slide_content = None
_test_module_data = None


# Scenario: Generate Assessment Criteria Slide
@given('I need assessment criteria for a module')
def step_need_assessment_criteria():
    """Set need for assessment criteria generation"""
    criteria_needed = True
    return {"criteria_needed": criteria_needed}


@when('I request an assessment criteria slide')
def step_request_assessment_slide():
    """Request assessment criteria slide generation"""
    config = load_config()
    generator = PresentationGenerator(config)
    module_data = config["modules"]["programming_with_ai"]  # Use specific module
    
    slide_content = generator.generate_slide("module_overview", 4, module_data)  # Index 4 is assessment criteria
    return {"slide_content": slide_content}


@then('I should receive criteria based on module difficulty')
def step_receive_difficulty_based_criteria(step_request_assessment_slide):
    """Verify criteria are based on module difficulty"""
    slide_content = step_request_assessment_slide["slide_content"]
    assert slide_content is not None
    assert "%" in slide_content  # Should contain percentage criteria
    assert "Assessment" in slide_content or "assessment" in slide_content.lower()


@then('the slide should show percentage breakdowns')
def step_slide_shows_percentages(step_request_assessment_slide):
    """Verify slide shows percentage breakdowns"""
    slide_content = step_request_assessment_slide["slide_content"]
    assert "30%" in slide_content or "40%" in slide_content


@then('the slide should include evaluation methods')
def step_slide_includes_evaluation(step_request_assessment_slide):
    """Verify slide includes evaluation methods"""
    slide_content = step_request_assessment_slide["slide_content"]
    evaluation_terms = ["Understanding", "Application", "Problem Solving", "evaluation", "assessment"]
    assert any(term in slide_content for term in evaluation_terms)


# Scenario: Handle Invalid Slide Requests
@given('I make an invalid slide request')
def step_invalid_slide_request():
    """Set up invalid slide request scenario"""
    invalid_request = {"template": "nonexistent", "index": 999}
    return invalid_request


@when('I request a slide with invalid parameters')
def step_request_invalid_slide():
    """Request slide with invalid parameters"""
    config = load_config()
    generator = PresentationGenerator(config)
    
    # Request non-existent template
    slide_content = generator.generate_slide("nonexistent_template", 0)
    return {"slide_content": slide_content}


@then('I should receive an appropriate error message')
def step_receive_error_message(step_request_invalid_slide):
    """Verify appropriate error message is received"""
    slide_content = step_request_invalid_slide["slide_content"]
    assert slide_content is not None
    assert "not found" in slide_content.lower() or "error" in slide_content.lower()


@then('the system should not crash')
def step_system_not_crash(step_request_invalid_slide):
    """Verify system doesn't crash on invalid requests"""
    slide_content = step_request_invalid_slide["slide_content"]
    assert slide_content is not None  # Should return something, not crash
    assert isinstance(slide_content, str)


# Scenario: Content Consistency Across Slides
@given('I generate multiple slides for the same module')
def step_generate_multiple_slides():
    """Generate multiple slides for consistency testing"""
    config = load_config()
    generator = PresentationGenerator(config)
    module_data = config["modules"]["programming_with_ai"]
    
    slides = []
    for i in range(3):  # Generate first 3 slides
        slide_content = generator.generate_slide("module_overview", i, module_data)
        slides.append(slide_content)
    
    return {"slides": slides, "module_data": module_data}


@when('I compare the slide contents')
def step_compare_slide_contents(step_generate_multiple_slides):
    """Compare slide contents for consistency"""
    slides = step_generate_multiple_slides["slides"]
    comparisons = {
        "all_different": len(set(slides)) == len(slides),
        "all_valid": all(slide is not None and len(slide) > 20 for slide in slides),
        "all_markdown": all(slide.startswith("#") for slide in slides)
    }
    return comparisons


@then('each slide should have unique content')
def step_unique_content(step_compare_slide_contents):
    """Verify each slide has unique content"""
    comparisons = step_compare_slide_contents
    assert comparisons["all_different"] is True


@then('all slides should maintain consistent formatting')
def step_consistent_formatting(step_compare_slide_contents):
    """Verify consistent formatting across slides"""
    comparisons = step_compare_slide_contents
    assert comparisons["all_markdown"] is True


@then('all slides should be well-formed')
def step_well_formed_slides(step_compare_slide_contents):
    """Verify all slides are well-formed"""
    comparisons = step_compare_slide_contents
    assert comparisons["all_valid"] is True
