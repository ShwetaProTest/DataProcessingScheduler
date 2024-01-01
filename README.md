# Flight Data Lookup and Merge

## Overview
The Flight Data Lookup and Merge project is designed to provide a comprehensive solution for retrieving and consolidating aviation-related data. The system comprises two main functionalities: *lookup* and *merge*. These operations leverage a structured dataset consisting of flight schedules, fleet information, and airport details to deliver insightful results.

## Features
1. Lookup Mode:
   - Flight Number Search: Users can input one or more flight numbers to retrieve detailed information about the specified flights.
   - Data Enrichment: The lookup functionality incorporates data from flight schedules and fleet records, offering a holistic view of the queried flights.

2. Merge Mode:
   - Data Integration: The merge operation combines data from flight schedules, fleet information, and airport details to generate a comprehensive dataset.
   - Result Output: The merged data is exported to a CSV file, providing users with a consolidated view of relevant flight information.

## Architecture Data Flow Diagram

The Architecture Data Flow Diagram illustrates the flow of information and control within our system. It provides a high-level representation of how data moves through various components, from the user interface to the core 
processing modules and external dependencies.

## Entity-Relationship (ER) Diagram

The Entity-Relationship (ER) Diagram outlines the relationships and interactions among the main entities in our system—flight schedules, fleet information, airports, and the resulting merged data. It provides a graphical representation of the database schema.

## Getting Started
To get started with the Flight Data Lookup and Merge project, follow the instructions below.

## Prerequisites
Make sure you have the following prerequisites installed before running the application.
Python 3.x
requirements.txt

## Installation
Follow these steps to install the Flight Data Lookup and Merge application on your system.

Clone the repository: git clone <repository name>
Navigate to the project directory: cd <folder name>

## Usage
To use the application, follow the examples below for lookup and merge operations.
python flight_data_app.py lookup <flight_numbers>
python flight_data_app.py merge

## Configuration
The project allows for easy configuration through external files, enabling users to customize the behavior of the application according to their specific requirements.

config/config.json

## Logging
The application logs key events and errors, providing users with a detailed record of the executed operations. Log files are stored in a dedicated directory for easy reference and troubleshooting.
