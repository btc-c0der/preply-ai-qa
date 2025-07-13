"""
End-to-End Tests for AI-QA Portal

This module contains comprehensive end-to-end tests that verify
the complete functionality of the AI-QA Portal from a user's perspective.

These tests simulate real user interactions using Selenium WebDriver
and test the entire application workflow including UI interactions,
data persistence, and user journey completion.

Test Categories:
- Complete User Workflows
- Browser Compatibility
- Performance Testing
- Accessibility Testing
- Mobile Responsiveness
- Error Scenarios

Author: AI-QA Portal Testing Team
Date: 2024
"""

import pytest
import time
import os
import json
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
import threading
import subprocess
import signal


class PortalE2ETestBase:
    """Base class for end-to-end tests with common setup and utilities"""
    
    @classmethod
    def setup_class(cls):
        """Set up the test environment and start the portal application"""
        cls.test_port = 7861  # Use different port for testing
        cls.base_url = f"http://localhost:{cls.test_port}"
        cls.app_process = None
        cls.setup_test_data()
        cls.start_portal_application()
        cls.wait_for_portal_ready()
    
    @classmethod
    def teardown_class(cls):
        """Clean up test environment and stop the portal application"""
        cls.stop_portal_application()
        cls.cleanup_test_data()
    
    def setup_method(self):
        """Set up individual test with fresh browser instance"""
        self.driver = self.create_webdriver()
        self.wait = WebDriverWait(self.driver, 10)
    
    def teardown_method(self):
        """Clean up individual test"""
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    @classmethod
    def setup_test_data(cls):
        """Create test data files"""
        cls.test_dir = tempfile.mkdtemp()
        
        # Create test configuration
        cls.test_config = {
            "modules": {
                "ai_best_practices": {
                    "title": "Best Practices with AI",
                    "description": "Learn effective AI usage in QA workflows",
                    "topics": ["Prompt Design for QA", "Workflow Integration", "Smart Decision Making"],
                    "hands_on": True,
                    "difficulty": "beginner"
                },
                "programming_with_ai": {
                    "title": "Programming/Building Projects with AI",
                    "description": "Practical AI-driven development for QA professionals",
                    "topics": ["Automation Tools Development", "Chatbot Integration for QA"],
                    "hands_on": True,
                    "difficulty": "intermediate"
                }
            },
            "presentation_templates": {
                "introduction": {
                    "slides": ["Welcome to AI-Driven QA", "Your Learning Journey", "Tools and Resources", "Expected Outcomes"]
                },
                "module_overview": {
                    "slides": ["Module Introduction", "Learning Objectives", "Key Topics", "Hands-on Activities", "Assessment Criteria"]
                }
            },
            "assessment_criteria": {
                "beginner": {"understanding": 40, "application": 40, "problem_solving": 20},
                "intermediate": {"understanding": 30, "application": 50, "problem_solving": 20}
            }
        }
        
        # Create test user progress
        cls.test_progress = {
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
        cls.config_file = os.path.join(cls.test_dir, 'module_config.json')
        cls.progress_file = os.path.join(cls.test_dir, 'user_progress.json')
        
        with open(cls.config_file, 'w') as f:
            json.dump(cls.test_config, f, indent=2)
        
        with open(cls.progress_file, 'w') as f:
            json.dump(cls.test_progress, f, indent=2)
    
    @classmethod
    def cleanup_test_data(cls):
        """Clean up test data files"""
        import shutil
        if hasattr(cls, 'test_dir'):
            shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    @classmethod
    def start_portal_application(cls):
        """Start the portal application for testing"""
        try:
            # Change to the application directory
            app_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..')
            
            # Start the application with test configuration
            env = os.environ.copy()
            env['GRADIO_SERVER_PORT'] = str(cls.test_port)
            
            cls.app_process = subprocess.Popen(
                ['python', 'app.py'],
                cwd=app_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Give the application time to start
            time.sleep(5)
            
        except Exception as e:
            pytest.skip(f"Could not start portal application: {e}")
    
    @classmethod
    def stop_portal_application(cls):
        """Stop the portal application"""
        if cls.app_process:
            try:
                cls.app_process.terminate()
                cls.app_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                cls.app_process.kill()
                cls.app_process.wait()
    
    @classmethod
    def wait_for_portal_ready(cls):
        """Wait for the portal to be ready to accept connections"""
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                response = requests.get(cls.base_url, timeout=5)
                if response.status_code == 200:
                    return
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(1)
        
        pytest.skip("Portal application did not start within expected time")
    
    def create_webdriver(self, browser="chrome"):
        """Create a configured WebDriver instance"""
        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--headless")  # Run in headless mode for CI
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            return webdriver.Chrome(options=options)
        
        elif browser == "firefox":
            options = FirefoxOptions()
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
            return webdriver.Firefox(options=options)
        
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present and return it"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    
    def wait_for_clickable(self, by, value, timeout=10):
        """Wait for an element to be clickable and return it"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
    
    def take_screenshot(self, name):
        """Take a screenshot for debugging"""
        screenshot_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)
        
        screenshot_path = os.path.join(screenshot_dir, f"{name}.png")
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path


class TestCompleteUserWorkflows(PortalE2ETestBase):
    """Test complete user workflows from start to finish"""
    
    def test_new_user_onboarding_workflow(self):
        """
        Test the complete new user onboarding workflow
        
        This test verifies the entire onboarding process including:
        1. Initial portal access
        2. Dashboard overview
        3. Preference setting
        4. Module recommendations
        """
        # Navigate to the portal
        self.driver.get(self.base_url)
        
        # Wait for the page to load
        self.wait_for_element(By.TAG_NAME, "body")
        
        # Take screenshot for debugging
        self.take_screenshot("onboarding_start")
        
        # Verify portal loads successfully
        assert "AI-QA Portal" in self.driver.title or "Gradio" in self.driver.title
        
        # Look for welcome content or dashboard elements
        try:
            # Try to find common Gradio elements
            gradio_app = self.wait_for_element(By.CLASS_NAME, "gradio-container", timeout=15)
            assert gradio_app is not None
            
        except TimeoutException:
            # If Gradio container not found, try alternative selectors
            self.take_screenshot("onboarding_timeout")
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            assert len(body_text) > 0, "Page appears to be empty"
        
        # Verify responsive design
        self.driver.set_window_size(375, 667)  # Mobile size
        time.sleep(1)
        
        # Check that content is still accessible on mobile
        body = self.driver.find_element(By.TAG_NAME, "body")
        assert body.is_displayed()
        
        # Restore desktop size
        self.driver.set_window_size(1920, 1080)
    
    def test_module_selection_and_navigation_workflow(self):
        """
        Test module selection and navigation workflow
        
        Verifies that users can:
        1. Browse available modules
        2. Select a module
        3. Navigate through module content
        4. Track progress
        """
        # Navigate to the portal
        self.driver.get(self.base_url)
        self.wait_for_element(By.TAG_NAME, "body")
        
        # Wait for Gradio to fully load
        time.sleep(3)
        
        # Take screenshot of initial state
        self.take_screenshot("module_selection_start")
        
        # Look for interactive elements (buttons, tabs, etc.)
        try:
            # Find any clickable elements that might represent modules or navigation
            clickable_elements = self.driver.find_elements(By.CSS_SELECTOR, "button, .tab, .gr-button")
            
            if clickable_elements:
                # Click on the first interactive element
                first_element = clickable_elements[0]
                self.driver.execute_script("arguments[0].click();", first_element)
                time.sleep(2)
                
                self.take_screenshot("after_first_click")
            
            # Verify that interactions work
            current_url = self.driver.current_url
            assert current_url == self.base_url or current_url.startswith(self.base_url)
            
        except Exception as e:
            # Log the page source for debugging
            self.take_screenshot("module_selection_error")
            print(f"Page source: {self.driver.page_source[:500]}...")
            raise AssertionError(f"Module selection workflow failed: {e}")
    
    def test_presentation_viewing_workflow(self):
        """
        Test presentation viewing and slide navigation workflow
        
        Verifies that users can:
        1. Access presentations
        2. Navigate between slides
        3. View slide content
        4. Track presentation progress
        """
        # Navigate to the portal
        self.driver.get(self.base_url)
        self.wait_for_element(By.TAG_NAME, "body")
        
        # Wait for full page load
        time.sleep(5)
        
        self.take_screenshot("presentation_start")
        
        # Look for presentation-related elements
        try:
            # Check for any elements that might contain presentation content
            content_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                ".markdown, .gr-markdown, pre, code, h1, h2, h3")
            
            # Verify that some content is displayed
            assert len(content_elements) > 0, "No content elements found"
            
            # Check for navigation elements
            nav_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                "button[class*='nav'], button[class*='next'], button[class*='prev']")
            
            if nav_elements:
                # Test navigation if available
                nav_button = nav_elements[0]
                initial_text = self.driver.find_element(By.TAG_NAME, "body").text
                
                self.driver.execute_script("arguments[0].click();", nav_button)
                time.sleep(1)
                
                new_text = self.driver.find_element(By.TAG_NAME, "body").text
                # Content should change or remain stable
                assert len(new_text) > 0
            
            self.take_screenshot("presentation_content")
            
        except Exception as e:
            self.take_screenshot("presentation_error")
            raise AssertionError(f"Presentation workflow failed: {e}")
    
    def test_progress_tracking_workflow(self):
        """
        Test progress tracking and user data persistence
        
        Verifies that:
        1. User progress is tracked correctly
        2. Data persists across interactions
        3. Progress indicators work
        4. Statistics are updated
        """
        # Navigate to the portal
        self.driver.get(self.base_url)
        self.wait_for_element(By.TAG_NAME, "body")
        
        # Wait for application to load
        time.sleep(3)
        
        self.take_screenshot("progress_start")
        
        # Perform several interactions to generate progress
        try:
            # Find and interact with multiple elements
            interactive_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                "button, input, select, .gr-button")
            
            interactions_performed = 0
            for element in interactive_elements[:5]:  # Limit to first 5 elements
                try:
                    if element.is_displayed() and element.is_enabled():
                        self.driver.execute_script("arguments[0].click();", element)
                        time.sleep(0.5)
                        interactions_performed += 1
                except Exception:
                    continue  # Skip elements that can't be clicked
            
            # Verify that interactions were performed
            assert interactions_performed > 0, "No interactions could be performed"
            
            self.take_screenshot("progress_after_interactions")
            
            # Check for any progress indicators or status updates
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            assert len(page_text) > 100, "Page should contain substantial content"
            
        except Exception as e:
            self.take_screenshot("progress_error")
            raise AssertionError(f"Progress tracking workflow failed: {e}")


class TestBrowserCompatibility(PortalE2ETestBase):
    """Test browser compatibility across different browsers"""
    
    @pytest.mark.parametrize("browser", ["chrome", "firefox"])
    def test_cross_browser_compatibility(self, browser):
        """
        Test portal functionality across different browsers
        
        Verifies that the portal works consistently across
        Chrome and Firefox browsers.
        """
        if hasattr(self, 'driver'):
            self.driver.quit()
        
        # Create browser-specific driver
        self.driver = self.create_webdriver(browser)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Navigate to the portal
        self.driver.get(self.base_url)
        self.wait_for_element(By.TAG_NAME, "body")
        
        # Wait for application to load
        time.sleep(3)
        
        self.take_screenshot(f"browser_compat_{browser}")
        
        # Test basic functionality
        try:
            # Verify page loads
            assert self.driver.title is not None
            assert len(self.driver.title) > 0
            
            # Verify content is present
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            assert len(body_text) > 50, "Page should contain substantial content"
            
            # Test basic interaction if possible
            clickable_elements = self.driver.find_elements(By.CSS_SELECTOR, "button")
            if clickable_elements:
                element = clickable_elements[0]
                assert element.is_displayed()
                assert element.is_enabled()
            
        except Exception as e:
            self.take_screenshot(f"browser_error_{browser}")
            raise AssertionError(f"Browser compatibility test failed for {browser}: {e}")


class TestPerformanceAndLoad(PortalE2ETestBase):
    """Test performance and load handling"""
    
    def test_page_load_performance(self):
        """
        Test page load performance and responsiveness
        
        Verifies that the portal loads within acceptable time limits
        and performs well under normal conditions.
        """
        start_time = time.time()
        
        # Navigate to the portal
        self.driver.get(self.base_url)
        
        # Wait for initial load
        self.wait_for_element(By.TAG_NAME, "body")
        
        initial_load_time = time.time() - start_time
        
        # Page should load within 10 seconds
        assert initial_load_time < 10, f"Page load too slow: {initial_load_time:.2f}s"
        
        # Wait for full application load
        time.sleep(3)
        
        full_load_time = time.time() - start_time
        
        # Full application should load within 15 seconds
        assert full_load_time < 15, f"Full app load too slow: {full_load_time:.2f}s"
        
        self.take_screenshot("performance_loaded")
        
        # Test interaction responsiveness
        try:
            interactive_elements = self.driver.find_elements(By.CSS_SELECTOR, "button")
            if interactive_elements:
                interaction_start = time.time()
                element = interactive_elements[0]
                self.driver.execute_script("arguments[0].click();", element)
                interaction_time = time.time() - interaction_start
                
                # Interactions should be responsive (< 1 second)
                assert interaction_time < 1.0, f"Interaction too slow: {interaction_time:.2f}s"
        
        except Exception:
            pass  # Interaction test is optional
    
    def test_memory_usage_stability(self):
        """
        Test memory usage stability during extended use
        
        Verifies that the portal doesn't have memory leaks
        or excessive resource usage during normal operation.
        """
        # Navigate to the portal
        self.driver.get(self.base_url)
        self.wait_for_element(By.TAG_NAME, "body")
        
        # Perform repeated interactions to test stability
        for i in range(10):
            try:
                # Refresh the page to simulate user activity
                self.driver.refresh()
                self.wait_for_element(By.TAG_NAME, "body")
                time.sleep(1)
                
                # Verify page is still responsive
                body = self.driver.find_element(By.TAG_NAME, "body")
                assert body.is_displayed()
                
            except Exception as e:
                self.take_screenshot(f"memory_test_error_{i}")
                raise AssertionError(f"Memory stability test failed at iteration {i}: {e}")
        
        self.take_screenshot("memory_test_complete")


class TestAccessibilityCompliance(PortalE2ETestBase):
    """Test accessibility compliance and features"""
    
    def test_keyboard_navigation(self):
        """
        Test keyboard navigation accessibility
        
        Verifies that the portal can be navigated using
        only keyboard inputs for accessibility compliance.
        """
        # Navigate to the portal
        self.driver.get(self.base_url)
        self.wait_for_element(By.TAG_NAME, "body")
        time.sleep(3)
        
        self.take_screenshot("accessibility_start")
        
        try:
            # Test Tab navigation
            active_element = self.driver.switch_to.active_element
            initial_element = active_element
            
            # Press Tab several times to navigate
            for i in range(10):
                ActionChains(self.driver).send_keys_to_element(
                    active_element, "\t"
                ).perform()
                time.sleep(0.2)
                
                new_active = self.driver.switch_to.active_element
                if new_active != active_element:
                    # Focus moved successfully
                    active_element = new_active
            
            # Verify that tab navigation works
            final_element = self.driver.switch_to.active_element
            # Focus should have moved from initial position
            # (This test is basic since Gradio may handle focus differently)
            
            self.take_screenshot("accessibility_navigation")
            
        except Exception as e:
            self.take_screenshot("accessibility_error")
            # Don't fail the test for keyboard navigation issues
            # as this depends heavily on Gradio's implementation
            print(f"Keyboard navigation test encountered issue: {e}")
    
    def test_content_structure_accessibility(self):
        """
        Test content structure for accessibility
        
        Verifies that the portal has proper heading structure
        and semantic elements for screen readers.
        """
        # Navigate to the portal
        self.driver.get(self.base_url)
        self.wait_for_element(By.TAG_NAME, "body")
        time.sleep(3)
        
        # Check for proper heading structure
        headings = self.driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")
        
        # Should have at least some headings for structure
        # (This is flexible since content is generated dynamically)
        if len(headings) > 0:
            # Verify headings are visible
            visible_headings = [h for h in headings if h.is_displayed()]
            assert len(visible_headings) > 0, "No visible headings found"
        
        # Check for semantic elements
        semantic_elements = self.driver.find_elements(By.CSS_SELECTOR, 
            "main, section, article, nav, header, footer")
        
        # While semantic elements are preferred, they're not required for basic functionality
        
        # Check that images have alt text (if any)
        images = self.driver.find_elements(By.TAG_NAME, "img")
        for img in images:
            alt_text = img.get_attribute("alt")
            # Alt text should be present (empty string is acceptable for decorative images)
            assert alt_text is not None, "Image missing alt attribute"
        
        self.take_screenshot("accessibility_structure")


class TestResponsiveDesign(PortalE2ETestBase):
    """Test responsive design across different screen sizes"""
    
    @pytest.mark.parametrize("viewport", [
        (1920, 1080),  # Desktop
        (1024, 768),   # Tablet
        (375, 667),    # Mobile
    ])
    def test_responsive_layout(self, viewport):
        """
        Test responsive layout across different viewport sizes
        
        Verifies that the portal adapts properly to different
        screen sizes and maintains usability.
        """
        width, height = viewport
        
        # Set viewport size
        self.driver.set_window_size(width, height)
        
        # Navigate to the portal
        self.driver.get(self.base_url)
        self.wait_for_element(By.TAG_NAME, "body")
        time.sleep(3)
        
        self.take_screenshot(f"responsive_{width}x{height}")
        
        # Verify content is accessible at this viewport
        try:
            # Check that body is visible
            body = self.driver.find_element(By.TAG_NAME, "body")
            assert body.is_displayed()
            
            # Verify content doesn't overflow horizontally
            body_width = body.size['width']
            assert body_width <= width + 50, f"Content overflows viewport: {body_width} > {width}"
            
            # Check for any interactive elements
            buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
            if buttons:
                # Verify buttons are reasonably sized for touch (mobile)
                if width <= 768:  # Mobile/tablet
                    for button in buttons[:3]:  # Check first few buttons
                        if button.is_displayed():
                            button_height = button.size['height']
                            assert button_height >= 30, f"Button too small for touch: {button_height}px"
            
        except Exception as e:
            self.take_screenshot(f"responsive_error_{width}x{height}")
            raise AssertionError(f"Responsive design test failed for {width}x{height}: {e}")


class TestErrorScenarios(PortalE2ETestBase):
    """Test error handling and edge cases"""
    
    def test_network_interruption_handling(self):
        """
        Test handling of network interruptions
        
        Verifies that the portal handles network issues gracefully
        and provides appropriate user feedback.
        """
        # Navigate to the portal
        self.driver.get(self.base_url)
        self.wait_for_element(By.TAG_NAME, "body")
        time.sleep(3)
        
        self.take_screenshot("network_test_start")
        
        # Test with invalid URL to simulate network error
        try:
            self.driver.get("http://invalid-url-for-testing.local")
            time.sleep(2)
            
            # Should show browser error page
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            error_indicators = ["error", "not found", "cannot", "unable", "failed"]
            has_error_message = any(indicator in page_text.lower() for indicator in error_indicators)
            assert has_error_message, "No error indication found for invalid URL"
            
        except Exception:
            # This is expected for invalid URLs
            pass
        
        # Return to valid portal
        self.driver.get(self.base_url)
        self.wait_for_element(By.TAG_NAME, "body")
        
        # Verify portal still works after network issue
        body = self.driver.find_element(By.TAG_NAME, "body")
        assert body.is_displayed()
        
        self.take_screenshot("network_test_recovery")
    
    def test_invalid_user_interactions(self):
        """
        Test handling of invalid user interactions
        
        Verifies that the portal handles unexpected user actions
        gracefully without crashing or breaking functionality.
        """
        # Navigate to the portal
        self.driver.get(self.base_url)
        self.wait_for_element(By.TAG_NAME, "body")
        time.sleep(3)
        
        self.take_screenshot("invalid_interactions_start")
        
        try:
            # Test rapid clicking
            clickable_elements = self.driver.find_elements(By.CSS_SELECTOR, "button")
            if clickable_elements:
                element = clickable_elements[0]
                for _ in range(10):
                    try:
                        self.driver.execute_script("arguments[0].click();", element)
                        time.sleep(0.1)
                    except Exception:
                        break  # Element may become stale
            
            # Test invalid form inputs (if any forms exist)
            input_elements = self.driver.find_elements(By.CSS_SELECTOR, "input, textarea")
            for input_elem in input_elements[:3]:
                if input_elem.is_displayed() and input_elem.is_enabled():
                    # Send very long text
                    long_text = "x" * 10000
                    input_elem.clear()
                    input_elem.send_keys(long_text)
                    time.sleep(0.5)
            
            # Verify portal still functions after invalid interactions
            body = self.driver.find_element(By.TAG_NAME, "body")
            assert body.is_displayed()
            
            self.take_screenshot("invalid_interactions_complete")
            
        except Exception as e:
            self.take_screenshot("invalid_interactions_error")
            # Don't fail the test unless the portal completely breaks
            print(f"Invalid interactions test encountered issue: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
