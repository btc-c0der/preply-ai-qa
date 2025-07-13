Feature: Basic Content Generation
  As a content management system
  I want to generate presentation slides dynamically
  So that learners receive contextual and relevant content

  Background:
    Given the presentation system is initialized
    And module configuration data is available

  Scenario: Generate Introduction Slide
    Given I want to generate an introduction slide
    When I request slide generation with no specific module
    Then I should receive a general introduction slide
    And the slide should contain welcome information
    And the slide should be properly formatted in Markdown

  Scenario: Generate Module Overview Slide
    Given I have a specific module selected
    When I request a module overview slide
    Then I should receive a slide with module-specific content
    And the slide should include learning objectives
    And the slide should include module topics
