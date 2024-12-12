import tkinter as tk

import Metricus.operations
import Metricus.operations.acceleration
import Metricus.operations.area
import Metricus.operations.complex_operations
import Metricus.operations.complex_operations.calculate_density
import Metricus.operations.complex_operations.calculate_displacement
import Metricus.operations.complex_operations.calculate_force
import Metricus.operations.complex_operations.calculate_pressure
from Metricus.utilities import *


def send_data(choice):
    try:
        from_unit_row = from_unit_entry.get()
        to_unit_row = to_unit_entry.get()

        input_value = float(input_entry.get())
        from_unit = humanize_input(from_unit_row)
        to_unit = humanize_input(to_unit_row)

        if choice == "Acceleration":
            result = Metricus.operations.acceleration_converter(
                input_value, from_unit, to_unit, with_unit=True
            )
        elif choice == "Area":
            result = Metricus.operations.area_converter(
                input_value, from_unit, to_unit, with_unit=True
            )
        elif choice == "Energy":
            result = Metricus.operations.energy_converter(
                input_value, from_unit, to_unit, with_unit=True
            )
        elif choice == "Force":
            result = Metricus.operations.force_converter(
                input_value, from_unit, to_unit, with_unit=True
            )
        elif choice == "Length":
            result = Metricus.operations.length_converter(
                input_value, from_unit, to_unit, with_unit=True
            )
        elif choice == "Mass":
            result = Metricus.operations.mass_converter(
                input_value, from_unit, to_unit, with_unit=True
            )
        elif choice == "Pressure":
            result = Metricus.operations.pressure_converter(
                input_value, from_unit, to_unit, with_unit=True
            )
        elif choice == "Speed":
            result = Metricus.operations.speed_converter(
                input_value, from_unit, to_unit, with_unit=True
            )
        elif choice == "Temperature":
            result = Metricus.operations.temperature_converter(
                input_value, from_unit, to_unit, with_unit=True
            )
        elif choice == "Time":
            result = Metricus.operations.time_converter(
                input_value, from_unit, to_unit, with_unit=True
            )
        elif choice == "Volume":
            result = Metricus.operations.volume_converter(
                input_value, from_unit, to_unit, with_unit=True
            )
        elif choice == "Electricity":
            resistance = float(resistance_entry.get()) if resistance_entry.get() else None
            current = float(current_entry.get()) if current_entry.get() else None
            voltage = float(voltage_entry.get()) if voltage_entry.get() else None
            time = float(time_entry.get()) if time_entry.get() else None
            freq = float(freq_entry.get()) if freq_entry.get() else None

            result = Metricus.operations.electricity_converter(
                input_value, from_unit, to_unit, with_unit=True,
                resistance=resistance,
                current=current,
                voltage=voltage,
                time=time,
                freq=freq
            )
        else:
            result = "Conversion not implemented for this choice."

        result_label.config(text=f"Result: {result}", fg="black")
    except Exception as e:
        result_label.config(text=f"Error: {e}", fg="red")


def send_data_complex(choice):
    global acceleration_unit_var
    global force_unit_var
    global area_unit_var
    try:
        input_value = float(input_entry.get())

        if choice == "Calculate Displacement":
            time_value = time_entry.get() if time_entry.get() else None
            speed_value = float(speed_entry.get()) if speed_entry.get() else None

            length_unit = length_unit_var.get() if length_unit_var else None
            speed_unit = speed_unit_var.get() if speed_unit_var else None

            result = Metricus.operations.complex_operations.calculate_displacement(
                input_value,
                speed_value,
                time_value,
                length_unit,
                speed_unit,
                with_unit=True,
            )

        elif choice == "Calculate Density":
            try:
                density_value = density_entry.get() if density_entry.get() else None
                volume_value = float(volume_entry.get()) if volume_entry.get() else None
                input_value = float(input_entry.get()) if input_entry.get() else None

                mass_unit = (
                    mass_unit_var.get() if "mass_unit_var" in globals() else None
                )
                volume_unit = (
                    volume_unit_var.get() if "volume_unit_var" in globals() else None
                )

                if not density_value or not volume_value or not input_value:
                    raise ValueError(
                        "All values (mass, volume, and density) are required."
                    )

                result = Metricus.operations.complex_operations.calculate_density(
                    input_value,
                    volume_value,
                    density_value,
                    mass_unit,
                    volume_unit,
                    with_unit=True,
                )

            except ValueError as ve:
                result_label.config(text=f"Error: {ve}", fg="red")

        elif choice == "Calculate Force":
            try:
                force_value = force_entry.get() if force_entry.get() else None
                acceleration_value = (
                    float(acceleration_entry.get())
                    if acceleration_entry.get()
                    else None
                )
                input_value = float(input_entry.get()) if input_entry.get() else None

                mass_unit = (
                    mass_unit_var.get() if "mass_unit_var" in globals() else None
                )
                acceleration_unit = (
                    acceleration_unit_var.get()
                    if "acceleration_unit_var" in globals()
                    else None
                )

                if not force_value or not acceleration_value or not input_value:
                    raise ValueError(
                        "All values (mass, volume, and force) are required."
                    )

                result = Metricus.operations.complex_operations.calculate_force(
                    input_value,
                    acceleration_value,
                    force_value,
                    mass_unit,
                    acceleration_unit,
                    with_unit=True,
                )

            except ValueError as ve:
                result_label.config(text=f"Error: {ve}", fg="red")

        elif choice == "Calculate Pressure":
            try:
                pressure_value = pressure_entry.get() if pressure_entry.get() else None
                area_value = float(area_entry.get()) if area_entry.get() else None
                input_value = float(input_entry.get()) if input_entry.get() else None

                force_unit = (
                    force_unit_var.get() if "force_unit_var" in globals() else None
                )
                area_unit = (
                    area_unit_var.get() if "area_unit_var" in globals() else None
                )

                if not input_value or not area_value or not pressure_value:
                    raise ValueError(
                        "All values (force, area, and pressure) are required."
                    )

                result = Metricus.operations.complex_operations.calculate_pressure(
                    input_value,
                    area_value,
                    pressure_value,
                    force_unit,
                    area_unit,
                    with_unit=True,
                )

            except ValueError as ve:
                result_label.config(text=f"Error: {ve}", fg="red")
            except Exception as e:
                result_label.config(text=f"Error: {e}", fg="red")

        else:
            result = "Complex calculation not implemented for this choice."

        result_label.config(text=f"Result: {result}", fg="black")

    except ValueError:
        result_label.config(text="Error: Invalid numeric input.", fg="red")
    except AttributeError as e:
        result_label.config(
            text=f"Error: Missing input or invalid variable. {e}", fg="red"
        )
    except Exception as e:
        result_label.config(text=f"Error: {e}", fg="red")


def show_choices(option):
    for widget in choices_frame.winfo_children():
        widget.destroy()

    back_button = tk.Button(
        choices_frame, text="Back", command=go_back_to_main, bg="gray", fg="white"
    )
    back_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    if option == 1:
        choices = [
            "Acceleration",
            "Area",
            "Electricity",
            "Energy",
            "Force",
            "Length",
            "Mass",
            "Pressure",
            "Speed",
            "Temperature",
            "Time",
            "Volume",
        ]
    elif option == 2:
        choices = [
            "Calculate Density",
            "Calculate Displacement",
            "Calculate Force",
            "Calculate Pressure",
        ]

    for i, choice in enumerate(choices):
        tk.Button(
            choices_frame,
            text=choice,
            command=lambda c=choice: show_sub_choices(c),
            width=20,
            height=1,
        ).grid(row=i + 1, column=1, padx=10, pady=2, sticky="n")


def go_back_to_main():
    choice_label.config(text="")

    for widget in choices_frame.winfo_children():
        widget.destroy()

    tk.Button(
        choices_frame,
        text="Simple Conversions",
        command=lambda: show_choices(1),
        width=20,
        height=2,
    ).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(
        choices_frame,
        text="Complex Conversions",
        command=lambda: show_choices(2),
        width=20,
        height=2,
    ).grid(row=1, column=1, padx=10, pady=10)


def show_sub_choices(choice):
    global input_entry, from_unit_entry, to_unit_entry, result_label, speed_entry, time_entry
    global speed_unit_var, length_unit_var, density_entry, mass_unit_var, volume_unit_var

    for widget in choices_frame.winfo_children():
        widget.destroy()

    choice_label.config(text=f"{choice}", fg="gray")

    back_button = tk.Button(
        choices_frame, text="Back", command=go_back_to_main, bg="gray", fg="white"
    )
    back_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    result_label = tk.Label(
        choices_frame, text="Result: ", bg="lightblue", fg="black", wraplength=400
    )
    result_label.grid(row=8, column=0, columnspan=2, pady=10)

    if "Calculate" not in choice:
        create_simple_inputs()
        if "Electricity" in choice:
            create_electricity_inputs()
            result_label.grid(row=14, column=0, columnspan=2, pady=10)
    elif "Displacement" in choice:
        create_displacement_inputs()
    elif "Density" in choice:
        create_density_inputs()
    elif "Force" in choice:
        create_force_inputs()
    elif "Pressure" in choice:
        create_pressure_inputs()
    else:
        tk.Label(choices_frame, text="Invalid choice.", bg="lightblue", fg="red").grid(
            row=1, column=0, columnspan=2
        )

    submit_button = tk.Button(
        choices_frame,
        text="Submit",
        command=lambda: (
            send_data_complex(choice) if "Calculate" in choice else send_data(choice)
        ),
    )
    submit_button.grid(row=7, column=0, columnspan=2, pady=10)
    if "Electricity" in choice:
        submit_button.grid(row=16, column=0, columnspan=2, pady=10)


def create_simple_inputs():
    tk.Label(choices_frame, text="Value (num):", bg="lightblue").grid(
        row=1, column=0, padx=10, pady=5, sticky="e"
    )
    global input_entry
    input_entry = tk.Entry(choices_frame)
    input_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(choices_frame, text="From Unit (str):", bg="lightblue").grid(
        row=2, column=0, padx=10, pady=5, sticky="e"
    )
    global from_unit_entry
    from_unit_entry = tk.Entry(choices_frame)
    from_unit_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(choices_frame, text="To Unit (str):", bg="lightblue").grid(
        row=3, column=0, padx=10, pady=5, sticky="e"
    )
    global to_unit_entry
    to_unit_entry = tk.Entry(choices_frame)
    to_unit_entry.grid(row=3, column=1, padx=10, pady=5)


def create_electricity_inputs():
    tk.Label(choices_frame, text="Resistance Value (Ω):", bg="lightblue").grid(
        row=4, column=0, padx=10, pady=5, sticky="e"
    )
    global resistance_entry
    resistance_entry = tk.Entry(choices_frame)
    resistance_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(choices_frame, text="Current Value (A):", bg="lightblue").grid(
        row=5, column=0, padx=10, pady=5, sticky="e"
    )
    global current_entry
    current_entry = tk.Entry(choices_frame)
    current_entry.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(choices_frame, text="Voltage Value (V):", bg="lightblue").grid(
        row=6, column=0, padx=10, pady=5, sticky="e"
    )
    global voltage_entry
    voltage_entry = tk.Entry(choices_frame)
    voltage_entry.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(choices_frame, text="Time Value (s):", bg="lightblue").grid(
        row=7, column=0, padx=10, pady=5, sticky="e"
    )
    global time_entry
    time_entry = tk.Entry(choices_frame)
    time_entry.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(choices_frame, text="Frequency Value (Hz):", bg="lightblue").grid(
        row=8, column=0, padx=10, pady=5, sticky="e"
    )
    global freq_entry
    freq_entry = tk.Entry(choices_frame)
    freq_entry.grid(row=8, column=1, padx=10, pady=5)


def create_displacement_inputs():
    tk.Label(choices_frame, text="Length (num):", bg="lightblue").grid(
        row=1, column=0, padx=10, pady=5, sticky="e"
    )
    global input_entry
    input_entry = tk.Entry(choices_frame)
    input_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(choices_frame, text="Speed (num):", bg="lightblue").grid(
        row=2, column=0, padx=10, pady=5, sticky="e"
    )
    global speed_entry
    speed_entry = tk.Entry(choices_frame)
    speed_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(choices_frame, text="Time (str):", bg="lightblue").grid(
        row=3, column=0, padx=10, pady=5, sticky="e"
    )
    global time_entry
    time_entry = tk.Entry(choices_frame)
    time_entry.grid(row=3, column=1, padx=10, pady=5)

    create_unit_menus(
        [
            "kilometer",
            "millimeter",
            "centimeter",
            "inch",
            "foot",
            "yard",
            "meter",
            "mile",
            "nautical_mile",
        ],
        "Length Unit:",
        4,
        "length_unit_var",
    )
    create_unit_menus(["km/h", "m/s", "mph", "kn"], "Speed Unit:", 5, "speed_unit_var")


def create_density_inputs():
    tk.Label(choices_frame, text="Mass (num):", bg="lightblue").grid(
        row=1, column=0, padx=10, pady=5, sticky="e"
    )
    global input_entry
    input_entry = tk.Entry(choices_frame)
    input_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(choices_frame, text="Volume (num):", bg="lightblue").grid(
        row=2, column=0, padx=10, pady=5, sticky="e"
    )
    global volume_entry
    volume_entry = tk.Entry(choices_frame)
    volume_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(choices_frame, text="Density (str):", bg="lightblue").grid(
        row=3, column=0, padx=10, pady=5, sticky="e"
    )
    global density_entry
    density_entry = tk.Entry(choices_frame)
    density_entry.grid(row=3, column=1, padx=10, pady=5)

    create_unit_menus(
        [
            "kilogram",
            "milligram",
            "carat",
            "gram",
            "ounce",
            "pound",
            "stone",
            "slug",
            "tonne",
        ],
        "Mass Unit:",
        4,
        "mass_unit_var",
    )

    create_unit_menus(
        ["m³", "mL", "cm³", "fl_oz", "cup", "pt", "qt", "L", "gal", "bbl"],
        "Volume Unit:",
        5,
        "volume_unit_var",
    )


def create_force_inputs():
    tk.Label(choices_frame, text="Mass (num):", bg="lightblue").grid(
        row=1, column=0, padx=10, pady=5, sticky="e"
    )
    global input_entry
    input_entry = tk.Entry(choices_frame)
    input_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(choices_frame, text="Acceleration (num):", bg="lightblue").grid(
        row=2, column=0, padx=10, pady=5, sticky="e"
    )
    global acceleration_entry
    acceleration_entry = tk.Entry(choices_frame)
    acceleration_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(choices_frame, text="Force (str):", bg="lightblue").grid(
        row=3, column=0, padx=10, pady=5, sticky="e"
    )
    global force_entry
    force_entry = tk.Entry(choices_frame)
    force_entry.grid(row=3, column=1, padx=10, pady=5)

    create_unit_menus(
        [
            "kilogram",
            "milligram",
            "carat",
            "gram",
            "ounce",
            "pound",
            "stone",
            "slug",
            "tonne",
        ],
        "Mass Unit:",
        4,
        "mass_unit_var",
    )

    create_unit_menus(
        [
            "meter_per_second_squared",
            "foot_per_second_squared",
            "centimeter_per_second_squared",
            "gal",
            "inch_per_second_squared",
            "kilometer_per_hour_squared",
            "mile_per_hour_squared",
            "gravity",
        ],
        "Acceleration Unit:",
        5,
        "acceleration_unit_var",
    )


def create_pressure_inputs():
    tk.Label(choices_frame, text="Force (num):", bg="lightblue").grid(
        row=1, column=0, padx=10, pady=5, sticky="e"
    )
    global input_entry
    input_entry = tk.Entry(choices_frame)
    input_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(choices_frame, text="Area (num):", bg="lightblue").grid(
        row=2, column=0, padx=10, pady=5, sticky="e"
    )
    global area_entry
    area_entry = tk.Entry(choices_frame)
    area_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(choices_frame, text="Pressure (str):", bg="lightblue").grid(
        row=3, column=0, padx=10, pady=5, sticky="e"
    )
    global pressure_entry
    pressure_entry = tk.Entry(choices_frame)
    pressure_entry.grid(row=3, column=1, padx=10, pady=5)

    create_unit_menus(
        [
            "newton",
            "dyne",
            "kilonewton",
            "pound_force",
            "ounce_force",
            "ton_force",
            "kilogram_force",
            "gram_force",
            "millinewton",
            "poundal",
            "slug_force",
        ],
        "Force Unit:",
        4,
        "force_unit_var",
    )

    create_unit_menus(
        [
            "square_meter",
            "square_centimeter",
            "square_foot",
            "square_yard",
            "acre",
            "hectare",
            "square_kilometer",
        ],
        "Area Unit:",
        5,
        "area_unit_var",
    )


def create_unit_menus(options, label_text, row, var_name):
    tk.Label(choices_frame, text=label_text, bg="lightblue").grid(
        row=row, column=0, padx=10, pady=5, sticky="e"
    )
    global_vars = globals()
    global_vars[var_name] = tk.StringVar(choices_frame)
    global_vars[var_name].set(options[0])
    tk.OptionMenu(choices_frame, global_vars[var_name], *options).grid(
        row=row, column=1, padx=10, pady=5
    )




def MetricusGUI():
    main_bg = "lightblue"

    root = tk.Tk()
    root.geometry("700x500")
    root.configure(bg=main_bg)

    label = tk.Label(
        root, text="Metricus GUI", bg=main_bg, fg="black", font=("Helvetica", 18)
    )
    label.grid(row=0, column=1, pady=10)

    global choices_frame
    choices_frame = tk.Frame(root, bg=main_bg)
    choices_frame.grid(row=1, column=1, pady=10, sticky="nsew")

    global choice_label
    choice_label = tk.Label(
        root, text="", fg="gray", bg="lightblue", font=("Helvetica", 12)
    )
    choice_label.grid(row=3, column=1, pady=5)
    go_back_to_main()

    close_button = tk.Button(
        root,
        text="Close",
        bg="darkred",
        fg="white",
        width=10,
        height=1,
        command=root.destroy,
    )
    close_button.grid(row=2, column=1, pady=10)

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(2, weight=1)

    root.mainloop()
