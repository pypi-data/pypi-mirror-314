class UnitConverter:
    def __init__(self):
        # Conversion tables for each category

        # Length conversion (base unit: meters)
        self.length_conversion = {
            'meters': 1,
            'kilometers': 1000,
            'miles': 1609.34,
            'feet': 0.3048,
            'inches': 0.0254
        }

        # Weight conversion (base unit: kilograms)
        self.weight_conversion = {
            'kilograms': 1,
            'grams': 1000,
            'pounds': 2.20462,
            'ounces': 35.274
        }

        # Temperature conversion (Celsius to other units)
        self.temperature_conversion = {
            'C': lambda x: x,  # Celsius to Celsius
            'F': lambda x: (x * 9/5) + 32,  # Celsius to Fahrenheit
            'K': lambda x: x + 273.15  # Celsius to Kelvin
        }
        self.temperature_reverse_conversion = {
            'F': lambda x: (x - 32) * 5/9,  # Fahrenheit to Celsius
            'C': lambda x: x,  # Celsius to Celsius
            'K': lambda x: x - 273.15  # Kelvin to Celsius
        }

        # Volume conversion (base unit: liters)
        self.volume_conversion = {
            'liters': 1,
            'milliliters': 1000,
            'gallons': 3.78541,
            'cups': 4.22675
        }

        # Time conversion (base unit: seconds)
        self.time_conversion = {
            'seconds': 1,
            'minutes': 60,
            'hours': 3600,
            'days': 86400
        }

        # Area conversion (base unit: square meters)
        self.area_conversion = {
            'square_meters': 1,
            'square_kilometers': 1e6,
            'square_miles': 2.59e6,
            'square_feet': 0.092903,
            'acres': 4046.86
        }

        # Speed conversion (base unit: meters per second)
        self.speed_conversion = {
            'meters_per_second': 1,
            'kilometers_per_hour': 0.277778,
            'miles_per_hour': 0.44704
        }

        # Energy conversion (base unit: joules)
        self.energy_conversion = {
            'joules': 1,
            'calories': 4.184,
            'kilocalories': 4184
        }

        # Power conversion (base unit: watts)
        self.power_conversion = {
            'watts': 1,
            'horsepower': 745.7
        }

    def convert(self, value: float, from_unit: str, to_unit: str, category: str):
        # Perform the conversion based on the category
        if category == 'length':
            return value * self.length_conversion[from_unit] / self.length_conversion[to_unit]
        elif category == 'weight':
            return value * self.weight_conversion[from_unit] / self.weight_conversion[to_unit]
        elif category == 'temperature':
            if from_unit == 'C' and to_unit in self.temperature_conversion:
                return self.temperature_conversion[to_unit](value)
            elif from_unit in self.temperature_reverse_conversion and to_unit == 'C':
                return self.temperature_reverse_conversion[from_unit](value)
            else:
                raise ValueError("Invalid temperature conversion")
        elif category == 'volume':
            return value * self.volume_conversion[from_unit] / self.volume_conversion[to_unit]
        elif category == 'time':
            return value * self.time_conversion[from_unit] / self.time_conversion[to_unit]
        elif category == 'area':
            return value * self.area_conversion[from_unit] / self.area_conversion[to_unit]
        elif category == 'speed':
            return value * self.speed_conversion[from_unit] / self.speed_conversion[to_unit]
        elif category == 'energy':
            return value * self.energy_conversion[from_unit] / self.energy_conversion[to_unit]
        elif category == 'power':
            return value * self.power_conversion[from_unit] / self.power_conversion[to_unit]
        else:
            raise ValueError("Invalid category")

    def get_available_units(self, category: str):
        # Return available units based on the category
        if category == 'length':
            return list(self.length_conversion.keys())
        elif category == 'weight':
            return list(self.weight_conversion.keys())
        elif category == 'temperature':
            return list(self.temperature_conversion.keys())
        elif category == 'volume':
            return list(self.volume_conversion.keys())
        elif category == 'time':
            return list(self.time_conversion.keys())
        elif category == 'area':
            return list(self.area_conversion.keys())
        elif category == 'speed':
            return list(self.speed_conversion.keys())
        elif category == 'energy':
            return list(self.energy_conversion.keys())
        elif category == 'power':
            return list(self.power_conversion.keys())
        else:
            raise ValueError("Invalid category")


# Function to handle user input and conversion process
def get_user_input():
    print("Welcome to the Unit Converter!")
    
    # Get value to convert
    value = float(input("Enter the value to convert: "))
    
    # Get category and provide relevant units
    category = input("Enter the category (length, weight, temperature, volume, time, area, speed, energy, power): ").lower()

    try:
        available_units = converter.get_available_units(category)
        print(f"Available units for {category}: {', '.join(available_units)}")
        
        from_unit = input(f"Enter the unit you are converting from ({', '.join(available_units)}): ").lower()
        if from_unit not in available_units:
            raise ValueError(f"Invalid 'from' unit: {from_unit}")
        
        to_unit = input(f"Enter the unit you want to convert to ({', '.join(available_units)}): ").lower()
        if to_unit not in available_units:
            raise ValueError(f"Invalid 'to' unit: {to_unit}")
        
        # Convert
        result = converter.convert(value, from_unit, to_unit, category)
        print(f"{value} {from_unit} is equal to {result} {to_unit}")
    
    except ValueError as e:
        print(f"Error: {e}")


# Instantiate converter and run conversion
converter = UnitConverter()
get_user_input()
