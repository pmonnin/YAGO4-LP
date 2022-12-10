import argparse
import csv
import math
import pickle

import SPARQLWrapper
import tqdm


def main():
    parser = argparse.ArgumentParser(prog="get_rel_triples", description="Get triples of relations of interest")
    parser.add_argument("--relations", dest="relations_file", help="Relations of interest", required=True)
    parser.add_argument("--batches", dest="batches", help="Number of batches for entities appearing in triples of "
                                                          "relations of interest", required=True, type=int)
    parser.add_argument("--triples", dest="triples", help="Output file for triples of relations of interest",
                        required=True)
    parser.add_argument("--rel_3si", dest="rel_3si", help="Output file for subpredicates, superpredicates, inverses, "
                                                          "and symmetric predicates of relations of interest",
                        required=True)
    parser.add_argument("--entities", dest="entities", help="Output file for entities appearing in triples of relations"
                                                            " of interest", required=True)
    args = parser.parse_args()

    yago_endpoint = SPARQLWrapper.SPARQLWrapper(
        "https://yago-knowledge.org/sparql/query"
    )
    yago_endpoint.setReturnFormat(SPARQLWrapper.JSON)

    triples = dict()
    rel_3si = dict()
    rel_3si["sub_predicates"] = dict()
    rel_3si["sup_predicates"] = dict()
    rel_3si["inverse_predicates"] = dict()
    rel_3si["symmetric_predicates"] = set()
    entities = set()
    relations = []

    with open(args.relations_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader)
        for r in csvreader:
            relations.append([r[0], r[1], r[2], int(r[3]), r[4] == "True"])

    for r in tqdm.tqdm(relations):
        if r[4]:
            # Test symmetry
            yago_endpoint.setQuery(f"""
                ASK 
                WHERE
                {{
                    <{r[0]}> a owl:SymmetricProperty .
                }}
                """)
            results = yago_endpoint.queryAndConvert()

            if results['boolean']:
                rel_3si["symmetric_predicates"].add(r[0])

            # Get inverse predicates
            yago_endpoint.setQuery(f"""
                SELECT DISTINCT ?inverse
                WHERE
                {{
                    {{ ?inverse owl:inverseOf <{r[0]}> . }}
                    UNION
                    {{ <{r[0]}> owl:inverseOf ?inverse . }}
                }}
                """)
            results = yago_endpoint.queryAndConvert()

            rel_3si["inverse_predicates"][r[0]] = set()
            for inv in results["results"]["bindings"]:
                rel_3si["inverse_predicates"][r[0]].add(inv["inverse"]["value"])

            # Get subpredicates
            yago_endpoint.setQuery(f"""
                SELECT DISTINCT ?subpredicate
                WHERE
                {{
                    ?subpredicate rdfs:subPropertyOf+ <{r[0]}> .
                }}
                """)
            results = yago_endpoint.queryAndConvert()

            rel_3si["sub_predicates"][r[0]] = set()
            for subp in results["results"]["bindings"]:
                rel_3si["sub_predicates"][r[0]].add(subp["subpredicate"]["value"])

            # Get superpredicates
            yago_endpoint.setQuery(f"""
                SELECT DISTINCT ?suppredicate
                WHERE
                {{
                    <{r[0]}> rdfs:subPropertyOf+ ?suppredicate.
                }}
                """)
            results = yago_endpoint.queryAndConvert()

            rel_3si["sup_predicates"][r[0]] = set()
            for supp in results["results"]["bindings"]:
                rel_3si["sup_predicates"][r[0]].add(supp["suppredicate"]["value"])

            # Get triples
            yago_endpoint.setQuery(f"""
                SELECT DISTINCT ?s ?o
                WHERE
                {{
                    ?s <{r[0]}> ?o.
                    FILTER(isURI(?o)) .
                }}
                """)
            results = yago_endpoint.queryAndConvert()

            triples[r[0]] = set()
            for t in results["results"]["bindings"]:
                triples[r[0]].add((t["s"]["value"], t["o"]["value"]))
                entities.add(t["s"]["value"])
                entities.add(t["o"]["value"])

    pickle.dump(triples, open(args.triples, "wb"))
    pickle.dump(rel_3si, open(args.rel_3si, "wb"))

    entities_batches = []
    entities = list(entities)
    entities_per_batch = math.ceil(len(entities) / args.batches)
    for i in range(0, args.batches):
        entities_batches.append(entities[i * entities_per_batch:min((i + 1) * entities_per_batch, len(entities))])

    pickle.dump(entities_batches, open(args.entities, "wb"))


if __name__ == '__main__':
    main()
