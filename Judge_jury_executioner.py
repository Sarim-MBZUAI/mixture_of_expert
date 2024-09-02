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

# Load the CSV file
df = pd.read_csv('./data/serial_killers_data.csv')

# Randomly select 3 serial killers
selected_killers = df.sample(n=15)
os.environ["GROQ_API_KEY"] = get_groq_api_key()
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")
def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 'Unknown'
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
        description=f"Preside over the court proceedings for {killer['Name']}, accused of {killer['Proven victims']} proven murders. Ensure fair trial, and provide final judgment based on the law and evidence presented.",
        expected_output="A detailed judgment including the verdict and sentencing.",
        agent=Judge,
    )
    
    get_jury = Task(
        description=f"""
        Listen to all evidence and arguments presented in court for {killer['Name']}'s case. Deliberate as a group to reach a verdict on the facts of the case. Provide a clear decision on guilt or innocence based solely on the evidence presented.
        """,
        expected_output="A clear verdict (guilty or not guilty) with a brief explanation of the decision.",
        agent=jury,
    )

    get_executioner = Task(
        description=f"""
        Based on the Judge's sentencing for {killer['Name']} and following all legal and ethical guidelines, outline the steps to carry out the court's decision. Focus on maintaining the dignity and rights of the convicted while ensuring the sentence is properly executed.
        """,
        expected_output="A detailed plan for carrying out the sentence in an ethical and lawful manner.",
        agent=executioner,
    )

    crew = Crew(
        agents=[Judge, jury, executioner],
        tasks=[get_judge, get_jury, get_executioner],
        verbose=2,
    )
    
    try:
        results = crew.kickoff()
        
        markdown_report = f"""
## Judge's Decision

{results}

## Jury's Verdict

{results}

## Executioner's Plan

{results}
"""
        
        return markdown_report
    except Exception as e:
        error_report = f"""
## Error Occurred

An error occurred while processing {killer['Name']}:

```
{str(e)}
```

Further processing was halted due to this error.
"""
        return error_report

def save_reports(killer_name, report_content):
    directory = "criminal_reports"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = f"{directory}/{killer_name.replace(' ', '_')}_report.md"
    
    with open(filename, "w", encoding='utf-8') as f:
        f.write(f"# Report for {killer_name}\n\n")
        f.write(report_content)
    
    print(f"Report saved for {killer_name} in {filename}")


def analyze_sentence(result):
    final_output = result['final_output'].lower()
    
    if "death" in final_output:
        sentence = "Death Sentence"
    elif "life" in final_output:
        sentence = "Life Sentence"
    else:
        sentence = "Other Sentence"
    
    analysis = f"""
    Sentence Analysis:
    Determined sentence: {sentence}
    """
    print(analysis)
    
    return sentence


# Process each selected killer
import traceback

# Process each selected killer
results = []
sentences = []
for _, killer in selected_killers.iterrows():
    print(f"\nProcessing killer: {killer['Name']}")
    try:
        result = process_killer(killer)
        
        save_reports(killer['Name'], result)
        
        # Determine sentence (you may need to adjust this based on the new output format)
        sentence = "Other Sentence"  # Default
        if "death" in result.lower():
            sentence = "Death Sentence"
        elif "life" in result.lower():
            sentence = "Life Sentence"
        
        sentences.append(sentence)
        
        print(f"Sentence for {killer['Name']}: {sentence}")
        
    except Exception as e:
        print(f"Error processing {killer['Name']}: {str(e)}")
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