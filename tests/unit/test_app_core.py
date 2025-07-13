"""
Unit Tests for Core Application Components

This module contains comprehensive unit tests for the main application components
including configuration loading, user progress management, and presentation generation.

Test Categories:
- Configuration Management
- User Progress Operations
- Presentation Generation
- Data Validation
- Error Handling

Author: AI-QA Portal Testing Team
Date: 2024
"""

import pytest
import json
import os
import tempfile
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

# Import functions from app.py
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app import (
    load_config,
    load_user_progress,
    save_user_progress,
    PresentationGenerator
)

class TestConfigurationManagement:
    """Test suite for configuration loading and validation"""
    
    def test_load_config_success(self, sample_module_config):
        """
        Test successful loading of module configuration
        
        Verifies that valid configuration files are loaded correctly
        and return expected data structure.
        """
        mock_config = json.dumps(sample_module_config)
        
        with patch("builtins.open", mock_open(read_data=mock_config)):
            config = load_config()
            
        assert config is not None
        assert "modules" in config
        assert "presentation_templates" in config
        assert len(config["modules"]) > 0
    
    def test_load_config_file_not_found(self):
        """
        Test configuration loading when file doesn't exist
        
        Ensures proper error handling when configuration file is missing.
        """
        with patch("builtins.open", side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError):
                load_config()
    
    def test_load_config_invalid_json(self):
        """
        Test configuration loading with malformed JSON
        
        Verifies that JSON parsing errors are properly handled.
        """
        invalid_json = "{ invalid json content"
        
        with patch("builtins.open", mock_open(read_data=invalid_json)):
            with pytest.raises(json.JSONDecodeError):
                load_config()
    
    def test_config_structure_validation(self, sample_module_config):
        """
        Test that loaded configuration has required structure
        
        Validates the presence of all required configuration sections
        and their expected data types.
        """
        mock_config = json.dumps(sample_module_config)
        
        with patch("builtins.open", mock_open(read_data=mock_config)):
            config = load_config()
        
        # Validate top-level structure
        assert isinstance(config["modules"], dict)
        assert isinstance(config["presentation_templates"], dict)
        assert isinstance(config["assessment_criteria"], dict)
        
        # Validate module structure
        for module_id, module_data in config["modules"].items():
            assert "title" in module_data
            assert "description" in module_data
            assert "topics" in module_data
            assert "hands_on" in module_data
            assert "difficulty" in module_data
            assert isinstance(module_data["topics"], list)
            assert isinstance(module_data["hands_on"], bool)


class TestUserProgressManagement:
    """Test suite for user progress operations"""
    
    def test_load_user_progress_success(self, sample_user_progress):
        """
        Test successful loading of user progress data
        
        Verifies that existing progress files are loaded correctly.
        """
        mock_progress = json.dumps(sample_user_progress)
        
        with patch("builtins.open", mock_open(read_data=mock_progress)):
            progress = load_user_progress()
        
        assert progress is not None
        assert "current_module" in progress
        assert "completed_modules" in progress
        assert "current_progress" in progress
        assert isinstance(progress["completed_modules"], list)
    
    def test_load_user_progress_file_not_found(self):
        """
        Test user progress loading when file doesn't exist
        
        Ensures default progress structure is returned when no file exists.
        """
        with patch("builtins.open", side_effect=FileNotFoundError):
            progress = load_user_progress()
        
        # Should return default structure
        assert progress["current_module"] is None
        assert progress["completed_modules"] == []
        assert progress["current_progress"] == 0
        assert "preferences" in progress
        assert "session_history" in progress
    
    def test_save_user_progress_success(self, sample_user_progress):
        """
        Test successful saving of user progress data
        
        Verifies that progress data is properly serialized and written.
        """
        mock_file = mock_open()
        
        with patch("builtins.open", mock_file):
            save_user_progress(sample_user_progress)
        
        mock_file.assert_called_once_with('user_progress.json', 'w')
        handle = mock_file()
        
        # Verify JSON was written
        written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
        parsed_data = json.loads(written_data)
        assert parsed_data == sample_user_progress
    
    def test_save_user_progress_write_error(self, sample_user_progress):
        """
        Test error handling during progress save operation
        
        Ensures proper error handling when write operations fail.
        """
        with patch("builtins.open", side_effect=PermissionError):
            with pytest.raises(PermissionError):
                save_user_progress(sample_user_progress)
    
    def test_progress_data_validation(self):
        """
        Test validation of progress data structure
        
        Ensures progress data maintains required structure and types.
        """
        progress = load_user_progress()
        
        # Required fields validation
        required_fields = [
            "current_module", "completed_modules", "current_progress",
            "skills_acquired", "assessments_completed", "hands_on_projects",
            "learning_path", "preferences", "session_history", "bookmarks", "notes"
        ]
        
        for field in required_fields:
            assert field in progress, f"Required field '{field}' missing from progress"
        
        # Type validation
        assert isinstance(progress["completed_modules"], list)
        assert isinstance(progress["current_progress"], (int, float))
        assert isinstance(progress["preferences"], dict)
        assert isinstance(progress["session_history"], list)


class TestPresentationGenerator:
    """Test suite for presentation generation functionality"""
    
    def setup_method(self):
        """Set up test fixtures for presentation generator tests"""
        self.sample_config = {
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
                }
            },
            "assessment_criteria": {
                "beginner": {"understanding": 40, "application": 30, "problem_solving": 30},
                "intermediate": {"understanding": 30, "application": 40, "problem_solving": 30},
                "advanced": {"understanding": 20, "application": 40, "problem_solving": 40}
            }
        }
        self.generator = PresentationGenerator(self.sample_config)
        
        self.sample_module = {
            "title": "Test Module",
            "description": "A test module for unit testing",
            "topics": ["Topic 1", "Topic 2", "Topic 3"],
            "hands_on": True,
            "difficulty": "intermediate"
        }
    
    def test_generator_initialization(self):
        """
        Test proper initialization of presentation generator
        
        Verifies that generator is correctly initialized with configuration.
        """
        assert self.generator.config == self.sample_config
        assert self.generator.templates == self.sample_config["presentation_templates"]
    
    def test_generate_introduction_slide(self):
        """
        Test generation of introduction slides
        
        Verifies that introduction slides are generated with proper content structure.
        """
        slide_content = self.generator.generate_slide("introduction", 0)
        
        assert "Welcome to AI-Driven QA" in slide_content
        assert "🚀" in slide_content  # Check for emoji formatting
        assert "What You'll Experience:" in slide_content
        assert isinstance(slide_content, str)
        assert len(slide_content) > 100  # Ensure substantial content
    
    def test_generate_module_overview_slide(self):
        """
        Test generation of module overview slides
        
        Verifies that module-specific slides are generated correctly.
        """
        slide_content = self.generator.generate_slide(
            "module_overview", 0, self.sample_module
        )
        
        assert self.sample_module["title"] in slide_content
        assert self.sample_module["description"] in slide_content
        assert "Intermediate" in slide_content  # Difficulty level
        assert "✅ Yes" in slide_content  # Hands-on indicator
    
    def test_generate_slide_invalid_template(self):
        """
        Test error handling for invalid template types
        
        Ensures proper error messages for non-existent templates.
        """
        result = self.generator.generate_slide("nonexistent_template", 0)
        assert result == "Template not found"
    
    def test_generate_slide_invalid_index(self):
        """
        Test error handling for invalid slide indices
        
        Ensures proper error messages for out-of-range slide indices.
        """
        result = self.generator.generate_slide("introduction", 999)
        assert result == "Slide not found"
    
    def test_generate_slide_no_module_data(self):
        """
        Test module overview generation without module data
        
        Verifies proper handling when module data is not provided.
        """
        result = self.generator.generate_slide("module_overview", 0, None)
        assert "Module data not available" in result
    
    def test_assessment_criteria_integration(self):
        """
        Test integration of assessment criteria in slides
        
        Verifies that assessment criteria are properly included in slides.
        """
        slide_content = self.generator.generate_slide(
            "module_overview", 4, self.sample_module
        )
        
        # Check for assessment percentages based on difficulty
        criteria = self.sample_config["assessment_criteria"]["intermediate"]
        assert f"{criteria['understanding']}%" in slide_content
        assert f"{criteria['application']}%" in slide_content
        assert f"{criteria['problem_solving']}%" in slide_content
    
    def test_content_formatting(self):
        """
        Test proper markdown formatting in generated content
        
        Ensures all slides use consistent markdown formatting.
        """
        slide_content = self.generator.generate_slide("introduction", 0)
        
        # Check for proper markdown headers
        assert slide_content.startswith("# ")
        assert "## " in slide_content  # Subheaders
        assert "- " in slide_content or "* " in slide_content  # Lists
        
        # Check for emoji usage (modern formatting)
        emojis = ["🚀", "🎯", "🛠️", "📊", "🤖"]
        assert any(emoji in slide_content for emoji in emojis)
    
    def test_slide_content_length(self):
        """
        Test that generated slides have appropriate content length
        
        Ensures slides are neither too short nor excessively long.
        """
        for template_type in self.sample_config["presentation_templates"]:
            slides = self.sample_config["presentation_templates"][template_type]["slides"]
            
            for i in range(len(slides)):
                if template_type == "module_overview":
                    content = self.generator.generate_slide(template_type, i, self.sample_module)
                else:
                    content = self.generator.generate_slide(template_type, i)
                
                # Content should be substantial but not excessive
                assert 50 <= len(content) <= 5000, f"Slide content length inappropriate for {template_type}[{i}]"
    
    def test_slide_uniqueness(self):
        """
        Test that different slides generate unique content
        
        Ensures each slide has distinct content appropriate to its purpose.
        """
        intro_slides = []
        for i in range(4):  # Introduction has 4 slides
            content = self.generator.generate_slide("introduction", i)
            intro_slides.append(content)
        
        # Each slide should be unique
        for i, slide1 in enumerate(intro_slides):
            for j, slide2 in enumerate(intro_slides):
                if i != j:
                    assert slide1 != slide2, f"Slides {i} and {j} have identical content"


class TestDataValidation:
    """Test suite for data validation and sanitization"""
    
    def test_module_data_validation(self, sample_module_config):
        """
        Test validation of module configuration data
        
        Ensures all module configurations meet required standards.
        """
        modules = sample_module_config["modules"]
        
        for module_id, module_data in modules.items():
            # Required fields
            assert "title" in module_data
            assert "description" in module_data
            assert "topics" in module_data
            assert "hands_on" in module_data
            assert "difficulty" in module_data
            
            # Data type validation
            assert isinstance(module_data["title"], str)
            assert isinstance(module_data["description"], str)
            assert isinstance(module_data["topics"], list)
            assert isinstance(module_data["hands_on"], bool)
            assert isinstance(module_data["difficulty"], str)
            
            # Value validation
            assert module_data["difficulty"] in ["beginner", "intermediate", "advanced"]
            assert len(module_data["topics"]) > 0
            assert len(module_data["title"]) > 0
            assert len(module_data["description"]) > 0
    
    def test_progress_data_integrity(self, sample_user_progress):
        """
        Test integrity of user progress data
        
        Validates that progress data maintains consistency and validity.
        """
        progress = sample_user_progress
        
        # Numeric validations
        assert 0 <= progress["current_progress"] <= 100
        
        # List validations
        assert isinstance(progress["completed_modules"], list)
        assert isinstance(progress["skills_acquired"], list)
        assert isinstance(progress["assessments_completed"], list)
        
        # Preference validations
        preferences = progress["preferences"]
        assert preferences["difficulty_level"] in ["beginner", "intermediate", "advanced"]
        assert isinstance(preferences["focus_areas"], list)
        assert isinstance(preferences["hands_on_preference"], bool)


class TestErrorHandling:
    """Test suite for error handling and edge cases"""
    
    def test_graceful_degradation(self):
        """
        Test graceful degradation when components fail
        
        Ensures the application handles component failures gracefully.
        """
        # Test with minimal config
        minimal_config = {"presentation_templates": {}, "assessment_criteria": {}}
        generator = PresentationGenerator(minimal_config)
        
        # Should not crash, but return appropriate messages
        result = generator.generate_slide("nonexistent", 0)
        assert isinstance(result, str)
        assert "not found" in result.lower()
    
    def test_malformed_data_handling(self):
        """
        Test handling of malformed or corrupted data
        
        Ensures robust handling of unexpected data formats.
        """
        malformed_module = {
            "title": "",  # Empty title
            "description": None,  # None description
            "topics": "not_a_list",  # Wrong type
            "hands_on": "maybe",  # Wrong type
            "difficulty": "expert"  # Invalid value
        }
        
        generator = PresentationGenerator({"presentation_templates": {}, "assessment_criteria": {}})
        
        # Should handle gracefully without crashing
        try:
            result = generator.generate_slide("module_overview", 0, malformed_module)
            assert isinstance(result, str)
        except Exception as e:
            # If it does raise an exception, it should be a handled one
            assert not isinstance(e, (AttributeError, KeyError, TypeError))
    
    def test_memory_efficiency(self):
        """
        Test memory efficiency with large data sets
        
        Ensures the application handles large configurations efficiently.
        """
        # Create a large configuration
        large_config = {
            "presentation_templates": {
                f"template_{i}": {
                    "slides": [f"Slide {j}" for j in range(100)]
                } for i in range(50)
            },
            "assessment_criteria": {}
        }
        
        generator = PresentationGenerator(large_config)
        
        # Should handle large configs without issues
        assert generator.config == large_config
        assert len(generator.templates) == 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
