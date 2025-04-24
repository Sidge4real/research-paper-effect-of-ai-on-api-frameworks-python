# The Impact of AI on Python API Frameworks
[Dutch version](readme.nl.md)

## 📘 Project Overview

This project explores the impact of Artificial Intelligence (AI) on the performance and behavior of various Python web API frameworks. We evaluate how frameworks like **Flask**, **FastAPI**, and **Django** perform under load and how they integrate with lightweight, open-source AI models.

The goal is to understand:
- How API frameworks handle AI-related workloads
- What performance trade-offs occur when AI features are embedded
- Which framework is most suitable for lightweight AI-enhanced applications

## 🔬 Research Question

**What is the effect of AI on API frameworks in Python?**  
We focus on performance (latency, memory, CPU, request throughput) and developer experience when integrating AI tasks such as text summarization or sentiment analysis.

## 🧪 Benchmarked Frameworks

We compare three major Python web frameworks:
- **Flask** – Minimalistic and synchronous
- **FastAPI** – Async-based and modern
- **Django** – Full-featured and monolithic

Each framework serves a simple **blogpost API** with optional AI-powered features.

## 🤖 AI Features Tested

To simulate real-world use of AI in APIs, we implemented the following endpoints:
- **Text summarization** of blog posts using HuggingFace's `bart-large-cnn`
- **Sentiment analysis** using `bert-base-multilingual-uncased-sentiment`
- **Title generation** with GPT-like models
- **Tag prediction** using custom-trained classifiers

These tasks are integrated using open-source transformer models via [HuggingFace Transformers](https://huggingface.co/).

## 📈 Performance Metrics Collected

We benchmarked each framework with and without AI features using the following metrics:
- Requests per second
- CPU usage
- Memory usage
- Average latency
- Total runtime under load

## 🧠 Key Insights

- **FastAPI** consistently delivered the highest request throughput, but showed increased CPU usage and latency when handling concurrent AI workloads.
- **Flask** had the lowest memory usage and moderate performance, but less suited for async AI tasks.
- **Django** showed the highest memory footprint and slowest performance, but benefits from built-in tools and structure for complex apps.

## 👨‍💻 Author

**Lukas Van der Spiegel**  
🌐 [lukasvanderspiegel.be](https://lukasvanderspiegel.be)  
🔗 [linkedin.com/in/sidge](https://www.linkedin.com/in/sidge)

## 📄 License

This project is licensed under the [MIT License](LICENSE.md).
