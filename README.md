# Gabay 🇵🇭

An AI-powered, offline-first assistive technology ecosystem engineered to bridge the digital generational gap for older Filipinos. **Gabay** automates the creation of high-accessibility, interactive app simulation tutorials by parsing raw smartphone screen recordings using Computer Vision and localized Vision-Language Models (VLMs).

---

## 🚀 The Vision & Problem Statement
As the Philippines rapidly transitions to digital-first infrastructure (e-governance, digital banking via GCash/Maya, and essential communication channels), older adults (Lolos and Lolas) are increasingly left vulnerable to digital exclusion and sophisticated social engineering scams. Meanwhile, younger family members are burdened as the default, repetitive household IT support.

**Gabay** solves this by letting a tech-savvy grandchild simply record a screen-recording of any app workflow. Our automated pipeline transforms that raw video into a lightweight, interactive, "Lola-proof" application simulation complete with empathetic text-to-speech guidance and progressive error scaffolding.

---

## 🛠️ System Architecture & Tech Stack

The project is decoupled into a high-performance automation pipeline and an ultra-accessible, front-end delivery system.

### 1. Automated Vision Pipeline (Python / Machine Learning)
* **Video Frame Ingestion & SSIM Filter:** Utilizes `OpenCV` and **Structural Similarity Index (SSIM)** scoring matrix to reduce thousands of raw video frames into discrete, high-information keyframes, eliminating computational redundancy.
* **Touch-Target Extraction:** Leverages a lightweight **YOLOv8** object detection architecture to track native device pointer/touch indicators, mapping precise absolute pixel coordinates $(x, y)$.
* **Coordinate Normalization:** Converts pixel boundaries into unitless percentage vectors ($0.0 \dots 1.0$) relative to the source dimension. This enforces dynamic relational scaling across different screen sizes and aspect ratios without target drift.
* **Local VLM & Language Synthesis:** Powered by **Ollama** running localized instances of `Llama-3.2-Vision` and `Llama-3`. It processes screen components, enforces structural JSON outputs via Pydantic schemas, and translates complex UI states into natural, conversational **Taglish** instructional nodes.

### 2. High-Accessibility Simulation Engine (React.js)
* **Adaptive Error Scaffolding:** Implements a **3-Strike Scaffolding Mechanism** that monitors client-side state. If an elderly user clicks an incorrect zone, the UI shifts from low-intrusive soft pulses to dynamic target-box expansions, culminating in an automated visual "show-me" animation.
* **Offline-First Audio Assist:** Integrates the native browser **Web Speech API** for localized Text-to-Speech (TTS) audio delivery, requiring zero cloud dependencies or network bandwidth during runtime.

---

## 🗂️ Repository Structure

```text
Gabay/
├── input_videos/           # Source .mp4 screen recordings from the student
├── output_keyframes/       # Extracted keyframes filtered via SSIM metrics
├── src/
│   ├── video_parser.py     # Stage 1: OpenCV & SSIM Frame Filter
│   ├── coordinate_norm.py  # Stage 2: Resolution scaling logic
│   ├── vision_agent.py     # Stage 3: Ollama/Llama-Vision pipeline
│   └── script_gen.py       # Stage 4: Taglish script generation & JSON export
├── venv/                   # Isolated Python Virtual Environment
├── .gitignore              # Configured to filter caching and binary environments
└── README.md               # System documentation
