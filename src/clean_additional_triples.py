import argparse
import csv
import math
import pickle

import tqdm


def main():
    parser = argparse.ArgumentParser(prog="clean_additional_triples", description="Clean additional triples by removing"
                                                                                  "excluded predicates and also output "
                                                                                  "their entities for type querying")
    parser.add_argument("--additional_triples", dest="additional_triples", help="File containing additional triples",
                        required=True)
    parser.add_argument("--additional_rels", dest="additional_rels", help="File storing information for additional "
                                                                          "relations involved in triples",
                        required=True)
    parser.add_argument("--output_triples", dest="output_triples", help="File to store cleaned additional triples",
                        required=True)
    parser.add_argument("--batches", dest="batches", help="Number of batches for entities appearing in triples",
                        required=True, type=int)
    parser.add_argument("--entities", dest="entities", help="File for entities appearing in triples", required=True)
    args = parser.parse_args()

    additional_triples = pickle.load(open(args.additional_triples, "rb"))

    additional_rels = set()
    with open(args.additional_rels, "r") as file:
        csvreader = csv.reader(file, delimiter=",")
        next(csvreader)

        for r in csvreader:
            # Only keep relations set to True
            if r[1] == "True":
                additional_rels.add(r[0])

    clean_triples = set()
    cleaned_entities = set()

    # Only keep triples whose relation is in additional_rels
    for t in tqdm.tqdm(additional_triples):
        if t[1] in additional_rels:
            clean_triples.add(t)
            cleaned_entities.add(t[0])
            cleaned_entities.add(t[2])

    pickle.dump(clean_triples, open(args.output_triples, "wb"))

    # Prepare entity batches for type querying
    entities_batches = []
    entities = list(cleaned_entities)
    entities_per_batch = math.ceil(len(entities) / args.batches)
    for i in range(0, args.batches):
        entities_batches.append(entities[i * entities_per_batch:min((i + 1) * entities_per_batch, len(entities))])

    pickle.dump(entities_batches, open(args.entities, "wb"))


if __name__ == '__main__':
    main()
