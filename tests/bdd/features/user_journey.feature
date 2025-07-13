# User Journey Features for AI-QA Portal
# 
# This file contains behavior-driven development (BDD) scenarios
# for the AI-QA Portal user journeys using Gherkin syntax.
#
# These scenarios test the complete user experience from
# registration through module completion and certification.

Feature: User Learning Journey
  As a QA professional interested in AI
  I want to learn AI-driven quality assurance techniques
  So that I can enhance my career and improve testing efficiency

  Background:
    Given the AI-QA Portal is running
    And the module configuration is loaded
    And the user progress system is initialized

  Scenario: New User Registration and Onboarding
    Given I am a new user visiting the portal
    When I access the dashboard for the first time
    Then I should see a welcome message
    And I should see an overview of available modules
    And I should see personalization options
    And my default progress should be initialized

    When I set my preferences:
      | field                | value        |
      | difficulty_level     | intermediate |
      | hands_on_preference  | true         |
      | focus_areas          | automation   |
    Then my preferences should be saved
    And the module recommendations should update based on my preferences

  Scenario: Module Selection and Navigation
    Given I am logged into the portal
    And I have set my preferences to "intermediate" difficulty
    When I view the available modules
    Then I should see modules marked with difficulty levels
    And I should see "Best Practices with AI" marked as "beginner"
    And I should see "Programming with AI" marked as "intermediate"
    And I should see "QA + AI Integration" marked as "advanced"

    When I select the "Best Practices with AI" module
    Then I should be taken to the module overview
    And I should see the module description
    And I should see the learning objectives
    And I should see the estimated duration
    And the module should be marked as "in progress" in my profile

  Scenario: Presentation Slide Navigation
    Given I have selected the "Best Practices with AI" module
    And I am viewing the module presentation
    When I navigate through the presentation slides
    Then I should see the "Module Introduction" slide first
    And I should be able to navigate to the "Learning Objectives" slide
    And I should be able to navigate to the "Key Topics" slide
    And I should be able to navigate to the "Hands-on Activities" slide
    And I should be able to navigate to the "Assessment Criteria" slide

    And my progress should update as I complete each slide:
      | slide_number | expected_progress |
      | 1           | 20%              |
      | 2           | 40%              |
      | 3           | 60%              |
      | 4           | 80%              |
      | 5           | 100%             |

  Scenario: Hands-on Lab Completion
    Given I have completed the presentation slides for "Programming with AI"
    And the module has hands-on activities enabled
    When I access the hands-on lab section
    Then I should see the lab setup instructions
    And I should see the step-by-step implementation guide
    And I should see code examples and templates

    When I complete the hands-on project:
      | project_component    | status    |
      | Environment Setup    | completed |
      | Core Implementation  | completed |
      | Testing & Validation | completed |
      | Documentation        | completed |
    Then the project should be marked as completed
    And it should be added to my portfolio
    And my skills should be updated with the relevant technologies

  Scenario: Module Assessment and Completion
    Given I have completed all slides and hands-on activities for "Best Practices with AI"
    When I take the module assessment
    Then I should see questions appropriate for "beginner" difficulty level
    And the assessment should cover:
      | assessment_area  | weight |
      | Understanding    | 40%    |
      | Application      | 40%    |
      | Problem Solving  | 20%    |

    When I submit my assessment with passing scores
    Then the module should be marked as "completed"
    And my overall progress should increase
    And I should earn the module completion certificate
    And the skills from this module should be added to my profile
    And I should see recommendations for the next module

  Scenario: Progress Tracking and Analytics
    Given I have completed "Best Practices with AI" module
    And I am currently working on "Programming with AI" module
    When I view my progress dashboard
    Then I should see my overall completion percentage
    And I should see a list of completed modules
    And I should see my current module with progress indicator
    And I should see my acquired skills list
    And I should see my learning time statistics

    And the dashboard should display:
      | metric                  | expected_value |
      | Modules Completed       | 1              |
      | Current Module Progress | 45%            |
      | Skills Acquired         | 4              |
      | Total Study Time        | 180 minutes    |
      | Learning Streak         | 5 days         |

  Scenario: Bookmark and Note Management
    Given I am viewing a presentation slide
    When I click the bookmark button
    Then the slide should be added to my bookmarks
    And I should see a confirmation message

    When I add a note to the current slide:
      """
      This is important for prompt engineering in QA automation.
      Remember to use specific context and examples.
      """
    Then the note should be saved
    And I should be able to access it from my notes section

    When I view my bookmarks and notes
    Then I should see all bookmarked slides organized by module
    And I should see all notes with timestamps and context
    And I should be able to search through my notes

  Scenario: Learning Path Progression
    Given I have completed beginner modules:
      | module                |
      | Best Practices with AI |
      | Essential AI Concepts  |
    When I view my learning path recommendations
    Then I should see intermediate modules recommended:
      | module                  | reason                    |
      | Programming with AI     | Matches skill progression |
      | AI Compliance & Governance | Builds on best practices  |

    And advanced modules should show prerequisites:
      | module              | prerequisite_status |
      | QA + AI Integration | Locked - Need 2 more modules |
      | Knowledge Bases     | Locked - Need programming skills |

Feature: Presentation Generation and Display
  As a learner using the portal
  I want to view well-structured presentations
  So that I can learn effectively and track my progress

  Scenario: Introduction Presentation Generation
    Given I am viewing the portal introduction
    When the introduction presentation loads
    Then I should see a "Welcome to AI-Driven QA" slide
    And the slide should contain:
      | element                    | content_type |
      | Welcome message            | text         |
      | Key benefits               | bullet_list  |
      | Learning approach overview | text         |
      | Visual elements            | emojis       |

    When I navigate to the "Your Learning Journey" slide
    Then I should see personalized content based on my preferences
    And I should see the available learning paths
    And I should see module difficulty indicators

  Scenario: Module-Specific Presentation Generation
    Given I have selected the "QA + AI Integration" module
    When the module presentation loads
    Then the "Module Introduction" slide should contain:
      | element              | expected_content                    |
      | Module title         | QA + AI Integration                 |
      | Difficulty indicator | Advanced                            |
      | Hands-on indicator   | Yes                                 |
      | Prerequisites        | Basic understanding of QA processes |

    And the "Learning Objectives" slide should show advanced-level objectives
    And the "Assessment Criteria" slide should reflect advanced weightings:
      | criteria         | weight |
      | Understanding    | 25%    |
      | Application      | 45%    |
      | Problem Solving  | 30%    |

  Scenario: Hands-on Session Presentation
    Given I am in a hands-on session for "Programming with AI"
    When I view the hands-on presentation slides
    Then I should see the "Setup and Prerequisites" slide with:
      | section              | content                        |
      | Technical requirements | Python 3.8+, pip, code editor |
      | Required packages     | gradio, openai, langchain      |
      | API keys             | OpenAI, Hugging Face           |
      | Project structure    | Folder organization guide     |

    When I navigate to the "Step-by-Step Implementation" slide
    Then I should see code examples
    And I should see implementation steps with time estimates
    And I should see the project we'll be building

Feature: Error Handling and Edge Cases
  As a user of the portal
  I want the system to handle errors gracefully
  So that I can continue learning even when issues occur

  Scenario: Network Connectivity Issues
    Given I am working through a module presentation
    When the network connection is interrupted
    Then I should see an appropriate error message
    And my current progress should be saved locally
    And I should be able to continue viewing cached content

    When the network connection is restored
    Then my progress should sync automatically
    And I should be notified of successful synchronization

  Scenario: Invalid Module Access
    Given I am a beginner user
    When I attempt to access an advanced module directly
    Then I should see a prerequisites warning
    And I should be redirected to recommended beginner modules
    And I should see my current learning path

  Scenario: Corrupted Progress Data Recovery
    Given my progress data becomes corrupted
    When I access the portal
    Then the system should detect the corruption
    And it should restore from the last valid backup
    And I should be notified about the recovery
    And I should not lose significant progress

Feature: Accessibility and Responsive Design
  As a user with accessibility needs
  I want the portal to be fully accessible
  So that I can learn effectively regardless of my abilities

  Scenario: Screen Reader Compatibility
    Given I am using a screen reader
    When I navigate through the portal
    Then all images should have descriptive alt text
    And all buttons should have clear labels
    And the navigation structure should be logical
    And content should be properly structured with headings

  Scenario: Keyboard Navigation
    Given I am navigating using only keyboard
    When I use tab to move through elements
    Then all interactive elements should be focusable
    And the focus order should be logical
    And I should be able to activate all buttons with Enter or Space
    And I should be able to navigate slides with arrow keys

  Scenario: Mobile Device Adaptation
    Given I am accessing the portal on a mobile device
    When I view the dashboard
    Then the layout should adapt to mobile screen size
    And text should be readable without zooming
    And buttons should be large enough for touch interaction
    And navigation should be optimized for mobile usage

    When I view presentations on mobile
    Then slides should be formatted for mobile viewing
    And I should be able to navigate with touch gestures
    And the progress indicator should remain visible
