from typing import List, Dict
import requests
import xml.etree.ElementTree as ET

def fetch_pubmed_ids(query: str, retmax: int = 20) -> List[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmax": retmax, "retmode": "json"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["esearchresult"]["idlist"]

def fetch_pubmed_details(ids: List[str]) -> str:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "pubmed", "id": ",".join(ids), "retmode": "xml"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text

def is_non_academic(affiliation: str) -> bool:
    if not affiliation: return False
    keywords = ["pharma", "biotech", "inc", "ltd", "corp", "gmbh", "pvt", "company"]
    academic_terms = ["university", "institute", "college", "school", "hospital", "lab"]
    affil = affiliation.lower()
    return any(k in affil for k in keywords) and not any(a in affil for a in academic_terms)

def parse_papers(xml_data: str) -> List[Dict]:
    root = ET.fromstring(xml_data)
    results = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year") or "Unknown"
        authors = article.findall(".//Author")
        non_acad_authors = []
        company_affils = []
        email = ""

        for author in authors:
            aff = author.findtext("AffiliationInfo/Affiliation") or ""
            if is_non_academic(aff):
                name = (author.findtext("ForeName") or "") + " " + (author.findtext("LastName") or "")
                non_acad_authors.append(name.strip())
                company_affils.append(aff.strip())
            if "@" in aff and not email:
                email = aff[aff.find("@") - 15:aff.find("@") + 15]

        results.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": "; ".join(non_acad_authors),
            "Company Affiliation(s)": "; ".join(company_affils),
            "Corresponding Author Email": email
        })

    return results