from Metricus.gui import MetricusGUI
from Metricus.operations import (acceleration_converter, area_converter,
                                 electricity_converter, energy_converter,
                                 force_converter, length_converter,
                                 mass_converter, pressure_converter,
                                 speed_converter, temperature_converter,
                                 time_converter, volume_converter)
from Metricus.operations.complex_operations import (calculate_density,
                                                    calculate_displacement,
                                                    calculate_force,
                                                    calculate_pressure)
from Metricus.utilities.round_number import round_number
from Metricus.utilities.humanize_input import humanize_input
from Metricus.utilities.decomputarize_input import decomputarize_input
from Metricus.utilities.plot_temperatures import plot_temperature_variation

# help(area_converter)
# help(electricity_converter)
# help(energy_converter)
# help(length_converter)
# help(mass_converter)
# help(pressure_converter)
# help(speed_converter)
# help(temperature_converter)
# help(time_converter)
# help(volume_converter)
# help(acceleration_converter)
# help(force_converter)
# help(calculate_force)
# help(calculate_density)
# help(calculate_displacement)
# help(calculate_pressure)

# Testing operations
print(area_converter(100, "square kilometer", "hectare", rounded_result=True, humanized_input=True))
print(electricity_converter(5, "kilowatt", "watt"))
print(energy_converter(10, "calorie", "joule"))
print(length_converter(5, "kilometer", "mile"))
print(mass_converter(1000, "gram", "pound"))
print(pressure_converter(1, "atmosphere", "pascal"))
print(speed_converter(100, "kn", "km/h"))
print(temperature_converter(25, "celsius", "fahrenheit"))
print(time_converter(1, "hour", "minute"))
print(volume_converter(1, "m3", "L"))
print(acceleration_converter(500, "gal", "gravity"))
print(force_converter(1000, "newton", "dyne"))
print(calculate_force(500, 10))
print(calculate_density(400, 500, mass_unit="tonne", volume_unit="L", with_unit=True))
print(calculate_displacement(100, 300, "minute", with_unit=True))
print(calculate_pressure(500, 100, "psi", "poundal", with_unit=True))

# Testing round number
result = time_converter(365, "day", "year", with_unit=True)
print(result)
print(round_number(result=result))

# Testing humanize input
from_acceleration = 'Meter Per Second Squared'
to_acceleration = 'Foot per second squared'
result_humanize = acceleration_converter(100, humanize_input(from_acceleration), humanize_input(to_acceleration), with_unit=True)
print(result_humanize)

# Testing decomputarize input
from_acceleration_computadorized = 'meter_per_second_squared'
to_acceleration_computadorized = 'foot_per_second_squared'
from_acceleration_decomputarize = decomputarize_input(from_acceleration_computadorized)
to_acceleration_decomputarize = decomputarize_input(to_acceleration_computadorized)
print(f"From acceleration: {from_acceleration_decomputarize}. To acceleration: {to_acceleration_decomputarize}.")

# Testing temperature plot
temperatures = [20.3, 12, 10, 15.4, 8, 17.5, 15.3]
plot_temperature_variation(temperatures, 'celsius', 'rankine')

# Testing GUI
MetricusGUI()
