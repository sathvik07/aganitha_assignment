# aganitha_assignment / pubmed_fetch



This file contains the code for the Take-Home Exercise.

This code has features like:

1. intially it sends API request to PubMed with retmax set to 100. and then extarcts all IDs from the response.
2. Then it is passed to fetch the content of those IDs and gets the response in xml format.
3. The xml format will be checked with given problem statement condition and then the papers will be added to list.
4. list of papers will be written to .csv file.
5. This code also creates command line arguemnts.


Methods and their working summary:

1. It creates the command line arguemnts like "query" -> for PubMed query to search, "-f" -> to mention output CSV filepath and "-d" -> to enable Debug mode.
2. class **Pebmed_Fetcher** has methods like search_papers, fetch_research_papers, parse_papers, write_to_csv.
3. **search_paper** method will sends an API request with custom parameters and extracts all the IDs.
4. **fetch_research_papers** by using the IDs list, will fetch all the research papers of those IDs but in XML format.
5. **parse_papers** will basically will check the data for the condition given in problem statement and adds the data to a papers list.
6. **write_to_scv** will take the data and saves it to the csv file with matching fieldnames.

End Result:
1. i was able to fetch papers from PubMed API and check for papers with authors affiliated with pharmaceutical or biotech companies, and then saves the results in a given CSV filename.
2. i was also able to create command line arguements as per the problem statement requirment.


---- If you have a moment, could you go through my code to ensure everything is in line with the expectations? I'd love to hear any thoughts you have.



# PubMed Fetcher

This program fetches research papers from PubMed based on a user-specified query, filters papers with authors affiliated with pharmaceutical or biotech companies, and saves the results in a CSV file.

## Requirements

- Python 3.8+
- Poetry for dependency management

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd pubmed-fetch
    ```

2. Install dependencies using Poetry:
    ```bash
    poetry install
    ```

## Usage

To fetch papers and save results to a CSV file:
```bash
poetry run wanted_papers "pharmaceutical research" -f result_papers.csv


