import typer
from pubmed_paper_fetcher.fetcher import fetch_pubmed_ids, fetch_pubmed_details, parse_papers
import pandas as pd

app = typer.Typer()

@app.command()
def main(query: str, file: str = None, debug: bool = False):
    if debug:
        print(f"Running query: {query}")
    ids = fetch_pubmed_ids(query)
    if debug:
        print(f"Found PubMed IDs: {ids}")
    xml = fetch_pubmed_details(ids)
    papers = parse_papers(xml)
    df = pd.DataFrame(papers)

    if file:
        df.to_csv(file, index=False)
        if debug:
            print(f"Results saved to {file}")
    else:
        print(df.to_string(index=False))

if __name__ == "__main__":
    app()