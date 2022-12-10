import argparse
import pickle

import SPARQLWrapper
import tqdm


def main():
    parser = argparse.ArgumentParser(prog="get_additional_triples", description="Get additional triples of entities "
                                                                                "appearing in triples of relations of "
                                                                                "interest to enrich the train set")
    parser.add_argument("--batch", dest="batch", help="Number of entity batch to query", required=True, type=int)
    parser.add_argument("--entities", dest="entities", help="File for entities appearing in triples of relations of "
                                                            "interest", required=True)
    parser.add_argument("--triples", dest="triples", help="Output file for triples", required=True)
    args = parser.parse_args()

    yago_endpoint = SPARQLWrapper.SPARQLWrapper(
        "https://yago-knowledge.org/sparql/query"
    )
    yago_endpoint.setReturnFormat(SPARQLWrapper.JSON)
    yago_endpoint.setTimeout(10)

    entities = pickle.load(open(args.entities, "rb"))

    additional_triples = set()

    for e in tqdm.tqdm(entities[args.batch]):
        # Query direct adjacency
        done = False

        while not done:
            try:
                yago_endpoint.setQuery(f"""
                            SELECT ?p ?o
                            WHERE
                            {{
                                <{e}> ?p ?o . 
                                FILTER(isURI(?o)) .
                            }} LIMIT 5
                            """)

                results = yago_endpoint.queryAndConvert()

                for r in results["results"]["bindings"]:
                    additional_triples.add((e, r["p"]["value"], r["o"]["value"]))

                done = True

            except Exception as exception:
                print(exception)

        # Query inverse adjacency
        done = False

        while not done:
            try:
                yago_endpoint.setQuery(f"""
                            SELECT ?s ?p
                            WHERE
                            {{
                                ?s ?p <{e}> .
                                FILTER(isURI(?s)) .
                            }} LIMIT 5
                            """)

                results = yago_endpoint.queryAndConvert()
                for r in results["results"]["bindings"]:
                    additional_triples.add((r["s"]["value"], r["p"]["value"], e))

                done = True

            except Exception as exception:
                print(exception)

    pickle.dump(additional_triples, open(args.triples, "wb"))


if __name__ == '__main__':
    main()
