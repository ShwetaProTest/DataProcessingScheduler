import unittest
import os
import sys
import json

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to the project root
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))

# Add the project root to the Python path
sys.path.append(project_root)

#import the module
from schedule_data_processing.flight_data_app import FlightLookupApp

class TestCLI(unittest.TestCase):
    """
    A test case for the FlightLookupApp command-line interface.

    This test case includes tests for the lookup and merge functionality.
    """
    def setUp(self):
        """
        Set up the test case.

        This method is called before each test function is executed.
        It initializes the FlightLookupApp instance and required data.
        """
        config_path = os.path.join(project_root, "config", "config.json")
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        self.app_instance = FlightLookupApp(config)
        self.schedule = self.app_instance.data_processor.schedule  
        self.fleet = self.app_instance.data_processor.fleet  
        self.airports = self.app_instance.data_processor.airports

    def generate_expected_result_columns(self):
        return [
            'flight_number',
            'aircraft_registration',
            'departure_airport',
            'arrival_airport',
            'scheduled_departure_time',
            'scheduled_takeoff_time',
            'scheduled_landing_time',
            'scheduled_arrival_time',
            'IATATypeDesignator',
            'TypeName',
            'Hub',
            'Haul',
            'distance_nm',
            'total_seats'
        ]

    def test_lookup(self):
        """
        Test the lookup functionality of the FlightLookupApp.

        This test case iterates through a list of flight numbers,
        performs a lookup for each flight, and asserts the correctness
        of the results.
        """
        flight_numbers = ["ZG2362", "ZG5001", "ZG5002"]  # Add more flight numbers as needed
        expected_result_columns = self.generate_expected_result_columns()

        results = []

        for flight_number in flight_numbers:
            with self.subTest(flight_number=flight_number):
                result = self.app_instance.lookup_flight(flight_number, self.schedule, self.fleet)
                if "error" in result:
                    error_message = f"Flight {flight_number} not found."
                    error_result = {"error": error_message}
                    print(error_result)
                    #print(f"Error for flight {flight_number}: {result['error']}")
                else:
                    for column in expected_result_columns:
                        self.assertIn(column, result, f"Column '{column}' is missing in the result for flight {flight_number}")

                    results.append(result)

        # Print the final list of results
        print(f"All results: {results}")


    # def test_lookup(self):
    #     expected_result = '{"aircraft_registration": "ZGAUI", "departure_airport": "MCO", "arrival_airport": "FRA", "scheduled_departure_time": "2020-01-01 16:05:00", "scheduled_takeoff_time": "2020-01-01 16:15:00", "scheduled_landing_time": "2020-01-02 00:55:00", "scheduled_arrival_time": "2020-01-02 01:05:00", "flight_number": "ZG2362", "IATATypeDesignator": "789", "TypeName": "Boeing 787-9", "Hub": "FRA", "Haul": "LH", "distance_nm": "4122.686732581713","total_seats": "216"}'
    #     expected_result_dict = json.loads(expected_result)  # Convert expected_result to a dictionary
    #     result = self.app_instance.lookup_flight("ZG2362", self.schedule, self.fleet)
    #     self.assertEqual(result, expected_result_dict, f"Expected: {expected_result_dict}, Got: {result}")

    def test_merge(self):
        """
        Test the data merging functionality of the FlightLookupApp.

        This test case checks if the data merging process completes successfully.
        """
        expected_result = ""
        result = self.app_instance.merge_data(self.schedule, self.fleet, self.airports)
        self.assertEqual(result, expected_result, f"Expected: {expected_result}, Got: {result}")

if __name__ == "__main__":
    unittest.main()
