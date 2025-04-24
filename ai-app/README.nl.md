# API Framework Vergelijkingsonderzoek

[Lees in het Engels](README.md)

## Projectoverzicht
Deze repository bevat de referentie-implementatie voor mijn AP Hogeschool onderzoekspaper: **"Wat is het effect van AI-gebruik op API-frameworks in Python?"**. Het vergelijkt prestatiekenmerken van populaire Python API-frameworks (Flask, Django, FastAPI) onder verschillende implementatiepatronen. In dit deel focussen we op niet AI geimplementeerd implementatie om de frameworks te vergelijken.

## Technische Implementatie

### Belangrijke Componenten
- **/no-ai-app**: Basisimplementaties zonder AI-integratie
- **/ai-integrated**: Experimentele implementaties met AI-ondersteunde ontwikkeling
- **benchmarks/**: Prestatietestscripts
- **requirements.txt**: Python-afhankelijkheden

### Framework Voorbeelden
```bash
# FastAPI (Productie)
uvicorn fastapi_app:app --host 0.0.0.0 --port 8001 --workers 4

# Flask Ontwikkeling
flask --app flask_app run -p 8002

# Django Productie
daphne django_project.asgi:application --port 8003
```

## Onderzoekscontext
Deze implementatie dient als basis voor het meten van:
1. Ontwikkelsnelheid met/zonder AI-assistentie
2. Runtime-prestatiekenmerken
3. Codekwaliteitsmetrics
4. Foutpercentagevergelijking

## Licentie
MIT Licentie - Zie [LICENSE.md](LICENSE.md)

---
**Auteur**: Lukas Van der Spiegel  
**Academische Affiliatie**: AP Hogeschool (ap.be)  
**Website**: [lukasvanderspiegel.be](https://lukasvanderspiegel.be)  
**LinkedIn**: [linkedin.com/in/sidge](https://linkedin.com/in/sidge)