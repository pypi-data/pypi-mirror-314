import argparse
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter


# Initialize Firebase Admin
def initialize_firestore(certificate_path: str | None = None):
    cred = (
        credentials.Certificate(certificate_path)
        if certificate_path
        else credentials.ApplicationDefault()
    )
    firebase_admin.initialize_app(cred)
    return firestore.client()


# Parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Firestore Query Executor")
    parser.add_argument("--path", required=True, help="Path to Firestore collection")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--set", action="store", help="Set a document")
    group.add_argument("--add", action="store_true", help="Add a document")
    group.add_argument("--update", action="store", help="Update a document")
    group.add_argument("--delete", action="store", help="Delete a document")
    parser.add_argument("--doc", action="store", help="path to document")
    args = parser.parse_args()
    return args


def read_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def execute_update(db: firestore.firestore.Client, args):
    collection = db.collection(args.path)
    # read the document from file path at args.doc
    if args.doc:
        doc = read_json_file(args.doc)
    if args.set:
        return collection.document(args.set).set(doc)
    elif args.add:
        return collection.add(doc)[1].path.split("/")[-1]
    elif args.update:
        return collection.document(args.update).update(doc)
    elif args.delete:
        return collection.document(args.delete).delete()


def main():
    args = parse_arguments()
    db = initialize_firestore()
    results = execute_update(db, args)
    print(results)


if __name__ == "__main__":
    main()
