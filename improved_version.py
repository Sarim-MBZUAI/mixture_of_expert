import os
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
from crewai import Agent, Crew, Process, Task
from langchain_groq import ChatGroq
from datetime import datetime
from utils import get_groq_api_key
from langchain.agents import load_tools
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.prompts import ChatPromptTemplate
import logging
import traceback
import numpy as np
import logging
from datetime import datetime
import os
random.seed(12)
np.random.seed(12)
if not os.path.exists('logs'):
    os.makedirs('logs')

# Generate a timestamp for the log file name

class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        
    def log(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {level.upper()} - {message}\n"
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            print(log_entry.strip())  # Also print to console
        except Exception as e:
            print(f"Error writing to log file: {str(e)}")

    def info(self, message):
        self.log("INFO", message)

    def debug(self, message):
        self.log("DEBUG", message)

    def error(self, message):
        self.log("ERROR", message)

    def warning(self, message):
        self.log("WARNING", message)

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Generate a timestamp for the log file name
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_name = f"logs/serial_killer_analysis_{timestamp}.txt"

# Initialize the logger
logger = Logger(log_file_name)

# Test logging
logger.info("Script execution started")
logger.debug("This is a debug message")
logger.warning("This is a warning message")
logger.error("This is an error message")

# Test logging
logger.info("Script execution started")

# Test logging

# Load the CSV file
df = pd.read_csv('./data/serial_killers_data.csv')
logger.info(f"Loaded CSV file with {len(df)} entries")

# Randomly select 1 serial killer
selected_killers = df.sample(n=15)
logger.info(f"Selected killer: {selected_killers['Name'].values[0]}")
os.environ["GROQ_API_KEY"] = get_groq_api_key()
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")



def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 'Unknown'

def save_reports(killer_name, report_content):
    directory = "criminal_reports"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = f"{directory}/{killer_name.replace(' ', '_')}_report.md"
    
    with open(filename, "w", encoding='utf-8') as f:
        f.write(f"# Report for {killer_name}\n\n")
        f.write(report_content)
    
    print(f"Report saved for {killer_name} in {filename}")

Judge = Agent(
    role="Senior Judge at Supreme Court",
    goal="Ensure fair trials and make impartial decisions based on law and evidence.",
    backstory="Experienced jurist known for wisdom and adherence to legal principles. Has presided over landmark cases shaping national law.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    memory=True,
)

jury = Agent(
    role="Jury Panel",
    goal="Evaluate evidence and arguments to reach a fair verdict.",
    backstory="Diverse group of 12 citizens selected for jury duty. Committed to impartiality and basing decisions solely on court evidence.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    memory=True,
)

executioner = Agent(
    role="Senior Corrections Officer",
    goal="Carry out court sentences professionally and ethically, respecting inmates' rights.",
    backstory="Experienced officer overseeing sentence implementation. Trained in ethics, conflict resolution, and maintaining order in the justice system.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    memory=True,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_killer(killer):
    get_judge = Task(
        description=f"""Preside over the court proceedings for {killer['Name']}, accused of {killer['Proven victims']} proven murders. 
        Ensure a fair trial, and provide a final judgment based on the law and evidence presented. 
        Your judgment MUST include a clear and specific sentence, such as 'death sentence', 'life imprisonment', or a specific number of years in prison. 
        Always conclude your judgment with the phrase 'The sentence is: [specific sentence].'""",
        expected_output="A detailed judgment including the verdict and a clearly specified sentence.",
        agent=Judge,
    )
    
    get_jury = Task(
        description=f"""
        As the jury in the case of {killer['Name']}, accused of {killer['Proven victims']} proven murders:
        1. Review all evidence and arguments presented in court.
        2. Deliberate as a group to reach a verdict on the facts of the case.
        3. Provide a clear decision on guilt or innocence based solely on the evidence presented.
        4. Explain the reasoning behind your verdict in your own words.
        5. Do NOT repeat the judge's decision or sentencing - focus only on determining guilt or innocence.
        Your response should be in the format:
        "Verdict: [Guilty/Not Guilty]
        Reasoning: [Your explanation]"
        """,
        expected_output="A clear verdict (guilty or not guilty) with a brief explanation of the decision, in the jury's own words.",
        agent=jury,
    )

    get_executioner = Task(
        description=f"""
        Based on the Judge's sentencing for {killer['Name']} and following all legal and ethical guidelines, outline the steps to carry out the court's decision. 
        Focus on maintaining the dignity and rights of the convicted while ensuring the sentence is properly executed.
        Provide a concise list of steps, not exceeding 5 main points.
        """,
        expected_output="A concise plan for carrying out the sentence in an ethical and lawful manner.",
        agent=executioner,
    )

    crew = Crew(
        agents=[Judge, jury, executioner],
        tasks=[get_judge, get_jury, get_executioner],
        verbose=2,
    )
    
    try:
        results = crew.kickoff()
        
        # Check if results is a string (single output) or a list of outputs
        if isinstance(results, str):
            combined_result = results
        else:
            # Assume it's a list of objects with raw_output attribute
            combined_result = "\n\n".join([r.raw_output for r in results if hasattr(r, 'raw_output')])
        
        markdown_report = f"""
# Report for {killer['Name']}

## Case Summary
- **Defendant:** {killer['Name']}
- **Charges:** {killer['Proven victims']} counts of murder

## Combined Results
{combined_result}
"""
        
        return markdown_report
    except Exception as e:
        logger.error(f"Error in process_killer for {killer['Name']}: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return f"Error processing {killer['Name']}: {str(e)}"

def analyze_sentence(result):
    result_lower = result.lower()
    
    # Look for the exact phrase first
    sentence_start = result_lower.find("the sentence is:")
    if sentence_start != -1:
        sentence_end = result_lower.find(".", sentence_start)
        if sentence_end != -1:
            return result[sentence_start:sentence_end].strip()
        else:
            return result[sentence_start:].strip()
    
    # If not found, search for alternative phrases
    alternatives = ["sentenced to", "punishment is", "verdict:", "imprisonment for"]
    for phrase in alternatives:
        alt_start = result_lower.find(phrase)
        if alt_start != -1:
            alt_end = result_lower.find(".", alt_start)
            if alt_end != -1:
                return result[alt_start:alt_end].strip()
            else:
                return result[alt_start:].strip()
    
    # If still not found, search for common sentence types
    sentence_types = ["life imprisonment", "years in prison", "death penalty", "death by hanging"]
    for sentence_type in sentence_types:
        type_start = result_lower.find(sentence_type)
        if type_start != -1:
            type_end = result_lower.find(".", type_start)
            if type_end != -1:
                return result[type_start:type_end].strip()
            else:
                return result[type_start:].strip()
    
    # If no sentence is found, return a message for manual review
    return "MANUAL REVIEW REQUIRED: No clear sentence found"

# Process each selected killer
results = []
sentences = []
for _, killer in selected_killers.iterrows():
    logger.info(f"Processing killer: {killer['Name']}")
    try:
        result = process_killer(killer)
        
        if "Error processing" not in result:
            logger.info(f"Successfully processed {killer['Name']}")
            sentence = analyze_sentence(result)
            sentences.append(sentence)
            logger.info(f"Extracted sentence for {killer['Name']}: {sentence}")
            
            # Save the report
            report_filename = f"criminal_reports/{killer['Name'].replace(' ', '_')}_report.md"
            with open(report_filename, 'w') as f:
                f.write(result)
            logger.info(f"Report saved as: {report_filename}")
        else:
            logger.warning(f"Error occurred while processing {killer['Name']}: {result}")
            sentences.append("Error")
        
    except Exception as e:
        logger.error(f"Unexpected error processing {killer['Name']}: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sentences.append("Error")

print("\nProcessed Killers and Sentences:")
for killer, sentence, victims in zip(selected_killers['Name'], sentences, selected_killers['Proven victims']):
    victim_count = safe_int(victims)
    print(f"{killer} (Proven victims: {victim_count}): {sentence}")

# Additional statistics
selected_killers['Sentence'] = sentences
selected_killers['Victim Count'] = selected_killers['Proven victims'].apply(safe_int)

# Visualization 1: Pie chart of sentences
plt.figure(figsize=(10, 6))
sentence_counts = pd.Series(sentences).value_counts()
plt.pie(sentence_counts.values, labels=sentence_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Sentences for Randomly Selected Serial Killers')
plt.axis('equal')
plt.savefig('./figures/sentence_distribution.png')
plt.close()

# Visualization 2: Bar plot of victim count by killer
plt.figure(figsize=(12, 6))
victim_count_data = selected_killers[selected_killers['Victim Count'] != 'Unknown']
if not victim_count_data.empty:
    sns.barplot(x='Name', y='Victim Count', data=victim_count_data)
    plt.title('Proven Victim Count by Serial Killer')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('./figures/victim_count_by_killer.png')
else:
    print("No valid victim count data for bar plot")
plt.close()

# Visualization 3: Box plot of victim count by sentence
plt.figure(figsize=(10, 6))
if not victim_count_data.empty:
    sns.boxplot(x='Sentence', y='Victim Count', data=victim_count_data)
    plt.title('Distribution of Proven Victim Count by Sentence')
    plt.savefig('./figures/victim_count_by_sentence.png')
else:
    print("No valid victim count data for box plot")
plt.close()

print("\nAnalysis complete. Reports saved in 'criminal_reports' directory.")
print("Visualizations saved as PNG files:")
print("1. sentence_distribution.png")
print("2. victim_count_by_killer.png (if valid data available)")
print("3. victim_count_by_sentence.png (if valid data available)")

# Print detailed results
for killer, sentence, victims in zip(selected_killers['Name'], sentences, selected_killers['Proven victims']):
    victim_count = safe_int(victims)
    print(f"{killer} (Proven victims: {victim_count}): {sentence}")

logger.info("Script execution completed")
print(f"Log file saved as: {log_file_name}")