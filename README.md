# YAGO4-LP

Link prediction datasets based on YAGO4 with the following files in ``YAGO4-22k/``, ``YAGO4-44k/``, ``YAGO4-77k``, ``YAGO4-27k``, and ``YAGO4-19k``:

* ``rel2id.txt``: tab-separated file in which each line associates a relation URI to its equivalent ID
* ``rel2id.pkl``: pickle file containing a dictionary associating a relation URI to its equivalent ID
* ``id2rel.txt``: tab-separated file in which each line associates a relation ID to its equivalent URI
* ``id2rel.pkl``: pickle file containing a dictionary associating a relation ID to its equivalent URI
* ``ent2id.txt``: tab-separated file in which each line associates an entity URI to its equivalent ID
* ``ent2id.pkl``: pickle file containing a dictionary associating an entity URI to its equivalent ID
* ``id2ent.txt``: tab-separated file in which each line associates an entity ID to its equivalent URI
* ``id2ent.pkl``: pickle file containing a dictionary associating an entity ID to its equivalent URI
* ``class2id.txt``: tab-separated file in which each line associates a class URI to its equivalent ID
* ``class2id.pkl``: pickle file containing a dictionary associating a class URI to its equivalent ID
* ``id2class.txt``: tab-separated file in which each line associates a class ID to its equivalent URI
* ``id2class.pkl``: pickle file containing a dictionary associating a class ID to its equivalent URI
* ``train.txt``: train set in which each line is of the form ``<subjectURI> <relationURI> <objectURI> .``
* ``train.pkl``: pickle file containing a list in which each element is a tuple ``(subjectURI, relationURI, objectURI)``
* ``valid.txt``: valid set in which each line is of the form ``<subjectURI> <relationURI> <objectURI> .``
* ``valid.pkl``: pickle file containing a list in which each element is a tuple ``(subjectURI, relationURI, objectURI)``
* ``test.txt``: test set in which each line is of the form ``<subjectURI> <relationURI> <objectURI> .``
* ``test.pkl``: pickle file containing a list in which each element is a tuple ``(subjectURI, relationURI, objectURI)``
* ``trainIDs.txt``: train set in which each line is tab-separated and of the form ``subjectID relationID objectID``
* ``trainIDs.pkl``: pickle file containing a list in which each element is a tuple ``(subjectID, relationID, objectID)``
* ``validIDs.txt``: valid set in which each line is tab-separated and of the form ``subjectID relationID objectID``
* ``validIDs.pkl``: pickle file containing a list in which each element is a tuple ``(subjectID, relationID, objectID)``
* ``testIDs.txt``: test set in which each line is tab-separated and of the form ``subjectID relationID objectID``
* ``testIDs.pkl``: pickle file containing a list in which each element is a tuple ``(subjectID, relationID, objectID)``
* ``ent2classes.txt``: tab-separated file in which each line associates an entity URI to the URI of one of its instantiated classes. Note that instantiated classes are computed taking into account the transitive closure of the instantiation and subsumption relations. 
* ``ent2classes.pkl``: pickle file containing a dictionary associating an entity URI to the list of the URIs of its instantiated classes.  Note that instantiated classes are computed taking into account the transitive closure of the instantiation and subsumption relations.
* ``entID2classIDs.txt``: tab-separated file in which each line associates an entity ID to the ID of one of its instantiated classes. Note that instantiated classes are computed taking into account the transitive closure of the instantiation and subsumption relations.  
* ``entID2classIDs.pkl``: pickle file containing a dictionary associating an entity ID to the list of the IDs of its instantiated classes.  Note that instantiated classes are computed taking into account the transitive closure of the instantiation and subsumption relations.
* ``class2entities.txt``: tab-separated file in which each line associates a class URI to the URI of one of its instances. Note that instances are computed taking into account the transitive closure of the instantiation and subsumption relations.
* ``class2entities.pkl``: pickle file containing a dictionary associating a class URI to the list of the URIs of its instances. Note that instances are computed taking into account the transitive closure of the instantiation and subsumption relations.
* ``classID2entIDs.txt``: tab-separated file in which each line associates a class ID to the ID of one of its instances. Note that instances are computed taking into account the transitive closure of the instantiation and subsumption relations.
* ``classID2entIDs.pkl``: pickle file containing a dictionary associating a class ID to the list of the IDs of its instances. Note that instances are computed taking into account the transitive closure of the instantiation and subsumption relations.
* ``r2dom.txt``: tab-separated file in which each line associates a relation URI to its domain URI
* ``r2dom.pkl``: pickle file containing a dictionary associating a relation UI to its domain URI
* ``rID2domID.txt``: tab-separated file in which each line associates a relation ID to its domain ID
* ``rID2domID.pkl``: pickle file containing a dictionary associating a relation ID to its domain ID
* ``r2range.txt``: tab-separated file in which each line associates a relation URI to its range URI
* ``r2range.pkl``: pickle file containing a dictionary associating a relation URI to its range URI
* ``rID2rangeID.txt``: tab-separated file in which each line associates a relation ID to its range ID
* ``rID2rangeID.pkl``: pickle file containing a dictionary associating a relation ID to its range ID
* ``class2allsuperclasses.txt``: tab-separated file in which each line associates a class URI to the URI of one of all its superclasses (taking into account the transitive closure of the subsumption relation)
* ``class2allsuperclasses.pkl``: pickle file containing a dictionary associating a class URI to the list of the URIs of all its superclasses (taking into account the transitive closure of the subsumption relation)
* ``classID2allsuperclassIDs.txt``: tab-separated file in which each line associates a class ID to the ID of one of all its superclasses (taking into account the transitive closure of the subsumption relation)
* ``classID2allsuperclassIDs.pkl``: pickle file containing a dictionary associating a class ID to the list of the IDs of all its superclasses (taking into account the transitive closure of the subsumption relation)
* ``class2directsuperclasses.txt``: tab-separated file in which each line associates a class URI to the URI of one of its direct superclasses
* ``class2directsuperclasses.pkl``: pickle file containing a dictionary associating a class URI to the list of the URIs of its direct superclasses
* ``classID2directsuperclassIDs.txt``: tab-separated file in which each line associates a class ID to the ID of one of its direct superclasses
* ``classID2directsuperclassIDs.pkl``: pickle file containing a dictionary associating a class ID to the list of the IDs of its direct superclasses
* ``statistics.md``: a file containing statistics for the dataset
* ``additonal_rels.csv``: a CSV file indicating which relations were considered when querying and cleaning additional triples to constitute the train set
* ``yago-relations.csv``: a CSV file containing YAGO relations with their domain, range, number of triples and whether they are considered in the valid/test set

The following commands have been used to build the dataset:

## 1. ``get_rel_info.py``

```python
python src/get_rel_info.py --output data/yago-relations.csv
```

Get domain, range, and number of triples of relations in YAGO4.

Output:
* One CSV file ``yago-relations.csv`` with columns:
  * Predicate: indicating the predicate URI
  * Domain: indicating the predicate domain
  * Range: indicating the predicate range
  * \# triples: indicating the number of triples involving the predicate
  * In valid/test set: number of triples of this relation to add to build the train/valid/test sets in scripts described below

We selected some relations of interest (with their number of triples set > 0 in ``YAGO4-XXk/yago-relations.csv``).

## 2. ``get_rel_triples.py``

```python
python src/get_rel_triples.py --relations data/yago-relations.csv --triples data/triples.pkl --rel_3si data/rel_3si.pkl --batches 5 --entities data/entities_in_rels.pkl
```

Get triples of relations of interest, entities involved in them (split in 5 batches), and information regarding relation inverses, subpredicates, superpredicates and symmetry.

Output:
* One pickle file ``triples.pkl`` containing a dictionary such that
```
triples[predicate] = set(tuple(head1,tail1), tuple(head2,tail2),...)
```
* One pickle file ``rel_3si.pkl`` containing a dictionary such that
```
rel_3si["sub_predicates"][predicate] = set(subpredicate1, subpredicate2, ...) (transitively computed)
rel_3si["sup_predicates"][predicate] = set(suppredicate1, suppredicate2, ...) (transitively computed)
rel_3si["inverse_predicates"][predicate] = set(invpredicate1, ...) 
rel_3si["symmetric_predicates"] = set(symmetricpredicate1, symmetricpredicate2, ...) 
```
* One pickle file ``entitites_in_rels.pkl`` containing a dictionary such that
```
entities_batches[batch number] = list(entity1, entity2, ...)
```

## 3. ``get_additional_triples.py``

```python
python src/get_additional_triples.py --batch 0 --entities data/entities_in_rels.pkl --triples data/additional_triples_b0.pkl
python src/get_additional_triples.py --batch 1 --entities data/entities_in_rels.pkl --triples data/additional_triples_b1.pkl
python src/get_additional_triples.py --batch 2 --entities data/entities_in_rels.pkl --triples data/additional_triples_b2.pkl
python src/get_additional_triples.py --batch 3 --entities data/entities_in_rels.pkl --triples data/additional_triples_b3.pkl
python src/get_additional_triples.py --batch 4 --entities data/entities_in_rels.pkl --triples data/additional_triples_b4.pkl
```

Get additional triples for entities appearing in triples involving the relations of interest. 
These triples will be used to enrich the train set.

Output
* One pickle file ``additional_triples_bN.pkl`` per execution containing a set such that
```
triples = set(tuple(subject1, predicate1, object1), tuple(subject2, predicate2, object2, ...)
```

## 4. ``merge_additional_triples.py``

```python
python src/merge_additional_triples.py --additional_triples data/additional_triples_b* --output_triples data/additional_triples.pkl --output_additional_rels data/additional_rels.csv
```

Merge additional triples batches into one file + output a list of predicates involved in these additional triples for further selection.

Output:
* One pickle file ``additional_triples.pkl`` containing a set such that
```
triples = set(tuple(subject1, predicate1, object1), tuple(subject2, predicate2, object2, ...)
```
* One CSV file ``additional_rels.csv`` with columns:
  * Predicate: the predicate URI
  * To keep: boolean indicate whether this predicate and its triples should be considered in the training set

We used this file to exclude ``rdf:type``, ``owl:sameAs``, and ``schema:image`` to avoid such triples in the train set.

## 5. ``clean_additional_triples.py``

```python
python src/clean_additional_triples.py --additional_triples data/additional_triples.pkl --output_triples data/cleaned_additional_triples.pkl --additional_rels data/additional_rels.csv --batches 5 --entities data/additional_entities.pkl
```

Clean additional triples by removing triples involving a predicate excluded in ``additional_rels.csv``, and extract entities involved in remaining triples for type querying.

Output:
* One pickle file ``cleaned_additional_triples.pkl`` containing a set such that
```
triples = set(tuple(subject1, predicate1, object1), tuple(subject2, predicate2, object2, ...)
```
* One pickle file ``additional_entities.pkl`` containing a dictionary such that
```
entities_batches[batch number] = list(entity1, entity2, ...)
```

## 6. ``query_types.py``

```python
python src/get_entity_types.py --batch 0 --entities data/entities_in_rels.pkl --entity_types data/types_entities_in_rel_b0.pkl
python src/get_entity_types.py --batch 1 --entities data/entities_in_rels.pkl --entity_types data/types_entities_in_rel_b1.pkl
python src/get_entity_types.py --batch 2 --entities data/entities_in_rels.pkl --entity_types data/types_entities_in_rel_b2.pkl
python src/get_entity_types.py --batch 3 --entities data/entities_in_rels.pkl --entity_types data/types_entities_in_rel_b3.pkl
python src/get_entity_types.py --batch 4 --entities data/entities_in_rels.pkl --entity_types data/types_entities_in_rel_b4.pkl
python src/get_entity_types.py --batch 0 --entities data/additional_entities.pkl --entity_types data/types_additional_entities_b0.pkl
python src/get_entity_types.py --batch 1 --entities data/additional_entities.pkl --entity_types data/types_additional_entities_b1.pkl
python src/get_entity_types.py --batch 2 --entities data/additional_entities.pkl --entity_types data/types_additional_entities_b2.pkl
python src/get_entity_types.py --batch 3 --entities data/additional_entities.pkl --entity_types data/types_additional_entities_b3.pkl
python src/get_entity_types.py --batch 4 --entities data/additional_entities.pkl --entity_types data/types_additional_entities_b4.pkl
```

Get all the types (``rdf:type/rdfs:subClassOf*``) of each entity.

Output:
* A pickle file ``entity_types.pkl`` containing a dictionary such that
```
entity_types[entity] = set(type1, type2, ...)
```

## 7. ``merge_types.py``

```python
python src/merge_types.py --entity_types data/types_* --output_entity_types data/entity_types.pkl --output_types data/all_types.pkl
```

Merge batches of types into one dictionary and get all types in a set to query superclasses

Output:
* A pickle file ``entity_types.pkl`` containing a dictionary such that
```
entity_types[entity] = set(type1, type2, ...)
```
* A pickle file ``all_types.pkl`` containing a set such that
```
all_types = set(type1, type2, type3, ...)
```

## 8. ``get_superclasses.py``

```python
python src/get_superclasses.py --types data/all_types.pkl --superclasses data/superclasses.pkl
```

Get superclasses of all types

Output:

* A pickle file ``superclasses.pkl`` containing a dictionary such that
```
superclasses[type1] = set(superclass1, superclass2, superclass3, ...)
```
Note that superclasses are computed taking into account the transitive closure of the subsumption relation

## 9. ``prepare_dataset.py``

```python
python src/prepare_dataset.py --entity_types data/entity_types.pkl --rel_triples data/triples.pkl --additional_triples data/cleaned_additional_triples.pkl --superclasses data/superclasses.pkl --rel_3si data/rel_3si.pkl --relations data/yago-relations.csv --output YAGO4-XXk
```

Build the YAGO4-XXk dataset whose files are described at the beginning of this document.

