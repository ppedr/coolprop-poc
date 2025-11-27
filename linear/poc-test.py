from linear import calculate_turbine_power

# --- Test Cases ---

test_cases = [
    {
        "name": "1. High Pressure Utility Turbine (Main Stage)",
        "description": "High pressure steam entering, exiting at medium pressure to go to a reheater.",
        "mass_flow": 100.0,    # 100 kg/s (Large flow)
        "P_in_bar": 160.0,     # 160 Bar (Very high pressure)
        "T_in_C": 550.0,       # 550°C (Superheated)
        "P_out_bar": 40.0,     # 40 Bar exit
        "efficiency": 0.90     # 90% efficient
    },
    {
        "name": "2. Low Pressure Condensing Turbine (Final Stage)",
        "description": "Low pressure steam expanding into a vacuum condenser. Watch for wet steam!",
        "mass_flow": 80.0,     # 80 kg/s
        "P_in_bar": 5.0,       # 5 Bar
        "T_in_C": 200.0,       # 200°C
        "P_out_bar": 0.05,     # 0.05 Bar (Deep vacuum)
        "efficiency": 0.85     # 85% efficient
    },
    {
        "name": "3. Small Industrial Backpressure Turbine",
        "description": "Generating power while reducing pressure for factory heating processes.",
        "mass_flow": 10.0,     # 10 kg/s (Small flow)
        "P_in_bar": 40.0,      # 40 Bar
        "T_in_C": 400.0,       # 400°C
        "P_out_bar": 5.0,      # 5 Bar (Exhaust used for heating)
        "efficiency": 0.75     # 75% efficient (Smaller machines are less efficient)
    }
]

print("\n--- RUNNING TEST CASES ---")

for case in test_cases:
    # Convert units for the function (Bar -> Pa, C -> K)
    p_in_pa = case["P_in_bar"] * 1e5
    t_in_k = case["T_in_C"] + 273.15
    p_out_pa = case["P_out_bar"] * 1e5
    
    result = calculate_turbine_power(
        case["mass_flow"], 
        p_in_pa, 
        t_in_k, 
        p_out_pa, 
        case["efficiency"]
    )
    
    print(f"\nScenario: {case['name']}")
    print(f"  Input: {case['P_in_bar']} Bar / {case['T_in_C']}°C")
    print(f"  Output Power: {result['power_output_mw']:.2f} MW")
    print(f"  Exit Temp:    {result['temperature_out_celsius']:.2f} °C")