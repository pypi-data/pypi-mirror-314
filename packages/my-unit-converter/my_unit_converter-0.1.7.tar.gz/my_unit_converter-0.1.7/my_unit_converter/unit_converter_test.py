# from Conversion import UnitConverter  # Make sure the module is correctly imported

#  # Make sure the module is correctly imported

# # Create a test instance
# def test_unit_converter():
#     converter = UnitConverter()  # Use UnitConverter here

#     # Test length conversion
#     result_length = converter.convert_length(1000, 'meters', 'kilometers')
#     assert result_length == 1, f"Expected 1, got {result_length}"

#     # Test weight conversion
#     result_weight = converter.convert_weight(1, 'kilograms', 'grams')
#     assert result_weight == 1000, f"Expected 1000, got {result_weight}"

#     # Test temperature conversion
#     result_temp = converter.convert_temperature(0, 'C', 'F')
#     assert result_temp == 32, f"Expected 32, got {result_temp}"

#     # Additional tests
#     # Test temperature conversion in reverse (Fahrenheit to Celsius)
#     result_temp_reverse = converter.convert_temperature(32, 'F', 'C')
#     assert result_temp_reverse == 0, f"Expected 0, got {result_temp_reverse}"


#     # Test time conversion (minutes to seconds)
#     result_time = converter.convert_time(1, 'minutes', 'seconds')
#     assert result_time == 60, f"Expected 60, got {result_time}"

#     print("All tests passed!")

#     print(converter.get_available_units("area"))

#     # Create an instance of the UnitConverter class
# converter = UnitConverter()

# # Call convert_weight to convert 2 kilograms to pounds
# result = converter.convert_weight(2, 'kilograms', 'pounds')

# # Print the result
# print(f"2 kilograms is equal to {result} pounds.")

# converter = UnitConverter()
# result = converter.convert_speed(10, 'meters_per_second', 'kilometers_per_hour')
# print(result)  # Output: 36.0


# # Run the test
# if __name__ == "__main__":
#     test_unit_converter()



from Conversion import UnitConverter

def test_unit_converter():
    # Instantiate the UnitConverter
    converter = UnitConverter()

    # Length conversion
    result_length = converter.convert_length(1000, 'meters', 'kilometers')
    print(f"1000 meters = {result_length} kilometers")

    # Weight conversion
    result_weight = converter.convert_weight(2, 'kilograms', 'pounds')
    print(f"2 kilograms = {result_weight} pounds")

    # Temperature conversion
    result_temp = converter.convert_temperature(30, 'C', 'F')
    print(f"30°C = {result_temp}°F")

    # Get available units for each category
    available_length_units = converter.get_available_units("length")
    print("Available length units:", available_length_units)

    available_weight_units = converter.get_available_units("weight")
    print("Available weight units:", available_weight_units)

    available_temperature_units = converter.get_available_units("temperature")
    print("Available temperature units:", available_temperature_units)

if __name__ == "__main__":
    test_unit_converter()


