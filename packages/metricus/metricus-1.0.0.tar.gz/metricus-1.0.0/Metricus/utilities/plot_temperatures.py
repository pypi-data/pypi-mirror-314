import matplotlib.pyplot as plt

def plot_temperature_variation(temperatures, temperature_unit, convert_to=None, save_path=None, with_info=True):
    """
    Plots a graph showing temperature variations throughout the month, 
    optionally including average temperature, the coldest day, and the hottest day.

    :param temperatures: List of daily temperatures.
    :param temperature_unit: The unit of the input temperatures (e.g., 'celsius', 'fahrenheit').
    :param convert_to: The unit to convert temperatures to (optional).
    :param save_path: File path to save the graph (optional).
    :param with_info: Whether to display statistical information on the graph (default: True).
    """
    from Metricus.operations import temperature_converter 
    
    # Days of the month
    days = list(range(1, len(temperatures) + 1))

    # Map of temperature units
    units_map = {
        "celsius": "°C",
        "fahrenheit": "°F",
        "kelvin": "°K",
        "rankine": "°R",
    }

    # Convert temperatures if necessary
    if convert_to:
        new_temperatures = []
        for temp in temperatures:
            converted_temperature = temperature_converter(temp, temperature_unit, convert_to)
            new_temperatures.append(converted_temperature)
        temperatures = new_temperatures
        temperature_unit = convert_to

    # Configure the plot
    plt.figure(figsize=(10, 5))
    plt.plot(days, temperatures, marker='o', linestyle='-', color='blue', label='Temperature')
    plt.title(f"Temperature Variation Over {len(days)} Days")
    plt.xlabel("Day")
    plt.ylabel(f"Temperature ({units_map[temperature_unit]})")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(days, rotation=45)
    plt.legend()

    # Add statistics to the plot if with_info is True
    if with_info:
        average_temperature = sum(temperatures) / len(temperatures)
        coldest_day = days[temperatures.index(min(temperatures))]
        hottest_day = days[temperatures.index(max(temperatures))]
        coldest_temperature = min(temperatures)
        hottest_temperature = max(temperatures)

        stats_text = (
            f"Average Temperature: {average_temperature:.2f}{units_map[temperature_unit]}\n"
            f"Coldest Day: Day {coldest_day} ({coldest_temperature:.2f}{units_map[temperature_unit]})\n"
            f"Hottest Day: Day {hottest_day} ({hottest_temperature:.2f}{units_map[temperature_unit]})"
        )
        plt.text(
            0.02, 0.98, stats_text, fontsize=10, ha='left', va='top', 
            transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray')
        )

    plt.tight_layout()

    # Display or save the plot
    if save_path:
        plt.savefig(save_path, format=save_path.split('.')[-1], dpi=300)
        print(f"Graph saved to {save_path}")
    else:
        plt.show()
