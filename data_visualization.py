import pandas as pd
import matplotlib.pyplot as plt

def visualize_flight_data(df):
    """
    Visualize various scenarios with flight data.

    Parameters:
    - df (pd.DataFrame): Flight data DataFrame.

    Returns:
    - None
    """
    plt.rcParams['figure.figsize'] = (15, 14)

    # Scenario 1: Total Seats per Flight (Class-wise)
    plt.subplot(3, 2, 1)
    class_columns = ['F', 'C', 'E', 'M']
    for class_col in class_columns:
        plt.bar(df['flight_number'], df[class_col], label=class_col, alpha=0.7)
    plt.xlabel('Flight Number')
    plt.ylabel('Total Seats')
    plt.title('Total Seats per Flight (Class-wise)')
    plt.legend()

    # # Scenario 2: Flight Distance vs. Aircraft Type
    # plt.subplot(3, 2, 2)
    # plt.scatter(df['distance_nm'], df['IATATypeDesignator'], alpha=0.5, color='orange')
    # plt.xlabel('Distance (Nautical Miles)')
    # plt.ylabel('Aircraft Type')
    # plt.title('Flight Distance vs. Aircraft Type')

    # # Scenario 3: Seat Distribution by Class
    # plt.subplot(3, 2, 3)
    # df[class_columns].plot(kind='bar', stacked=True)
    # plt.xlabel('Flight Number')
    # plt.ylabel('Total Seats')
    # plt.title('Seat Distribution by Class')

    # # Scenario 4: Haul Type Distribution
    # plt.subplot(3, 2, 4)
    # df['Haul'].value_counts().plot.pie(autopct='%1.1f%%', colors=['orange', 'yellow', 'green'])
    # plt.title('Haul Type Distribution')

    # # Scenario 5: Flight Count by Hub
    # plt.subplot(3, 2, 5)
    # df['Hub'].value_counts().plot(kind='bar', color='purple')
    # plt.xlabel('Hub')
    # plt.ylabel('Number of Flights')
    # plt.title('Flight Count by Hub')

    # # Scenario 6: Flight Duration Distribution
    # plt.subplot(3, 2, 6)
    # df['scheduled_departure_time'] = pd.to_datetime(df['scheduled_departure_time'])
    # df['scheduled_arrival_time'] = pd.to_datetime(df['scheduled_arrival_time'])
    # flight_durations = (df['scheduled_arrival_time'] - df['scheduled_departure_time']).dt.total_seconds() / 3600
    # plt.hist(flight_durations, bins=20, color='skyblue', edgecolor='black')
    # plt.xlabel('Flight Duration (hours)')
    # plt.ylabel('Frequency')
    # plt.title('Flight Duration Distribution')

    # plt.tight_layout()
    # plt.show()

    # Group by departure and arrival countries and sum the distances

    # plt.rcParams['figure.figsize'] = (12, 6)

    # # Extract country information from departure and arrival airports
    # df['departure_country'] = df['departure_airport'].str.split(',').str[-1].str.strip()
    # df['arrival_country'] = df['arrival_airport'].str.split(',').str[-1].str.strip()

    # # Group by departure and arrival countries and sum the distances
    # departure_country_totals = df.groupby('departure_country')['distance_nm'].sum()
    # arrival_country_totals = df.groupby('arrival_country')['distance_nm'].sum()

    # # Sort values for better visualization
    # departure_country_totals = departure_country_totals.sort_values(ascending=False)
    # arrival_country_totals = arrival_country_totals.sort_values(ascending=False)

    # # Plotting
    # plt.subplot(1, 2, 1)
    # departure_country_totals.plot(kind='bar', color='skyblue')
    # plt.xlabel('Departure Country')
    # plt.ylabel('Total Distance (Nautical Miles)')
    # plt.title('Most Traveled Departure Countries')

    # plt.subplot(1, 2, 2)
    # arrival_country_totals.plot(kind='bar', color='orange')
    # plt.xlabel('Arrival Country')
    # plt.ylabel('Total Distance (Nautical Miles)')
    # plt.title('Most Traveled Arrival Countries')

    # plt.tight_layout()
    # plt.show()

    # plt.rcParams['figure.figsize'] = (10, 10)

    # # Extract departure country column
    # departure_countries = df['departure_airport']

    # # Calculate the count of flights for each departure country
    # departure_country_counts = departure_countries.value_counts()

    # # Plotting
    # plt.pie(departure_country_counts, labels=departure_country_counts.index, autopct='%1.1f%%', startangle=140)
    # plt.title('Distribution of Flights Based on Departure Countries')
    plt.show()

# Example usage:
# Assuming df is your DataFrame with flight data
df = pd.read_csv('Result/Flight_results.csv')
visualize_flight_data(df)

# df['departure_country'] = df['departure_airport'].str.split(',').str[-1].str.strip()
# df['arrival_country'] = df['arrival_airport'].str.split(',').str[-1].str.strip()

