import CoolProp.CoolProp as CP
from scipy.optimize import newton

# --- 1. THE COMPLEX PHYSICS ENGINE ---.
def simulate_turbine_physics(mass_flow_rate, P_in, T_in, P_out, efficiency):
    fluid = 'Water'
    
    # Calculate Inlet State
    h_in = CP.PropsSI('H', 'P', P_in, 'T', T_in, fluid)
    s_in = CP.PropsSI('S', 'P', P_in, 'T', T_in, fluid)
    
    # Calculate Outlet State
    h_out_ideal = CP.PropsSI('H', 'P', P_out, 'S', s_in, fluid)
    delta_h_actual = (h_in - h_out_ideal) * efficiency
    
    # Calculate Power
    power_watts = mass_flow_rate * delta_h_actual
    return power_watts

# --- 2. THE PROBLEM DEFINITION ---
# These are the fixed constraints of your engine
FIXED_P_IN = 100 * 1e5   # 100 Bar
FIXED_T_IN = 500 + 273.15 # 500 C
FIXED_P_OUT = 0.1 * 1e5  # 0.1 Bar
FIXED_EFF = 0.85         # 85%

# This is what the user WANTS
TARGET_POWER_WATTS = 50 * 1e6 # 50 MW

# --- 3. THE OBJECTIVE FUNCTION ---
# The solver calls THIS function repeatedly.
# It asks: "If I try this mass flow, how far off is the power from the target?"
def error_function(mass_flow_guess):
    # A. Run the Physics (Call CoolProp)
    actual_power = simulate_turbine_physics(
        mass_flow_guess, 
        FIXED_P_IN, 
        FIXED_T_IN, 
        FIXED_P_OUT, 
        FIXED_EFF
    )
    
    # B. Calculate the Error (Difference)
    error = actual_power - TARGET_POWER_WATTS
    return error

# --- 4. RUN THE SOLVER ---
print(f"Target Power: {TARGET_POWER_WATTS/1e6} MW")
print("Solver is starting...")

# We give it a starting guess of 1.0 kg/s
# The solver will now run 'error_function' -> which runs 'simulate_turbine_physics' -> which runs CoolProp
# It will do this over and over until error is 0.
result_mass_flow = newton(error_function, x0=1.0)

print(f"Solver finished!")
print(f"Required Mass Flow: {result_mass_flow:.4f} kg/s")

# --- 5. VERIFY ---
# Let's plug the result back in to be sure
final_power = simulate_turbine_physics(result_mass_flow, FIXED_P_IN, FIXED_T_IN, FIXED_P_OUT, FIXED_EFF)
print(f"Verification Power: {final_power/1e6:.4f} MW")