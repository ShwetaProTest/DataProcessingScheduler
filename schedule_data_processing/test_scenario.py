from geopy.distance import geodesic

# Coordinates for the departure airport (LHR) and arrival airport (RAK)
departure_coords = (51.4706, -0.461941)  # London Heathrow Airport (LHR)
arrival_coords = (31.60689926, -8.036299706)  # Menara Airport (RAK)

# Calculate the distance in nautical miles
distance_nm = geodesic(departure_coords, arrival_coords).nautical

# Display the calculated distance
print(f"Calculated Distance for ZG5001: {distance_nm} nautical miles")



