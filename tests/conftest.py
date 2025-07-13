"""
Pytest configuration and shared fixtures for AI-QA Studies Portal tests.

This module provides common test fixtures, configuration, and utilities
used across all test modules in the test suite.
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Generator
from unittest.mock import Mock, patch
import pandas as pd
import plotly.graph_objects as go

# Test data imports
from tests.fixtures.sample_configs import SAMPLE_MODULE_CONFIG, SAMPLE_USER_PROGRESS
from tests.fixtures.test_data import MOCK_PRESENTATION_DATA, MOCK_CHART_DATA


@pytest.fixture(scope="session")
def temp_workspace() -> Generator[Path, None, None]:
    """
    Create a temporary workspace directory for testing.
    
    Yields:
        Path: Temporary directory path for test workspace
    """
    temp_dir = tempfile.mkdtemp(prefix="ai_qa_test_")
    workspace_path = Path(temp_dir)
    
    # Create basic workspace structure
    (workspace_path / "configs").mkdir()
    (workspace_path / "data").mkdir()
    (workspace_path / "reports").mkdir()
    
    yield workspace_path
    
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_module_config() -> Dict[str, Any]:
    """
    Provide sample module configuration for testing.
    
    Returns:
        Dict[str, Any]: Sample module configuration data
    """
    return SAMPLE_MODULE_CONFIG.copy()


@pytest.fixture
def sample_user_progress() -> Dict[str, Any]:
    """
    Provide sample user progress data for testing.
    
    Returns:
        Dict[str, Any]: Sample user progress data
    """
    return SAMPLE_USER_PROGRESS.copy()


@pytest.fixture
def mock_config_file(temp_workspace: Path, sample_module_config: Dict[str, Any]) -> Path:
    """
    Create a mock configuration file for testing.
    
    Args:
        temp_workspace: Temporary workspace directory
        sample_module_config: Sample configuration data
        
    Returns:
        Path: Path to the created config file
    """
    config_file = temp_workspace / "configs" / "module_config.json"
    with open(config_file, 'w') as f:
        json.dump(sample_module_config, f, indent=2)
    return config_file


@pytest.fixture
def mock_progress_file(temp_workspace: Path, sample_user_progress: Dict[str, Any]) -> Path:
    """
    Create a mock user progress file for testing.
    
    Args:
        temp_workspace: Temporary workspace directory
        sample_user_progress: Sample progress data
        
    Returns:
        Path: Path to the created progress file
    """
    progress_file = temp_workspace / "data" / "user_progress.json"
    with open(progress_file, 'w') as f:
        json.dump(sample_user_progress, f, indent=2)
    return progress_file


@pytest.fixture
def mock_presentation_generator():
    """
    Mock presentation generator for testing.
    
    Returns:
        Mock: Mocked PresentationGenerator instance
    """
    from app import PresentationGenerator
    
    mock_gen = Mock(spec=PresentationGenerator)
    mock_gen.generate_slide.return_value = MOCK_PRESENTATION_DATA["sample_slide"]
    mock_gen.config = SAMPLE_MODULE_CONFIG
    mock_gen.templates = SAMPLE_MODULE_CONFIG["presentation_templates"]
    
    return mock_gen


@pytest.fixture
def mock_plotly_chart():
    """
    Mock Plotly chart for testing visualization components.
    
    Returns:
        Mock: Mocked Plotly figure
    """
    mock_fig = Mock(spec=go.Figure)
    mock_fig.to_html.return_value = MOCK_CHART_DATA["html_output"]
    mock_fig.to_json.return_value = json.dumps(MOCK_CHART_DATA["json_data"])
    
    return mock_fig


@pytest.fixture
def mock_gradio_interface():
    """
    Mock Gradio interface for testing UI components.
    
    Returns:
        Mock: Mocked Gradio interface
    """
    import gradio as gr
    
    mock_interface = Mock(spec=gr.Interface)
    mock_interface.launch.return_value = None
    mock_interface.close.return_value = None
    
    return mock_interface


@pytest.fixture
def mock_pandas_dataframe():
    """
    Mock pandas DataFrame for testing data processing.
    
    Returns:
        pd.DataFrame: Sample DataFrame with test data
    """
    return pd.DataFrame(MOCK_CHART_DATA["sample_data"])


@pytest.fixture(autouse=True)
def reset_mocks():
    """
    Automatically reset all mocks after each test.
    """
    yield
    # Any cleanup code can go here


@pytest.fixture
def api_client():
    """
    Create a test client for API testing.
    
    Returns:
        TestClient: FastAPI test client
    """
    from fastapi.testclient import TestClient
    from app import create_main_interface
    
    # Create a test version of the app
    app = create_main_interface()
    return TestClient(app)


@pytest.fixture
def authenticated_user():
    """
    Mock authenticated user for testing secure endpoints.
    
    Returns:
        Dict[str, Any]: User authentication data
    """
    return {
        "user_id": "test_user_123",
        "username": "test_user",
        "email": "test@example.com",
        "roles": ["learner", "qa_professional"],
        "progress": {
            "completed_modules": ["ai_best_practices"],
            "current_module": "programming_with_ai",
            "total_progress": 25.5
        }
    }


@pytest.fixture(scope="session")
def browser_context():
    """
    Create browser context for end-to-end testing.
    
    Yields:
        BrowserContext: Playwright browser context
    """
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="AI-QA-Portal-Test-Agent/1.0"
        )
        yield context
        context.close()
        browser.close()


# Pytest markers for test categorization
pytestmark = [
    pytest.mark.asyncio,  # Enable async test support
]


def pytest_configure(config):
    """
    Configure pytest with custom markers and settings.
    """
    config.addinivalue_line(
        "markers", 
        "unit: marks tests as unit tests (deselect with '-m \"not unit\"')"
    )
    config.addinivalue_line(
        "markers", 
        "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", 
        "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", 
        "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers based on file location.
    """
    for item in items:
        # Add markers based on file path
        if "/unit/" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "/integration/" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "/e2e/" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        elif "/performance/" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
        elif "/security/" in str(item.fspath):
            item.add_marker(pytest.mark.security)


# Custom assertion helpers
class CustomAssertions:
    """Custom assertion methods for AI-QA Portal testing."""
    
    @staticmethod
    def assert_valid_progress_data(progress_data: Dict[str, Any]) -> None:
        """
        Assert that progress data has required structure.
        
        Args:
            progress_data: User progress data to validate
        """
        required_keys = [
            "current_module", "completed_modules", "current_progress",
            "skills_acquired", "assessments_completed", "learning_path"
        ]
        for key in required_keys:
            assert key in progress_data, f"Missing required key: {key}"
        
        assert isinstance(progress_data["completed_modules"], list)
        assert isinstance(progress_data["current_progress"], (int, float))
        assert 0 <= progress_data["current_progress"] <= 100
    
    @staticmethod
    def assert_valid_module_config(config_data: Dict[str, Any]) -> None:
        """
        Assert that module configuration has required structure.
        
        Args:
            config_data: Module configuration data to validate
        """
        assert "modules" in config_data
        assert "presentation_templates" in config_data
        assert "assessment_criteria" in config_data
        
        for module_id, module_data in config_data["modules"].items():
            required_keys = ["title", "description", "topics", "hands_on", "difficulty"]
            for key in required_keys:
                assert key in module_data, f"Missing key {key} in module {module_id}"
    
    @staticmethod
    def assert_valid_presentation_slide(slide_content: str) -> None:
        """
        Assert that presentation slide content is valid.
        
        Args:
            slide_content: Slide content to validate
        """
        assert isinstance(slide_content, str)
        assert len(slide_content) > 0
        assert slide_content.startswith("#")  # Should be markdown with header


# Make custom assertions available as pytest fixture
@pytest.fixture
def assertions():
    """Provide custom assertion helpers."""
    return CustomAssertions()
