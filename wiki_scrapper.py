import requests
from bs4 import BeautifulSoup
import csv
import sys

def scrape_wikipedia_tables():
    url = "https://en.wikipedia.org/wiki/List_of_serial_killers_by_number_of_victims"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all tables with both 'wikitable' and 'sortable' classes
    tables = soup.find_all('table', class_=lambda x: x and 'wikitable' in x and 'sortable' in x)
    
    if not tables:
        print("Could not find any tables with both 'wikitable' and 'sortable' classes.")
        sys.exit(1)
    
    print(f"Found {len(tables)} relevant tables. Extracting data...")

    all_data = []
    for i, table in enumerate(tables):
        print(f"Processing table {i+1}...")
        
        # Extract table headers
        headers = [header.text.strip() for header in table.find_all('th')]
        
        # Extract table rows
        for row in table.find_all('tr')[1:]:  # Skip the header row
            cells = row.find_all('td')
            if len(cells) == len(headers):
                row_data = [cell.text.strip() for cell in cells]
                all_data.append(row_data)
    
    if not all_data:
        print("No data found in the tables. The page structure might have changed.")
        sys.exit(1)
    
    # Write data to CSV file
    try:
        with open('serial_killers_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Assuming all tables have the same headers
            writer.writerows(all_data)
        print("Data has been successfully scraped and saved to 'serial_killers_data.csv'")
        print(f"Total number of entries: {len(all_data)}")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    scrape_wikipedia_tables()