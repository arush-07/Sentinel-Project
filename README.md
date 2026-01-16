Markdown
# 🚀 Team CS on Top - TechSprint GDG MUJ

<div align="center">
  <img src="https://img.shields.io/badge/Made%20with-Pathway-blue?style=for-the-badge&logo=python" alt="Pathway">
  <img src="https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/Team-Bitwise-green?style=for-the-badge" alt="Team Bitwise">
</div>

<br />

> **A Next-Gen GenAI solution built for the TechSprint GDG MUJ hackathon.**

---

## 📖 About
This project leverages the power of **Pathway's** real-time data processing engine combined with **Generative AI** to solve complex problems with live data contexts. 

The system is designed to ingest streaming data, process it dynamically using Pathway, and provide intelligent, context-aware insights via a user-friendly Streamlit interface. By simulating real-time data environments, we demonstrate how GenAI can react and adapt to changing information instantaneously.

**Key Features:**
* ⚡ **Real-time Data Processing:** Utilizing Pathway for low-latency stream handling.
* 🧠 **GenAI Integration:** LLM-powered insights on live data.
* 🔄 **Live Simulation:** Includes a data simulator to mimic real-world streaming scenarios.
* 📊 **Interactive UI:** A clean Streamlit dashboard for visualization and interaction.

---

## 🛠️ Technology Stack
We used a modern tech stack focused on speed, scalability, and AI capabilities:

* **Core Engine:** [Pathway](https://pathway.com/) (Data Processing & RAG)
* **Language:** Python
* **Frontend:** Streamlit
* **AI/LLM:** OpenAI GPT / Gemini (via API)
* **Data Simulation:** Custom Python Simulator

---

## 📂 Repo Structure
```bash
IIT-MADRAS/
├── backend.py          # Main Pathway backend logic (RAG/Indexing)
├── simulator.py        # Script to simulate real-time data streaming
├── frontend.py         # Streamlit application for the UI
├── requirements.txt    # List of project dependencies
└── README.md           # Project documentation
```

---

## 🎥 Demo
_Check out our project in action below_

![Model](https://github.com/user-attachments/assets/c8c5410f-bcbc-4a0b-8a9e-7729d3580928)


---

## 🚀 How to Clone and Run Locally
Follow these steps to get the project up and running on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/arush-07/IIT-MADRAS.git](https://github.com/arush-07/Sentinel-Project/
cd Sentinel-Project
```

### 2. Install Dependancies
Make sure you have Python installed. Then run:
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a .env file in the root directory and add your API keys (e.g. Gemini, OpenAI, Pathway license if applicable):
```bash
GEMINI_API_KEY=your_api_key_here
```

### 4. Run the Application
You need to run the components in the order below.

**🔹 Step A: Start the Backend**
Initialize the Pathway engine to listen for data.
```bash
python backend.py
```
**🔹 Step B: Start the Simulator**
Open a new terminal and run the simulator to start streaming data to the backend.
```bash
python simulator.py
```

**🔹 Step C: Launch the Frontend**
Open a third terminal and launch the Streamlit dashboard.
```bash
streamlit run frontend.py
```
---

## 👥 Team Bitwise
Made with ❤️ by:

- **Arush Pradhan**
- **Drishti Verma**
- **Aryan Verma**
- **Bhavya Jaggi**

<div align="center">
  <i>Built for the TechSprint GDG MUJ hackathon.</i>
</div>
