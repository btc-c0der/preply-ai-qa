Feature: Basic User Journey
  As a learner using the AI-QA Portal
  I want to navigate through the learning platform
  So that I can acquire new AI-QA skills effectively

  Background:
    Given the AI-QA Portal is running
    And the module configuration is loaded
    And user progress data is available

  Scenario: New User First Visit
    Given I am a new user visiting the portal for the first time
    When I access the portal homepage
    Then I should see the welcome screen
    And I should see available learning modules
    And I should see my progress dashboard

  Scenario: Module Selection and Start
    Given I have selected a module to study
    When I click on "Start Module"
    Then I should see the module introduction slide
    And I should see navigation controls
    And my progress should be updated
