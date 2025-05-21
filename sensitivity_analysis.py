#!/usr/bin/env python3

import sys
import os

# Add the parent directory to the Python path to allow importing 'api'
# This assumes 'sensitivity_analysis.py' is in the same directory as 'api.py'
# or that 'api.py' is in a way that it can be imported directly.
# For robustness, especially if structure changes, consider packaging or more explicit path management.

# Attempt to import the simulation function. 
# This assumes api.py is in the same directory or PYTHONPATH is set up.
try:
    from api import run_financial_simulation, chaos_events
except ImportError as e:
    # If api.py is in the same directory, this should work.
    # If it's in a subdirectory or elsewhere, sys.path might need adjustment.
    # Example: current_dir = os.path.dirname(os.path.abspath(__file__))
    # sys.path.append(current_dir) # Or parent_dir if api.py is one level up, etc.
    print(f"Error importing 'run_financial_simulation' from 'api.py': {e}")
    print("Please ensure 'api.py' is in the same directory as this script or in the PYTHONPATH.")
    sys.exit(1)

def perform_sensitivity_analysis():
    initial_expenditure = 4  # Default initial annual expenditure in lakhs, based on financial_modeling.py
    start_age = 26
    target_age = 60
    num_simulations_per_combination = 100
    neutral_luck_factor = "neutral"

    # Define ranges for initial salary and initial capital (in lakhs)
    # These ranges can be adjusted based on desired granularity and computational time
    initial_salaries = range(20, 61, 5)  # e.g., 20L to 60L, step 5L
    initial_capitals = range(0, 101, 10) # e.g., 0L to 100L, step 10L

    successful_combinations = []

    print(f"Starting sensitivity analysis...")
    print(f"Parameters: Start Age={start_age}, Target Age={target_age}, Expenditure={initial_expenditure}L/year, Luck Factor='{neutral_luck_factor}', Runs per combo={num_simulations_per_combination}")
    print("-----------------------------------------------------")

    total_combinations = len(list(initial_salaries)) * len(list(initial_capitals))
    current_combination_count = 0

    for salary in initial_salaries:
        for capital in initial_capitals:
            current_combination_count += 1
            print(f"\nTesting combination {current_combination_count}/{total_combinations}: Initial Salary = {salary}L, Initial Capital = {capital}L")
            
            debt_free_in_all_runs = True
            max_debt_encountered_for_combo = 0

            for i in range(num_simulations_per_combination):
                # Ensure chaos_events is available to run_financial_simulation
                # It's defined globally in api.py, so direct import of the function should be fine.
                simulation_results = run_financial_simulation(
                    initial_income_param=salary,
                    initial_expenditure_param=initial_expenditure,
                    initial_capital_param=capital,
                    current_age_param=start_age,
                    future_age_param=target_age,
                    luck_factor_param=neutral_luck_factor
                )
                
                final_year_data = None
                for year_data in simulation_results:
                    if year_data['age'] == target_age:
                        final_year_data = year_data
                        break
                
                if final_year_data is None:
                    print(f"  Run {i+1}/{num_simulations_per_combination}: Error - Target age {target_age} not found in results.")
                    debt_free_in_all_runs = False # Mark as failure for safety
                    break 

                if final_year_data['totalDebt'] > 0:
                    debt_free_in_all_runs = False
                    max_debt_encountered_for_combo = max(max_debt_encountered_for_combo, final_year_data['totalDebt'])
                    # print(f"  Run {i+1}/{num_simulations_per_combination}: Debt of {final_year_data['totalDebt']:.2f}L at age {target_age}.")
                    break # This combination failed, no need for more runs for it
            
            if debt_free_in_all_runs:
                print(f"  SUCCESS: Salary={salary}L, Capital={capital}L -> Consistently NO DEBT by age {target_age}.")
                successful_combinations.append({'salary': salary, 'capital': capital})
            else:
                print(f"  FAILURE: Salary={salary}L, Capital={capital}L -> Potential debt by age {target_age}. Max debt observed: {max_debt_encountered_for_combo:.2f}L")

    print("\n--- Sensitivity Analysis Complete ---")
    
    # Ensure unique combinations before printing and sort them
    # Convert list of dicts to list of tuples for set operation, then sort
    if successful_combinations:
        # Create a set of tuples to get unique pairs, then convert back to a list of dicts or tuples for sorted printing
        unique_combo_tuples = sorted(list(set((d['salary'], d['capital']) for d in successful_combinations)))
        
        print(f"Found {len(unique_combo_tuples)} unique combinations that result in no debt by age {target_age} across all {num_simulations_per_combination} '{neutral_luck_factor}' luck simulations:")
        for salary, capital in unique_combo_tuples:
            print(f"  - Initial Salary: {salary} Lakhs, Initial Capital: {capital} Lakhs")
    else:
        # This case handles when successful_combinations is empty from the start
        print(f"Found 0 combinations that result in no debt by age {target_age} across all {num_simulations_per_combination} '{neutral_luck_factor}' luck simulations:")
        print("  No combinations found that consistently guarantee no debt under the specified conditions and ranges.")
        print("  Consider expanding the ranges for salary/capital or adjusting other parameters.")

if __name__ == "__main__":
    # This is to ensure that api.py (and its chaos_events) can be found if it's in the same directory
    # This might not be necessary if the project is structured as a package or PYTHONPATH is set
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    perform_sensitivity_analysis()