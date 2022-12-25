import argparse
import csv

import SPARQLWrapper
import tqdm


def main():
    parser = argparse.ArgumentParser(prog="get_rel_info", description="Get domain, range, and number of triples of "
                                                                      "relations")
    parser.add_argument("--output", dest="output", help="Output file", required=True)
    args = parser.parse_args()

    yago_endpoint = SPARQLWrapper.SPARQLWrapper(
        "https://yago-knowledge.org/sparql/query"
    )
    yago_endpoint.setReturnFormat(SPARQLWrapper.JSON)

    relations = []

    try:
        yago_endpoint.setQuery("""
            SELECT ?pred ?domain ?range
            WHERE
            {
                ?pred rdfs:domain ?domain .
                ?pred rdfs:range ?range .
            }
            """)

        results = yago_endpoint.queryAndConvert()

        for r in results["results"]["bindings"]:
            relations.append([r["pred"]["value"], r["domain"]["value"], r["range"]["value"], 0, 0])

        for r in tqdm.tqdm(relations):
            yago_endpoint.setQuery(f"""
                SELECT (COUNT(*) AS ?tripleNumber) WHERE {{
                    [] <{r[0]}> [] .
                }} 
                """)

            results = yago_endpoint.queryAndConvert()
            r[3] = results["results"]["bindings"][0]["tripleNumber"]["value"]

    except Exception as e:
        print(e)

    with open(args.output, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(["Predicate", "Domain", "Range", "# triples", "In valid/test set"])
        csvwriter.writerows(relations)


if __name__ == '__main__':
    main()
