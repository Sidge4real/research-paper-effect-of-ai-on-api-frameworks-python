# De Impact van AI op Python API Frameworks
[English version](README.md)

## 📘 Projectoverzicht

Dit project onderzoekt de impact van Artificiële Intelligentie (AI) op de prestaties en het gedrag van verschillende Python web-API frameworks. We evalueren hoe frameworks zoals **Flask**, **FastAPI** en **Django** presteren onder belasting en hoe ze integreren met lichte, open-source AI-modellen.

Het doel is om te begrijpen:
- Hoe API-frameworks omgaan met AI-gerelateerde workloads
- Welke prestatieverschillen optreden bij het toevoegen van AI-functionaliteit
- Welk framework het meest geschikt is voor lichte AI-gebaseerde toepassingen

## 🔬 Onderzoeksvraag

**Wat is het effect van AI op API-frameworks in Python?**  
We focussen op prestatie (latency, geheugen, CPU, requests per seconde) en ontwikkelaarsgemak bij het integreren van AI-taken zoals tekstsamenvatting of sentimentanalyse.

## 🧪 Vergeleken Frameworks

We vergelijken drie populaire Python web-frameworks:
- **Flask** – Minimalistisch en synchroon
- **FastAPI** – Asynchroon en modern
- **Django** – Volledig en monolithisch

Elk framework biedt een eenvoudige **blogpost API** met optionele AI-functies.

## 🤖 Geteste AI-functionaliteiten

Om het gebruik van AI in echte API's te simuleren, implementeerden we de volgende eindpunten:
- **Tekstsamenvatting** van blogposts via HuggingFace's `bart-large-cnn`
- **Sentimentanalyse** met `bert-base-multilingual-uncased-sentiment`
- **Titelgeneratie** met GPT-achtige modellen
- **Tag-voorspelling** via zelfgetrainde AI-classifiers

Deze functies zijn geïntegreerd met open-source modellen via [HuggingFace Transformers](https://huggingface.co/).

## 📈 Verzamelde Prestatiegegevens

We hebben elk framework getest met en zonder AI-functionaliteiten, met de volgende metrieken:
- Requests per seconde
- CPU-gebruik
- Geheugengebruik
- Gemiddelde latency
- Totale looptijd onder belasting

## 🧠 Belangrijkste Inzichten

- **FastAPI** leverde consistent het hoogste aantal verzoeken per seconde, maar toonde ook verhoogd CPU-gebruik en latency bij gelijktijdige AI-verwerking.
- **Flask** had het laagste geheugengebruik en een degelijke prestatie, maar is minder geschikt voor asynchrone AI-taken.
- **Django** had het hoogste geheugengebruik en de traagste prestaties, maar biedt wel ingebouwde tools en structuur voor grotere toepassingen.

## 👨‍💻 Auteur

**Lukas Van der Spiegel**  
🌐 [lukasvanderspiegel.be](https://lukasvanderspiegel.be)  
🔗 [linkedin.com/in/sidge](https://www.linkedin.com/in/sidge)

## 📄 Licentie

Dit project is gelicentieerd onder de [MIT Licentie](LICENSE.md).
