# Hugging Face Spaces Deployment Guide

This document provides step-by-step instructions to deploy the AI-QA Portal to Hugging Face Spaces.

## Prerequisites

1. **Hugging Face Account**: Create an account at [huggingface.co](https://huggingface.co)
2. **Git LFS**: Install Git Large File Storage (optional, for large files)
3. **Access Token**: Generate a Hugging Face access token with write permissions

## Deployment Methods

### Method 1: Direct GitHub Integration (Recommended)

1. **Navigate to Hugging Face Spaces**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"

2. **Configure Space Settings**
   - **Space name**: `ai-qa-portal`
   - **License**: MIT
   - **SDK**: Gradio
   - **Hardware**: CPU Basic (free tier)
   - **Visibility**: Public

3. **Connect GitHub Repository**
   - Select "Clone from Git"
   - Repository URL: `https://github.com/btc-c0der/preply-ai-qa.git`
   - Branch: `main`

4. **Automatic Deployment**
   - Hugging Face will automatically detect the `README.md` metadata
   - The app will build and deploy automatically
   - Monitor deployment progress in the Spaces interface

### Method 2: Manual Git Push

1. **Clone the Hugging Face Space Repository**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/ai-qa-portal
   cd ai-qa-portal
   ```

2. **Add Remote for Source Repository**
   ```bash
   git remote add source https://github.com/btc-c0der/preply-ai-qa.git
   git pull source main
   ```

3. **Push to Hugging Face**
   ```bash
   git push origin main
   ```

### Method 3: Hugging Face CLI (Advanced)

1. **Install Hugging Face CLI**
   ```bash
   pip install huggingface_hub
   ```

2. **Login to Hugging Face**
   ```bash
   huggingface-cli login
   ```

3. **Create and Upload Space**
   ```bash
   huggingface-cli repo create ai-qa-portal --type space --space_sdk gradio
   huggingface-cli upload ai-qa-portal . --repo-type space
   ```

## Configuration Details

### README.md Metadata
The following YAML configuration in README.md controls the Spaces deployment:

```yaml
---
title: AI-QA Portal - Interactive Learning Platform
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
short_description: Interactive AI-powered QA learning portal with comprehensive study modules
tags:
- artificial-intelligence
- quality-assurance
- education
- learning
- gradio
- testing
- qa
- automation
---
```

### Application Configuration
- **Entry Point**: `app.py`
- **Dependencies**: Defined in `requirements.txt`
- **Python Version**: 3.8+ (automatically detected)
- **Port**: 7860 (Gradio default)

## Environment Variables (Optional)

If your application requires environment variables, create a `.env` file or configure them in the Spaces settings:

```bash
# Example environment variables
OPENAI_API_KEY=your_api_key_here
HF_TOKEN=your_hugging_face_token
DEBUG=false
```

## Deployment Verification

### 1. Check Build Logs
- Monitor the "Logs" tab in your Space
- Verify all dependencies install correctly
- Ensure no build errors occur

### 2. Test Functionality
- **Homepage Loading**: Verify the main interface loads
- **Module Selection**: Test module navigation
- **Presentation Generation**: Verify slide generation works
- **Progress Tracking**: Check data persistence
- **Responsive Design**: Test on different screen sizes

### 3. Performance Monitoring
- **Load Time**: Should be under 30 seconds for cold start
- **Memory Usage**: Monitor in the Space metrics
- **User Interactions**: Test all UI components

## Post-Deployment Configuration

### Custom Domain (Pro Feature)
```bash
# Configure custom domain in Space settings
# Example: ai-qa-portal.yourcompany.com
```

### Analytics Integration
```python
# Add analytics tracking in app.py
import gradio as gr

# Configure analytics
gr.Interface.analytics = True
```

### SEO Optimization
Update the README.md metadata for better discoverability:
- Enhance description and tags
- Add relevant keywords
- Include usage examples

## Troubleshooting

### Common Issues

1. **Build Timeout**
   - Reduce dependency versions
   - Optimize requirements.txt
   - Use lighter alternatives

2. **Memory Errors**
   - Upgrade to better hardware tier
   - Optimize data structures
   - Implement lazy loading

3. **Port Conflicts**
   - Ensure app.py uses port 7860
   - Check server_name is "0.0.0.0"

4. **File Not Found Errors**
   - Verify all file paths are relative
   - Check .gitignore doesn't exclude necessary files
   - Ensure data files are committed

### Debug Commands
```bash
# Check deployment status
curl -I https://huggingface.co/spaces/YOUR_USERNAME/ai-qa-portal

# Test local deployment
python app.py

# Validate requirements
pip install -r requirements.txt
```

## Maintenance

### Regular Updates
1. **Update Dependencies**: Keep requirements.txt current
2. **Security Patches**: Monitor and apply security updates
3. **Performance Optimization**: Regular performance audits
4. **Content Updates**: Keep learning modules current

### Monitoring
- **Space Analytics**: Monitor usage patterns
- **Error Tracking**: Set up error alerting
- **User Feedback**: Implement feedback collection
- **Performance Metrics**: Track load times and usage

## Support Resources

- **Hugging Face Documentation**: [docs.huggingface.co](https://docs.huggingface.co)
- **Gradio Documentation**: [gradio.app/docs](https://gradio.app/docs)
- **Community Forum**: [discuss.huggingface.co](https://discuss.huggingface.co)
- **GitHub Issues**: Report bugs in the source repository

## Next Steps After Deployment

1. **Share the Space**: Promote your deployed application
2. **Collect Feedback**: Gather user feedback for improvements
3. **Monitor Usage**: Track analytics and performance metrics
4. **Iterate**: Continuously improve based on user needs
5. **Scale**: Consider upgrading hardware for increased usage

The AI-QA Portal is now ready for production deployment on Hugging Face Spaces!
