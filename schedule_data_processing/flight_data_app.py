# Script Name: flight_data_app.py
# Description: This module serves as the main application for the Flight Data Lookup and Merge system. It orchestrates
#              the interaction between the user interface, data processing modules, and external dependencies. The
#              application provides functionalities for looking up detailed information about flights and merging
#              datasets to generate comprehensive reports. It leverages the FlightDataProcessor class and incorporates
#              a command-line interface for user interaction.
# Developer: SSD
# Created at: 16-11-2023

import os
import sys
import json
import logging
import argparse
from datetime import datetime
#from schedule_data_processing.package.data_processor import FlightDataProcessor
from package.data_processor import FlightDataProcessor

class FlightLookupApp:

    def __init__(self, config):
        """
        Initializes the FlightLookupApp with the provided configuration.

        Args:
            config (dict): The configuration dictionary.
        """
        # Determine project root dynamically based on the location of requirements.txt
        project_root = self.find_project_root()

        # Update the configuration with the project root
        config["project_root"] = project_root

        # Use absolute paths for directories and files
        config["log_directory"] = os.path.join(project_root, config["log_directory"])
        log_filename = f"data_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        config["log_filepath"] = os.path.join(config["log_directory"], log_filename)

        # Create the log directory if it doesn't exist
        os.makedirs(config["log_directory"], exist_ok=True)

        # Use absolute paths for other important directories
        config["data_directory"] = os.path.join(project_root, config["data_directory"])
        config["result_directory"] = os.path.join(project_root, config["result_directory"])
        config["config_directory"] = os.path.join(project_root, config["config_directory"])

        # Update the initialization of FlightDataProcessor
        self.data_processor = FlightDataProcessor(config)
        self.data_processor.import_libraries()
        self.data_processor.get_data()

        # Store the configuration in the instance
        self.config = config

    def find_project_root(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        while current_directory:
            if "requirements.txt" in os.listdir(current_directory):
                return current_directory
            current_directory = os.path.dirname(current_directory)
        raise FileNotFoundError("Could not find project root with requirements.txt file.")

    def perform_operation(self, mode, flight_numbers=None):
        """
        Perform flight lookup or merge operation based on the specified mode.

        Args:
            mode (str): The mode of operation, either 'lookup' or 'merge'.
            flight_numbers (list): A list of flight numbers for lookup operation.

        Returns:
            str: JSON representation of results for lookup, or the path of the merged result file for merge.

        Raises:
            ValueError: If an unsupported mode is provided.
        """
        try:
            logging.info(f"Performing {mode} operation.")
            print(f"Performing {mode} operation.")
            # self.data_processor.import_libraries()
            # self.data_processor.get_data()
            schedule, fleet, airports = (
                self.data_processor.schedule, self.data_processor.fleet, self.data_processor.airports
            )
            self.data_processor.calculate_distances()

            # Ensure flight_numbers is a list of separate flight numbers
            flight_numbers = flight_numbers[0].split(",") if flight_numbers else None

            if mode == "lookup":
                if flight_numbers is None:
                    raise ValueError("For 'lookup' mode, at least one flight number must be provided.")

                results = []
                for flight_number in flight_numbers:
                    try:
                        result = self.lookup_flight(flight_number, schedule, fleet)
                        results.append(result)
                    except ValueError as e:
                        # Handle the error and append a dictionary with "error" key
                        results.append({"error": str(e)})

                return json.dumps(results, default=str)

            elif mode == "merge":
                result_path = self.merge_data(schedule, fleet, airports)
                return result_path

            else:
                error_message = f"Unsupported mode: {mode}. Supported modes are 'lookup' and 'merge'."
                logging.error(error_message)
                raise ValueError(error_message)

        except Exception as e:
            logging.exception(f"An unexpected error occurred: {str(e)}")
            raise

    def lookup_flight(self, flight_number, schedule, fleet):
        """
        Looks up detailed information about a specific flight.

        Args:
            flight_number (str): The flight number to look up.
            schedule (DataFrame): The schedule data.
            fleet (DataFrame): The fleet data.

        Returns:
            dict: Dictionary containing information about the flight.

        Raises:
            ValueError: If the flight number is not found.
        """
        self.modify_fleet_dataframe(fleet)
        joined = schedule.merge(fleet, on="aircraft_registration")
        result = joined[joined.flight_number == flight_number]

        if result.empty:
            error_message = f"Flight {flight_number} not found."
            logging.error(error_message)
            error_result = {"error": error_message}
            return error_result
            #raise ValueError(error_message)

        logging.info(f"Successfully looked up flight {flight_number}.")

        result = result.to_dict(orient="records")[0]  # Extract the first (and only) record from the list

        keys_to_delete = ["F", "C", "E", "M", "RangeLower", "RangeUpper", "Reg"]
        for key in keys_to_delete:
            if key in result:
                del result[key]

        result["total_seats"] = str(result["Total"])
        del result["Total"]
        result["distance_nm"] = str(result["distance_nm"])

        # Convert timestamp to string
        result["scheduled_departure_time"] = str(result["scheduled_departure_time"])
        result["scheduled_takeoff_time"] = str(result["scheduled_takeoff_time"])
        result["scheduled_landing_time"] = str(result["scheduled_landing_time"])
        result["scheduled_arrival_time"] = str(result["scheduled_arrival_time"])

        return result

    def modify_fleet_dataframe(self, fleet):
        """
        Modifies the fleet DataFrame by adding an 'aircraft_registration' column.

        Args:
            fleet (DataFrame): The fleet data.
        """
        fleet["aircraft_registration"] = fleet["Reg"]

    def merge_data(self, schedule, fleet, airports):
        """
        Modifies the fleet DataFrame by adding an 'aircraft_registration' column.

        Args:
            schedule (DataFrame: The schedule data.
            fleet (DataFrame): The fleet data.
            airports (DataFrame): The airports data.
        """
        try:
            self.modify_fleet_dataframe(fleet)
            # Rename 'aircraft_registration' column in fleet to avoid suffix
            fleet = fleet.rename(columns={'aircraft_registration': 'aircraft_registration_fleet'})

            # Merge Schedule and Fleet based on aircraft_registration
            joined = schedule.merge(fleet, left_on="aircraft_registration", right_on="aircraft_registration_fleet", how="inner")

            if joined.empty:
                logging.error("No matches found during merge.")
                raise ValueError("No matches found during merge.")

            logging.info("Successfully performed merge operation.")

            # Merge with Airports for arrival_airport only
            joined = joined.merge(airports, left_on="arrival_airport", right_on="Airport", how="inner", suffixes=("", "_arrival"))

            # Merge with Airports for departure_airport only
            joined = joined.merge(airports, left_on="departure_airport", right_on="Airport", how="inner", suffixes=("", "_departure"))

            # Drop redundant or not-required columns
            columns_to_drop = [
                "aircraft_registration_fleet",
                "Reg",
                # Add more columns if needed
            ]
            joined.drop(columns=columns_to_drop, inplace=True)

            # Drop additional columns with '_arrival' and '_departure' suffix
            columns_to_drop_arrival = [
                col for col in joined.columns if col.endswith(("_arrival", "_departure")) and col not in ["arrival_airport", "departure_airport"]
            ]
            joined.drop(columns=columns_to_drop_arrival, inplace=True)

            # Output to CSV
            output_columns = list(joined.columns)
            output_directory = self.config["result_directory"]
            output_path = os.path.join(output_directory, "Flight_results.csv")

            # Create the directory if it doesn't exist
            os.makedirs(output_directory, exist_ok=True)

            joined.to_csv(output_path, columns=output_columns, index=False)

            #logging.info(f"Content of the response:\n{joined[output_columns].to_dict(orient='list')}")
            print(f"Merge process completed! Result file created in : {output_path}")
            return ""

        except Exception as e:
            logging.exception(f"An unexpected error occurred in merge_data: {str(e)}")
            raise
        
    def main(self, args):
        parser = argparse.ArgumentParser(description="Flight Data Lookup and Merge")
        parser.add_argument("mode", choices=["lookup", "merge"], help="Mode of operation")

        # Flight numbers are only required for the "lookup" mode
        if "lookup" in args:
            parser.add_argument("flight_numbers", nargs="+", help="Comma-separated flight numbers for lookup mode")

        args = parser.parse_args(args[1:])

        try:
            result = self.perform_operation(args.mode, getattr(args, "flight_numbers", None))
            print(result)
        except ValueError as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Determine project root dynamically based on the location of requirements.txt
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Determine the configuration file path based on the project root
    config_file_path = os.path.join(project_root, 'config', 'config.json')

    try:
        with open(config_file_path) as config_file:
            config = json.load(config_file)
            config["project_root"] = project_root  # Add the project_root to the config
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at {config_file_path}")

    app = FlightLookupApp(config)
    app.main(sys.argv)