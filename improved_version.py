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

# Load the CSV file
df = pd.read_csv('./data/serial_killers_data.csv')
logger.info(f"Loaded CSV file with {len(df)} entries")

# Randomly select 1 serial killer
selected_killers = df.sample(n=20)
logger.info(f"Selected killer: {selected_killers['Name'].values[0]}")
os.environ["GROQ_API_KEY"] = get_groq_api_key()
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 'Unknown'

def save_individual_results(killer_name, role, content):
    directory = "criminal_reports"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = f"{directory}/{killer_name.replace(' ', '_')}_{role.lower().replace(' ', '_')}_report.md"
    
    with open(filename, "w", encoding='utf-8') as f:
        f.write(f"# {role} Report for {killer_name}\n\n")
        f.write(content)
    
    logger.info(f"{role} report saved for {killer_name} in {filename}")

judge = Agent(
    role="Presiding Judge",
    goal="Ensure a fair trial by maintaining order in the court, ruling on objections, instructing the jury, and applying the law.",
    backstory="An experienced jurist with a deep understanding of the law and a commitment to impartial justice.",
    verbose=False,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    memory=True,
)

jury = Agent(
    role="Jury Panel",
    goal="Determine the facts of the case and reach a verdict based solely on the evidence presented in court.",
    backstory="A diverse group of citizens sworn to impartially evaluate the evidence and follow the judge's instructions on the law.",
    verbose=False,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    memory=True,
)

prosecutor = Agent(
    role="District Attorney",
    goal="Present the case against the accused on behalf of the state, adhering to ethical standards and seeking justice, not merely convictions.",
    backstory="An experienced prosecutor dedicated to upholding the law and protecting public safety through fair and ethical prosecution.",
    verbose=False,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    memory=True,
)

defense_attorney = Agent(
    role="Defense Counsel",
    goal="Zealously represent the accused, ensuring their constitutional rights are protected and presenting the strongest possible defense.",
    backstory="A skilled attorney committed to the principle that every accused person deserves a vigorous defense and a fair trial.",
    verbose=False,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    memory=True,
)

def process_killer(killer):
    get_judge = Task(
        description=f"""
        As the presiding judge in the case of {killer['Name']}, accused of {killer['Proven victims']} proven murders:
        1. Maintain order and decorum in the courtroom throughout the trial.
        2. Make rulings on the admissibility of evidence and objections raised by counsel.
        3. Provide clear instructions to the jury on the applicable laws and their duty.
        4. If the defendant is found guilty, consider all relevant factors and determine an appropriate sentence within the bounds of the law.
        5. Deliver a clear and concise judgment, explaining the reasoning behind your decision.
        
        Your final statement should include:
        "Based on [key factors], the court sentences the defendant to [specific sentence]."
        """,
        expected_output="A comprehensive report on the trial proceedings, including key rulings, jury instructions, and if applicable, a clearly reasoned sentencing decision.",
        agent=judge,
    )

    get_jury = Task(
        description=f"""
        As jurors in the case of {killer['Name']}, accused of {killer['Proven victims']} proven murders:
        1. Pay close attention to all evidence and testimony presented during the trial.
        2. Follow the judge's instructions on the law and your responsibilities as jurors.
        3. Deliberate as a group, considering only the evidence presented in court.
        4. Reach a unanimous decision on whether the prosecution has proven guilt beyond a reasonable doubt.
        5. Deliver your verdict to the court without any additional commentary or recommendations.
        
        Your response should be limited to:
        "We, the jury, find the defendant [guilty/not guilty] of [specific charges]."
        """,
        expected_output="A clear, concise verdict on each charge, without any additional explanation or sentencing recommendations.",
        agent=jury,
    )

    get_prosecutor = Task(
        description=f"""
        As the prosecutor in the case against {killer['Name']}, accused of {killer['Proven victims']} proven murders:
        1. Present the state's case, introducing evidence and examining witnesses.
        2. Make clear and persuasive opening and closing arguments.
        3. Anticipate and respond to defense strategies.
        4. Ensure all actions comply with legal and ethical standards.
        5. If a guilty verdict is reached, recommend an appropriate sentence based on the law and the specific circumstances of the case.
        
        Provide a summary of your key arguments and evidence presented, and if applicable, your sentencing recommendation.
        """,
        expected_output="A concise summary of the prosecution's case, including key evidence and arguments, and if relevant, a sentencing recommendation.",
        agent=prosecutor,
    )

    get_defense_attorney = Task(
        description=f"""
        As the defense attorney for {killer['Name']}, accused of {killer['Proven victims']} proven murders:
        1. Vigorously defend your client's rights throughout the trial process.
        2. Challenge the prosecution's evidence and arguments.
        3. Present any exculpatory evidence or mitigating factors.
        4. Make persuasive opening and closing statements.
        5. If your client is found guilty, advocate for the most favorable sentence possible given the circumstances.
        
        Provide a summary of your defense strategy, key arguments, and if applicable, your position on sentencing.
        """,
        expected_output="A concise summary of the defense's case, including key arguments and evidence presented, and if relevant, arguments for leniency in sentencing.",
        agent=defense_attorney,
    )

    crew_judge = Crew(
        agents=[judge],
        tasks=[get_judge],
        verbose=2,
    )

    crew_jury = Crew(
        agents=[judge, jury],
        tasks=[get_judge, get_jury],
        verbose=2,
    )

    crew_prosecutor = Crew(
        agents=[judge, jury, prosecutor],
        tasks=[get_judge, get_jury, get_prosecutor],
        verbose=2,
    )

    crew = Crew(
        agents=[judge, jury, prosecutor, defense_attorney],
        tasks=[get_judge, get_jury, get_prosecutor, get_defense_attorney],
        verbose=2,
    )

    try:
        logger.info(f"Processing results for {killer['Name']}")

        # Execute each crew and save results
        results_judge = crew_judge.kickoff()
        logger.info("Judge results obtained")
        if isinstance(results_judge, list) and len(results_judge) > 0:
            save_individual_results(killer['Name'], "Presiding Judge", results_judge[0].raw_output if hasattr(results_judge[0], 'raw_output') else str(results_judge[0]))
        else:
            logger.warning("Unexpected judge results format")
            save_individual_results(killer['Name'], "Presiding Judge", str(results_judge))

        results_jury = crew_jury.kickoff()
        logger.info("Jury results obtained")
        if isinstance(results_jury, list) and len(results_jury) > 1:
            save_individual_results(killer['Name'], "Jury Panel", results_jury[1].raw_output if hasattr(results_jury[1], 'raw_output') else str(results_jury[1]))
        else:
            logger.warning("Unexpected jury results format")
            save_individual_results(killer['Name'], "Jury Panel", str(results_jury))

        results_prosecutor = crew_prosecutor.kickoff()
        logger.info("Prosecutor results obtained")
        if isinstance(results_prosecutor, list) and len(results_prosecutor) > 2:
            save_individual_results(killer['Name'], "District Attorney", results_prosecutor[2].raw_output if hasattr(results_prosecutor[2], 'raw_output') else str(results_prosecutor[2]))
        else:
            logger.warning("Unexpected prosecutor results format")
            save_individual_results(killer['Name'], "District Attorney", str(results_prosecutor))

        # Execute full crew to get defense attorney results
        results = crew.kickoff()
        logger.info("Full crew results obtained")
        
        # Save defense attorney results
        if isinstance(results, list):
            defense_result = next((r for r in results if hasattr(r, 'agent') and r.agent.role == "Defense Counsel"), None)
            if defense_result:
                save_individual_results(killer['Name'], "Defense Counsel", defense_result.raw_output if hasattr(defense_result, 'raw_output') else str(defense_result))
            else:
                logger.warning("Defense Counsel results not found in list")
                save_individual_results(killer['Name'], "Defense Counsel", "Defense Counsel results not available")
        else:
            logger.warning("Unexpected full crew results format")
            save_individual_results(killer['Name'], "Defense Counsel", str(results))

        logger.info(f"All individual reports saved for {killer['Name']}")
        
        return "All reports generated and saved successfully."
    except Exception as e:
        logger.error(f"Error in process_killer for {killer['Name']}: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return f"Error processing {killer['Name']}: {str(e)}"

def save_individual_results(killer_name, role, content):
    try:
        directory = "criminal_reports"
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")
        
        filename = f"{directory}/{killer_name.replace(' ', '_')}_{role.lower().replace(' ', '_')}_report.md"
        
        logger.info(f"Attempting to save file: {filename}")
        
        with open(filename, "w", encoding='utf-8') as f:
            f.write(f"# {role} Report for {killer_name}\n\n")
            f.write(content)
        
        logger.info(f"Successfully saved {role} report for {killer_name} in {filename}")
        
        # Verify file was created
        if os.path.exists(filename):
            logger.info(f"Verified: File {filename} exists")
        else:
            logger.error(f"File verification failed: {filename} does not exist")
    
    except Exception as e:
        logger.error(f"Error in save_individual_results for {killer_name}, {role}: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")

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
        else:
            logger.warning(f"Error occurred while processing {killer['Name']}: {result}")
            sentences.append("Error")
        
    except Exception as e:
        logger.error(f"Unexpected error processing {killer['Name']}: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sentences.append("Error")

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

# Print detailed results
for killer, sentence, victims in zip(selected_killers['Name'], sentences, selected_killers['Proven victims']):
    victim_count = safe_int(victims)
    print(f"{killer} (Proven victims: {victim_count}): {sentence}")

logger.info("Script execution completed")
print(f"Log file saved as: {log_file_name}")