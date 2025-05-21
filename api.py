from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import random

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# --- Constants and Chaos Event Probabilities (copied from financial_modeling.py) ---
chaos_events = {
    'job_loss': {
        'prob': 0.08, # Annual probability
        'min_duration_months': 3,
        'max_duration_months': 18,
        'salary_drop_range': (0.6, 0.85), # New salary as % of old
        'recovery_time_years_range': (1, 3) # Years to recover to pre-loss income trajectory
    },
    'medical_emergency': {
        'base_prob': 0.03, # Base annual probability
        'age_factor': 0.0015, # Probability increases by this factor * age
        'cost_range_lakhs': (5, 30)
    },
    'market_crash': {
        'prob': 0.1, # Annual probability of a crash starting
        'return_range': (-0.35, -0.15), # Equity return during crash year
        'recovery_years_range': (2, 4) # Years for market to return to normal returns
    },
    'family_expense': { # General large unexpected family expenses
        'prob': 0.05, # Annual probability
        'cost_range_lakhs': (3, 15)
    },
    'black_swan': {
        'prob': 0.015, # Probability per simulation (once-in-a-lifetime type)
        'savings_loss_multiplier': 0.4, # Retain 40% of savings
        'income_loss_multiplier': 0.6 # Retain 60% of income
    },
    'children_education': {
        'cost_per_child_lakhs': 30,
        'age_windows': [(17, 19), (20, 22)] # Child's age for expense
    },
    'children_marriage': {
        'cost_per_child_lakhs': 30,
        'age_window': (25, 30) # Child's age for expense
    },
    'child_birth': {
        'cost_range_lakhs': (1, 5) # Initial cost when a child is born
    },
    'career_advancement': {
        'prob': 0.20, # Annual probability
        'salary_boost_multiplier_range': (1.15, 1.30)
    },
    'inheritance': {
        'age_window_person': (45, 55),
        'prob_in_window_annual': 0.05, # Annual chance if in age window and not yet received
        'amount_range_lakhs': (20, 100)
    },
    'business_venture': {
        'age_window_person': (35, 45),
        'prob_in_window_annual': 0.03, # Annual chance to attempt if in window
        'investment_range_lakhs': (25, 75),
        'success_prob': 0.3,
        'success_return_multiplier_range': (2.0, 5.0), # Multiplies investment
        'failure_loss_percentage': 0.80 # Lose 80% of investment
    },
    'divorce': {
        'prob_if_married_annual': 0.02, # Assuming marriage happens around 28-32
        'savings_loss_percentage': 0.5,
        'income_loss_percentage_temp': 0.2 # Temporary reduction due to alimony/disruption
    }
}

# --- Simulation Logic (adapted from financial_modeling.py) ---
def run_financial_simulation(initial_income_param, initial_expenditure_param, initial_capital_param, current_age_param, future_age_param, luck_factor_param="neutral"):
    def adjust_for_luck(base_value, luck_factor, is_probability=True, is_good_event=False, lower_bound=None, upper_bound=None):
        multiplier = 1.0
        if luck_factor == 'unlucky':
            multiplier = 1.25 if not is_good_event else 0.75
        elif luck_factor == 'lucky':
            multiplier = 0.75 if not is_good_event else 1.25
        
        adjusted_value = base_value * multiplier
        
        if is_probability:
            adjusted_value = max(0, min(1, adjusted_value))
        
        if lower_bound is not None:
            adjusted_value = max(lower_bound, adjusted_value)
        if upper_bound is not None:
            adjusted_value = min(upper_bound, adjusted_value)
            
        return adjusted_value
    # Use passed parameters
    initial_income = initial_income_param
    initial_expenditure = initial_expenditure_param
    initial_capital = initial_capital_param
    current_age = current_age_param
    future_age = future_age_param

    years_to_simulate = future_age - current_age
    
    total_savings = initial_capital
    current_income_annual = initial_income
    current_expenditure_annual = initial_expenditure
    current_debt = 0
    
    year_list = [0]
    age_list = [current_age]
    income_list = [current_income_annual]
    post_tax_income_list = [current_income_annual * 0.7]
    expenditure_list = [current_expenditure_annual]
    savings_this_year_list = [post_tax_income_list[0] - expenditure_list[0]]
    total_savings_list = [total_savings]
    debt_list = [current_debt]
    event_log = ["Initial State"]

    tax_rate = 0.30
    base_equity_return_rate = 0.10
    base_fd_return_rate = 0.06
    equity_allocation = 0.60
    fd_allocation = 0.40
    expenditure_base_growth_rate = 0.07
    inflation_rate = 0.06

    num_children = random.randint(0, 2)
    children_birth_years = []
    if num_children >= 1:
        children_birth_years.append(random.randint(2, 6))
    if num_children == 2:
        first_child_birth_year = children_birth_years[0]
        second_child_birth_year = random.randint(max(first_child_birth_year + 1, 6), 9)
        children_birth_years.append(second_child_birth_year)
        children_birth_years.sort()

    children_ages = [-1] * num_children
    children_education_spent = [False for _ in range(num_children)]
    children_marriage_spent = [False] * num_children

    job_loss_active_months = 0
    job_loss_recovery_years_remaining = 0
    income_before_job_loss = 0
    market_crash_recovery_years_remaining = 0
    effective_equity_return_rate = base_equity_return_rate
    
    inheritance_received = False
    business_venture_taken = False
    divorce_occurred = False
    black_swan_event_occurred = False
    married_implicitly_year = random.randint(2,6)

    for year_idx in range(1, years_to_simulate + 1):
        current_sim_age = current_age + year_idx
        is_retired = current_sim_age > 60  # Retirement condition
        annual_event_log_entries = []

        # Initial income for the year
        if is_retired:
            current_year_income = 0
            # Ensure current_income_annual is also 0 if it's used as a base for the next year's income
            # This will be set again before appending to lists, but good to be clear here.
            if not any("Retired" in entry for entry in event_log[-1].split(", ")):
                 annual_event_log_entries.append("🌴 Retired: Income set to 0.")
        else:
            current_year_income = current_income_annual
        
        for i in range(num_children):
            if year_idx == children_birth_years[i]:
                cost = random.uniform(*chaos_events['child_birth']['cost_range_lakhs'])
                total_savings -= cost
                annual_event_log_entries.append(f"👶 Child {i+1} Born (-{cost:.2f}L)")

        for i in range(num_children):
            if year_idx >= children_birth_years[i]:
                children_ages[i] = current_sim_age - (current_age + children_birth_years[i])

        current_year_expenditure = current_expenditure_annual

        # --- Chaos Events --- 

        # 2. Medical Emergency (can happen anytime)
        base_medical_prob = chaos_events['medical_emergency']['base_prob'] + (current_sim_age * chaos_events['medical_emergency']['age_factor'])
        medical_prob = adjust_for_luck(base_medical_prob, luck_factor_param, is_probability=True, is_good_event=False)
        if random.random() < medical_prob:
            cost = random.uniform(*chaos_events['medical_emergency']['cost_range_lakhs'])
            total_savings -= cost
            annual_event_log_entries.append(f"🏥 Medical Emergency (-{cost:.2f}L)")

        # 3. Market Crash (affects investments, can happen regardless of retirement status)
        # Assuming market crash logic should remain active as it affects investments, not personal "life events"
        effective_equity_return_rate = base_equity_return_rate # Reset to base before checking for new crash or ongoing recovery
        if market_crash_recovery_years_remaining > 0:
            market_crash_recovery_years_remaining -= 1
            annual_event_log_entries.append(f"📉 Market Recovery Ongoing ({market_crash_recovery_years_remaining} yrs left)")
            if market_crash_recovery_years_remaining == 0:
                 annual_event_log_entries.append("📈 Market Fully Recovered")
        elif random.random() < adjust_for_luck(chaos_events['market_crash']['prob'], luck_factor_param, is_probability=True, is_good_event=False):
            effective_equity_return_rate = random.uniform(*chaos_events['market_crash']['return_range'])
            market_crash_recovery_years_remaining = random.randint(*chaos_events['market_crash']['recovery_years_range'])
            annual_event_log_entries.append(f"📉 Market Crash! Equity returns {effective_equity_return_rate*100:.0f}%. Recovery: {market_crash_recovery_years_remaining} yrs.")

        # Events that only occur if NOT retired
        if not is_retired:
            # 1. Job Loss
            if job_loss_active_months > 0:
                job_loss_active_months -= 12
                current_year_income = 0 
                annual_event_log_entries.append(f"🧨 Job Loss Ongoing ({job_loss_active_months // 12 if job_loss_active_months > 0 else 0} yrs left)")
                if job_loss_active_months <= 0:
                    drop_factor = random.uniform(*chaos_events['job_loss']['salary_drop_range'])
                    current_income_annual = income_before_job_loss * drop_factor
                    job_loss_recovery_years_remaining = random.randint(*chaos_events['job_loss']['recovery_time_years_range'])
                    annual_event_log_entries.append(f"💸 Job Ended. New salary {current_income_annual:.2f}L. Recovery: {job_loss_recovery_years_remaining} yrs.")
            elif job_loss_recovery_years_remaining > 0:
                recovery_increment = (income_before_job_loss - current_income_annual) / job_loss_recovery_years_remaining
                current_income_annual += recovery_increment
                job_loss_recovery_years_remaining -= 1
                annual_event_log_entries.append(f"📈 Job Recovery. Income: {current_income_annual:.2f}L. {job_loss_recovery_years_remaining} yrs left.")
                if job_loss_recovery_years_remaining == 0: current_income_annual = income_before_job_loss
            elif random.random() < adjust_for_luck(chaos_events['job_loss']['prob'], luck_factor_param, is_probability=True, is_good_event=False):
                income_before_job_loss = current_income_annual
                duration_months = random.randint(chaos_events['job_loss']['min_duration_months'], chaos_events['job_loss']['max_duration_months'])
                job_loss_active_months = duration_months
                current_year_income = 0
                annual_event_log_entries.append(f"🧨 Job Loss Started ({duration_months} months)")

            # 4. Family Expense
            if random.random() < chaos_events['family_expense']['prob']:
                cost = random.uniform(*chaos_events['family_expense']['cost_range_lakhs'])
                total_savings -= cost
                annual_event_log_entries.append(f"👨‍👩‍👧‍👦 Family Expense (-{cost:.2f}L)")

            # 5. Black Swan
            if not black_swan_event_occurred and random.random() < chaos_events['black_swan']['prob'] / years_to_simulate :
                total_savings *= chaos_events['black_swan']['savings_loss_multiplier']
                current_income_annual *= chaos_events['black_swan']['income_loss_multiplier']
                if job_loss_active_months > 0 or job_loss_recovery_years_remaining >0 : income_before_job_loss *= chaos_events['black_swan']['income_loss_multiplier']
                black_swan_event_occurred = True
                annual_event_log_entries.append("🌪️ BLACK SWAN! Savings & Income Hit!")

            # 6. Children's Education
            for i in range(num_children):
                if children_ages[i] != -1:
                    if not children_education_spent[i] and children_ages[i] == 18:
                        cost = chaos_events['children_education']['cost_per_child_lakhs']
                        total_savings -= cost
                        children_education_spent[i] = True
                        annual_event_log_entries.append(f"🎓 Child {i+1} Edu. (-{cost:.2f}L, Age {children_ages[i]})" )
            
            # 7. Children's Marriage
            for i in range(num_children):
                 if children_ages[i] != -1 and not children_marriage_spent[i] and chaos_events['children_marriage']['age_window'][0] <= children_ages[i] <= chaos_events['children_marriage']['age_window'][1]:
                    if children_ages[i] == chaos_events['children_marriage']['age_window'][0]: # Assuming expense occurs at the start of the window
                        cost = chaos_events['children_marriage']['cost_per_child_lakhs']
                        total_savings -= cost
                        children_marriage_spent[i] = True
                        annual_event_log_entries.append(f"💒 Child {i+1} Marriage (-{cost:.2f}L, Age {children_ages[i]})" )

            # 9. Career Advancement
            base_career_advancement_prob = chaos_events['career_advancement']['prob']
            if current_sim_age > 35:
                base_career_advancement_prob *= max(0.1, 1 - (current_sim_age - 35) * 0.02)
            
            career_advancement_prob_final = adjust_for_luck(base_career_advancement_prob, luck_factor_param, is_probability=True, is_good_event=True)
            if job_loss_active_months <= 0 and random.random() < career_advancement_prob_final:
                boost = random.uniform(*chaos_events['career_advancement']['salary_boost_multiplier_range'])
                current_income_annual *= boost
                current_income_annual = min(current_income_annual, 150) # Cap income
                if job_loss_recovery_years_remaining > 0 : income_before_job_loss *= boost
                annual_event_log_entries.append(f"🚀 Career Advancement! New Income: {current_income_annual:.2f}L (Age {current_sim_age})" )

            # 10. Inheritance
            if not inheritance_received and chaos_events['inheritance']['age_window_person'][0] <= current_sim_age <= chaos_events['inheritance']['age_window_person'][1]:
                if random.random() < chaos_events['inheritance']['prob_in_window_annual']:
                    amount = random.uniform(*chaos_events['inheritance']['amount_range_lakhs'])
                    total_savings += amount
                    inheritance_received = True
                    annual_event_log_entries.append(f"💰 Inheritance Received! (+{amount:.2f}L)")

            # 11. Business Venture
            if not business_venture_taken and chaos_events['business_venture']['age_window_person'][0] <= current_sim_age <= chaos_events['business_venture']['age_window_person'][1]:
                if random.random() < chaos_events['business_venture']['prob_in_window_annual']:
                    investment = random.uniform(*chaos_events['business_venture']['investment_range_lakhs'])
                    if total_savings >= investment:
                        total_savings -= investment
                        business_venture_taken = True
                        if random.random() < chaos_events['business_venture']['success_prob']:
                            returns = investment * random.uniform(*chaos_events['business_venture']['success_return_multiplier_range'])
                            total_savings += returns
                            annual_event_log_entries.append(f"📈 Business Success! Invested {investment:.2f}L, Returned {returns:.2f}L")
                        else:
                            loss = investment * chaos_events['business_venture']['failure_loss_percentage']
                            # total_savings += (investment - loss) # This was adding back part of investment, should be just loss from capital
                            # Correct: investment is already subtracted, if failed, nothing is added back beyond remaining investment value if not 100% loss
                            # The current logic implies (investment - loss) is added back, meaning if 80% loss, 20% of investment is returned to savings.
                            # Let's assume the original intent was that the *remaining value* of the venture is (investment - loss), which is effectively already handled if investment was fully subtracted.
                            # If failure_loss_percentage is 0.8, it means 20% of investment value remains. So, add back investment * (1-failure_loss_percentage)
                            total_savings += investment * (1 - chaos_events['business_venture']['failure_loss_percentage'])
                            annual_event_log_entries.append(f"📉 Business Failed. Invested {investment:.2f}L, Lost {investment * chaos_events['business_venture']['failure_loss_percentage']:.2f}L")
                    else:
                        annual_event_log_entries.append("💸 Wanted Business Venture, Insufficient Capital")
            
            # 12. Divorce
            if not divorce_occurred and year_idx > married_implicitly_year and random.random() < chaos_events['divorce']['prob_if_married_annual']:
                savings_hit = total_savings * chaos_events['divorce']['savings_loss_percentage']
                total_savings -= savings_hit
                income_reduction = current_income_annual * chaos_events['divorce']['income_loss_percentage_temp']
                current_income_annual -= income_reduction
                current_year_income = current_income_annual # Update current_year_income if it changed mid-year due to divorce
                if job_loss_active_months > 0 or job_loss_recovery_years_remaining >0 : income_before_job_loss -= income_reduction
                divorce_occurred = True
                annual_event_log_entries.append(f"💔 Divorce. Savings -{savings_hit:.2f}L, Temp Income Drop -{income_reduction:.2f}L")
        # --- End of non-retired events ---

        # Final income adjustments for the year if retired
        if is_retired:
            current_year_income = 0
            current_income_annual = 0 # Ensure base for next year is also zero

        income_after_tax = current_year_income * (1 - tax_rate)
        savings_this_year = income_after_tax - current_year_expenditure
        
        investable_capital = total_savings + (savings_this_year if savings_this_year > 0 else 0)
        equity_investment = 0
        fd_investment = 0
        equity_return = 0
        fd_return = 0

        if investable_capital > 0:
            equity_investment = investable_capital * equity_allocation
            fd_investment = investable_capital * fd_allocation
            equity_return = equity_investment * effective_equity_return_rate
            fd_return = fd_investment * base_fd_return_rate
        
        total_savings += savings_this_year
        total_savings += equity_return + fd_return

        if total_savings < 0:
            new_debt_this_year = abs(total_savings)
            current_debt += new_debt_this_year
            total_savings = 0 
            annual_event_log_entries.append(f"🆘 Incurred Debt: {new_debt_this_year:.2f}L. Total Debt: {current_debt:.2f}L")
        elif current_debt > 0 and total_savings > 0:
            pay_off_amount = min(current_debt, total_savings)
            current_debt -= pay_off_amount
            total_savings -= pay_off_amount
            annual_event_log_entries.append(f"💰 Paid Off Debt: {pay_off_amount:.2f}L. Remaining Debt: {current_debt:.2f}L")

        # Annual income growth (salary increases) - only if not retired
        if not is_retired:
            if job_loss_active_months <= 0 and job_loss_recovery_years_remaining <=0 : # And not in active job loss
                if current_income_annual >= 150:
                    pass # Cap reached or near cap, minimal/no growth
                elif current_income_annual >= 100:
                    current_income_annual *= random.uniform(1.005, 1.015) # Slower growth at higher incomes
                elif current_sim_age < 35: # Prime growth years
                    current_income_annual *= random.uniform(1.07, 1.15)
                elif current_sim_age < 50: # Mid-career growth
                    current_income_annual *= random.uniform(1.04, 1.08)
                else: # Later career growth, slowing down
                    current_income_annual *= random.uniform(1.01, 1.03)
                current_income_annual = min(current_income_annual, 150) # Ensure cap after growth
        else:
            current_income_annual = 0 # Explicitly ensure income remains zero in retirement for next year's base
        
        child_expense_factor = sum([0.03 for i in range(num_children) if children_ages[i] != -1 and children_ages[i] < 18])
        current_expenditure_annual *= (1 + inflation_rate + expenditure_base_growth_rate + child_expense_factor)
        current_expenditure_annual = min(current_expenditure_annual, current_income_annual * 0.8 if current_income_annual > 0 else 100)

        year_list.append(year_idx)
        age_list.append(current_sim_age)
        income_list.append(current_income_annual)
        post_tax_income_list.append(income_after_tax)
        expenditure_list.append(current_year_expenditure)
        savings_this_year_list.append(savings_this_year)
        total_savings_list.append(total_savings)
        debt_list.append(current_debt)
        event_log.append(", ".join(annual_event_log_entries) if annual_event_log_entries else "Normal Year")

    results_data = []
    for i in range(len(year_list)):
        results_data.append({
            'year': year_list[i],
            'age': age_list[i],
            'income': round(income_list[i], 2),
            'postTaxIncome': round(post_tax_income_list[i], 2),
            'expenditure': round(expenditure_list[i], 2),
            'savingsThisYear': round(savings_this_year_list[i], 2),
            'totalSavings': round(total_savings_list[i], 2),
            'totalDebt': round(debt_list[i], 2),
            'events': event_log[i]
        })
    return results_data

@app.route('/simulate', methods=['POST'])
def handle_simulation():
    data = request.get_json()
    initial_income = float(data.get('initial_income', 20))
    initial_expenditure = float(data.get('initial_expenditure', 4))
    initial_capital = float(data.get('initial_capital', 20))
    current_age = int(data.get('current_age', 26))
    future_age = int(data.get('future_age', 60))
    luck_factor = data.get('luck_factor', 'neutral')

    simulation_results = run_financial_simulation(
        initial_income,
        initial_expenditure,
        initial_capital,
        current_age,
        future_age,
        luck_factor
    )
    return jsonify(simulation_results)

@app.route('/sensitivity_analysis', methods=['POST'])
def handle_sensitivity_analysis():
    data = request.get_json()

    income_min = float(data.get('income_min', 10))
    income_max = float(data.get('income_max', 30))
    income_step = float(data.get('income_step', 5))

    # Expenditure is now derived from income, so these are no longer direct inputs for iteration
    # We can define a default ratio or make it configurable if needed later
    expenditure_to_income_ratio = data.get('expenditure_to_income_ratio', 0.2) # Default to 20% of income

    capital_min = float(data.get('capital_min', 5))
    capital_max = float(data.get('capital_max', 40))
    capital_step = float(data.get('capital_step', 5))

    current_age = int(data.get('current_age', 26))
    future_age = int(data.get('future_age', 60))
    luck_factor = data.get('luck_factor', 'neutral')
    
    num_simulations_per_combination = int(data.get('num_simulations_per_combination', 10))
    # Target savings at future_age (e.g., retirement) to be considered successful
    success_threshold_savings = float(data.get('success_threshold_savings', 200)) # e.g. 2 Crore
    min_success_rate_pct = float(data.get('min_success_rate_pct', 50)) # e.g. 50%

    all_results = [] # This will store data for all combinations (income, capital)

    for income in np.arange(income_min, income_max + income_step, income_step):
        for expenditure in np.arange(expenditure_min, expenditure_max + expenditure_step, expenditure_step):
            for capital in np.arange(capital_min, capital_max + capital_step, capital_step):
                if expenditure >= income * 0.8: # Basic sanity check: expenditure shouldn't be too high relative to income
                    continue

                final_savings_values = []
                all_debt_incurred_years_counts = []
                for _ in range(num_simulations_per_combination):
                    # Pass the expenditure_to_income_ratio to the simulation function
                    # The simulation function itself will calculate the initial expenditure
                    simulation_run_output = run_financial_simulation(income, capital, current_age, future_age, luck_factor, expenditure_to_income_ratio)
                    final_savings_values.append(simulation_run_output['final_savings'])
                    all_debt_incurred_years_counts.append(simulation_run_output['debt_incurred_years'])
                
                num_successful_runs = sum(s >= success_threshold_savings for s in final_savings_values)
                success_rate_pct = (num_successful_runs / num_simulations_per_combination) * 100
                average_debt_incurred_years = np.mean(all_debt_incurred_years_counts) if all_debt_incurred_years_counts else 0

                current_expenditure_calculated = round(income * expenditure_to_income_ratio, 2)

                combination_data = {
                    'initial_income': round(income, 2),
                    'initial_expenditure_calculated': current_expenditure_calculated, # Store the calculated expenditure
                    'initial_capital': round(capital, 2),
                    'success_rate_pct': round(success_rate_pct, 2),
                    'average_final_savings': round(np.mean(final_savings_values) if final_savings_values else 0, 2),
                    'median_final_savings': round(np.median(final_savings_values) if final_savings_values else 0, 2),
                    'num_successful_runs': num_successful_runs,
                    'num_total_runs': num_simulations_per_combination,
                    'average_debt_incurred_years': round(average_debt_incurred_years, 2)
                }
                all_results.append(combination_data)

    # The API will now return all combinations with their debt stats, 
    # allowing the frontend to build both the success table and the debt tipping point chart.
    return jsonify(all_results)

if __name__ == '__main__':
    app.run(debug=True)