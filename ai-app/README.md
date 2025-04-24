# API Framework Comparison Research Project

[Read in Dutch](README.nl.md)

## Project Overview
This repository contains the reference implementation for my AP University research paper: **"What is the effect of AI usage on API frameworks in Python?"**. It compares performance characteristics of popular Python API frameworks (Flask, Django, FastAPI) under different implementation patterns. In this part we focus on a no-AI implementation to compare the frameworks.

## Technical Implementation

### Key Components
- **/no-ai-app**: Contains baseline implementations without AI integration
- **/ai-integrated**: Experimental implementations with AI-assisted development
- **benchmarks/**: Performance testing scripts
- **requirements.txt**: Python dependencies

### Framework Examples
```bash
# FastAPI (Production)
uvicorn fastapi_app:app --host 0.0.0.0 --port 8001 --workers 4

# Flask Development
flask --app flask_app run -p 8002

# Django Production
daphne django_project.asgi:application --port 8003
```

## Research Context
This implementation serves as the foundation for measuring:
1. Development velocity with/without AI assistance
2. Runtime performance characteristics
3. Code quality metrics
4. Error rate comparison

## License
MIT License - See [LICENSE.md](LICENSE.md)

---
**Author**: Lukas Van der Spiegel  
**Academic Affiliation**: AP University (ap.be)  
**Website**: [lukasvanderspiegel.be](https://lukasvanderspiegel.be)  
**LinkedIn**: [linkedin.com/in/sidge](https://linkedin.com/in/sidge)