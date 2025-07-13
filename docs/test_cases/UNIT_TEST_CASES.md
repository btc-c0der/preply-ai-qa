# Unit Test Cases for AI-QA Portal

## Overview
This document provides detailed test case specifications for unit testing the AI-QA Portal core components. Each test case includes objectives, prerequisites, steps, and expected outcomes.

## Configuration Management Test Cases

### TC-U001: Load Valid Configuration
**Objective**: Verify that valid configuration files are loaded correctly

**Prerequisites**:
- Valid module_config.json file exists
- File contains proper JSON structure
- All required configuration sections present

**Test Steps**:
1. Create a valid configuration file with all required sections
2. Call `load_config()` function
3. Verify configuration object is returned
4. Validate all required sections are present
5. Check data types and structure

**Expected Results**:
- Configuration loads without errors
- All sections (modules, presentation_templates, assessment_criteria) present
- Data structure matches expected format
- Function returns dictionary object

**Test Data**:
```json
{
  "modules": {
    "test_module": {
      "title": "Test Module",
      "description": "Test description",
      "topics": ["Topic 1", "Topic 2"],
      "hands_on": true,
      "difficulty": "intermediate"
    }
  },
  "presentation_templates": {
    "introduction": {
      "slides": ["Welcome", "Overview"]
    }
  },
  "assessment_criteria": {
    "intermediate": {
      "understanding": 30,
      "application": 50,
      "problem_solving": 20
    }
  }
}
```

**Implementation Notes**:
- Use mocking to avoid file system dependencies
- Test with realistic configuration data
- Verify error handling for edge cases

---

### TC-U002: Handle Missing Configuration File
**Objective**: Verify proper error handling when configuration file is missing

**Prerequisites**:
- Configuration file does not exist
- File system access is available

**Test Steps**:
1. Ensure configuration file does not exist
2. Call `load_config()` function
3. Verify appropriate exception is raised
4. Check exception type and message

**Expected Results**:
- `FileNotFoundError` exception is raised
- Exception message indicates missing file
- Application handles error gracefully
- No silent failures or incorrect data

**Error Scenarios**:
- File completely missing
- File exists but is empty
- File exists but cannot be read (permissions)

---

### TC-U003: Handle Invalid JSON Configuration
**Objective**: Verify error handling for malformed JSON in configuration

**Prerequisites**:
- Configuration file exists
- File contains invalid JSON syntax

**Test Steps**:
1. Create configuration file with invalid JSON
2. Call `load_config()` function
3. Verify `JSONDecodeError` is raised
4. Check error message content

**Expected Results**:
- `json.JSONDecodeError` exception is raised
- Error message indicates JSON parsing failure
- Line number information available (if applicable)
- No partial loading of corrupted data

**Invalid JSON Examples**:
```json
// Missing closing brace
{
  "modules": {
    "test": {}
// Comments not allowed
/* Block comment */
// Trailing comma
{
  "modules": {},
}
// Invalid syntax
{
  modules: {}
}
```

---

## User Progress Management Test Cases

### TC-U004: Load Existing User Progress
**Objective**: Verify successful loading of existing user progress data

**Prerequisites**:
- Valid user_progress.json file exists
- File contains properly formatted progress data

**Test Steps**:
1. Create valid progress file with complete data structure
2. Call `load_user_progress()` function
3. Verify progress object is returned
4. Validate all required fields are present
5. Check data types and relationships

**Expected Results**:
- Progress loads without errors
- All required fields present and valid
- Completed modules list is accessible
- Current progress values are numeric
- Preferences object is properly structured

**Test Data Structure**:
```json
{
  "current_module": "programming_with_ai",
  "completed_modules": ["ai_best_practices"],
  "current_progress": 65,
  "skills_acquired": ["Prompt Engineering", "API Integration"],
  "assessments_completed": ["Module 1 Assessment"],
  "hands_on_projects": ["AI Test Generator"],
  "learning_path": "intermediate",
  "preferences": {
    "difficulty_level": "intermediate",
    "focus_areas": ["automation"],
    "hands_on_preference": true
  },
  "session_history": [
    {
      "date": "2024-01-15",
      "module": "ai_best_practices",
      "duration": 120
    }
  ],
  "bookmarks": [],
  "notes": {}
}
```

---

### TC-U005: Create Default Progress for New User
**Objective**: Verify default progress structure is created for new users

**Prerequisites**:
- User progress file does not exist
- Default structure is well-defined

**Test Steps**:
1. Ensure progress file does not exist
2. Call `load_user_progress()` function
3. Verify default structure is returned
4. Check all required fields have appropriate defaults
5. Validate data types and initial values

**Expected Results**:
- Default progress structure is returned
- No exceptions or errors occur
- All required fields are present with sensible defaults
- User can immediately start using the system

**Default Values Validation**:
- `current_module`: null
- `completed_modules`: empty array
- `current_progress`: 0
- `preferences.difficulty_level`: "intermediate"
- `preferences.hands_on_preference`: true

---

### TC-U006: Save User Progress Successfully
**Objective**: Verify user progress data is saved correctly to file

**Prerequisites**:
- Valid progress data object available
- File system write access available

**Test Steps**:
1. Create valid progress data object
2. Call `save_user_progress(progress_data)` function
3. Verify file write operation completes
4. Check file contents match input data
5. Validate JSON formatting is correct

**Expected Results**:
- File is created/updated successfully
- JSON content matches input data exactly
- File is properly formatted and readable
- No data corruption or loss occurs

**Validation Steps**:
- Parse saved JSON and compare with original
- Verify all nested objects are preserved
- Check array ordering is maintained
- Confirm numeric precision is preserved

---

## Presentation Generator Test Cases

### TC-U007: Initialize Presentation Generator
**Objective**: Verify presentation generator initializes correctly with configuration

**Prerequisites**:
- Valid configuration object available
- Presentation templates defined

**Test Steps**:
1. Create presentation generator with valid config
2. Verify generator object is created
3. Check configuration is stored correctly
4. Validate templates are accessible

**Expected Results**:
- Generator initializes without errors
- Configuration is properly stored
- Templates dictionary is accessible
- Generator is ready for slide creation

---

### TC-U008: Generate Introduction Slides
**Objective**: Verify introduction slides are generated with proper content

**Prerequisites**:
- Presentation generator is initialized
- Introduction template is defined

**Test Steps**:
1. Call `generate_slide("introduction", 0)` for first slide
2. Verify slide content is returned
3. Check content contains expected elements
4. Validate markdown formatting
5. Test all introduction slide indices

**Expected Results**:
- Slide content is generated successfully
- Content includes welcome message and key information
- Markdown formatting is proper (headers, lists, etc.)
- Content is appropriate length and structure
- Emojis and visual elements are included

**Content Validation**:
- Header starts with "# " (markdown H1)
- Contains "Welcome" or similar greeting
- Includes bullet points with benefits
- Has engaging visual elements (emojis)
- Length is appropriate (50-5000 characters)

---

### TC-U009: Generate Module Overview Slides
**Objective**: Verify module-specific slides are generated correctly

**Prerequisites**:
- Presentation generator is initialized
- Module data is available
- Module overview template is defined

**Test Steps**:
1. Prepare sample module data
2. Call `generate_slide("module_overview", index, module_data)` for each slide
3. Verify content includes module-specific information
4. Check assessment criteria integration
5. Validate difficulty-appropriate content

**Expected Results**:
- Module title and description are included
- Difficulty level is properly indicated
- Hands-on status is correctly shown
- Assessment criteria match difficulty level
- Topics are listed appropriately

**Module Data Example**:
```python
{
  "title": "Programming with AI",
  "description": "Build AI-powered QA tools",
  "topics": ["Automation", "Chatbots"],
  "hands_on": True,
  "difficulty": "intermediate"
}
```

**Assessment Criteria Validation**:
- Beginner: 40% understanding, 40% application, 20% problem solving
- Intermediate: 30% understanding, 50% application, 20% problem solving
- Advanced: 25% understanding, 45% application, 30% problem solving

---

### TC-U010: Handle Invalid Template Requests
**Objective**: Verify proper error handling for invalid template types

**Prerequisites**:
- Presentation generator is initialized
- Invalid template name is used

**Test Steps**:
1. Call `generate_slide("nonexistent_template", 0)`
2. Verify appropriate error message is returned
3. Check that application doesn't crash
4. Validate error message is user-friendly

**Expected Results**:
- Returns "Template not found" message
- No exceptions are raised
- Application continues to function
- Error message is clear and helpful

---

### TC-U011: Handle Invalid Slide Index
**Objective**: Verify error handling for out-of-range slide indices

**Prerequisites**:
- Presentation generator is initialized
- Valid template with known slide count

**Test Steps**:
1. Call `generate_slide("introduction", 999)` with invalid index
2. Verify appropriate error message is returned
3. Check application stability
4. Test boundary conditions (negative numbers, zero)

**Expected Results**:
- Returns "Slide not found" message
- No exceptions or crashes occur
- Boundary conditions are handled properly
- Error messages are consistent

---

## Data Validation Test Cases

### TC-U012: Validate Module Configuration Structure
**Objective**: Verify module configuration data meets required standards

**Prerequisites**:
- Sample module configurations available
- Validation criteria defined

**Test Steps**:
1. Load module configuration data
2. Iterate through all modules
3. Validate required fields are present
4. Check data types and value constraints
5. Verify difficulty levels are valid

**Expected Results**:
- All modules have required fields (title, description, topics, hands_on, difficulty)
- Data types are correct (strings, lists, booleans)
- Difficulty values are from allowed set
- Topics lists are not empty
- Titles and descriptions have content

**Validation Rules**:
- `title`: non-empty string
- `description`: non-empty string  
- `topics`: non-empty list of strings
- `hands_on`: boolean
- `difficulty`: one of ["beginner", "intermediate", "advanced"]

---

### TC-U013: Validate User Progress Data Integrity
**Objective**: Verify user progress data maintains consistency and validity

**Prerequisites**:
- Sample user progress data
- Validation rules defined

**Test Steps**:
1. Load user progress data
2. Validate numeric fields are within valid ranges
3. Check list data structures
4. Verify preference data consistency
5. Validate session history format

**Expected Results**:
- Progress percentages are 0-100
- Module lists contain valid module IDs
- Preferences have valid values
- Session history has proper date formats
- Skills lists contain strings

**Validation Rules**:
- `current_progress`: 0 <= value <= 100
- `difficulty_level`: one of ["beginner", "intermediate", "advanced"]
- `focus_areas`: list of valid area names
- `hands_on_preference`: boolean
- Session dates: valid ISO date format

---

## Error Handling Test Cases

### TC-U014: Test Graceful Degradation
**Objective**: Verify application handles component failures gracefully

**Prerequisites**:
- Minimal or corrupted configuration
- Error simulation capabilities

**Test Steps**:
1. Create presentation generator with minimal config
2. Attempt to generate slides with missing templates
3. Verify graceful failure handling
4. Check that partial functionality remains

**Expected Results**:
- Application doesn't crash completely
- Appropriate error messages are returned
- Core functionality remains available
- User can recover from errors

---

### TC-U015: Test Memory Efficiency with Large Datasets
**Objective**: Verify application handles large configurations efficiently

**Prerequisites**:
- Large test configuration (50+ templates, 100+ slides each)
- Memory monitoring capabilities

**Test Steps**:
1. Create large configuration with many templates
2. Initialize presentation generator
3. Generate multiple slides
4. Monitor memory usage and performance
5. Verify acceptable performance limits

**Expected Results**:
- Initialization completes within 1 second
- Memory usage remains reasonable
- Slide generation is fast (< 0.1 seconds)
- No memory leaks or excessive growth

**Performance Benchmarks**:
- Configuration loading: < 1 second
- Slide generation: < 0.1 seconds
- Memory overhead: < 2x configuration size
- No memory leaks across multiple operations

---

## Integration Points Test Cases

### TC-U016: Test Assessment Criteria Integration
**Objective**: Verify assessment criteria are properly integrated in slides

**Prerequisites**:
- Assessment criteria defined for all difficulty levels
- Module data with various difficulties

**Test Steps**:
1. Generate assessment slides for each difficulty level
2. Verify correct percentages are displayed
3. Check that totals equal 100%
4. Validate content matches difficulty level

**Expected Results**:
- Correct assessment percentages for each difficulty
- Percentages sum to 100% for each level
- Content reflects appropriate difficulty expectations
- Assessment criteria are clearly presented

---

### TC-U017: Test Content Formatting Consistency
**Objective**: Verify all generated content follows consistent formatting rules

**Prerequisites**:
- Multiple slide types and templates
- Formatting standards defined

**Test Steps**:
1. Generate slides from different templates
2. Check markdown formatting consistency
3. Verify emoji usage patterns
4. Validate content structure standards

**Expected Results**:
- All slides start with proper markdown headers
- Consistent use of subheaders and lists
- Appropriate emoji usage for engagement
- Content length within acceptable ranges

**Formatting Standards**:
- Headers: Start with "# " for H1, "## " for H2
- Lists: Use "- " or "* " consistently
- Emojis: Include relevant emojis for visual appeal
- Length: 50-5000 characters per slide
- Structure: Logical flow and organization

---

## Test Data Requirements

### Configuration Test Data
- Valid complete configuration
- Minimal valid configuration
- Invalid JSON configurations
- Missing required sections
- Empty configurations

### Progress Test Data
- New user (no progress file)
- Beginner user progress
- Intermediate user progress
- Advanced user progress
- Corrupted progress data

### Module Test Data
- Beginner difficulty modules
- Intermediate difficulty modules
- Advanced difficulty modules
- Modules with/without hands-on
- Edge case module data

### Performance Test Data
- Large configurations (50+ templates)
- Many slides per template (100+)
- Long content strings
- Nested data structures
- Concurrent access scenarios

## Test Execution Guidelines

### Setup Requirements
1. Python test environment with pytest
2. Mock libraries for file system operations
3. Test data generation utilities
4. Coverage measurement tools

### Execution Commands
```bash
# Run all unit tests
pytest tests/unit/ -v

# Run specific test file
pytest tests/unit/test_app_core.py -v

# Run with coverage
pytest tests/unit/ --cov=app --cov-report=html

# Run specific test method
pytest tests/unit/test_app_core.py::TestConfigurationManagement::test_load_config_success -v
```

### Maintenance Guidelines
1. Update test data when application requirements change
2. Add new test cases for new functionality
3. Review and update error handling tests regularly
4. Maintain performance benchmarks
5. Keep test documentation current

This comprehensive unit test case documentation ensures thorough testing of all core components while providing clear guidance for test development and maintenance.
