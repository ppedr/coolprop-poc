import CoolProp.CoolProp as CP
from scipy.optimize import newton
import math

# --- 1. THE COMPLEX PHYSICS ENGINE ---
def simulate_real_turbine(mass_flow_rate, P_in, T_in, P_out):
    fluid = 'Water'
    
    # --- THE COMPLEXITY: DYNAMIC EFFICIENCY ---
    # In this model, efficiency is a curve, not a fixed number.
    # If flow is low, efficiency crashes. If flow is high, it stabilizes.
    # We use a mathematical curve: 0.90 * (1 - e^(-flow/10))
    
    max_efficiency = 0.90
    
    # Safety: Solver might guess negative numbers, so we take absolute value
    flow = abs(mass_flow_rate) 
    
    # This formula creates a curve where efficiency is bad at low flow
    current_efficiency = max_efficiency * (1 - math.exp(-flow / 10))
    
    # --- STANDARD COOLPROP PHYSICS ---
    h_in = CP.PropsSI('H', 'P', P_in, 'T', T_in, fluid)
    s_in = CP.PropsSI('S', 'P', P_in, 'T', T_in, fluid)
    
    # Ideal expansion
    h_out_ideal = CP.PropsSI('H', 'P', P_out, 'S', s_in, fluid)
    
    # Actual expansion using our DYNAMIC efficiency
    delta_h_ideal = h_in - h_out_ideal
    delta_h_actual = delta_h_ideal * current_efficiency
    
    # Calculate Power
    power_watts = mass_flow_rate * delta_h_actual
    
    return power_watts, current_efficiency

# --- 2. THE ERROR FUNCTION ---
def objective_function(mass_flow_guess):
    # Run the simulation with the guess
    calculated_power, _ = simulate_real_turbine(mass_flow_guess, P_IN, T_IN, P_OUT)
    
    # Calculate error
    return calculated_power - TARGET_POWER_WATTS


# --- 3. THE PROBLEM DEFINITION ---
# These are the constraints of your engine
P_IN = 100 * 1e5   # 60 Bar
T_IN = 500 + 273.15 # 450 C
P_OUT = 0.1 * 1e5 # 0.1 Bar

# This is what the user WANTS
TARGET_POWER_WATTS = 50 * 1e6 # 50 MW

# --- 4. RUN THE SOLVER ---
print(f"Target Power: {TARGET_POWER_WATTS/1e6} MW")
print("Solver is starting...")

# We start guessing at 1.0 kg/s
required_mass_flow = newton(objective_function, x0=1.0)

print(f"Solution Found!")
print(f"Required Mass Flow: {required_mass_flow:.2f} kg/s")

# --- 5. ANALYZE THE RESULT ---
# Now that we have the flow, let's see what the efficiency actually was
final_power, final_eff = simulate_real_turbine(required_mass_flow, P_IN, T_IN, P_OUT)

print(f"--- Final State ---")
print(f"Resulting Power: {final_power/1e6:.2f} MW")
print(f"Resulting Efficiency: {final_eff*100:.2f}%") 
# Notice: The efficiency is NOT 0.90. It was calculated dynamically!