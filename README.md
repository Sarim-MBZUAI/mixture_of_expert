# mixture_of_expert


This project analyzes data about serial killers, generates reports using AI agents simulating a court process, and creates visualizations based on the analysis.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Project Structure](#project-structure)
5. [Data Processing](#data-processing)
6. [AI-Powered Court Simulation](#ai-powered-court-simulation)
7. [Report Generation](#report-generation)
8. [Visualizations](#visualizations)
9. [Dependencies](#dependencies)
10. [License](#license)

## Project Overview

This project uses AI agents to simulate a court process for a randomly selected group of serial killers. It generates detailed reports for each killer and creates visualizations to provide insights into the sentencing outcomes and victim counts.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/serial-killer-analysis.git
   cd serial-killer-analysis
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your GROQ API key in a `utils.py` file or as an environment variable.

## Usage

Run the main script:
```
python Judge_jury_executioner.py
```

This will process the data, generate reports, and create visualizations.

## Project Structure

- `Judge_jury_executioner.py`: Main script for processing data, generating reports, and creating visualizations
- `utils.py`: Utility functions (e.g., API key retrieval)
- `data/`: Directory containing the input CSV file
- `criminal_reports/`: Directory where individual killer reports are saved
- `figures/`: Directory where visualizations are saved
- `wiki_scrapper.py` : Code to scrap the wiki data

## Data Processing

The script processes data from a CSV file (`serial_killers_data.csv`) containing information about serial killers. It randomly selects a subset of killers for analysis.

## AI-Powered Court Simulation

The project uses the CrewAI library to simulate a court process for each selected killer:

- A Judge agent presides over the proceedings and makes final judgments
- A Jury agent evaluates evidence and reaches a verdict
- An Executioner agent outlines the steps to carry out the court's decision

## Report Generation

For each selected serial killer, the script generates a Markdown report containing:
- Judge's decision
- Jury's verdict
- Executioner's plan

Reports are saved in the `criminal_reports/` directory.

## Visualizations

The script generates several visualizations:
1. Pie chart of sentence distributions
2. Bar plot of victim count by killer
3. Box plot of victim count by sentence

Visualizations are saved in the `figures/` directory.

## Dependencies

- pandas
- matplotlib
- seaborn
- crewai
- langchain_groq
- langchain
- langchain_community

For a complete list of dependencies, see `requirements.txt`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.