import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

st.set_page_config(page_title="Enhanced Chaotic Financial Simulator", layout="wide")

# Constants and initial parameters
initial_income = 20  # in lakhs
initial_expenditure = 4  # in lakhs
initial_capital = 20  # in lakhs
current_age = 26
future_age = 60 # Extended to retirement age

# Chaos Event Probabilities and Parameters
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

def simulate():
    years_to_simulate = future_age - current_age
    
    # Simulation state variables
    total_savings = initial_capital
    current_income_annual = initial_income
    current_expenditure_annual = initial_expenditure
    current_debt = 0
    
    # Lists for storing data
    year_list = [0]
    age_list = [current_age]
    income_list = [current_income_annual]
    post_tax_income_list = [current_income_annual * 0.7] # Assuming 30% flat tax for simplicity
    expenditure_list = [current_expenditure_annual]
    savings_this_year_list = [post_tax_income_list[0] - expenditure_list[0]]
    total_savings_list = [total_savings]
    debt_list = [current_debt]
    event_log = ["Initial State"]

    # Financial Parameters
    tax_rate = 0.30
    base_equity_return_rate = 0.10 # More conservative
    base_fd_return_rate = 0.06 # More conservative
    equity_allocation = 0.60
    fd_allocation = 0.40
    expenditure_base_growth_rate = 0.07
    inflation_rate = 0.06 # Standard inflation rate

    # Event-specific state variables
    num_children = random.randint(0, 2)
    children_birth_years = []
    if num_children >= 1:
        # First child born between age 28-32 (years 2-6 into simulation)
        children_birth_years.append(random.randint(2, 6))
    if num_children == 2:
        # Second child born between age 32-35 (years 6-9 into simulation), after first child
        first_child_birth_year = children_birth_years[0]
        second_child_birth_year = random.randint(max(first_child_birth_year + 1, 6), 9)
        children_birth_years.append(second_child_birth_year)
        children_birth_years.sort()

        children_ages = [-1] * num_children
        children_education_spent = [False for _ in range(num_children)] # Only one education event at age 18
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
        married_implicitly_year = random.randint(2,6) # Assume marriage happens 2-6 years into simulation

        for year_idx in range(1, years_to_simulate + 1):
            current_sim_age = current_age + year_idx
            annual_event_log_entries = []
            
            # Update children's ages
            # Apply child birth cost if this is the birth year
            for i in range(num_children):
                if year_idx == children_birth_years[i]:
                    cost = random.uniform(*chaos_events['child_birth']['cost_range_lakhs'])
                    total_savings -= cost
                    annual_event_log_entries.append(f"👶 Child {i+1} Born (-{cost:.2f}L)")

            # Update children's ages
            for i in range(num_children):
                if year_idx >= children_birth_years[i]:
                    children_ages[i] = current_sim_age - (current_age + children_birth_years[i])

            # --- CHAOS EVENTS & LIFE EVENTS --- 
            current_year_income = current_income_annual
            current_year_expenditure = current_expenditure_annual

            # 1. Job Loss
            if job_loss_active_months > 0:
                job_loss_active_months -= 12
                current_year_income = 0 # No income during job loss year
                annual_event_log_entries.append(f"🧨 Job Loss Ongoing ({job_loss_active_months // 12 if job_loss_active_months > 0 else 0} yrs left)")
                if job_loss_active_months <= 0:
                    drop_factor = random.uniform(*chaos_events['job_loss']['salary_drop_range'])
                    current_income_annual = income_before_job_loss * drop_factor
                    job_loss_recovery_years_remaining = random.randint(*chaos_events['job_loss']['recovery_time_years_range'])
                    annual_event_log_entries.append(f"💸 Job Ended. New salary {current_income_annual:.2f}L. Recovery: {job_loss_recovery_years_remaining} yrs.")
            elif job_loss_recovery_years_remaining > 0:
                # Simple linear recovery
                recovery_increment = (income_before_job_loss - current_income_annual) / job_loss_recovery_years_remaining
                current_income_annual += recovery_increment
                job_loss_recovery_years_remaining -= 1
                annual_event_log_entries.append(f"📈 Job Recovery. Income: {current_income_annual:.2f}L. {job_loss_recovery_years_remaining} yrs left.")
                if job_loss_recovery_years_remaining == 0: current_income_annual = income_before_job_loss
            elif random.random() < chaos_events['job_loss']['prob']:
                income_before_job_loss = current_income_annual
                duration_months = random.randint(chaos_events['job_loss']['min_duration_months'], chaos_events['job_loss']['max_duration_months'])
                job_loss_active_months = duration_months
                current_year_income = 0
                annual_event_log_entries.append(f"🧨 Job Loss Started ({duration_months} months)")

            # 2. Medical Emergency (Progressive)
            medical_prob = chaos_events['medical_emergency']['base_prob'] + (current_sim_age * chaos_events['medical_emergency']['age_factor'])
            if random.random() < medical_prob:
                cost = random.uniform(*chaos_events['medical_emergency']['cost_range_lakhs'])
                total_savings -= cost
                annual_event_log_entries.append(f"🏥 Medical Emergency (-{cost:.2f}L)")

            # 3. Market Crash
            effective_equity_return_rate = base_equity_return_rate # Default
            if market_crash_recovery_years_remaining > 0:
                # Assume gradual recovery, for simplicity still using base rate or slightly subdued if needed
                market_crash_recovery_years_remaining -= 1
                annual_event_log_entries.append(f"📉 Market Recovery Ongoing ({market_crash_recovery_years_remaining} yrs left)")
                if market_crash_recovery_years_remaining == 0:
                     annual_event_log_entries.append("📈 Market Fully Recovered")
            elif random.random() < chaos_events['market_crash']['prob']:
                effective_equity_return_rate = random.uniform(*chaos_events['market_crash']['return_range'])
                market_crash_recovery_years_remaining = random.randint(*chaos_events['market_crash']['recovery_years_range'])
                annual_event_log_entries.append(f"📉 Market Crash! Equity returns {effective_equity_return_rate*100:.0f}%. Recovery: {market_crash_recovery_years_remaining} yrs.")

            # 4. Family Expense
            if random.random() < chaos_events['family_expense']['prob']:
                cost = random.uniform(*chaos_events['family_expense']['cost_range_lakhs'])
                total_savings -= cost
                annual_event_log_entries.append(f"👨‍👩‍👧‍👦 Family Expense (-{cost:.2f}L)")

            # 5. Black Swan (Once per simulation)
            if not black_swan_event_occurred and random.random() < chaos_events['black_swan']['prob'] / years_to_simulate : # Spread prob over sim
                total_savings *= chaos_events['black_swan']['savings_loss_multiplier']
                current_income_annual *= chaos_events['black_swan']['income_loss_multiplier']
                if job_loss_active_months > 0 or job_loss_recovery_years_remaining >0 : income_before_job_loss *= chaos_events['black_swan']['income_loss_multiplier'] # Adjust baseline if job loss ongoing
                black_swan_event_occurred = True
                annual_event_log_entries.append("🌪️ BLACK SWAN! Savings & Income Hit!")

            # 6. Children's Education
            for i in range(num_children):
                if children_ages[i] != -1: # Child exists and has an age
                    # Education cost at age 18
                    if not children_education_spent[i] and children_ages[i] == 18:
                        cost = chaos_events['children_education']['cost_per_child_lakhs']
                        total_savings -= cost
                        children_education_spent[i] = True
                        annual_event_log_entries.append(f"🎓 Child {i+1} Edu. (-{cost:.2f}L, Age {children_ages[i]})")
            
            # 7. Children's Marriage
            for i in range(num_children):
                 if children_ages[i] != -1 and not children_marriage_spent[i] and chaos_events['children_marriage']['age_window'][0] <= children_ages[i] <= chaos_events['children_marriage']['age_window'][1]:
                    # Marriage cost occurs once within the age window (25-30)
                    # We'll trigger it on the first year the child is within the window
                    if children_ages[i] == chaos_events['children_marriage']['age_window'][0]:
                        cost = chaos_events['children_marriage']['cost_per_child_lakhs']
                        total_savings -= cost
                        children_marriage_spent[i] = True
                        annual_event_log_entries.append(f"💒 Child {i+1} Marriage (-{cost:.2f}L, Age {children_ages[i]})")


            # 9. Career Advancement (Age-dependent probability)
            # Ensure career advancement doesn't happen during an active job loss period
            career_advancement_prob = chaos_events['career_advancement']['prob']
            # Decrease probability as age increases
            if current_sim_age > 35:
                career_advancement_prob *= max(0.1, 1 - (current_sim_age - 35) * 0.02) # Decrease by 2% per year after 35, min 10%
            
            if job_loss_active_months <= 0 and random.random() < career_advancement_prob:
                boost = random.uniform(*chaos_events['career_advancement']['salary_boost_multiplier_range'])
                current_income_annual *= boost
                current_income_annual = min(current_income_annual, 150) # Cap income at 150 lakhs after boost
                # income_before_job_loss should only be adjusted if there's no active job loss,
                # but this entire block is now conditional on no active job loss, so direct adjustment is fine.
                # However, if career advancement happens *before* a potential job loss in the same year's logic (which it does not here),
                # then income_before_job_loss would need careful handling. Given current order, this is fine.
                if job_loss_recovery_years_remaining > 0 : income_before_job_loss *= boost # Adjust baseline only if in recovery, not active loss
                annual_event_log_entries.append(f"🚀 Career Advancement! New Income: {current_income_annual:.2f}L (Age {current_sim_age})")

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
                        business_venture_taken = True # Assume one major venture
                        if random.random() < chaos_events['business_venture']['success_prob']:
                            returns = investment * random.uniform(*chaos_events['business_venture']['success_return_multiplier_range'])
                            total_savings += returns
                            annual_event_log_entries.append(f"📈 Business Success! Invested {investment:.2f}L, Returned {returns:.2f}L")
                        else:
                            loss = investment * chaos_events['business_venture']['failure_loss_percentage']
                            # total_savings already reduced by full investment, so add back non-lost part
                            total_savings += (investment - loss)
                            annual_event_log_entries.append(f"📉 Business Failed. Invested {investment:.2f}L, Lost {loss:.2f}L")
                    else:
                        annual_event_log_entries.append("💸 Wanted Business Venture, Insufficient Capital")
            
            # 12. Divorce
            if not divorce_occurred and year_idx > married_implicitly_year and random.random() < chaos_events['divorce']['prob_if_married_annual']:
                savings_hit = total_savings * chaos_events['divorce']['savings_loss_percentage']
                total_savings -= savings_hit
                income_reduction = current_income_annual * chaos_events['divorce']['income_loss_percentage_temp']
                current_income_annual -= income_reduction
                if job_loss_active_months > 0 or job_loss_recovery_years_remaining >0 : income_before_job_loss -= income_reduction # Adjust baseline
                divorce_occurred = True
                annual_event_log_entries.append(f"💔 Divorce. Savings -{savings_hit:.2f}L, Temp Income Drop -{income_reduction:.2f}L")

            # --- FINANCIAL CALCULATIONS --- 
            income_after_tax = current_year_income * (1 - tax_rate)
            
            # Additional retirement savings boost after age 50 - Feature Removed

            savings_this_year = income_after_tax - current_year_expenditure
            
            # Investment Returns (on previous year's total_savings + current year's savings if positive before investment)
            investable_capital = total_savings + (savings_this_year if savings_this_year > 0 else 0)
            equity_investment = 0
            fd_investment = 0
            equity_return = 0
            fd_return = 0

            if investable_capital > 0:
                equity_investment = investable_capital * equity_allocation
                fd_investment = investable_capital * fd_allocation
                equity_return = equity_investment * effective_equity_return_rate
                fd_return = fd_investment * base_fd_return_rate # FD returns are generally stable
            
            total_savings += savings_this_year # Add/subtract this year's operational savings/deficit
            total_savings += equity_return + fd_return # Add investment returns

            # Debt Handling
            if total_savings < 0:
                new_debt_this_year = abs(total_savings)
                current_debt += new_debt_this_year
                total_savings = 0 # Savings cannot be negative, it's debt
                annual_event_log_entries.append(f"🆘 Incurred Debt: {new_debt_this_year:.2f}L. Total Debt: {current_debt:.2f}L")
            elif current_debt > 0 and total_savings > 0: # Try to pay off debt if surplus
                pay_off_amount = min(current_debt, total_savings)
                current_debt -= pay_off_amount
                total_savings -= pay_off_amount
                annual_event_log_entries.append(f"💰 Paid Off Debt: {pay_off_amount:.2f}L. Remaining Debt: {current_debt:.2f}L")

            # --- GROWTH & UPDATES FOR NEXT YEAR --- 
            # Income Growth (Age-dependent)
            if job_loss_active_months <= 0 and job_loss_recovery_years_remaining <=0 : # No growth if unemployed or in specific recovery phase
                if current_income_annual >= 150:
                    # Stagnation: No growth after 150 lakhs
                    pass # No growth applied
                elif current_income_annual >= 100:
                    # Stagnation: Very slow or zero growth after 1 crore (100 lakhs)
                    current_income_annual *= random.uniform(1.005, 1.015) # Example: 0.5% to 1.5% growth
                elif current_sim_age < 35:
                    current_income_annual *= random.uniform(1.07, 1.15) # Faster growth early career
                elif current_sim_age < 50:
                    current_income_annual *= random.uniform(1.04, 1.08) # Moderate growth mid-career
                else:
                    current_income_annual *= random.uniform(1.01, 1.03) # Slower pre-retirement
            
            # Expenditure Growth (Base + Child-dependent)
            child_expense_factor = sum([0.03 for i in range(num_children) if children_ages[i] != -1 and children_ages[i] < 18]) # 3% extra per child under 18
            # Include inflation and base growth
            current_expenditure_annual *= (1 + inflation_rate + expenditure_base_growth_rate + child_expense_factor)
            current_expenditure_annual = min(current_expenditure_annual, current_income_annual * 0.8 if current_income_annual > 0 else 100) # Cap expenditure

            # Store annual values
            year_list.append(year_idx)
            age_list.append(current_sim_age)
            income_list.append(current_income_annual) # Store end-of-year projected income for next year
            post_tax_income_list.append(income_after_tax)
            expenditure_list.append(current_year_expenditure) # Store actual expenditure for this year
            savings_this_year_list.append(savings_this_year)
            total_savings_list.append(total_savings)
            debt_list.append(current_debt)
            event_log.append(", ".join(annual_event_log_entries) if annual_event_log_entries else "Normal Year")

        df = pd.DataFrame({
            'Year': year_list,
            'Age': age_list,
            'Income (L)': income_list,
            'Post-tax Income (L)': post_tax_income_list,
            'Expenditure (L)': expenditure_list,
            'Savings This Year (L)': savings_this_year_list,
            'Total Savings (L)': total_savings_list,
            'Total Debt (L)': debt_list,
            'Events': event_log
        })
        return df

    # --- Streamlit Layout ---
    st.title("💸 Enhanced Chaotic Financial Life Simulator")
    st.write("Simulates income, expenditure, savings, debt, and life events from age 26 to 60.")

    if st.button("🔁 Simulate Enhanced Chaos"):
        df_results = simulate()

        st.subheader("📊 Financial Summary Table")
        st.dataframe(df_results.style.format({
            'Income (L)': '{:.2f}',
            'Post-tax Income (L)': '{:.2f}',
            'Expenditure (L)': '{:.2f}',
            'Savings This Year (L)': '{:.2f}',
            'Total Savings (L)': '{:.2f}',
            'Total Debt (L)': '{:.2f}'
        }), height=600)

        st.subheader("📈 Financials Over Time")
        fig, ax1 = plt.subplots(figsize=(14, 7))

        color = 'tab:green'
        ax1.set_xlabel('Year in Simulation')
        ax1.set_ylabel('Total Savings (L)', color=color)
        ax1.plot(df_results['Year'], df_results['Total Savings (L)'], color=color, marker='o', label='Total Savings (L)')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True, linestyle=':')

        ax2 = ax1.twinx() # instantiate a second axes that shares the same x-axis
        color = 'tab:red'
        ax2.set_ylabel('Total Debt (L)', color=color) 
        ax2.plot(df_results['Year'], df_results['Total Debt (L)'], color=color, marker='x', linestyle='--', label='Total Debt (L)')
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout() # otherwise the right y-label is slightly clipped
        plt.title('💰 Total Savings and Debt Over Time')
        st.pyplot(fig)

        st.subheader("📉 Income & Expenditure Over Time")
        fig2, ax = plt.subplots(figsize=(14, 7))
        ax.plot(df_results['Year'], df_results['Income (L)'], label='Gross Income (L)', marker='.', color='blue')
        ax.plot(df_results['Year'], df_results['Post-tax Income (L)'], label='Post-tax Income (L)', linestyle='--', color='skyblue')
        ax.plot(df_results['Year'], df_results['Expenditure (L)'], label='Expenditure (L)', marker='.', color='orangered')
        ax.set_xlabel('Year in Simulation')
        ax.set_ylabel('Amount (Lakhs)')
        ax.set_title('💸 Income and Expenditure Projection')
        ax.legend()
        ax.grid(True, linestyle=':')
        st.pyplot(fig2)

        st.subheader("🗓️ Event Timeline")
        st.dataframe(df_results[['Year', 'Age', 'Events']])
    else:
        st.info("Click the button above to generate your enhanced chaotic financial life simulation.")


st.title("Financial Modeling Simulation")

# Sidebar for inputs
st.sidebar.header("Simulation Parameters")

initial_income = st.sidebar.number_input("Initial Annual Income (Lakhs)", min_value=1, value=20)
initial_expenditure = st.sidebar.number_input("Initial Annual Expenditure (Lakhs)", min_value=1, value=4)
initial_capital = st.sidebar.number_input("Initial Capital (Lakhs)", min_value=0, value=20)
current_age = st.sidebar.number_input("Current Age", min_value=18, value=26)
future_age = st.sidebar.number_input("Target Age", min_value=current_age + 1, value=60)
