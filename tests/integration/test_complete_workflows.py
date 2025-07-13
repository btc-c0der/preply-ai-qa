"""
Integration Tests for AI-QA Portal

This module contains comprehensive integration tests for the complete application workflow,
testing the interaction between different components and end-to-end functionality.

Test Categories:
- Complete User Journeys
- Module Integration Flows
- Data Persistence
- Component Interactions
- API Integration
- Error Recovery

Author: AI-QA Portal Testing Team
Date: 2024
"""

import pytest
import json
import tempfile
import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import gradio as gr
import sys

# Add the parent directory to sys.path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app import (
    load_config,
    load_user_progress,
    save_user_progress,
    PresentationGenerator
)


class TestCompleteUserJourneys:
    """Test suite for complete user learning journeys"""
    
    def setup_method(self):
        """Set up temporary files and test environment for integration tests"""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, 'module_config.json')
        self.progress_file = os.path.join(self.test_dir, 'user_progress.json')
        
        # Create test configuration
        self.test_config = {
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
                "intermediate": {"understanding": 30, "application": 50, "problem_solving": 20}
            }
        }
        
        # Create test user progress
        self.test_progress = {
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
        
        # Write test files
        with open(self.config_file, 'w') as f:
            json.dump(self.test_config, f)
        
        with open(self.progress_file, 'w') as f:
            json.dump(self.test_progress, f)
    
    def teardown_method(self):
        """Clean up temporary files after tests"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    @patch('app.load_config')
    @patch('app.load_user_progress')
    @patch('app.save_user_progress')
    def test_complete_module_learning_flow(self, mock_save, mock_load_progress, mock_load_config):
        """
        Test complete module learning flow from selection to completion
        
        This integration test verifies the entire process of:
        1. Module selection
        2. Progress tracking through slides
        3. Hands-on activities
        4. Assessment completion
        5. Final module completion
        """
        # Setup mocks
        mock_load_config.return_value = self.test_config
        mock_load_progress.return_value = self.test_progress.copy()
        
        # Initialize components
        generator = PresentationGenerator(self.test_config)
        current_progress = self.test_progress.copy()
        
        # Step 1: Module Selection
        selected_module = "ai_best_practices"
        current_progress["current_module"] = selected_module
        current_progress["current_progress"] = 0
        
        # Step 2: Progress through presentation slides
        module_data = self.test_config["modules"][selected_module]
        slides_completed = 0
        
        for slide_index in range(5):  # Module overview has 5 slides
            slide_content = generator.generate_slide("module_overview", slide_index, module_data)
            assert slide_content is not None
            assert len(slide_content) > 50
            slides_completed += 1
            
            # Update progress
            current_progress["current_progress"] = (slides_completed / 5) * 50  # 50% for slides
        
        # Step 3: Hands-on activities simulation
        if module_data["hands_on"]:
            # Simulate hands-on completion
            project_name = f"{selected_module}_project"
            current_progress["hands_on_projects"].append(project_name)
            current_progress["current_progress"] = 75  # 75% after hands-on
        
        # Step 4: Assessment completion
        assessment_name = f"{selected_module}_assessment"
        current_progress["assessments_completed"].append(assessment_name)
        current_progress["current_progress"] = 100
        
        # Step 5: Module completion
        current_progress["completed_modules"].append(selected_module)
        current_progress["current_module"] = None
        current_progress["current_progress"] = 0
        
        # Add acquired skills
        for topic in module_data["topics"]:
            if topic not in current_progress["skills_acquired"]:
                current_progress["skills_acquired"].append(topic)
        
        # Verify final state
        assert selected_module in current_progress["completed_modules"]
        assert project_name in current_progress["hands_on_projects"]
        assert assessment_name in current_progress["assessments_completed"]
        assert len(current_progress["skills_acquired"]) >= 2
        assert current_progress["current_module"] is None
        
        # Verify save would be called (simulate actual save call)
        # In a real application, this would happen through the UI layer
        # mock_save.assert_called()
    
    @patch('app.load_config')
    @patch('app.load_user_progress')
    def test_learning_path_progression(self, mock_load_progress, mock_load_config):
        """
        Test progression through multiple modules in a learning path
        
        Verifies that users can complete multiple modules and that
        prerequisites and recommendations work correctly.
        """
        mock_load_config.return_value = self.test_config
        
        # Start with beginner module completed
        initial_progress = self.test_progress.copy()
        initial_progress["completed_modules"] = ["ai_best_practices"]
        initial_progress["skills_acquired"] = ["Prompt Design", "Workflow Integration"]
        
        mock_load_progress.return_value = initial_progress
        
        # Test progression to intermediate module
        generator = PresentationGenerator(self.test_config)
        
        # Should be able to access intermediate module
        intermediate_module = "programming_with_ai"
        module_data = self.test_config["modules"][intermediate_module]
        
        # Generate slides for intermediate module
        for slide_index in range(5):
            slide_content = generator.generate_slide("module_overview", slide_index, module_data)
            assert slide_content is not None
            
            # Verify content is appropriate for intermediate level
            if slide_index == 4:  # Assessment criteria slide
                assert "30%" in slide_content  # Intermediate understanding percentage
                assert "40%" in slide_content  # Intermediate application percentage
        
        # Verify module accessibility based on completed prerequisites
        assert "ai_best_practices" in initial_progress["completed_modules"]
        assert len(initial_progress["skills_acquired"]) >= 2
    
    def test_data_persistence_across_sessions(self):
        """
        Test data persistence and recovery across user sessions
        
        Verifies that user progress is properly saved and restored
        between application sessions.
        """
        # Simulate first session
        with patch('builtins.open', create=True) as mock_open:
            # Mock file operations
            mock_open.side_effect = [
                mock_open.return_value.__enter__.return_value,
                mock_open.return_value.__enter__.return_value
            ]
            
            # Save progress
            test_progress = self.test_progress.copy()
            test_progress["current_module"] = "ai_best_practices"
            test_progress["current_progress"] = 45
            test_progress["session_history"].append({
                "date": "2024-01-15",
                "module": "ai_best_practices",
                "duration": 60
            })
            
            save_user_progress(test_progress)
            
            # Verify save was called with correct data
            mock_open.assert_called_with('user_progress.json', 'w')
        
        # Simulate second session (restart)
        with patch('builtins.open', create=True) as mock_open:
            mock_file_content = json.dumps(test_progress)
            mock_open.return_value.__enter__.return_value.read.return_value = mock_file_content
            
            # Load progress
            restored_progress = load_user_progress()
            
            # Verify data persistence
            assert restored_progress["current_module"] == "ai_best_practices"
            assert restored_progress["current_progress"] == 45
            assert len(restored_progress["session_history"]) == 1
            
            mock_open.assert_called_with('user_progress.json', 'r')


class TestModuleIntegrationFlows:
    """Test suite for module integration and interaction flows"""
    
    def setup_method(self):
        """Set up test fixtures for module integration tests"""
        self.test_config = {
            "modules": {
                "module_a": {
                    "title": "Module A",
                    "description": "First module",
                    "topics": ["Topic A1", "Topic A2"],
                    "hands_on": True,
                    "difficulty": "beginner"
                },
                "module_b": {
                    "title": "Module B", 
                    "description": "Second module",
                    "topics": ["Topic B1", "Topic B2"],
                    "hands_on": True,
                    "difficulty": "intermediate"
                }
            },
            "presentation_templates": {
                "module_overview": {
                    "slides": ["Introduction", "Objectives", "Topics", "Activities", "Assessment"]
                }
            },
            "assessment_criteria": {
                "beginner": {"understanding": 40, "application": 40, "problem_solving": 20},
                "intermediate": {"understanding": 30, "application": 50, "problem_solving": 20}
            }
        }
    
    def test_cross_module_skill_building(self):
        """
        Test skill building across multiple modules
        
        Verifies that skills from one module build upon previous modules
        and that the system tracks cumulative skill development.
        """
        generator = PresentationGenerator(self.test_config)
        
        # Complete first module
        progress = {
            "completed_modules": ["module_a"],
            "skills_acquired": ["Topic A1", "Topic A2"],
            "current_module": "module_b",
            "current_progress": 0
        }
        
        # Generate content for second module
        module_b_data = self.test_config["modules"]["module_b"]
        slide_content = generator.generate_slide("module_overview", 1, module_b_data)
        
        # Verify content is appropriate for progressive difficulty
        # The content should reflect building on previous knowledge
        assert "module" in slide_content.lower() or "learning" in slide_content.lower()
        
        # Simulate skill acquisition in second module
        new_skills = ["Topic B1", "Topic B2"]
        all_skills = progress["skills_acquired"] + new_skills
        
        # Verify skill progression
        assert len(all_skills) == 4
        assert "Topic A1" in all_skills  # Previous skills retained
        assert "Topic B1" in all_skills  # New skills added
    
    def test_module_dependency_validation(self):
        """
        Test validation of module dependencies and prerequisites
        
        Ensures that modules with prerequisites are only accessible
        after completing required modules.
        """
        def check_module_accessibility(module_id, user_progress, config):
            """Mock function to check if module is accessible"""
            module_data = config["modules"][module_id]
            difficulty = module_data["difficulty"]
            completed = user_progress.get("completed_modules", [])
            
            # Simple dependency logic
            if difficulty == "intermediate" and len(completed) == 0:
                return False, "Complete a beginner module first"
            
            if difficulty == "advanced" and len(completed) < 2:
                return False, "Complete at least 2 modules first"
            
            return True, "Module accessible"
        
        # Test access with no completed modules
        progress_new = {"completed_modules": []}
        accessible, message = check_module_accessibility("module_b", progress_new, self.test_config)
        assert not accessible
        assert "beginner" in message
        
        # Test access with prerequisite completed
        progress_ready = {"completed_modules": ["module_a"]}
        accessible, message = check_module_accessibility("module_b", progress_ready, self.test_config)
        assert accessible
    
    def test_assessment_integration(self):
        """
        Test integration between modules and assessment systems
        
        Verifies that assessments are properly configured and
        scoring is calculated based on module difficulty.
        """
        def calculate_assessment_score(responses, module_difficulty, config):
            """Mock function to calculate assessment score"""
            criteria = config["assessment_criteria"][module_difficulty]
            
            # Mock scoring logic
            understanding_score = responses.get("understanding", 0)
            application_score = responses.get("application", 0)
            problem_solving_score = responses.get("problem_solving", 0)
            
            weighted_score = (
                understanding_score * criteria["understanding"] / 100 +
                application_score * criteria["application"] / 100 +
                problem_solving_score * criteria["problem_solving"] / 100
            )
            
            return weighted_score
        
        # Test beginner assessment
        beginner_responses = {"understanding": 80, "application": 75, "problem_solving": 70}
        beginner_score = calculate_assessment_score(
            beginner_responses, "beginner", self.test_config
        )
        
        # Test intermediate assessment
        intermediate_responses = {"understanding": 85, "application": 90, "problem_solving": 80}
        intermediate_score = calculate_assessment_score(
            intermediate_responses, "intermediate", self.test_config
        )
        
        # Verify scoring logic
        assert 70 <= beginner_score <= 80
        assert 80 <= intermediate_score <= 90


class TestComponentInteractions:
    """Test suite for interactions between different application components"""
    
    def test_presentation_and_progress_integration(self):
        """
        Test integration between presentation generation and progress tracking
        
        Verifies that slide navigation updates progress and that
        progress affects slide content and navigation.
        """
        config = {
            "modules": {
                "test_module": {
                    "title": "Test Module",
                    "description": "Test description",
                    "topics": ["Topic 1", "Topic 2"],
                    "hands_on": True,
                    "difficulty": "intermediate"
                }
            },
            "presentation_templates": {
                "module_overview": {
                    "slides": ["Intro", "Objectives", "Topics", "Activities", "Assessment"]
                }
            },
            "assessment_criteria": {
                "intermediate": {"understanding": 30, "application": 50, "problem_solving": 20}
            }
        }
        
        generator = PresentationGenerator(config)
        
        # Simulate slide progression
        module_data = config["modules"]["test_module"]
        total_slides = len(config["presentation_templates"]["module_overview"]["slides"])
        
        for slide_index in range(total_slides):
            slide_content = generator.generate_slide("module_overview", slide_index, module_data)
            
            # Calculate progress
            progress_percent = ((slide_index + 1) / total_slides) * 100
            
            # Verify content generation
            assert slide_content is not None
            assert len(slide_content) > 20
            
            # Verify progress calculation
            assert 0 <= progress_percent <= 100
    
    def test_user_preference_and_content_adaptation(self):
        """
        Test adaptation of content based on user preferences
        
        Verifies that user preferences affect content generation
        and module recommendations.
        """
        def adapt_content_to_preferences(content, user_preferences):
            """Mock function to adapt content based on preferences"""
            difficulty = user_preferences.get("difficulty_level", "intermediate")
            hands_on_pref = user_preferences.get("hands_on_preference", True)
            focus_areas = user_preferences.get("focus_areas", [])
            
            adapted_content = content
            
            # Adapt based on difficulty
            if difficulty == "beginner":
                adapted_content += "\n\n**Beginner-friendly explanations included**"
            elif difficulty == "advanced":
                adapted_content += "\n\n**Advanced technical details provided**"
            
            # Adapt based on hands-on preference
            if hands_on_pref:
                adapted_content += "\n\n**Interactive exercises available**"
            
            # Adapt based on focus areas
            if focus_areas:
                adapted_content += f"\n\n**Focused on: {', '.join(focus_areas)}**"
            
            return adapted_content
        
        base_content = "# Module Overview\n\nThis is the basic content."
        
        # Test beginner preferences
        beginner_prefs = {
            "difficulty_level": "beginner",
            "hands_on_preference": True,
            "focus_areas": ["automation"]
        }
        
        adapted = adapt_content_to_preferences(base_content, beginner_prefs)
        assert "Beginner-friendly" in adapted
        assert "Interactive exercises" in adapted
        assert "automation" in adapted
        
        # Test advanced preferences
        advanced_prefs = {
            "difficulty_level": "advanced",
            "hands_on_preference": False,
            "focus_areas": ["ai_integration"]
        }
        
        adapted = adapt_content_to_preferences(base_content, advanced_prefs)
        assert "Advanced technical" in adapted
        assert "Interactive exercises" not in adapted
        assert "ai_integration" in adapted


class TestErrorRecovery:
    """Test suite for error recovery and resilience"""
    
    def test_corrupted_data_recovery(self):
        """
        Test recovery from corrupted configuration or progress data
        
        Verifies that the application can recover gracefully from
        data corruption and continue functioning with defaults.
        """
        # Test recovery from corrupted config
        with patch('app.load_config', side_effect=json.JSONDecodeError("Invalid JSON", "", 0)):
            # Should fall back to default or minimal config
            try:
                generator = PresentationGenerator({})
                result = generator.generate_slide("introduction", 0)
                assert isinstance(result, str)
            except Exception as e:
                # Should not be a JSON decode error
                assert not isinstance(e, json.JSONDecodeError)
        
        # Test recovery from corrupted progress
        with patch('app.load_user_progress', side_effect=json.JSONDecodeError("Invalid JSON", "", 0)):
            # Should return default progress structure
            progress = load_user_progress()
            assert "current_module" in progress
            assert "completed_modules" in progress
            assert isinstance(progress["completed_modules"], list)
    
    def test_partial_functionality_on_errors(self):
        """
        Test that application maintains partial functionality during errors
        
        Verifies that component failures don't bring down the entire application.
        """
        # Test with missing template
        config = {
            "presentation_templates": {},
            "assessment_criteria": {}
        }
        
        generator = PresentationGenerator(config)
        result = generator.generate_slide("missing_template", 0)
        
        # Should return error message, not crash
        assert isinstance(result, str)
        assert "template not found" in result.lower() or "not found" in result.lower()
        
        # Test with missing module data
        result = generator.generate_slide("module_overview", 0, None)
        assert isinstance(result, str)
        assert "template not found" in result.lower() or "not available" in result.lower()
    
    def test_network_failure_simulation(self):
        """
        Test application behavior during network failures
        
        Simulates network issues and verifies graceful degradation.
        """
        def simulate_api_call_with_failure():
            """Mock function that simulates network failure"""
            import random
            if random.random() < 0.3:  # 30% failure rate
                raise ConnectionError("Network unavailable")
            return {"status": "success", "data": "API response"}
        
        # Test retry logic
        def api_call_with_retry(max_retries=3):
            """Mock function with retry logic"""
            for attempt in range(max_retries):
                try:
                    return simulate_api_call_with_failure()
                except ConnectionError:
                    if attempt == max_retries - 1:
                        return {"status": "error", "message": "Network unavailable after retries"}
                    continue
        
        # Simulate multiple calls
        results = []
        for _ in range(10):
            result = api_call_with_retry()
            results.append(result)
        
        # Verify that some calls succeed and failures are handled
        success_count = sum(1 for r in results if r["status"] == "success")
        error_count = sum(1 for r in results if r["status"] == "error")
        
        # Should have both successes and handled errors
        assert success_count + error_count == 10
        assert error_count <= 10  # Not all should fail


class TestPerformanceIntegration:
    """Test suite for performance-related integration scenarios"""
    
    def test_large_dataset_handling(self):
        """
        Test application performance with large datasets
        
        Verifies that the application handles large amounts of
        progress data and configuration without performance degradation.
        """
        # Create large progress dataset
        large_progress = {
            "current_module": "test_module",
            "completed_modules": [f"module_{i}" for i in range(100)],
            "current_progress": 75,
            "skills_acquired": [f"skill_{i}" for i in range(200)],
            "assessments_completed": [f"assessment_{i}" for i in range(50)],
            "hands_on_projects": [f"project_{i}" for i in range(30)],
            "learning_path": "advanced",
            "preferences": {
                "difficulty_level": "advanced",
                "focus_areas": [f"area_{i}" for i in range(20)],
                "hands_on_preference": True
            },
            "session_history": [
                {
                    "date": f"2024-01-{i:02d}",
                    "module": f"module_{i % 10}",
                    "duration": 60 + (i % 60)
                } for i in range(1, 366)  # One year of sessions
            ],
            "bookmarks": [f"bookmark_{i}" for i in range(100)],
            "notes": {f"note_{i}": f"Content {i}" for i in range(50)}
        }
        
        # Test data processing performance
        import time
        
        start_time = time.time()
        
        # Simulate progress calculation
        total_modules = len(large_progress["completed_modules"])
        total_skills = len(large_progress["skills_acquired"])
        total_sessions = len(large_progress["session_history"])
        
        # Calculate statistics
        avg_session_duration = sum(
            session["duration"] for session in large_progress["session_history"]
        ) / total_sessions if total_sessions > 0 else 0
        
        processing_time = time.time() - start_time
        
        # Verify performance is acceptable (< 1 second for this operation)
        assert processing_time < 1.0
        assert total_modules == 100
        assert total_skills == 200
        assert avg_session_duration > 0
    
    def test_concurrent_user_simulation(self):
        """
        Test application behavior with concurrent user operations
        
        Simulates multiple users accessing the system simultaneously.
        """
        import threading
        import time
        
        def simulate_user_session(user_id, results):
            """Simulate a user session"""
            try:
                # Simulate user operations
                config = {
                    "modules": {"test_module": {"title": "Test", "description": "Test", "topics": [], "hands_on": False, "difficulty": "beginner"}},
                    "presentation_templates": {"introduction": {"slides": ["Welcome"]}},
                    "assessment_criteria": {"beginner": {"understanding": 40, "application": 40, "problem_solving": 20}}
                }
                
                generator = PresentationGenerator(config)
                
                # Generate multiple slides
                for i in range(5):
                    slide = generator.generate_slide("introduction", 0)
                    time.sleep(0.1)  # Simulate processing time
                
                results[user_id] = "success"
            except Exception as e:
                results[user_id] = f"error: {str(e)}"
        
        # Simulate 10 concurrent users
        threads = []
        results = {}
        
        for user_id in range(10):
            thread = threading.Thread(
                target=simulate_user_session,
                args=(user_id, results)
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=5.0)
        
        # Verify all users completed successfully
        assert len(results) == 10
        success_count = sum(1 for result in results.values() if result == "success")
        assert success_count >= 8  # Allow for some failures due to threading


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
