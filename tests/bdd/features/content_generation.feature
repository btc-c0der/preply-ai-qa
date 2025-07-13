# Content Generation Features for AI-QA Portal
#
# This file contains BDD scenarios for testing the content generation
# functionality, including presentation slides, dynamic content adaptation,
# and personalization features.

Feature: Presentation Content Generation
  As a learner using the AI-QA Portal
  I want to receive high-quality, personalized content
  So that I can learn effectively at my skill level

  Background:
    Given the presentation generator is initialized
    And the module configuration is loaded
    And the assessment criteria are defined

  Scenario: Introduction Slide Generation
    Given I am requesting introduction slides
    When I generate the "Welcome to AI-Driven QA" slide
    Then the slide should contain a welcoming header
    And it should include an overview of benefits:
      | benefit                      |
      | Practical AI Integration     |
      | Hands-on Projects           |
      | Template-driven Learning    |
      | AI Tools and Techniques     |
    And it should include the learning approach description
    And it should use engaging visual elements like emojis

  Scenario: Module Overview Slide Generation for Different Difficulties
    Given I have modules with different difficulty levels
    When I generate module overview slides for "Best Practices with AI" (beginner)
    Then the "Assessment Criteria" slide should show:
      | criteria         | weight |
      | Understanding    | 40%    |
      | Application      | 40%    |
      | Problem Solving  | 20%    |

    When I generate module overview slides for "Programming with AI" (intermediate)
    Then the "Assessment Criteria" slide should show:
      | criteria         | weight |
      | Understanding    | 30%    |
      | Application      | 50%    |
      | Problem Solving  | 20%    |

    When I generate module overview slides for "QA + AI Integration" (advanced)
    Then the "Assessment Criteria" slide should show:
      | criteria         | weight |
      | Understanding    | 25%    |
      | Application      | 45%    |
      | Problem Solving  | 30%    |

  Scenario: Hands-on Session Content Generation
    Given I am generating hands-on session content
    When I create the "Setup and Prerequisites" slide
    Then it should include technical requirements:
      | requirement        | details              |
      | Python version     | 3.8+                |
      | Package manager    | pip                 |
      | Code editor        | VS Code, PyCharm    |
      | Terminal access    | Command line        |
    And it should include required packages installation commands
    And it should include API key setup instructions
    And it should include project structure guidelines

  Scenario: Dynamic Content Adaptation Based on Module Data
    Given I have a module with the following data:
      | field       | value                              |
      | title       | AI Test Case Generation           |
      | description | Learn to create intelligent tests  |
      | difficulty  | intermediate                       |
      | hands_on    | true                              |
      | topics      | Automation, LLM Integration       |

    When I generate the "Module Introduction" slide
    Then the slide should include the module title
    And it should include the module description
    And it should indicate "Intermediate" difficulty level
    And it should show "✅ Yes" for hands-on component
    And it should list the module topics

  Scenario: Error Handling in Content Generation
    Given the presentation generator is running
    When I request a slide with an invalid template type
    Then it should return "Template not found"
    And it should not crash the application

    When I request a slide with an invalid slide index
    Then it should return "Slide not found"
    And it should handle the error gracefully

    When I request a module overview slide without module data
    Then it should return "Module data not available"
    And it should provide a meaningful error message

Feature: Content Personalization
  As a learner with specific preferences
  I want content to be adapted to my learning style
  So that I can learn more effectively

  Scenario: Difficulty Level Content Adaptation
    Given I have set my difficulty preference to "beginner"
    When content is generated for me
    Then it should include beginner-friendly explanations
    And it should avoid overly technical jargon
    And it should provide more context and background information

    Given I have set my difficulty preference to "advanced"
    When content is generated for me
    Then it should include advanced technical details
    And it should assume prior knowledge
    And it should focus on complex scenarios and edge cases

  Scenario: Hands-on Preference Adaptation
    Given I have enabled hands-on learning preference
    When I view module content
    Then it should emphasize practical exercises
    And it should include interactive code examples
    And it should provide project-based learning opportunities

    Given I have disabled hands-on learning preference
    When I view module content
    Then it should focus more on theoretical concepts
    And it should provide comprehensive explanations
    And it should include case studies instead of coding exercises

  Scenario: Focus Area Content Customization
    Given I have selected "automation" as a focus area
    When I view content across modules
    Then automation-related topics should be highlighted
    And examples should focus on automation scenarios
    And related projects should emphasize automation tools

    Given I have selected "ai_integration" as a focus area
    When I view content across modules
    Then AI integration concepts should be emphasized
    And examples should show AI tool integration
    And projects should focus on AI-powered solutions

Feature: Content Quality and Consistency
  As a content reviewer
  I want all generated content to meet quality standards
  So that learners receive consistent, high-quality education

  Scenario: Content Length Validation
    Given I am generating slides for any module
    When a slide is created
    Then it should have substantial content (at least 50 characters)
    And it should not be excessively long (no more than 5000 characters)
    And it should be appropriate for a presentation slide format

  Scenario: Markdown Formatting Consistency
    Given I am generating any type of slide
    When the slide content is created
    Then it should start with a proper markdown header (#)
    And it should use consistent subheader formatting (##)
    And it should use proper list formatting (- or *)
    And it should include appropriate emoji usage for engagement

  Scenario: Content Uniqueness Validation
    Given I am generating multiple slides for a template
    When I create slides for the same template
    Then each slide should have unique content
    And the content should be appropriate for each slide's purpose
    And there should be no duplicate slide content

  Scenario: Educational Content Standards
    Given I am generating educational content
    When any slide is created
    Then it should have clear learning objectives
    And it should include practical examples when appropriate
    And it should use accessible language for the target audience
    And it should follow adult learning principles

Feature: Multi-language and Accessibility Support
  As an international learner
  I want content to be accessible and inclusive
  So that I can learn regardless of my location or abilities

  Scenario: Content Structure for Screen Readers
    Given I am generating accessible content
    When slides are created
    Then they should have proper heading hierarchy
    And they should include descriptive text for visual elements
    And they should have logical reading order
    And they should avoid relying solely on visual formatting

  Scenario: Content Clarity and Readability
    Given I am generating content for diverse audiences
    When slide content is created
    Then it should use clear, simple language
    And it should avoid unnecessary jargon
    And it should include definitions for technical terms
    And it should have good contrast between text and background

  Scenario: Cultural Sensitivity in Examples
    Given I am generating content with examples
    When examples are included in slides
    Then they should be culturally neutral
    And they should represent diverse scenarios
    And they should avoid cultural assumptions
    And they should be inclusive of different backgrounds

Feature: Performance and Scalability
  As a system administrator
  I want content generation to be efficient and scalable
  So that the system can handle multiple users and large amounts of content

  Scenario: Large Configuration Handling
    Given I have a configuration with 50 presentation templates
    And each template has 100 slides
    When the presentation generator is initialized
    Then it should load the configuration without performance issues
    And it should be able to generate any slide efficiently
    And memory usage should remain reasonable

  Scenario: Concurrent Content Generation
    Given multiple users are requesting content simultaneously
    When 10 users request slide generation at the same time
    Then all requests should be processed successfully
    And response times should remain acceptable (under 2 seconds)
    And the system should not experience performance degradation

  Scenario: Content Caching and Optimization
    Given frequently requested content exists
    When the same slide is requested multiple times
    Then the system should optimize for repeated requests
    And response times should improve for cached content
    And memory usage should be optimized for frequent access patterns
