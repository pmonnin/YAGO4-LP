import argparse
import csv
import pickle

import tqdm


def main():
    parser = argparse.ArgumentParser(prog="merge_additional_triples", description="Merge additional triples")
    parser.add_argument("--additional_triples", dest="additional_triples", help="Files containing additional triples",
                        required=True, nargs="+")
    parser.add_argument("--output_triples", dest="output_triples", help="File to store merged additional triples",
                        required=True)
    parser.add_argument("--output_additional_rels", dest="output_additional_rels", help="File to store information for "
                                                                                        "additional relations involved "
                                                                                        "in triples", required=True)
    args = parser.parse_args()

    additional_triples = set()
    for f in tqdm.tqdm(args.additional_triples):
        triples = pickle.load(open(f, "rb"))
        additional_triples = additional_triples.union(triples)

    relations = set()
    for t in additional_triples:
        relations.add(t[1])

    pickle.dump(additional_triples, open(args.output_triples, "wb"))
    with open(args.output_additional_rels, 'w') as output_additional_rels:
        csvwriter = csv.writer(output_additional_rels, delimiter=",")
        csvwriter.writerow(["Predicate", "To keep"])
        for r in relations:
            csvwriter.writerow([r, "True"])


if __name__ == '__main__':
    main()
