# 🍽️ KitchenAI  

**Instantly turn AI Jupyter Notebooks into production-ready APIs.**  

[![Falco](https://img.shields.io/badge/built%20with-falco-success)](https://github.com/Tobi-De/falco)  
[![Hatch Project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)  
[![Docs](https://img.shields.io/badge/Docs-kitchenai.dev-blue)](https://docs.kitchenai.dev)

---

![kitchenai-list](../docs/_static/images/kitchenai-list.gif)


## **What is KitchenAI?**  
KitchenAI bridges the gap between **AI developers**, **Application developers**, and **Infrastructure developers** making it easy to:

- Author multiple AI techniques
- Quickly test and iterate
- Easily build and share

![kitchenai-dev](../docs/_static/images/kitchenai-highlevel1.png)

- For **AI Developers**: Focus on your techniques like RAG or embeddings—KitchenAI handles the server piece. You can continue to work in the notebook you already feel comfortable in without worrying about the underlying infrastructure. KitchenAI will convert your notebook into a production-ready application. 

- For **App Developers**: Seamlessly integrate AI with a set of API's you can build an application on top of. Quickly test to see which AI technique best fits your application.  

- For **Infrastructure Developers**: Integrate with AI tooling, customize Django backends, build plugins, and leverage built-in support for observability platforms like Sentry and OpenTelemetry. KitchenAI is extensible to modify for more advanced use cases. 

**Say goodbye to boilerplate!**  

## 🚀 **Go from notebook to production in minutes.**
Example notebook: [kitchenai-community/llama_index_starter](https://github.com/epuerta9/kitchenai-community/blob/main/src/kitchenai_community/llama_index_starter/notebook.ipynb)

By annotating your notebook with KitchenAI annotations, you can go from this:

![kitchenai-dev](../docs/_static/images/jupyter-notebook.png)

To interacting with the API using the built in client:

![kitchenai-dev](../docs/_static/images/cli-query.png)
---

## 🚀 **Why KitchenAI?**  

Integrating AI into applications is getting more complicated, making it tough to test, tweak, and improve your code quickly. KitchenAI is here to fix that by meeting AI developers and data scientists where they already work. It makes the journey from Jupyter notebooks to a fully functional AI backend seamless—getting you up and running in just minutes.

With KitchenAI, you can bridge the gap between experimenting and going live, helping teams work faster and stay productive. The goal is simple: give you a set of tools that cuts the time it takes to turn AI ideas into production-ready solutions in half, so you can focus on what really matters—delivering results. 

**The ultimate tool in your AI development kit. Improve your LLMOps.**

![kitchenai-dev](../docs/_static/images/workflow.png)


Close the feedback loop between AI developers and App developers.

🔗 Learn more at [docs.kitchenai.dev](https://docs.kitchenai.dev/develop/).  

---

## ⚡ **Quickstart**  

1. **Set Up Environment**  
   ```bash
   export OPENAI_API_KEY=<your key>
   python -m venv venv && source venv/bin/activate && pip install kitchenai
   ```

2. **Start a Project**  
   ```bash
   kitchenai cook list && kitchenai cook select llama-index-starter
   ```

3. **Run the Server**  
   ```bash
   kitchenai init && kitchenai dev --module app:kitchen
   ```
   Alternatively, you can run the server with jupyter notebook:
   ```bash
   kitchenai dev --module app:kitchen --jupyter
   ```

4. **Test the API**  

   ```bash
   kitchenai client health
   ```
   ```bash
   kitchenai client labels
   ```
   ![kitchenai-client](../docs/_static/images/kitchenai-dev-client.gif)

5. **Build Docker Container**  
   ```bash
   kitchenai build . app:kitchenai
   ```  

📖 Full quickstart guide at [docs.kitchenai.dev](https://docs.kitchenai.dev/cookbooks/quickstarts/).  

---

## ✨ **Features**  

![kitchenai-features](../docs/_static/images/kitchenai-highlevel4.png)

- **📦 Quick Cookbook Creation**: Build cookbooks in seconds.  
- **🚀 Production-Ready AI**: Turn AI code into robust endpoints.  
- **🔌 Extensible Framework**: Add custom recipes and plugins effortlessly.  
- **🐳 Docker-First Deployment**: Deploy with ease.  

---

## 🔧 **Under the Hood**  

- **Django Ninja**: Async-first API framework for high-performance endpoints.  
- **Django Q2**: Background workers for long-running tasks. 
- **Plugin Framework**: Django DJP integration
- **AI Ecosystem**: Integrations to AI ecosystem and tools 
- **S6 Overlay**: Optimized container orchestration.  

KitchenAI is **built for developers**, offering flexibility and scalability while letting you focus on AI.

---

## 🛠️ **Roadmap**  

- **SDKs** for Python, Go, JS, and Rust.  
- Enhanced plugin system.  
- Signal-based architecture for event-driven apps.  
- Built-in support for **Postgres** and **pgvector**.  

---

## 🧑‍🍳 **Contribute**  

KitchenAI is in **alpha**—we welcome your contributions and feedback!  

### 🛠️ **Setup**  
```bash
just bootstrap && just setup
```

- Requirements: Python 3.11+, Hatch, and Just.  
- Creates a dev environment with pre-configured superuser (`admin@localhost` / `admin`).  

Contributing details at [docs.kitchenai.dev](https://docs.kitchenai.dev).  

---

## 🙏 **Acknowledgements**  

Inspired by the [Falco Project](https://github.com/Tobi-De/falco). Thanks to the Python community for best practices and tools!  

---

## 📊 **Telemetry**  

KitchenAI collects **anonymous usage data** to improve the framework—no PII or sensitive data is collected.  

> Your feedback and support shape KitchenAI. Let's build the future of AI development together!  