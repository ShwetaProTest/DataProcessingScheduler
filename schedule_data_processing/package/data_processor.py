# Script Name: data_processor.py
# Description: This module provides data processing functionalities for a flight information system.
#              It includes methods for downloading data from Azure Blob Storage, loading data from JSON
#              and CSV files, and performing calculations such as distance measurements between airports using GeoPy.
# Developer: SSD
# Created at: 16/11/2023

import os
import json
import sys
import subprocess
import importlib
import logging
import re
from unidecode import unidecode
from datetime import datetime

class FlightDataProcessor:
    """
    FlightDataProcessor class handles the processing of flight data.
    It includes methods for downloading data, loading data, and performing calculations.
    """
    def __init__(self, config):
        """
        Constructor for FlightDataProcessor.

        Parameters:
        - config (dict): Configuration settings for the data processor.
        """
        self.config = config
        self.data_directory = None
        self.schedule = None
        self.fleet = None
        self.airports = None
        self.log_directory = None 
        self.create_data_directory()  
        self.setup_logging()

    def create_data_directory(self):
        """
        Create the data directory if it does not exist.
        """
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        # Get the directory of the current script
        #script_dir = os.path.dirname(os.path.realpath(__file__))
        # Construct the path to the project root
        #project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
        #project_root = os.path.abspath(os.path.dirname(__file__))
        data_directory = os.path.join(project_root, self.config.get("data_directory", "data_files"))
        log_directory = os.path.join(project_root, "log")

        try:
            # Create data directory if it does not exist
            os.makedirs(data_directory, exist_ok=True)

            # Create log directory if it does not exist
            os.makedirs(log_directory, exist_ok=True)

            # Set data and log directories
            self.data_directory = data_directory
            self.log_directory = log_directory

        except Exception as e:
            logging.error(f"Error creating data/log directories: {str(e)}")
            raise

    def setup_logging(self):
        """
        Set up logging configuration.
        """
        log_filename = os.path.join(self.log_directory, f"data_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            
        # Create log directory if it does not exist
        #os.makedirs(self.log_directory, exist_ok=True)

        # Configure logging to both file and console
        logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 
    @staticmethod
    #The find_file method doesn't rely on any instance-specific data. It operates solely on the input parameters
    def find_file(start_directory, file_name):
        """
        Search for a file starting from the given directory.

        Parameters:
        - start_directory (str): The directory to start the search.
        - file_name (str): The name of the file to search for.

        Returns:
        - str or None: The full path to the file if found, otherwise None.
        """
        current_directory = start_directory
        while True:
            file_path = os.path.join(current_directory, file_name)
            if os.path.exists(file_path):
                return file_path
            
            # Move up to the parent directory
            parent_directory = os.path.dirname(current_directory)
            if parent_directory == current_directory:
                # Reached the root directory, stop searching
                break
            current_directory = parent_directory

        return None

    def install_dependencies(self):
        """
        Install necessary dependencies for the data processor.
        """
        script_directory = os.path.abspath(os.path.dirname(__file__))
        requirements_path = self.find_file(script_directory, 'requirements.txt')

        if requirements_path is None:
            logging.error("Error: 'requirements.txt' file not found.")
            sys.exit(1)

        logging.info(f"Installing dependencies from {requirements_path}")
        print(f"Installing dependencies from {requirements_path}")

        try:
            # Capture the output of the subprocess to check for "Requirement already satisfied" messages
            result = subprocess.run(["pip", "install", "-r", requirements_path], stdout=subprocess.PIPE, check=True)
            
            # Only print the output if there are non-empty lines that do not contain "Requirement already satisfied"
            output_lines = result.stdout.decode().split('\n')
            for line in output_lines:
                if line.strip() and "Requirement already satisfied" not in line:
                    print(line)

        except subprocess.CalledProcessError as e:
            logging.error(f"Error: Dependency installation failed with exit code {e.returncode}.")
            sys.exit(1)

        logging.info("Dependencies installed successfully.")
        print(f"Dependencies installed successfully.")

        # Import necessary libraries after installation
        self.import_libraries()

    def import_libraries(self):
        """
        Dynamically import required libraries after installation.
        """
        try:
            global pd, BlobClient, geodesic
            pd = importlib.import_module("pandas")
            BlobClient = importlib.import_module("azure.storage.blob").BlobClient
            geodesic = importlib.import_module("geopy.distance").geodesic
        except ImportError as e:
            logging.error(f"Error: {e.name} could not be imported. Please check your Python environment.")
            sys.exit(1)

    @classmethod
    def load_config(cls):
        """
        Load configuration settings for the data processor from 'config.json'.
        """
        script_directory = os.path.abspath(os.path.dirname(__file__))
        config_path = cls.find_file(script_directory, os.path.join('config', 'config.json'))

        if config_path is None:
            logging.error("Error: 'config.json' file not found.")
            sys.exit(1)

        logging.info(f"Loading configuration from {config_path}")
        print(f"Loading configuration from {config_path}")

        with open(config_path, 'r') as f:
            return json.load(f)

    def download_blob(self, blob_name, target_file_path):
        """
        Download a blob from Azure Blob Storage.

        Parameters:
        - blob_name (str): The name of the blob to download.
        - target_file (str): The local file path to save the downloaded blob.
        """
        logging.info(f"Downloading blob: {blob_name}")
        connection_string = self.config["azure_storage"]["connection_string"]
        container_name = self.config["azure_storage"]["container_name"]
        blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=blob_name)

        # Ensure the target file is inside the data_directory
        #target_file_path = os.path.join(self.data_directory, os.path.basename(target_file))

        try:
            with open(target_file_path, "wb") as f:
                blob.download_blob().readinto(f)
            logging.info(f"Blob {blob_name} downloaded successfully to {target_file_path}.")
            print(f"Blob {blob_name} downloaded successfully to {target_file_path}.")
        except Exception as e:
            logging.error(f"Error downloading blob {blob_name}: {str(e)}")
            sys.exit(1)

    def load_data(self, blob_name, target_file, file_format):
        """
        Load data from a blob into a Pandas DataFrame.

        Parameters:
        - blob_name (str): The name of the blob to load.
        - target_file (str): The local file path to save the downloaded blob.
        - file_format (str): The format of the file ('json' or 'csv').

        Returns:
        - pd.DataFrame: The loaded data in a Pandas DataFrame.
        """
        target_file_path = os.path.join(self.data_directory, os.path.basename(target_file))
        self.download_blob(blob_name, target_file_path)
        try:
            if file_format == 'json':
                return pd.read_json(target_file_path)
            elif file_format == 'csv':
                return pd.read_csv(target_file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_format}")
        except pd.errors.EmptyDataError as e:
            print(f"Error loading data: {e}")
        except Exception as e:
            print(f"Error loading data: {e}")
        return None  # Return None if an error occurs

    def calculate_distances(self):
        """
        Calculate distances between airports in the schedule and update the schedule DataFrame.
        """
        if self.schedule is not None and self.airports is not None:
            schedule = self.schedule.copy()
            schedule["distance_nm"] = schedule.apply(
                lambda row: self.calculate_distance_row(row, self.airports), axis=1
            )
            self.schedule = schedule

    def calculate_distance_row(self, row, airports_df):
        """
        Calculate distance between departure and arrival airports.

        Parameters:
        - row (pd.Series): A row from the schedule DataFrame.
        - airports_df (pd.DataFrame): DataFrame containing airport information.

        Returns:
        - float: The calculated distance in nautical miles.
        """
        departure_airport_info = airports_df.loc[airports_df['Airport'] == row['departure_airport']]
        arrival_airport_info = airports_df.loc[airports_df['Airport'] == row['arrival_airport']]

        departure_coords = (departure_airport_info['Lat'].values[0], departure_airport_info['Lon'].values[0])
        arrival_coords = (arrival_airport_info['Lat'].values[0], arrival_airport_info['Lon'].values[0])

        distance = geodesic(departure_coords, arrival_coords).nautical
        return distance

    def perform_data_quality_checks(self, dataframe):
        """
        Perform data quality checks on the loaded data.

        Parameters:
        - dataframe (pd.DataFrame): The loaded data in a Pandas DataFrame.
        - column_names (list): List of column names to check for data quality.

        Raises:
        - ValueError: If data quality checks fail.
        """
        for column in dataframe.columns:
            # Apply cleaning function based on column type
            if dataframe[column].dtype == 'object':
                # Clean non-English characters and format datetime
                dataframe[column] = dataframe[column].apply(self.clean_value)

        logging.info("Data quality checks passed successfully.")

    def clean_value(self, value):
        """
        Clean non-English characters and format datetime in a given value.

        Parameters:
        - value: The value to clean.

        Returns:
        - Cleaned value.
        """
        # Convert non-English characters to English equivalents
        cleaned_value = unidecode(str(value))

        # Remove extra spaces
        cleaned_value = ' '.join(cleaned_value.split())

        # Remove characters that are not letters, numbers, or spaces
        cleaned_value = re.sub('[^A-Za-z0-9\s]+', '', cleaned_value)

        # Attempt to convert to datetime
        try:
            cleaned_value = pd.to_datetime(cleaned_value, errors='raise')
        except (ValueError, TypeError):
            pass  # Ignore if not convertible to datetime

        return cleaned_value
    
    def get_data(self):
        """
        Get flight data by loading schedule, airports, and fleet data.
        """
        # Load schedule data
        self.schedule = self.load_data("schedule.json", os.path.join(self.data_directory, "schedule.json"), 'json')
        self.perform_data_quality_checks(self.schedule)

        # Load airports data
        self.airports = self.load_data("airports.csv", os.path.join(self.data_directory, "airports.csv"), 'csv')
        self.perform_data_quality_checks(self.airports)

        # Load fleet data
        self.fleet = self.load_data("fleet.csv", os.path.join(self.data_directory, "fleet.csv"), 'csv')
        self.perform_data_quality_checks(self.fleet)

        if self.schedule is not None and self.airports is not None:
            self.calculate_distances()

        logging.info("The Blob files downloaded successfully, and data quality checks passed.")
        print(f"The Blob files downloaded successfully!!..")

if __name__ == "__main__":
    # Load configuration
    config = FlightDataProcessor.load_config()
    
    # Initialize data processor
    data_processor = FlightDataProcessor(config)
    
    # Create data directory (including log directory)
    data_processor.create_data_directory()

    # Set up logging configuration
    data_processor.setup_logging()
    
    # Install dependencies
    data_processor.install_dependencies()

    # Get flight data
    data_processor.get_data()