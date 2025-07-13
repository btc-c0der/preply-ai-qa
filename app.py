import gradio as gr
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Union
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Load configuration
def load_config():
    with open('module_config.json', 'r') as f:
        return json.load(f)

def load_user_progress():
    try:
        with open('user_progress.json', 'r') as f:
            return json.load(f)
    except:
        return {
            "current_module": None,
            "completed_modules": [],
            "current_progress": 0,
            "skills_acquired": [],
            "assessments_completed": [],
            "hands_on_projects": [],
            "learning_path": "custom",
            "preferences": {
                "difficulty_level": "intermediate",
                "focus_areas": [],
                "hands_on_preference": True
            },
            "session_history": [],
            "bookmarks": [],
            "notes": {}
        }

def save_user_progress(progress_data):
    with open('user_progress.json', 'w') as f:
        json.dump(progress_data, f, indent=2)

# Initialize data
config = load_config()
user_progress = load_user_progress()

class PresentationGenerator:
    def __init__(self, config):
        self.config = config
        self.templates = config['presentation_templates']
    
    def generate_slide(self, template_type: str, slide_index: int, module_data: Optional[Dict] = None):
        """Generate a slide based on template and module data"""
        if template_type not in self.templates:
            return "Template not found"
        
        slides = self.templates[template_type]['slides']
        if slide_index >= len(slides):
            return "Slide not found"
        
        slide_title = slides[slide_index]
        
        # Generate content based on slide type and module
        if template_type == "introduction":
            return self.generate_introduction_slide(slide_title, slide_index)
        elif template_type == "module_overview":
            return self.generate_module_overview_slide(slide_title, slide_index, module_data)
        elif template_type == "hands_on_session":
            return self.generate_hands_on_slide(slide_title, slide_index, module_data)
        elif template_type == "conclusion":
            return self.generate_conclusion_slide(slide_title, slide_index)
        
        return f"# {slide_title}\n\nContent for this slide type is being developed..."
    
    def generate_introduction_slide(self, title: str, index: int):
        content = {
            0: f"""# 🚀 {title}
            
Welcome to the **AI-Driven Quality Assurance Professional Development Portal**!

## What You'll Experience:
- 🎯 **Practical AI Integration** in QA workflows
- 🛠️ **Hands-on Projects** with real-world applications
- 📊 **Template-driven Learning** with structured presentations
- 🤖 **AI Tools and Techniques** specific to QA professionals

## Our Approach:
- **Theory + Practice**: Balance conceptual understanding with practical implementation
- **Personalized Learning**: Adapt to your experience level and interests
- **Community Focus**: Connect with fellow QA professionals exploring AI

Ready to transform your QA practice with AI? Let's begin! 🌟""",
            
            1: f"""# 📚 {title}
            
## Your Personalized Learning Path

### 🎯 Core Modules Available:
1. **Programming/Building Projects with AI** - Build automation tools and chatbots
2. **Best Practices with AI** - Learn effective and safe AI usage
3. **QA + AI Integration** - Advanced testing process automation
4. **Knowledge Bases with AI** - Create intelligent QA assistants
5. **AI Compliance & Governance** - Ethical and legal frameworks
6. **Essential AI Concepts** - MCP, RAG, Fine-Tuning basics

### 🛤️ Learning Paths:
- **Beginner**: Start with AI fundamentals and best practices
- **Intermediate**: Focus on practical integration and tools
- **Advanced**: Deep dive into custom solutions and governance

### 📊 Progress Tracking:
- Real-time progress monitoring
- Skill acquisition tracking
- Hands-on project portfolio
- Personalized recommendations""",
            
            2: f"""# 🛠️ {title}
            
## Essential Tools & Platforms

### 🤖 AI Platforms:
- **OpenAI GPT Models** - For text generation and analysis
- **Langchain** - For building AI applications
- **Vector Databases** - ChromaDB, FAISS for knowledge bases
- **Gradio** - For creating interactive interfaces

### 🔧 QA-Specific Tools:
- **Test Automation Frameworks** - Selenium, Playwright integration
- **API Testing** - Postman, REST Assured with AI enhancement
- **Performance Testing** - JMeter with AI-driven analysis
- **Bug Tracking** - Jira integration with AI insights

### 📚 Resources:
- **Documentation** - Interactive guides and tutorials
- **Code Repositories** - GitHub templates and examples
- **Community Forums** - Peer support and knowledge sharing
- **Certification Paths** - Industry-recognized credentials

### 🔐 Setup Requirements:
- Python 3.8+ environment
- API keys for AI services
- Development tools installation
- Access to testing environments""",
            
            3: f"""# 🎯 {title}
            
## What You'll Achieve

### 🚀 Immediate Outcomes:
- **Automate repetitive QA tasks** using AI tools
- **Generate intelligent test cases** from requirements
- **Analyze bugs and failures** with AI assistance
- **Create custom QA chatbots** for your team

### 🎓 Skill Development:
- **Prompt Engineering** for QA-specific tasks
- **AI Model Integration** in testing workflows
- **Knowledge Base Creation** for QA documentation
- **Compliance Understanding** for AI in enterprise

### 📈 Career Advancement:
- **Enhanced Productivity** - Automate routine tasks
- **Strategic Value** - Become an AI-savvy QA professional
- **Innovation Leadership** - Drive AI adoption in your organization
- **Continuous Learning** - Stay ahead of industry trends

### 🌟 Long-term Impact:
- Transform from traditional QA to AI-enhanced QA
- Lead digital transformation initiatives
- Mentor others in AI adoption
- Contribute to the future of quality assurance

**Ready to start your AI-QA journey?** 🚀"""
        }
        
        return content.get(index, f"# {title}\n\nContent coming soon...")
    
    def generate_module_overview_slide(self, title: str, index: int, module_data: Optional[Dict]):
        if not module_data:
            return f"# {title}\n\nModule data not available"
        
        content = {
            0: f"""# 📖 {title}: {module_data.get('title', 'Module')}
            
## Module Overview
{module_data.get('description', 'No description available')}

### 🎯 Target Audience:
- **Difficulty Level**: {module_data.get('difficulty', 'Not specified').title()}
- **Hands-on Component**: {'✅ Yes' if module_data.get('hands_on', False) else '❌ No'}
- **Prerequisites**: Basic understanding of QA processes

### 📊 Module Structure:
- **Duration**: 2-4 hours (flexible pacing)
- **Format**: Interactive presentations + practical exercises
- **Assessment**: Hands-on projects and knowledge checks
- **Certification**: Module completion certificate

### 🔧 What You'll Need:
- Python development environment
- Access to AI APIs (OpenAI, etc.)
- Basic command line familiarity
- Willingness to experiment and learn!""",
            
            1: f"""# 🎯 {title}
            
## Learning Objectives

By the end of this module, you will be able to:

### 📚 Understand:
- Core concepts and terminology
- Real-world applications in QA
- Benefits and limitations
- Best practices and common pitfalls

### 🛠️ Apply:
- Practical implementation techniques
- Integration with existing workflows
- Troubleshooting and optimization
- Quality assurance principles

### 🚀 Create:
- Custom solutions for your QA needs
- Automated testing enhancements
- AI-powered QA tools
- Documentation and knowledge sharing

### 🔍 Evaluate:
- Effectiveness of AI solutions
- Quality metrics and KPIs
- Risk assessment and mitigation
- Continuous improvement strategies

*These objectives align with industry standards and career advancement requirements.*""",
            
            2: f"""# 📋 {title}
            
## Key Topics Covered

### 🔍 Deep Dive Topics:
""" + "\n".join([f"- **{topic}**" for topic in module_data.get('topics', [])]) + f"""

### 🎯 Focus Areas:
- **Theoretical Foundation**: Understanding core concepts
- **Practical Application**: Real-world implementation
- **Industry Standards**: Best practices and compliance
- **Future Trends**: Emerging technologies and approaches

### 📊 Content Structure:
1. **Introduction & Context** (15 minutes)
2. **Core Concepts** (30 minutes)
3. **Hands-on Practice** (60 minutes)
4. **Advanced Techniques** (30 minutes)
5. **Assessment & Review** (15 minutes)

### 🔗 Integration Points:
- Connection to other modules
- Cross-functional applications
- Industry use cases
- Career development paths

*Each topic includes practical examples and real-world case studies.*""",
            
            3: f"""# 🛠️ {title}
            
## Hands-on Activities

### 🎮 Interactive Exercises:
- **Live Coding Sessions** - Build AI tools together
- **Problem-Solving Challenges** - Real QA scenarios
- **Peer Collaboration** - Group projects and discussions
- **Tool Exploration** - Hands-on with latest AI platforms

### 🔨 Practical Projects:
1. **Mini-Project**: Quick implementation (30 minutes)
2. **Main Project**: Comprehensive solution (90 minutes)
3. **Extension Challenge**: Advanced features (optional)

### 🎯 Learning Methodologies:
- **Learning by Doing**: Immediate application
- **Guided Discovery**: Structured exploration
- **Peer Learning**: Collaborative problem-solving
- **Reflection**: Understanding and improvement

### 📱 Tools & Resources:
- **Interactive Notebooks** - Jupyter/Colab environments
- **Code Repositories** - GitHub templates and examples
- **Testing Environments** - Safe spaces to experiment
- **Documentation** - Step-by-step guides

*All activities are designed for practical application in your work environment.*""",
            
            4: f"""# 📊 {title}
            
## Assessment Criteria

### 🎯 Evaluation Framework:
Based on difficulty level: **{module_data.get('difficulty', 'intermediate').title()}**

### 📈 Assessment Components:
- **Understanding** ({config['assessment_criteria'][module_data.get('difficulty', 'intermediate')]['understanding']}%): Conceptual grasp
- **Application** ({config['assessment_criteria'][module_data.get('difficulty', 'intermediate')]['application']}%): Practical implementation
- **Problem Solving** ({config['assessment_criteria'][module_data.get('difficulty', 'intermediate')]['problem_solving']}%): Critical thinking

### ✅ Success Indicators:
- **Completion of hands-on projects**
- **Demonstration of key concepts**
- **Ability to adapt solutions**
- **Quality of implementation**

### 🏆 Recognition:
- **Module Completion Certificate**
- **Skill Badges** for specific competencies
- **Portfolio Projects** for career advancement
- **Peer Recognition** through community contributions

### 🔄 Continuous Improvement:
- Regular feedback collection
- Performance analytics
- Personalized recommendations
- Adaptive learning paths

*Assessment is designed to be supportive and growth-oriented.*"""
        }
        
        return content.get(index, f"# {title}\n\nContent coming soon...")
    
    def generate_hands_on_slide(self, title: str, index: int, module_data: Optional[Dict]):
        content = {
            0: f"""# 🚀 {title}
            
## Setup and Prerequisites

### 🔧 Technical Requirements:
- **Python 3.8+** installed on your system
- **pip** package manager
- **Code editor** (VS Code, PyCharm, or similar)
- **Terminal/Command line** access

### 📦 Required Packages:
```bash
pip install gradio openai langchain chromadb pandas numpy matplotlib
```

### 🔑 API Keys & Access:
- **OpenAI API Key** - For GPT models
- **Hugging Face Token** - For open-source models
- **Database Access** - For knowledge bases
- **Testing Environment** - Sandbox for experiments

### 📁 Project Structure:
```
ai-qa-project/
├── src/
├── data/
├── tests/
├── config/
└── notebooks/
```

### ✅ Verification Steps:
1. Run `python --version` (should be 3.8+)
2. Test package imports
3. Verify API connectivity
4. Check project structure

*Don't worry if you encounter issues - we'll troubleshoot together!*""",
            
            1: f"""# 👨‍💻 {title}
            
## Step-by-Step Implementation

### 🎯 Today's Project:
Building an **AI-Powered Test Case Generator**

### 📋 Implementation Steps:

#### Step 1: Environment Setup (5 minutes)
```python
import openai
import gradio as gr
import json
from datetime import datetime
```

#### Step 2: Core Function Development (20 minutes)
- Create the test case generation function
- Implement prompt engineering for QA
- Add validation and error handling

#### Step 3: Gradio Interface (15 minutes)
- Design user-friendly input forms
- Create output display components
- Add interactive elements

#### Step 4: Integration & Testing (10 minutes)
- Connect components
- Test with sample data
- Refine based on results

### 🔄 Iterative Development:
- **Build** → **Test** → **Refine** → **Repeat**
- Real-time feedback and improvements
- Collaborative problem-solving

*We'll code together, step by step!*""",
            
            2: f"""# ⚠️ {title}
            
## Common Challenges

### 🐛 Technical Issues:
- **API Rate Limits**: Implement proper throttling
- **Token Limits**: Optimize prompt length
- **Network Connectivity**: Add retry mechanisms
- **Package Conflicts**: Use virtual environments

### 🤔 Conceptual Challenges:
- **Prompt Engineering**: Crafting effective prompts
- **Model Selection**: Choosing the right AI model
- **Quality Validation**: Ensuring output quality
- **Integration Complexity**: Connecting with existing tools

### 💡 Solutions & Workarounds:
- **Error Handling**: Graceful failure management
- **Fallback Strategies**: Alternative approaches
- **Performance Optimization**: Efficient processing
- **User Experience**: Intuitive interfaces

### 🔧 Troubleshooting Tips:
1. **Check logs** for detailed error messages
2. **Test incrementally** - small steps
3. **Use debugging tools** - print statements, debuggers
4. **Seek help** - community support available

### 📚 Resources:
- **Documentation**: Official guides and tutorials
- **Stack Overflow**: Community Q&A
- **GitHub Issues**: Known problems and solutions
- **Office Hours**: Direct support sessions

*Remember: Every expert was once a beginner!*""",
            
            3: f"""# 🌟 {title}
            
## Best Practices

### 🎯 Development Principles:
- **Start Simple**: Begin with basic functionality
- **Iterate Quickly**: Rapid prototyping and testing
- **Document Everything**: Clear code and process documentation
- **Test Thoroughly**: Validate all components

### 🔒 Security & Compliance:
- **API Key Management**: Secure storage and rotation
- **Data Privacy**: Protect sensitive information
- **Access Controls**: Implement proper permissions
- **Audit Trails**: Track all activities

### 📊 Quality Assurance:
- **Code Reviews**: Peer validation
- **Automated Testing**: Unit and integration tests
- **Performance Monitoring**: Track system metrics
- **User Feedback**: Continuous improvement

### 🚀 Performance Optimization:
- **Efficient Algorithms**: Choose optimal approaches
- **Caching Strategies**: Reduce redundant processing
- **Async Processing**: Handle concurrent requests
- **Resource Management**: Optimize memory and CPU usage

### 🤝 Collaboration:
- **Version Control**: Git best practices
- **Documentation**: Clear and comprehensive
- **Knowledge Sharing**: Team learning sessions
- **Mentorship**: Support junior developers

*These practices ensure sustainable, scalable solutions.*""",
            
            4: f"""# 🔮 {title}
            
## Next Steps

### 🎯 Immediate Actions:
- **Complete the current project**
- **Test in your environment**
- **Document your learnings**
- **Share with your team**

### 📈 Skill Development:
- **Advanced Prompt Engineering**
- **Custom Model Training**
- **API Integration Mastery**
- **Performance Optimization**

### 🌐 Community Engagement:
- **Join AI-QA Forums**
- **Contribute to Open Source**
- **Attend Conferences**
- **Network with Peers**

### 🔄 Continuous Learning:
- **Follow Industry Trends**
- **Experiment with New Tools**
- **Practice Regularly**
- **Seek Feedback**

### 🏆 Career Advancement:
- **Build Portfolio Projects**
- **Obtain Certifications**
- **Lead AI Initiatives**
- **Mentor Others**

### 📚 Recommended Resources:
- **Books**: "AI for Quality Assurance"
- **Courses**: Advanced AI specializations
- **Blogs**: Industry thought leaders
- **Podcasts**: AI in testing discussions

*Your AI-QA journey is just beginning!*"""
        }
        
        return content.get(index, f"# {title}\n\nContent coming soon...")
    
    def generate_conclusion_slide(self, title: str, index: int):
        content = {
            0: f"""# 🎉 {title}
            
## What You've Accomplished

### 🏆 Skills Acquired:
- **AI Integration** in QA workflows
- **Prompt Engineering** for testing scenarios
- **Tool Development** using modern frameworks
- **Problem-Solving** with AI assistance

### 🛠️ Practical Outcomes:
- **Automated Test Generation** tools
- **AI-Enhanced Bug Analysis** systems
- **Custom QA Chatbots** for team support
- **Knowledge Base** creation and management

### 📊 Measurable Impact:
- **Efficiency Gains**: 40-60% reduction in manual effort
- **Quality Improvement**: Enhanced test coverage
- **Innovation**: New approaches to QA challenges
- **Career Growth**: Expanded skill set and opportunities

### 🌟 Personal Growth:
- **Confidence**: Working with AI technologies
- **Creativity**: Innovative problem-solving approaches
- **Leadership**: Driving AI adoption in QA
- **Adaptability**: Embracing technological change

### 🔮 Future Readiness:
- **Emerging Technologies**: Prepared for AI evolution
- **Industry Trends**: Understanding of QA direction
- **Continuous Learning**: Foundation for ongoing development
- **Professional Network**: Connections with AI-QA community

*You're now equipped to lead AI transformation in QA!*""",
            
            1: f"""# 📚 {title}
            
## Further Resources

### 📖 Essential Reading:
- **"AI-Powered Testing"** by Tariq King
- **"The Art of Prompt Engineering"** by Various Authors
- **"Quality Assurance in the AI Era"** by Industry Experts
- **"Automation Testing with AI"** by Practical Guides

### 🌐 Online Resources:
- **AI Testing Handbook** - Comprehensive guide
- **OpenAI Documentation** - API references and examples
- **Gradio Documentation** - Interface development
- **Langchain Tutorials** - AI application building

### 🎥 Video Content:
- **YouTube Channels**: AI testing specialists
- **Webinar Series**: Industry expert sessions
- **Conference Talks**: Latest trends and techniques
- **Tutorial Playlists**: Step-by-step implementations

### 🔧 Tools & Platforms:
- **GitHub Repositories**: Open-source projects
- **Hugging Face Hub**: Pre-trained models
- **Kaggle Datasets**: Training data for AI models
- **Google Colab**: Free computing resources

### 📧 Newsletters & Updates:
- **AI Testing Weekly** - Latest news and trends
- **QA Innovation** - Industry developments
- **Tech Updates** - Tool and platform updates
- **Community Digest** - Peer insights and discussions

*Stay connected with the rapidly evolving AI-QA landscape!*""",
            
            2: f"""# 🤝 {title}
            
## Community and Support

### 🌐 Online Communities:
- **AI-QA Professionals Group** - LinkedIn community
- **Reddit r/QualityAssurance** - Peer discussions
- **Stack Overflow** - Technical Q&A
- **Discord Servers** - Real-time chat support

### 📱 Social Media:
- **Twitter/X**: Follow AI-QA thought leaders
- **LinkedIn**: Professional networking
- **YouTube**: Educational content creators
- **Medium**: Technical articles and insights

### 🏢 Professional Organizations:
- **Association for Software Testing (AST)**
- **International Software Testing Qualifications Board (ISTQB)**
- **AI Testing Institute** - Specialized certification
- **Local QA Meetups** - In-person networking

### 🎓 Mentorship Opportunities:
- **Industry Mentors** - Experienced professionals
- **Peer Mentoring** - Learning together
- **Reverse Mentoring** - Sharing AI knowledge
- **Community Leaders** - Guidance and support

### 📞 Direct Support:
- **Office Hours** - Weekly Q&A sessions
- **Email Support** - Technical assistance
- **Discussion Forums** - Community help
- **Private Consulting** - Personalized guidance

### 🎯 Contributing Back:
- **Open Source Projects** - Code contributions
- **Knowledge Sharing** - Blog posts and tutorials
- **Community Moderation** - Supporting others
- **Conference Speaking** - Sharing experiences

*Together, we're building the future of AI-enhanced QA!*""",
            
            3: f"""# 🎓 {title}
            
## Certification Path

### 🏆 Available Certifications:

#### 📋 Foundation Level:
- **AI-QA Fundamentals** - Basic concepts and applications
- **Prompt Engineering for QA** - Effective AI communication
- **Duration**: 4-6 weeks
- **Prerequisites**: Basic QA knowledge

#### 🔧 Practitioner Level:
- **AI Test Automation Specialist** - Advanced automation
- **QA AI Integration Expert** - Workflow optimization
- **Duration**: 8-12 weeks
- **Prerequisites**: Foundation certification

#### 🚀 Expert Level:
- **AI-QA Solution Architect** - Enterprise-level design
- **Innovation Leader** - Driving AI transformation
- **Duration**: 12-16 weeks
- **Prerequisites**: Practitioner certification

### 📊 Assessment Format:
- **Practical Projects** (60%) - Real-world implementations
- **Written Examination** (25%) - Theoretical knowledge
- **Peer Review** (15%) - Community evaluation

### 🎯 Industry Recognition:
- **Employer Validation** - Recognized by top companies
- **Career Advancement** - Promotion opportunities
- **Salary Impact** - 15-30% increase potential
- **Global Acceptance** - International recognition

### 🔄 Continuous Certification:
- **Annual Renewal** - Stay current with trends
- **Continuing Education** - Ongoing learning requirements
- **Professional Development** - Skill maintenance
- **Community Contribution** - Give back to the field

*Your certification journey starts here!*"""
        }
        
        return content.get(index, f"# {title}\n\nContent coming soon...")

# Initialize presentation generator
presentation_gen = PresentationGenerator(config)

def get_module_list():
    """Return list of available modules"""
    return [(module_id, module_data['title']) for module_id, module_data in config['modules'].items()]

def generate_presentation_slide(module_id, template_type, slide_index):
    """Generate a presentation slide"""
    module_data = config['modules'].get(module_id, {}) if module_id else None
    slide_content = presentation_gen.generate_slide(template_type, slide_index, module_data)
    return slide_content

def get_progress_chart():
    """Generate progress visualization"""
    modules = list(config['modules'].keys())
    completed = user_progress.get('completed_modules', [])
    progress_data = [1 if module in completed else 0 for module in modules]
    
    fig = go.Figure(data=[
        go.Bar(
            x=[config['modules'][m]['title'] for m in modules],
            y=progress_data,
            marker_color=['green' if p else 'lightgray' for p in progress_data]
        )
    ])
    
    fig.update_layout(
        title='Learning Progress',
        xaxis_title='Modules',
        yaxis_title='Completion Status',
        yaxis=dict(range=[0, 1])
    )
    
    return fig

def get_skills_radar():
    """Generate skills radar chart"""
    skills = ['AI Integration', 'Prompt Engineering', 'Automation', 'Analysis', 'Innovation']
    # Mock data - in real implementation, this would come from assessments
    values = [0.8, 0.6, 0.9, 0.7, 0.5]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=skills,
        fill='toself',
        name='Current Skills'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=True,
        title='Skills Assessment'
    )
    
    return fig

def update_user_progress(module_id, action):
    """Update user progress"""
    global user_progress
    
    if action == "complete":
        if module_id not in user_progress['completed_modules']:
            user_progress['completed_modules'].append(module_id)
            user_progress['current_progress'] = len(user_progress['completed_modules']) / len(config['modules']) * 100
            
            # Add skills from completed module
            module_data = config['modules'].get(module_id, {})
            for topic in module_data.get('topics', []):
                if topic not in user_progress['skills_acquired']:
                    user_progress['skills_acquired'].append(topic)
    
    elif action == "start":
        user_progress['current_module'] = module_id
    
    # Add to session history
    user_progress['session_history'].append({
        'timestamp': datetime.now().isoformat(),
        'module': module_id,
        'action': action
    })
    
    save_user_progress(user_progress)
    return f"Progress updated: {action} for module {module_id}"

def create_hands_on_demo():
    """Create a hands-on demo interface"""
    demo_code = """
import openai
import gradio as gr

def generate_test_case(requirement):
    prompt = f'''
    Given this requirement: {requirement}
    
    Generate a comprehensive test case including:
    1. Test Case ID
    2. Test Description
    3. Preconditions
    4. Test Steps
    5. Expected Results
    6. Priority Level
    '''
    
    # Note: Replace with actual OpenAI API call
    return "Generated test case would appear here"

# Create Gradio interface
iface = gr.Interface(
    fn=generate_test_case,
    inputs=gr.Textbox(placeholder="Enter requirement description..."),
    outputs=gr.Textbox(label="Generated Test Case"),
    title="AI Test Case Generator"
)

if __name__ == "__main__":
    iface.launch()
"""
    return demo_code

# Main Gradio Interface
def create_main_interface():
    with gr.Blocks(title="AI-QA Studies Portal", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🚀 AI-Driven QA Professional Development Portal")
        gr.Markdown("**Transform your QA practice with AI-powered tools and techniques**")
        
        with gr.Tabs():
            # Dashboard Tab
            with gr.TabItem("📊 Dashboard"):
                gr.Markdown("## Welcome to Your Learning Dashboard")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 📈 Your Progress")
                        progress_chart = gr.Plot(value=get_progress_chart())
                        
                    with gr.Column(scale=1):
                        gr.Markdown("### 🎯 Skills Assessment")
                        skills_chart = gr.Plot(value=get_skills_radar())
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 🎓 Current Status")
                        current_module = gr.Textbox(
                            value=user_progress.get('current_module', 'No module selected'),
                            label="Current Module",
                            interactive=False
                        )
                        
                        completed_count = gr.Number(
                            value=len(user_progress.get('completed_modules', [])),
                            label="Completed Modules",
                            interactive=False
                        )
                        
                        overall_progress = gr.Slider(
                            value=user_progress.get('current_progress', 0),
                            minimum=0,
                            maximum=100,
                            label="Overall Progress (%)",
                            interactive=False
                        )
            
            # Presentations Tab
            with gr.TabItem("📽️ Presentations"):
                gr.Markdown("## Template-Driven Learning Presentations")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        module_dropdown = gr.Dropdown(
                            choices=get_module_list(),
                            label="Select Module",
                            value=None
                        )
                        
                        template_dropdown = gr.Dropdown(
                            choices=[
                                ("introduction", "Introduction"),
                                ("module_overview", "Module Overview"),
                                ("hands_on_session", "Hands-on Session"),
                                ("conclusion", "Conclusion")
                            ],
                            label="Presentation Template",
                            value="introduction"
                        )
                        
                        slide_number = gr.Slider(
                            minimum=0,
                            maximum=4,
                            value=0,
                            step=1,
                            label="Slide Number"
                        )
                        
                        generate_btn = gr.Button("Generate Slide", variant="primary")
                        
                        # Progress tracking buttons
                        with gr.Row():
                            start_btn = gr.Button("Start Module", variant="secondary")
                            complete_btn = gr.Button("Complete Module", variant="success")
                    
                    with gr.Column(scale=2):
                        slide_content = gr.Markdown(
                            value="Select a module and click 'Generate Slide' to begin",
                            elem_id="slide-content"
                        )
                        
                        progress_message = gr.Textbox(
                            label="Progress Updates",
                            interactive=False
                        )
                
                # Event handlers
                generate_btn.click(
                    generate_presentation_slide,
                    inputs=[module_dropdown, template_dropdown, slide_number],
                    outputs=slide_content
                )
                
                start_btn.click(
                    lambda module_id: update_user_progress(module_id, "start"),
                    inputs=module_dropdown,
                    outputs=progress_message
                )
                
                complete_btn.click(
                    lambda module_id: update_user_progress(module_id, "complete"),
                    inputs=module_dropdown,
                    outputs=progress_message
                )
            
            # Hands-on Lab Tab
            with gr.TabItem("🛠️ Hands-on Lab"):
                gr.Markdown("## Interactive Learning Environment")
                
                with gr.Tabs():
                    with gr.TabItem("Code Demo"):
                        gr.Markdown("### AI Test Case Generator Demo")
                        code_editor = gr.Code(
                            value=create_hands_on_demo(),
                            language="python",
                            label="Sample Code"
                        )
                        
                        with gr.Row():
                            requirement_input = gr.Textbox(
                                placeholder="Enter a requirement to generate test cases...",
                                label="Requirement Description"
                            )
                            
                            generate_test_btn = gr.Button("Generate Test Case", variant="primary")
                        
                        test_output = gr.Textbox(
                            label="Generated Test Case",
                            lines=10,
                            interactive=False
                        )
                        
                        def mock_generate_test_case(requirement):
                            return f"""
**Test Case ID**: TC_001
**Test Description**: Verify {requirement}
**Preconditions**: System is accessible and user is logged in
**Test Steps**:
1. Navigate to the relevant feature
2. Input test data
3. Execute the functionality
4. Verify the outcome
**Expected Results**: System should behave as per requirement
**Priority**: High
"""
                        
                        generate_test_btn.click(
                            mock_generate_test_case,
                            inputs=requirement_input,
                            outputs=test_output
                        )
                    
                    with gr.TabItem("AI Chat Assistant"):
                        gr.Markdown("### QA AI Assistant")
                        
                        chatbot = gr.Chatbot(
                            value=[["Hello!", "Hi! I'm your AI QA assistant. How can I help you today?"]],
                            height=400
                        )
                        
                        with gr.Row():
                            msg = gr.Textbox(
                                placeholder="Ask me anything about QA and AI...",
                                label="Your Question"
                            )
                            send_btn = gr.Button("Send", variant="primary")
                        
                        def respond(message, history):
                            response = f"I understand you're asking about: {message}. This is a demo response. In a real implementation, this would use an AI model to provide helpful QA insights."
                            history.append([message, response])
                            return history, ""
                        
                        send_btn.click(
                            respond,
                            inputs=[msg, chatbot],
                            outputs=[chatbot, msg]
                        )
            
            # Resources Tab
            with gr.TabItem("📚 Resources"):
                gr.Markdown("## Learning Resources & Documentation")
                
                with gr.Tabs():
                    with gr.TabItem("Quick Reference"):
                        gr.Markdown("""
### 🔧 Essential AI Tools for QA
- **OpenAI GPT**: Text generation and analysis
- **Langchain**: Building AI applications
- **Gradio**: Creating interactive interfaces
- **ChromaDB**: Vector databases for knowledge
- **Selenium**: Web automation with AI enhancement

### 📋 Common Prompt Templates
- **Test Case Generation**: "Generate test cases for [requirement]"
- **Bug Analysis**: "Analyze this bug report and suggest root causes"
- **API Testing**: "Create API test scenarios for [endpoint]"
- **Performance Analysis**: "Interpret these performance metrics"

### 🚀 Quick Start Commands
```bash
pip install gradio openai langchain
python -m gradio app.py
```
""")
                    
                    with gr.TabItem("Best Practices"):
                        gr.Markdown("""
### 🎯 AI-QA Best Practices

#### Prompt Engineering:
- Be specific and clear in your requests
- Provide context and examples
- Use structured formats for consistent outputs
- Iterate and refine prompts based on results

#### Integration Guidelines:
- Start with simple use cases
- Validate AI outputs with human review
- Implement proper error handling
- Monitor performance and quality metrics

#### Security Considerations:
- Protect sensitive data in prompts
- Use appropriate access controls
- Implement audit trails
- Regular security assessments

#### Quality Assurance:
- Test AI tools thoroughly
- Validate outputs against known standards
- Implement continuous monitoring
- Regular model updates and retraining
""")
                    
                    with gr.TabItem("Community"):
                        gr.Markdown("""
### 🤝 Join Our Community

#### Online Forums:
- **AI-QA Discord**: Real-time discussions
- **LinkedIn Group**: Professional networking
- **Reddit Community**: Peer support
- **Stack Overflow**: Technical Q&A

#### Events & Meetups:
- **Monthly Webinars**: Expert presentations
- **Local Meetups**: In-person networking
- **Conference Workshops**: Hands-on learning
- **Online Hackathons**: Collaborative projects

#### Contribution Opportunities:
- **Open Source Projects**: Code contributions
- **Documentation**: Help improve resources
- **Mentorship**: Support new learners
- **Content Creation**: Share your expertise

#### Stay Connected:
- **Newsletter**: Weekly updates
- **Social Media**: Follow @AIQAPortal
- **Blog**: Latest articles and tutorials
- **Podcast**: Industry insights and interviews
""")
        
        # Footer
        gr.Markdown("""
---
### 🌟 Transform Your QA Career with AI
*Built with ❤️ for QA professionals embracing the future*
""")
    
    return demo

if __name__ == "__main__":
    demo = create_main_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
