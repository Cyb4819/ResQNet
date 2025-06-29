import math

class GPSHelper:
    """
    GPSHelper handles basic location and direction calculations.
    """

    def __init__(self):
        self.last_known_location = None  # (lat, lon) tuple
        self.destination = None  # (lat, lon)

    def update_location(self, lat: float, lon: float):
        """
        Update current location.
        """
        self.last_known_location = (lat, lon)

    def set_destination(self, lat: float, lon: float):
        """
        Set navigation target destination.
        """
        self.destination = (lat, lon)

    @staticmethod
    def calculate_bearing(pointA, pointB):
        """
        Calculate bearing between two points.
        Input:
            pointA: (lat1, lon1) in decimal degrees
            pointB: (lat2, lon2) in decimal degrees
        Returns:
            bearing in degrees from pointA to pointB (0-360)
        """
        lat1 = math.radians(pointA[0])
        lat2 = math.radians(pointB[0])
        diffLong = math.radians(pointB[1] - pointA[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1)*math.sin(lat2) - (math.sin(lat1)*math.cos(lat2)*math.cos(diffLong))

        initial_bearing = math.atan2(x, y)
        # Convert from radians to degrees and normalize
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360

        return compass_bearing

    @staticmethod
    def direction_to_text(bearing, heading):
        """
        Convert bearing difference to human-readable direction.
        """
        diff = (bearing - heading + 360) % 360

        if diff < 15 or diff > 345:
            return "straight ahead"
        elif 15 <= diff < 45:
            return "slightly right"
        elif 45 <= diff < 135:
            return "right"
        elif 135 <= diff < 180:
            return "sharp right"
        elif 180 <= diff < 225:
            return "sharp left"
        elif 225 <= diff < 315:
            return "left"
        else:
            return "slightly left"

    def get_navigation_instruction(self, current_heading: float):
        """
        Returns a textual direction for the user to follow to reach destination.
        """
        if not self.last_known_location or not self.destination:
            return "Location or destination not set."

        bearing = self.calculate_bearing(self.last_known_location, self.destination)
        direction = self.direction_to_text(bearing, current_heading)
        distance = self.haversine_distance(self.last_known_location, self.destination)
        return f"Move {direction}, approximately {distance:.1f} km to destination."

    @staticmethod
    def haversine_distance(pointA, pointB):
        """
        Calculate distance between two lat/lon points in kilometers.
        """
        R = 6371  # Earth radius km
        lat1, lon1 = pointA
        lat2, lon2 = pointB
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
