import argparse
import json
import os
import sys
from pathlib import Path

from mongo.mongo_configs import MongoConnectionConfig
from mongo.mongo_connector import MongoConnector
from patent_finder.patent_finder_mongo_db import PatentFinderMongoDB
from utils.common_utils import add_patents_to_df, save_df_to_csv, load_data_from_csv


def find(config_path: str):
    """
    Main function to process the input configuration and run the pipeline.

    Args:
        config_path (str): Path to the configuration JSON file.
    """
    # Step 1: Load configuration
    if not os.path.exists(config_path):
        print(f"❌ Error: Configuration file not found at {config_path}")
        sys.exit(1)

    print("📁 Loading configuration...")
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    # Step 2: Extract paths and MongoDB settings
    mongo_config = MongoConnectionConfig()
    mongo_config.load_from_json(config["MONGO_CONNECTION"])
    report_folder = config["REPORT_FOLDER"]
    data_file = config["DATA_FOLDER"]

    print("📂 Ensuring report folder exists...")
    Path(report_folder).mkdir(parents=True, exist_ok=True)

    # Step 4: Load input SMILES data
    print("📄 Loading input SMILES data...")
    try:
        smiles_df = load_data_from_csv(data_file)
    except Exception as e:
        print(f"❌ Error loading SMILES data from {data_file}: {e}")
        sys.exit(1)

    # Step 5: Initialize MongoDB connector
    print("🔗 Initializing MongoDB connection...")
    try:
        mongo_connector = MongoConnector(mongo_config)
        mongo_connector.connect()
        print("✅ MongoDB connection established successfully!")
    except Exception as e:
        print(f"❌ Error initializing MongoDB connection: {e}")
        sys.exit(1)

    # Step 6: Initialize Patent Finder
    print("🔍 Initializing Patent Finder...")
    patent_finder = PatentFinderMongoDB(smiles_df, mongo_connector)

    # Step 7: Find patents in parallel
    print("📜 Finding patents in parallel...")
    try:
        patents = patent_finder.find_all_patents()
    except Exception as e:
        print(f"❌ Error finding patents: {e}")
        sys.exit(1)

    # Step 8: Add patents to DataFrame
    print("📊 Adding patents to DataFrame...")
    try:
        result_df = add_patents_to_df(smiles_df, patents)
    except Exception as e:
        print(f"❌ Error adding patents to DataFrame: {e}")
        sys.exit(1)

    # Step 9: Save output to CSV
    output_file = os.path.join(report_folder, "patents_report.csv")
    print("💾 Saving output to CSV...")
    try:
        save_df_to_csv(result_df, output_file)
        print(f"✅ Report saved successfully to {output_file} 🎉")
    except Exception as e:
        print(f"❌ Error saving report to {output_file}: {e}")
        sys.exit(1)

    # Step 10: Close MongoDB connection
    finally:
        print("🔒 Closing MongoDB connection...")
        mongo_connector.close()
        print("✅ MongoDB connection closed.")


def main():
    """
    Main function to run the pipeline.
    """
    args = parse_args()
    find(args.config_path)


def parse_args():
    parser = argparse.ArgumentParser(description="Better Molecules Patent Finder")
    parser.add_argument(
        '--config-path',
        type=str,
        required=True,
        help='Path to the configuration file'
    )
    return parser.parse_args()
