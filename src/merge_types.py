import argparse
import pickle


def main():
    parser = argparse.ArgumentParser(prog="merge_types", description="Merge types that have been queried by batch")
    parser.add_argument("--entity_types", dest="entity_types", help="Files containing entity types", required=True,
                        nargs="+")
    parser.add_argument("--output_entity_types", dest="output_entity_types", help="File to store merged entity types",
                        required=True)
    parser.add_argument("--output_types", dest="output_types", help="File storing all types involved",
                        required=True)
    args = parser.parse_args()

    entity_types = dict()
    all_types = set()
    for f in args.entity_types:
        for e, t in pickle.load(open(f, "rb")).items():
            if e not in entity_types:
                entity_types[e] = t
            else:
                entity_types[e] = entity_types[e].union(t)

            all_types = all_types.union(t)

    pickle.dump(entity_types, open(args.output_entity_types, "wb"))
    pickle.dump(all_types, open(args.output_types, "wb"))


if __name__ == '__main__':
    main()
