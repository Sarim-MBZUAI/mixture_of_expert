<!-- # 🔍 LLM Agents: Serial Killer Analysis

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

This project analyzes data about serial killers, generates reports using AI agents simulating a court process, and creates visualizations based on the analysis.

## 📚 Table of Contents

1. [Project Overview](#-project-overview)
2. [Installation](#-installation)
3. [Usage](#-usage)
4. [Project Structure](#-project-structure)
5. [Data Processing](#-data-processing)
6. [AI-Powered Court Simulation](#-ai-powered-court-simulation)
7. [Report Generation](#-report-generation)
8. [Visualizations](#-visualizations)
9. [Dependencies](#-dependencies)
10. [License](#-license)

## 🔎 Project Overview

This cutting-edge project harnesses the power of AI to simulate a court process for a randomly selected group of serial killers. It generates detailed reports for each case and creates insightful visualizations to provide a comprehensive analysis of sentencing outcomes and victim counts.

## 🛠 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/mixture_of_expert.git
   cd mixture_of_expert
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your GROQ API key in a `utils.py` file or as an environment variable.

## 🚀 Usage

Run the main script:
```bash
python Judge_jury_executioner.py
```

This will initiate the data processing, report generation, and visualization creation.

## 📁 Project Structure

```
mixture_of_expert/
│
├── Judge_jury_executioner.py
├── utils.py
├── requirements.txt
├── README.md
├── LICENSE
│
├── data/
│   └── serial_killers_data.csv
│
├── criminal_reports/
│   └── [Generated Killer Reports]
│
├── figures/
│   └── [Generated Visualizations]
│
└── wiki_scrapper.py
```

## 🔢 Data Processing

The script processes data from `serial_killers_data.csv`, containing detailed information about serial killers. A subset of killers is randomly selected for in-depth analysis.

## ⚖️ AI-Powered Court Simulation

Leveraging the CrewAI library, the project simulates a comprehensive court process for each selected killer:

- 👨‍⚖️ **Judge Agent**: Presides over proceedings and delivers final judgments
- 👥 **Jury Agent**: Evaluates evidence and reaches a verdict
- 🕴️ **Executioner Agent**: Outlines steps to carry out the court's decision

## 📝 Report Generation

For each analyzed serial killer, the script generates a detailed Markdown report containing:
- Judge's decision
- Jury's verdict
- Executioner's plan

Reports are saved in the `criminal_reports/` directory.

## 📊 Visualizations

The script generates several insightful visualizations:
1. 🥧 Pie chart of sentence distributions
2. 📊 Bar plot of victim count by killer
3. 📦 Box plot of victim count by sentence

All visualizations are saved in the `figures/` directory.

## 🔗 Dependencies

- pandas
- matplotlib
- seaborn
- crewai
- langchain_groq
- langchain
- langchain_community

For a complete list of dependencies, see `requirements.txt`.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
 -->


 # 🔍 Mixture of Expert: Advanced Serial Killer Case Analysis

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

This project conducts an in-depth analysis of serial killer cases using AI-powered agents to simulate a comprehensive court process, generate detailed reports, and create insightful visualizations.

## 📚 Table of Contents

1. [Project Overview](#-project-overview)
2. [Installation](#-installation)
3. [Usage](#-usage)
4. [Project Structure](#-project-structure)
5. [Data Processing](#-data-processing)
6. [AI-Powered Court Simulation](#-ai-powered-court-simulation)
7. [Report Generation](#-report-generation)
8. [Visualizations](#-visualizations)
9. [Logging](#-logging)
10. [Dependencies](#-dependencies)
11. [License](#-license)

## 🔎 Project Overview

This advanced project utilizes AI to simulate a comprehensive court process for a randomly selected group of serial killers. It generates detailed reports for each case, creates insightful visualizations, and maintains thorough logs of the entire process.

## 🛠 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/mixture_of_expert_advanced.git
   cd mixture_of_expert
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your GROQ API key in a `utils.py` file or as an environment variable.

## 🚀 Usage

Run the main script:
```bash
python Judge_jury_executioner.py
```

This will initiate the data processing, court simulation, report generation, and visualization creation.

## 📁 Project Structure

```
mixture_of_expert/
│
├── Judge_jury_executioner.py
├── utils.py
├── requirements.txt
├── README.md
├── LICENSE
│
├── data/
│   └── serial_killers_data.csv
│
├── criminal_reports/
│   └── [Generated Individual Role Reports]
│
├── figures/
│   └── [Generated Visualizations]
│
├── logs/
│   └── [Detailed Execution Logs]
│
└── wiki_scrapper.py
```

## 🔢 Data Processing

The script processes data from `serial_killers_data.csv`, containing detailed information about serial killers. A subset of killers is randomly selected for in-depth analysis.

## ⚖️ AI-Powered Court Simulation

Leveraging the CrewAI library, the project simulates a comprehensive court process for each selected killer with the following agents:

- 👨‍⚖️ **Presiding Judge**: Maintains order, makes rulings, and delivers sentences
- 👥 **Jury Panel**: Evaluates evidence and reaches a verdict
- 👨‍🏫 **District Attorney**: Presents the case for the prosecution
- 👨‍💼 **Defense Counsel**: Represents the accused and presents the defense

## 📝 Report Generation

For each analyzed serial killer, the script generates detailed individual reports for each role in the court process:
- Presiding Judge's decision
- Jury's verdict
- District Attorney's arguments
- Defense Counsel's strategy

Reports are saved as separate Markdown files in the `criminal_reports/` directory.

## 📊 Visualizations

The script generates several insightful visualizations:
1. 🥧 Pie chart of sentence distributions
2. 📊 Bar plot of victim count by killer
3. 📦 Box plot of victim count by sentence

All visualizations are saved in the `figures/` directory.

## 📜 Logging

The project implements a custom logging system that:
- Creates timestamped log files in the `logs/` directory
- Captures detailed information about the script's execution
- Logs errors, warnings, and important events throughout the process

## 🔗 Dependencies

- pandas
- matplotlib
- seaborn
- crewai
- langchain_groq
- langchain
- langchain_community
- numpy

For a complete list of dependencies, see `requirements.txt`.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: This project is for educational and research purposes only. It deals with sensitive topics and should be used responsibly.
