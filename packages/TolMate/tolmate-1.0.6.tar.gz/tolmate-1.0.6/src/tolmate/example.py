
from tmate import configure_behavior, tolmate

# Main program
def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15

# Main loop for initial value input
try:
    # Configure global behavior (example: enable both message and popup)
    configure_behavior(show_popup=True, show_message=True)
    
    value = float(input("\nEnter the temperature in degrees Celsius: "))

    if tolmate(value, 20, 30, 10, 50, -10, 80):  # Example ranges
        kelvin = celsius_to_kelvin(value)
        print(f"\nThe temperature in Kelvin is: {kelvin:.2f}\n")

except ValueError:
    print("\nPlease enter a valid number!")
