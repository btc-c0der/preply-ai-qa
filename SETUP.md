# AI QA Studies Portal - Setup Guide

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Portal**
   ```bash
   python app.py
   ```

3. **Access the Portal**
   Open your browser and go to: `http://localhost:7860`

## Features

### 🏠 Home Dashboard
- Progress tracking
- Learning streak monitoring
- Quick access to modules

### 📚 Learning Modules
- **Programming with AI**: Build automation tools, chatbots, and assistants
- **AI Best Practices**: Prompt engineering, workflow integration, decision making
- **QA + AI Integration**: Test automation, bug analysis, LLM integration
- **Knowledge Bases**: RAG implementation, vector databases, intelligent assistants
- **AI Compliance**: Governance, ethics, regulatory compliance
- **Essential Concepts**: MCP, RAG, Fine-tuning essentials

### 💻 Interactive Examples
- Test case generator
- Bug analysis tool
- Hands-on coding exercises

### 📊 Analytics Dashboard
- QA metrics visualization
- Bug distribution analysis
- Test execution trends

### 🎯 Practice Exercises
- Prompt engineering challenges
- Strategy development exercises
- Real-world scenarios

### 📖 Resources
- Curated reading list
- Tool recommendations
- Community links
- Certification paths

## Customization

### Adding New Modules
1. Update `module_config.json` with module details
2. Add slide content to the `create_slide_content()` function in `app.py`
3. Include any interactive examples in the appropriate tab

### Modifying Styling
- Update the CSS in the `main()` function
- Modify the color scheme and layout as needed

### Adding AI Integration
- Replace placeholder functions with actual AI API calls
- Configure your preferred AI service (OpenAI, Azure, etc.)
- Update environment variables for API keys

## Environment Variables

Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_key_here
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_KEY=your_azure_key
```

## Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 7860

CMD ["python", "app.py"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For questions or issues:
- Check the documentation
- Review the example code
- Contact the development team

## License

This project is licensed under the MIT License.
