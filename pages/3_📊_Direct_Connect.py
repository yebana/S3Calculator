import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="AWS Direct Connect Calculator", layout="wide")

# Title and description
st.title("AWS Direct Connect Calculator - Spain Region")
st.write("Calculate monthly port hour charges and data transfer charges for AWS Direct Connect in Spain.")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    
    # Location details
    st.write("**Fixed Configuration:**")
    st.write("- AWS Region: Spain")
    st.write("- AWS Direct Connect Location: Spain")
    
    st.subheader("Port Configuration")
    num_locations = st.number_input("Number of AWS Direct Connect locations", min_value=1, value=1, step=1)
    ports_per_location = st.number_input("Ports in use per location", min_value=1, value=1, step=1)
    port_type = st.selectbox("Port type", ["Dedicated", "Hosted"])
    
    # Dynamic port capacity options based on port type
    if port_type == "Dedicated":
        port_capacity = st.selectbox("Port capacity", [
            "1 Gbps", "10 Gbps", "100 Gbps", "400 Gbps"
        ])
    else:  # Hosted
        port_capacity = st.selectbox("Port capacity", [
            "50 Mbps", "100 Mbps", "200 Mbps", "300 Mbps", "400 Mbps", "500 Mbps",
            "1 Gbps", "2 Gbps", "5 Gbps", "10 Gbps", "25 Gbps"
        ])
        hours_connected = st.number_input("Hours connected", min_value=1, max_value=744, value=730, step=1)
    
    st.subheader("Data Transfer")
    data_transfer_out = st.number_input("Data transferred out (GB)", min_value=0.0, value=0.0, step=100.0)
    
    # Calculate button
    calculate_button = st.button("Calculate Charges")

# Define pricing constants
PORT_PRICING = {
    "Dedicated": {
        "1 Gbps": 0.30,
        "10 Gbps": 2.25,
        "100 Gbps": 22.50,
        "400 Gbps": 85.00
    },
    "Hosted": {
        "50 Mbps": 0.03,
        "100 Mbps": 0.06,
        "200 Mbps": 0.08,
        "300 Mbps": 0.12,
        "400 Mbps": 0.16,
        "500 Mbps": 0.20,
        "1 Gbps": 0.33,
        "2 Gbps": 0.66,
        "5 Gbps": 1.65,
        "10 Gbps": 2.48,
        "25 Gbps": 6.20
    }
}

DATA_TRANSFER_RATE = 0.02  # $0.02 per GB

# Calculate charges
if calculate_button:
    # Calculate port charges
    hourly_port_rate = PORT_PRICING[port_type][port_capacity]
    total_ports = num_locations * ports_per_location
    port_charges = total_ports * hourly_port_rate * hours_connected

    # Calculate data transfer charges
    data_transfer_charges = data_transfer_out * DATA_TRANSFER_RATE

    # Total charges
    total_charges = port_charges + data_transfer_charges

    # Display results
    st.header("Monthly Charges Summary")
    
    # Create a DataFrame for the detailed breakdown
    breakdown = pd.DataFrame([
        ["Port Charges", f"${port_charges:,.2f}", 
         f"{total_ports} ports × ${hourly_port_rate}/hour × {hours_connected} hours"],
        ["Data Transfer Charges", f"${data_transfer_charges:,.2f}", 
         f"{data_transfer_out:,.2f} GB × ${DATA_TRANSFER_RATE}/GB"],
        ["Total Charges", f"${total_charges:,.2f}", "Sum of all charges"]
    ], columns=["Component", "Amount", "Calculation"])
    
    st.table(breakdown)

    # Additional details
    st.subheader("Configuration Details")
    st.write(f"- Total number of ports: {total_ports}")
    st.write(f"- Port type: {port_type}")
    st.write(f"- Port capacity: {port_capacity}")
    st.write(f"- Hours connected: {hours_connected}")
    st.write(f"- Data transferred out: {data_transfer_out:,.2f} GB")

# Add footer with disclaimer
st.markdown("---")
st.caption("Disclaimer: This calculator provides estimated costs. Actual AWS charges may vary. Please refer to AWS pricing documentation for the most accurate and up-to-date pricing information.")