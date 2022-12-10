import argparse
import pickle

import SPARQLWrapper
import tqdm


def main():
    parser = argparse.ArgumentParser(prog="get_entity_types", description="Get types of entities in batch")
    parser.add_argument("--batch", dest="batch", help="Number of entity batch to query", required=True, type=int)
    parser.add_argument("--entities", dest="entities", help="File containing batches of entities", required=True)
    parser.add_argument("--entity_types", dest="entity_types", help="Output file for entity types", required=True)
    args = parser.parse_args()

    yago_endpoint = SPARQLWrapper.SPARQLWrapper(
        "https://yago-knowledge.org/sparql/query"
    )
    yago_endpoint.setReturnFormat(SPARQLWrapper.JSON)
    yago_endpoint.setTimeout(10)

    entities = pickle.load(open(args.entities, "rb"))
    entity_types = dict()

    # Query types of each entity
    for e in tqdm.tqdm(entities[args.batch]):
        done = False

        while not done:
            try:
                yago_endpoint.setQuery(f"""
                    SELECT DISTINCT ?type
                    WHERE
                    {{
                        <{e}> rdf:type/rdfs:subClassOf* ?type .
                    }}
                    """)
                results = yago_endpoint.queryAndConvert()

                entity_types[e] = set()
                for r in results["results"]["bindings"]:
                    entity_types[e].add(r["type"]["value"])

                done = True

            except Exception as exception:
                print(exception)

    pickle.dump(entity_types, open(args.entity_types, "wb"))


if __name__ == '__main__':
    main()
