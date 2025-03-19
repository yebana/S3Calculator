import streamlit as st
import pandas as pd
import plotly.express as px

# Set page title and configuration
st.set_page_config(page_title='S3 Deep Archive Cost Calculator', layout='wide')
st.title('S3 Deep Archive Cost Calculator (Direct Connect)')

# Initialize session state for all inputs
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.months = 1
    st.session_state.monthly_growth_gb = 0.0
    st.session_state.puts = 1000
    st.session_state.gets = 100
    st.session_state.deletes = 50
    st.session_state.transitions = 10
    st.session_state.standard_recoveries = 5
    st.session_state.standard_recovery_size = 100
    st.session_state.bulk_recoveries = 2
    st.session_state.bulk_recovery_size = 500
    st.session_state.storage_cost_per_gb = 0.00099
    st.session_state.put_cost_per_k = 0.05
    st.session_state.get_cost_per_k = 0.0004
    st.session_state.transition_cost_per_k = 0.05
    st.session_state.standard_recovery_cost_per_gb = 0.10
    st.session_state.bulk_recovery_cost_per_gb = 0.025

def reset_inputs():
    st.session_state.months = 1
    st.session_state.monthly_growth_gb = 0.0
    st.session_state.puts = 0
    st.session_state.gets = 0
    st.session_state.deletes = 0
    st.session_state.transitions = 0
    st.session_state.standard_recoveries = 0
    st.session_state.standard_recovery_size = 0
    st.session_state.bulk_recoveries = 0
    st.session_state.bulk_recovery_size = 0
    st.session_state.storage_cost_per_gb = 0.00099
    st.session_state.put_cost_per_k = 0.05
    st.session_state.get_cost_per_k = 0.0004
    st.session_state.transition_cost_per_k = 0.05
    st.session_state.standard_recovery_cost_per_gb = 0.10
    st.session_state.bulk_recovery_cost_per_gb = 0.025
    if 'initial_gb' not in st.session_state:
        st.session_state.initial_gb = 1

# Input parameters
with st.sidebar:
    st.header('Simulation Parameters')
    st.button('Reset All Inputs to Zero (Except Months and Initial Storage)', on_click=reset_inputs)
    months = st.number_input('Simulation Duration (months)', min_value=1, max_value=120, value=1, key='months')
    initial_gb = st.number_input('Initial Storage (GB)', min_value=1, value=1)
    monthly_growth_gb = st.number_input('Monthly Growth (GB)', min_value=0.0, value=0.0, key='monthly_growth_gb', help='Absolute monthly storage growth in GB')
    
    st.header('Operations')
    puts = st.number_input('Number of PUT/COPY/POST/LIST operations', min_value=0, value=1000, key='puts')
    gets = st.number_input('Number of GET/SELECT operations', min_value=0, value=100, key='gets')
    deletes = st.number_input('Number of DELETE operations', min_value=0, value=50, key='deletes')
    transitions = st.number_input('Number of Transitions', min_value=0, value=10, key='transitions')
    
    st.header('Recovery Operations')
    standard_recoveries = st.number_input('Number of Standard Recoveries', min_value=0, value=5, key='standard_recoveries')
    standard_recovery_size = st.number_input('Standard Recovery Size (GB)', min_value=0, value=100, key='standard_recovery_size')
    bulk_recoveries = st.number_input('Number of Bulk Recoveries', min_value=0, value=2, key='bulk_recoveries')
    bulk_recovery_size = st.number_input('Bulk Recovery Size (GB)', min_value=0, value=500, key='bulk_recovery_size')
    
    st.markdown('<h3 style="color: red;">Unit Costs ($)</h3>', unsafe_allow_html=True)
    storage_cost_per_gb = st.number_input('s3 Deep Archive Storage Cost per GB per Month', min_value=0.0, value=0.00099, format='%f', key='storage_cost_per_gb',
                                        help='Cost per GB per month for S3 Deep Archive storage')
    put_cost_per_k = st.number_input('PUT/COPY/POST/LIST Cost per 1,000 Requests', min_value=0.0, value=0.05, format='%f', key='put_cost_per_k',
                                    help='Cost per 1,000 PUT requests')
    get_cost_per_k = st.number_input('GET/SELECT Cost per 1,000 Requests', min_value=0.0, value=0.0004, format='%f', key='get_cost_per_k',
                                    help='Cost per 1,000 GET requests')
    transition_cost_per_k = st.number_input('Lifecycle Transition Requests into Cost per 1,000 Requests', min_value=0.0, value=0.05, format='%f', key='transition_cost_per_k',
                                          help='Cost per 1,000 lifecycle transition requests')
    standard_recovery_cost_per_gb = st.number_input('Standard Recovery Cost per GB', min_value=0.0, value=0.10, format='%f', key='standard_recovery_cost_per_gb',
                                                  help='Cost per GB for Standard recovery')
    bulk_recovery_cost_per_gb = st.number_input('Bulk Recovery Cost per GB', min_value=0.0, value=0.025, format='%f', key='bulk_recovery_cost_per_gb',
                                              help='Cost per GB for Bulk recovery')
    


# Cost calculations
def calculate_monthly_costs(month, current_storage):
    # Operation costs
    put_cost = put_cost_per_k * (puts / 1000)
    get_cost = get_cost_per_k * (gets / 1000)
    delete_cost = 0  # Free
    transition_cost = transition_cost_per_k * (transitions / 1000)
    
    # Recovery costs
    standard_recovery_cost = standard_recovery_cost_per_gb * standard_recovery_size
    bulk_recovery_cost = bulk_recovery_cost_per_gb * bulk_recovery_size
    
    # Calculate storage cost
    storage_cost = current_storage * storage_cost_per_gb
    print(f"Storage cost for month {month}: {storage_cost}")
    
    # Total cost
    total_cost = (storage_cost + put_cost + get_cost + delete_cost + 
                 transition_cost + standard_recovery_cost + bulk_recovery_cost)
    
    return {
        'Month': month,
        'Storage (GB)': current_storage,
        'Storage Cost': storage_cost,
        'Operation Cost': put_cost + get_cost + delete_cost + transition_cost,
        'Recovery Cost': standard_recovery_cost + bulk_recovery_cost,
        'Total Cost': total_cost
    }

# Generate cost data for the entire simulation period
data = []
current_storage = initial_gb

for month in range(1, months + 1):
    monthly_data = calculate_monthly_costs(month, current_storage)
    data.append(monthly_data)
    current_storage += monthly_growth_gb  # Add fixed GB growth instead of percentage

# Create DataFrame
df = pd.DataFrame(data)

# Display results
st.header('Cost Analysis')

# Create cost evolution graph using Plotly
fig = px.line(df, x='Month', y=['Storage Cost', 'Operation Cost', 'Recovery Cost', 'Total Cost'],
              title='Cost Evolution Over Time',
              labels={'value': 'Cost ($)', 'variable': 'Cost Type'})
st.plotly_chart(fig, use_container_width=True)

# Display summary statistics
st.header('Summary Statistics')
col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Total Storage Cost', f"${df['Storage Cost'].sum():.5f}")

with col2:
    st.metric('Total Operation Cost', f"${df['Operation Cost'].sum():.5f}")

with col3:
    st.metric('Total Recovery Cost', f"${df['Recovery Cost'].sum():.5f}")

# Display detailed data
st.header('Detailed Monthly Costs')
st.dataframe(df.round(5))