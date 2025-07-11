# PubMed Paper Fetcher

## 🎯 Purpose
CLI tool to fetch PubMed papers with non-academic (pharma/biotech) author affiliations.

## 📦 Setup Instructions
```bash
poetry install
poetry run get-papers-list "cancer immunotherapy" --file results.csv --debug
```

## 📊 Output Columns
- PubmedID
- Title
- Publication Date
- Non-academic Author(s)
- Company Affiliation(s)
- Corresponding Author Email

## 🤖 LLM Assistance
This project was built using ChatGPT (GPT-4) to help with:
- Designing the code structure
- Writing heuristics for detecting pharma/biotech affiliations
- Optimizing and debugging

## 🧪 Sample Run
```bash
poetry run get-papers-list "covid vaccine" --file covid_results.csv
```