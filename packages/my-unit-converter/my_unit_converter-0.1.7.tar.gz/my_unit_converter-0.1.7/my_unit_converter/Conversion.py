class UnitConverter:
    def __init__(self):
        # Initialize conversion dictionaries for each category
        self.length_conversion = {'meters': 1, 'kilometers': 1000, 'miles': 1609.34, 'feet': 0.3048, 'inches': 0.0254}
        self.weight_conversion = {'kilograms': 1, 'grams': 1000, 'pounds': 2.20462, 'ounces': 35.274}
        self.temperature_conversion = {'C': lambda x: x, 'F': lambda x: (x * 9 / 5) + 32, 'K': lambda x: x + 273.15}
        self.temperature_reverse_conversion = {'F': lambda x: (x - 32) * 5 / 9, 'C': lambda x: x, 'K': lambda x: x - 273.15}
        self.volume_conversion = {'liters': 1, 'milliliters': 1000, 'gallons': 3.78541, 'cups': 4.22675}
        self.time_conversion = {'seconds': 1, 'minutes': 60, 'hours': 3600, 'days': 86400}
        self.area_conversion = {'square_meters': 1, 'square_kilometers': 1e6, 'square_miles': 2.59e6, 'square_feet': 0.092903, 'acres': 4046.86}
        self.speed_conversion = {'meters_per_second': 1, 'kilometers_per_hour': 0.277778, 'miles_per_hour': 0.44704}
        self.energy_conversion = {'joules': 1, 'calories': 4.184, 'kilocalories': 4184}
        self.power_conversion = {'watts': 1, 'horsepower': 745.7}

    # Length conversion
    def convert_length(self, value, from_unit, to_unit):
        return value * self.length_conversion[from_unit] / self.length_conversion[to_unit]

    # Weight conversion (fixed)
    def convert_weight(self, value, from_unit, to_unit):
        # Special handling for weight conversions (kilograms <-> grams)
        if from_unit == 'kilograms' and to_unit == 'grams':
            return value * self.weight_conversion[to_unit]
        elif from_unit == 'grams' and to_unit == 'kilograms':
            return value / self.weight_conversion[from_unit]
        else:
            # General case for other units
            return value * self.weight_conversion[from_unit] / self.weight_conversion[to_unit]

    # Temperature conversion
    def convert_temperature(self, value, from_unit, to_unit):
        if from_unit == 'C' and to_unit in self.temperature_conversion:
            return self.temperature_conversion[to_unit](value)
        elif from_unit in self.temperature_reverse_conversion and to_unit == 'C':
            return self.temperature_reverse_conversion[from_unit](value)
        else:
            raise ValueError("Invalid temperature conversion")

    # Time conversion
    def convert_time(self, value, from_unit, to_unit):
        return value * self.time_conversion[from_unit] / self.time_conversion[to_unit]

    # Area conversion
    def convert_area(self, value, from_unit, to_unit):
        return value * self.area_conversion[from_unit] / self.area_conversion[to_unit]

    # Speed conversion
    def convert_speed(self, value, from_unit, to_unit):
        return value * self.speed_conversion[from_unit] / self.speed_conversion[to_unit]

    # Energy conversion
    def convert_energy(self, value, from_unit, to_unit):
        return value * self.energy_conversion[from_unit] / self.energy_conversion[to_unit]

    # Power conversion
    def convert_power(self, value, from_unit, to_unit):
        return value * self.power_conversion[from_unit] / self.power_conversion[to_unit]

    # Get available units for a category
    def get_available_units(self, category):
        category_dict = {
            'length': self.length_conversion,
            'weight': self.weight_conversion,
            'temperature': self.temperature_conversion,
            'volume': self.volume_conversion,
            'time': self.time_conversion,
            'area': self.area_conversion,
            'speed': self.speed_conversion,
            'energy': self.energy_conversion,
            'power': self.power_conversion
        }
        if category in category_dict:
            return list(category_dict[category].keys())
        else:
            raise ValueError("Invalid category")
