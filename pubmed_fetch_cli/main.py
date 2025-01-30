import argparse
import sys

from pubmed_fetch_cli.fetch_filter import Pebmed_Fether

def main():
    parser = argparse.ArgumentParser(description='Fetch research papers from PubMed')
    parser.add_argument("query", help="PubMed query to search")
    parser.add_argument("-f", "--file", help="Output CSV filepath")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable Debug mode")
    args = parser.parse_args()

    try:
        fetcher = Pebmed_Fether()

        if args.debug:
            print(f"searching papers from PubMed for query:{args.query}")

        ids = fetcher.search_papers(args.query)
        if args.debug:
            print(f"found {len(ids)} papers")
            print(f"Found IDs: {ids}")

        xml_data = fetcher.fetch_research_papers(ids)
        papers = fetcher.parse_papers(xml_data)
        # print("papers are", papers)
        if args.file:
            fetcher.write_to_csv(papers, args.file)
            print(f"Results written to {args.file} file")
        else:
            for paper in papers:
                print(paper)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.debug:
            raise



if __name__ == "__main__":
    main()







