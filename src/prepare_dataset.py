import argparse
import csv
import math
import pickle
import random


def build_train_valid_test_sets(rel_triples, additional_triples, rel_3si):
    train_set = set()
    valid_set = set()
    test_set = set()

    for r in rel_triples:
        triples = [(s, r, o) for (s, o) in rel_triples[r]]
        train_upper_bound = math.ceil(0.70 * len(triples))
        valid_upper_bound = math.ceil(0.85 * len(triples))

        train_set |= set(triples[0:train_upper_bound])
        valid_set |= set(triples[train_upper_bound+1:valid_upper_bound])
        test_set |= set(triples[valid_upper_bound+1:len(triples)])

    train_set |= additional_triples

    # Avoid leakage
    for r in rel_triples:
        # Detect all inverses of r, its subpredicates, or its superpredicates
        invr = set(rel_3si["inverse_predicates"][r])

        if r in rel_3si["symmetric_predicates"]:
            invr.add(r)

        for subp in rel_3si["sub_predicates"][r]:
            if subp in rel_3si["symmetric_predicates"]:
                invr.add(subp)

            if subp in rel_3si["inverse_predicates"]:
                invr.add(set(rel_3si["inverse_predicates"][subp]))

        for supp in rel_3si["sup_predicates"][r]:
            if supp in rel_3si["symmetric_predicates"]:
                invr.add(supp)

            if supp in rel_3si["inverse_predicates"]:
                invr.add(set(rel_3si["inverse_predicates"][supp]))

        # Detect all super and subpredicates of r
        subpr = set(rel_3si["sub_predicates"][r]).union(set(rel_3si["sup_predicates"][r]))

        # Remove potential inverse triples
        for t in test_set:
            if t[1] == r:
                for inv in invr:
                    train_set.discard((t[2], inv, t[0]))
                    valid_set.discard((t[2], inv, t[0]))
                for p in subpr:
                    train_set.discard((t[0], p, t[2]))
                    valid_set.discard((t[0], p, t[2]))

        for t in valid_set:
            if t[1] == r:
                for inv in invr:
                    train_set.discard((t[2], inv, t[0]))
                    test_set.discard((t[2], inv, t[0]))
                for p in subpr:
                    train_set.discard((t[0], p, t[2]))
                    test_set.discard((t[0], p, t[2]))

        for t in train_set:
            if t[1] == r:
                for inv in invr:
                    valid_set.discard((t[2], inv, t[0]))
                    test_set.discard((t[2], inv, t[0]))
                for p in subpr:
                    valid_set.discard((t[0], p, t[2]))
                    test_set.discard((t[0], p, t[2]))

    train_set = list(train_set)
    random.shuffle(train_set)
    valid_set = list(valid_set)
    random.shuffle(valid_set)
    test_set = list(test_set)
    random.shuffle(test_set)

    return train_set, valid_set, test_set


def save_set_uris_to_text(set_uris, file_path):
    with open(file_path, "w") as file:
        for t in set_uris:
            file.write(f"""<{t[0]}> <{t[1]}> <{t[2]}> .\n""")


def save_set_ids_to_text(set_ids, file_path):
    with open(file_path, "w") as file:
        for t in set_ids:
            file.write(f"""{t[0]}\t{t[1]}\t{t[2]}\n""")


def build_relation_ids(additional_triples, rel_triples):
    relations = {r for _, r, _ in additional_triples}
    relations |= set(rel_triples.keys())
    relations = list(relations)
    random.shuffle(relations)

    i = 0
    rel2id = dict()
    id2rel = dict()
    for r in relations:
        rel2id[r] = i
        id2rel[i] = r
        i += 1

    return rel2id, id2rel


def build_entity_ids(entity_types):
    entities = {e for e in entity_types}
    entities = list(entities)
    random.shuffle(entities)

    i = 0
    ent2id = dict()
    id2ent = dict()
    for e in entities:
        ent2id[e] = i
        id2ent[i] = e
        i += 1

    return ent2id, id2ent


def build_class_ids(entity_types, superclasses, offset):
    types = set(superclasses.keys())
    types.union({t for t2 in superclasses.values() for t in t2})
    types.union({t for t2 in entity_types.values() for t in t2})
    types = list(types)
    random.shuffle(types)

    i = offset + 1
    class2id = dict()
    id2class = dict()

    for t in types:
        class2id[t] = i
        id2class[i] = t
        i += 1

    return class2id, id2class


def save_dict_to_text(to_save, file_path):
    with open(file_path, "w") as file:
        for k, v in to_save.items():
            if isinstance(v, list):
                for v2 in v:
                    file.write(str(k) + "\t" + str(v2) + "\n")
            else:
                file.write(str(k) + "\t" + str(v) + "\n")


def convert_set_to_ids(triple_uris, ent2id, rel2id):
    triple_ids = list()

    for t in triple_uris:
        triple_ids.append((ent2id[t[0]], rel2id[t[1]], ent2id[t[2]]))

    return triple_ids


def convert_dict_to_k_v_ids(to_convert, k2id, v2id):
    converted = dict()

    for k, v in to_convert.items():
        converted[k2id[k]] = [v2id[v2] for v2 in v]

    return converted


def inverse_dict(to_inverse):
    inverse = dict()

    for k, v in to_inverse.items():
        for v2 in v:
            if v2 not in inverse:
                inverse[v2] = set()

            if k not in inverse[v2]:
                inverse[v2].add(k)

    for k in inverse.keys():
        inverse[k] = list(inverse[k])

    return inverse


def keep_direct_hierarchy(class2allsuperclasses):
    class2directsuperclasses = {k: set(v) for k, v in class2allsuperclasses.items()}

    for k in class2directsuperclasses:
        for k2 in class2allsuperclasses[k]:
            class2directsuperclasses[k] -= set(class2allsuperclasses[k2])

        class2directsuperclasses[k] = list(class2directsuperclasses[k])

    return class2directsuperclasses


def get_number_of_entities_from_triple_set(triple_set):
    entities = {t[0] for t in triple_set}
    entities.union(t[2] for t in triple_set)

    return len(entities)


def get_number_of_relations_from_triple_set(triple_set):
    return len({t[1] for t in triple_set})


def get_number_of_classes_from_triple_set(triple_set, ent2classes):
    types = set()

    for t in triple_set:
        types |= set(ent2classes[t[0]])
        types |= set(ent2classes[t[2]])

    return len(types)


def compute_statistics(train_set_uris, valid_set_uris, test_set_uris, ent2classes, file_path):
    sets = [
        ("Total", train_set_uris + valid_set_uris + test_set_uris),
        ("Train", train_set_uris),
        ("Valid", valid_set_uris),
        ("Test", test_set_uris)
    ]

    with open(file_path, "w") as file:
        file.write("# YAGO4-65k statistics\n")

        file.write("| Set | Triples | Entities | Relations | Types |\n")
        file.write("|-------|---------|----------|-----------|-------|\n")
        for label, triple_set in sets:
            file.write(f"|{label}"
                       f"|{len(triple_set)}"
                       f"|{get_number_of_entities_from_triple_set(triple_set)}"
                       f"|{get_number_of_relations_from_triple_set(triple_set)}"
                       f"|{get_number_of_classes_from_triple_set(triple_set, ent2classes)}"
                       f"|\n")


def main():
    parser = argparse.ArgumentParser(prog="prepare_dataset", description="Prepare the final dataset from intermediary "
                                                                         "files")
    parser.add_argument("--entity_types", dest="entity_types", help="Files containing entity types", required=True)
    parser.add_argument("--rel_triples", dest="rel_triples", help="Files containing triples with relations of interest",
                        required=True)
    parser.add_argument("--additional_triples", dest="additional_triples", help="Files containing additional triples "
                                                                                "for the training set", required=True)
    parser.add_argument("--superclasses", dest="superclasses", help="Files containing superclasses", required=True)
    parser.add_argument("--rel_3si", dest="rel_3si", help="Files containing inverse and symmetry of relations of "
                                                          "interest", required=True)
    parser.add_argument("--relations", dest="relations_file", help="Relations of interest", required=True)
    parser.add_argument("--output", dest="output", help="Output folder for dataset files", required=True)
    args = parser.parse_args()

    entity_types = pickle.load(open(args.entity_types, "rb"))
    rel_triples = pickle.load(open(args.rel_triples, "rb"))
    additional_triples = pickle.load(open(args.additional_triples, "rb"))
    superclasses = pickle.load(open(args.superclasses, "rb"))
    rel_3si = pickle.load(open(args.rel_3si, "rb"))

    output = args.output
    if output[-1] != "/":
        output += "/"

    # Build & save relation IDs
    rel2id, id2rel = build_relation_ids(additional_triples, rel_triples)
    save_dict_to_text(rel2id, output + "rel2id.txt")
    save_dict_to_text(id2rel, output + "id2rel.txt")
    pickle.dump(rel2id, open(output + "rel2id.pkl", "wb"))
    pickle.dump(id2rel, open(output + "id2rel.pkl", "wb"))

    # Build & save entity IDs
    ent2id, id2ent = build_entity_ids(entity_types)
    save_dict_to_text(ent2id, output + "ent2id.txt")
    save_dict_to_text(id2ent, output + "id2ent.txt")
    pickle.dump(ent2id, open(output + "ent2id.pkl", "wb"))
    pickle.dump(id2ent, open(output + "id2ent.pkl", "wb"))

    # Build & save class IDs
    class2id, id2class = build_class_ids(entity_types, superclasses, max(id2ent.keys()))
    save_dict_to_text(class2id, output + "class2id.txt")
    save_dict_to_text(id2class, output + "id2class.txt")
    pickle.dump(class2id, open(output + "class2id.pkl", "wb"))
    pickle.dump(id2class, open(output + "id2class.pkl", "wb"))

    # Build & save train / valid / test sets
    train_set_uris, valid_set_uris, test_set_uris = build_train_valid_test_sets(rel_triples, additional_triples,
                                                                                rel_3si)

    save_set_uris_to_text(train_set_uris, output + "train.txt")
    pickle.dump(train_set_uris, open(output + "train.pkl", "wb"))

    save_set_uris_to_text(valid_set_uris, output + "valid.txt")
    pickle.dump(valid_set_uris, open(output + "valid.pkl", "wb"))

    save_set_uris_to_text(test_set_uris, output + "test.txt")
    pickle.dump(test_set_uris, open(output + "test.pkl", "wb"))

    # Build & save train / valid / test ID sets
    train_set_ids = convert_set_to_ids(train_set_uris, ent2id, rel2id)
    valid_set_ids = convert_set_to_ids(valid_set_uris, ent2id, rel2id)
    test_set_ids = convert_set_to_ids(test_set_uris, ent2id, rel2id)
    save_set_ids_to_text(train_set_ids, output + "trainIDs.txt")
    pickle.dump(train_set_ids, open(output + "trainIDs.pkl", "wb"))
    save_set_ids_to_text(valid_set_ids, output + "validIDs.txt")
    pickle.dump(valid_set_ids, open(output + "validIDs.pkl", "wb"))
    save_set_ids_to_text(test_set_ids, output + "testIDs.txt")
    pickle.dump(test_set_ids, open(output + "testIDs.pkl", "wb"))

    # Build & save ent2class
    ent2classes = {k: list(v) for k, v in entity_types.items()}
    ent_id2class_ids = convert_dict_to_k_v_ids(ent2classes, ent2id, class2id)
    save_dict_to_text(ent2classes, output + "ent2classes.txt")
    pickle.dump(ent2classes, open(output + "ent2classes.pkl", "wb"))
    save_dict_to_text(ent_id2class_ids, output + "entID2classIDs.txt")
    pickle.dump(ent_id2class_ids, open(output + "entID2classIDs.pkl", "wb"))

    # Build & save class2ent
    class2entities = inverse_dict(ent2classes)
    class_id2ent_ids = convert_dict_to_k_v_ids(class2entities, class2id, ent2id)
    save_dict_to_text(class2entities, output + "class2entities.txt")
    pickle.dump(class2entities, open(output + "class2entities.pkl", "wb"))
    save_dict_to_text(class_id2ent_ids, output + "classID2entIDs.txt")
    pickle.dump(class_id2ent_ids, open(output + "classID2entIDs.pkl", "wb"))

    # Build & save r2dom and r2range
    r2dom = dict()
    r_id2dom_id = dict()
    r2range = dict()
    r_id2range_id = dict()

    with open(args.relations_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader)
        for r in csvreader:
            if r[4] == "True":
                r2dom[r[0]] = r[1]
                r_id2dom_id[rel2id[r[0]]] = class2id[r[1]]
                r2range[r[0]] = r[2]
                r_id2range_id[rel2id[r[0]]] = class2id[r[2]]

    save_dict_to_text(r2dom, output + "r2dom.txt")
    pickle.dump(r2dom, open(output + "r2dom.pkl", "wb"))
    save_dict_to_text(r_id2dom_id, output + "rID2domID.txt")
    pickle.dump(r_id2dom_id, open(output + "rID2domID.pkl", "wb"))
    save_dict_to_text(r2range, output + "r2range.txt")
    pickle.dump(r2range, open(output + "r2range.pkl", "wb"))
    save_dict_to_text(r_id2range_id, output + "rID2rangeID.txt")
    pickle.dump(r_id2range_id, open(output + "rID2rangeID.pkl", "wb"))

    # Build & save class2allsuperclasses
    class2allsuperclasses = {k: list(v) for k, v in superclasses.items()}
    class_id2allsuperclass_ids = convert_dict_to_k_v_ids(class2allsuperclasses, class2id, class2id)
    save_dict_to_text(class2allsuperclasses, output + "class2allsuperclasses.txt")
    pickle.dump(class2allsuperclasses, open(output + "class2allsuperclasses.pkl", "wb"))
    save_dict_to_text(class_id2allsuperclass_ids, output + "classID2allsuperclassIDs.txt")
    pickle.dump(class_id2allsuperclass_ids, open(output + "classID2allsuperclassIDs.pkl", "wb"))

    # Build & save class2directsuperclasses
    class2directsuperclasses = keep_direct_hierarchy(class2allsuperclasses)
    class_id2directsuperclass_ids = convert_dict_to_k_v_ids(class2directsuperclasses, class2id, class2id)
    save_dict_to_text(class2directsuperclasses, output + "class2directsuperclasses.txt")
    pickle.dump(class2directsuperclasses, open(output + "class2directsuperclases.pkl", "wb"))
    save_dict_to_text(class_id2directsuperclass_ids, output + "classID2directsuperclassIDs.txt")
    pickle.dump(class_id2directsuperclass_ids, open(output + "classID2directsuperclassIDs.pkl", "wb"))

    # Compute & save statistics
    compute_statistics(train_set_uris, valid_set_uris, test_set_uris, ent2classes, output + "statistics.md")


if __name__ == '__main__':
    main()
