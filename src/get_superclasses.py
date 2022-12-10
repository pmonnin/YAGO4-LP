import argparse
import pickle

import SPARQLWrapper
import tqdm


def main():
    parser = argparse.ArgumentParser(prog="get_superclasses", description="Get superclasses of all types")
    parser.add_argument("--types", dest="types", help="File storing all types involved", required=True)
    parser.add_argument("--superclasses", dest="superclasses", help="File storing superclasses of each type",
                        required=True)
    args = parser.parse_args()

    yago_endpoint = SPARQLWrapper.SPARQLWrapper(
        "https://yago-knowledge.org/sparql/query"
    )
    yago_endpoint.setReturnFormat(SPARQLWrapper.JSON)
    yago_endpoint.setTimeout(10)

    all_types = pickle.load(open(args.types, "rb"))
    superclasses = dict()

    for t in tqdm.tqdm(all_types):
        done = False

        while not done:
            try:
                yago_endpoint.setQuery(f"""
                            SELECT DISTINCT ?superclass
                            WHERE
                            {{
                                <{t}> rdfs:subClassOf+ ?superclass .
                            }}
                            """)
                results = yago_endpoint.queryAndConvert()

                superclasses[t] = set()
                for r in results["results"]["bindings"]:
                    superclasses[t].add(r["superclass"]["value"])

                done = True

            except Exception as exception:
                print(exception)

    pickle.dump(superclasses, open(args.superclasses, "wb"))


if __name__ == '__main__':
    main()
