import csv
from typing import List, Dict

import requests
import xml.etree.ElementTree as ET



class Pebmed_Fether:
    """Fethces research papers from PubMed API."""

    Base_Search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    Base_fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def __init__(self, api_key: str=None):
        """Initialising PubMedFetcher
        :param api_key: Optional API key for PubMed API
        """
        self.api_key = api_key


    def search_papers(self, query: str, retmax: int = 100) -> list[str]:
        """Research Papers
        :param query: Query string
        :param retmax: Maximum number of results to return
        :return: List of PubMed ID's"""

        params = {
            "db": "pubmed",
            "retmax": retmax,
            "term": query,
            "retmode": "json",
        }

        if self.api_key:
            params["api_key"] = self.api_key


        response = requests.get(self.Base_Search_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])


    def fetch_research_papers(self, idlist: List[str]) -> str:
        """Fetch research papers from PubMed API
        :param ids: List of PubMed ID's
        :return: xml data as string"""

        params = {
            "db": "pubmed",
            "retmode": "xml",
            "id": ",".join(idlist),
        }

        print("params are :", params)
        if self.api_key:
            params["api_key"] = self.api_key

        response = requests.get(self.Base_fetch_url, params=params)
        print(response.status_code)
        response.raise_for_status()
        return response.text

    def parse_papers(self, xml_data: str) -> list[Dict]:
        """Parse PubMed paper details from XML data
        :param xml_data: XML data as string
        :return: List of paper details"""


        root = ET.fromstring(xml_data)
        papers = []



        for article in root.findall(".//PubMedArticle"):
            pubmed_id = article.find(".//PubMedID").text if article.find(".//PubMedID") is not None else "N/A"
            title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "N/A"
            publication_date = "N/A"
            pub_date_elem = article.find(".//PubDate")
            if pub_date_elem:
                year = pub_date_elem.find(".//Year").text if pub_date_elem.find(".//Year") is not None else ""
                month = pub_date_elem.find(".//Month").text if pub_date_elem.find(".//Month") is not None else ""
                day = pub_date_elem.find(".//Day").text if pub_date_elem.find(".//Day") is not None else ""
                publication_date = f"{year}-{month}-{day}".strip("-")


            non_academic_authors = []
            company_affiliations = []
            corresponding_author_email = "N/A"

            for author in article.findall(".//Author"):
                affiliations = [aff.text for aff in author.findall("AffiliationInfo/Affiliation") if aff.text]
                if any("pharma" in aff.lower() or "biotech" in aff.lower() for aff in affiliations):
                    company_affiliations.extend(aff for aff in affiliations if "pharma" in aff.lower() or "biotech" in aff.lower())
                    non_academic_authors.append(author.find("LastName").text if author.find("LastName") is not None else "Unknown Author")


                papers.append({
                    "PubmedID": pubmed_id,
                    "Title": title,
                    "Publication Date": publication_date,
                    "Non-academic Author(s)": non_academic_authors,
                    "Company Affiliation(s)": company_affiliations,
                    "Corresponding Author Email": corresponding_author_email,
                })


        return papers

    def write_to_csv(self, data, file_path: str) -> None:
        """save paper details to csv file"""

        fieldnames = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)













