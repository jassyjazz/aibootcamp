import streamlit as st
import requests
import pandas as pd

# Function 1: HDB Resale Flat Affordability Calculator
def affordability_calculator():
    st.title('HDB Resale Flat Affordability Calculator')
    
    # User Inputs
    income = st.number_input('Enter your monthly household income (SGD)', min_value=0)
    cpf_savings = st.number_input('Enter your total CPF savings available (SGD)', min_value=0)
    cash_savings = st.number_input('Enter your cash savings available (SGD)', min_value=0)
    grant_eligibility = st.selectbox('Are you eligible for any grants?', ['Yes', 'No'])
    
    # Simple calculations
    grant_amount = 50000 if grant_eligibility == 'Yes' else 0  # Example grant amount for simplicity
    total_savings = cpf_savings + cash_savings + grant_amount
    max_loan = income * 60  # A simple calculation of loan eligibility (income * 60 months)

    # Display Results
    if st.button('Calculate'):
        max_price = total_savings + max_loan
        st.write(f'Based on your input, you can afford a resale flat priced up to S${max_price:,.0f}.')
        
        # Store the max price in session state to use in the next page
        st.session_state.max_price = max_price
        st.session_state.calculated = True  # Set the flag to indicate calculation is done

# Function 2: Display Filtered Resale Flats Based on User's Budget
def filtered_resale_flats():
    st.title("Filtered Resale Flats")

    if 'max_price' not in st.session_state:
        st.write("Please use the Affordability Calculator to calculate your budget first.")
        return
    
    max_price = st.session_state.max_price
    st.write(f"Fetching resale flats that match your budget of up to S${max_price:,.0f}...")

    # API call to get resale flat data
    datasetId = "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"
    url = f"https://data.gov.sg/api/action/datastore_search?resource_id={datasetId}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['result']['records']
        df = pd.DataFrame(data)

        # Convert price fields to numeric and filter by max price
        df['resale_price'] = pd.to_numeric(df['resale_price'], errors='coerce')
        filtered_flats = df[df['resale_price'] <= max_price]

        if not filtered_flats.empty:
            st.write(f"Found {len(filtered_flats)} flats within your budget:")
            st.dataframe(filtered_flats[['town', 'flat_type', 'resale_price', 'storey_range', 'floor_area_sqm']])
        else:
            st.write("No flats found within your budget.")
    else:
        st.write("Failed to fetch resale flat data. Please try again later.")

# Function 3: HDB Resale Process Navigator
def resale_process_navigator():
    st.title("HDB Resale Process Navigator")
    st.write("""
        The process of buying an HDB resale flat can be complex. Here are the general steps involved:
        
        1. **Determine Eligibility**: Ensure that you meet the eligibility criteria for purchasing an HDB resale flat.
        2. **Calculate Affordability**: Use the affordability calculator to understand how much you can afford.
        3. **Find a Resale Flat**: Start your search for suitable resale flats within your budget.
        4. **Secure Financing**: Explore financing options, including loans and CPF usage.
        5. **Make an Offer**: Once you find a flat, make an offer to the seller.
        6. **Option to Purchase**: Upon acceptance, sign an Option to Purchase (OTP) with the seller.
        7. **Complete the Sale**: Complete all necessary paperwork and payments to finalize the purchase.
        
        Feel free to navigate to the affordability calculator or explore filtered resale flats after understanding the process!
    """)

# "About Us" Page
def about_us_page():
    st.title("About Us")
    st.write("""
        This application is designed to assist potential buyers in navigating the complex process of buying an HDB resale flat in Singapore.
        We provide two main tools:
        1. **Affordability Calculator**: Helps you determine the maximum flat price you can afford based on your financial information.
        2. **Resale Process Navigator**: Guides you step-by-step through the process of purchasing an HDB resale flat.
        
        **Data Sources**:
        - HDB official website for grant and eligibility information.
        - CPF Board for financial calculations related to CPF savings and usage.
    """)

# "Methodology" Page
def methodology_page():
    st.title("Methodology")
    st.write("""
        The following outlines the methodology used in this application:
        
        **Affordability Calculator**:
        - The calculator takes into account your CPF savings, cash savings, and eligible grants to calculate the total savings available.
        - Your loan eligibility is estimated by multiplying your monthly income by 60 (representing a loan term of 5 years).
        - The total affordable price is the sum of your total savings and your estimated loan eligibility.
        
        **Filtered Resale Flats**:
        - After calculating your affordability, we fetch data from the HDB resale flats dataset provided by data.gov.sg.
        - We filter the flats based on the user's maximum budget and display those that are within the affordable price range.
        
        Flowcharts for each of the use cases:
    """)
    st.image('affordability_calculator_flowchart.png')  # You can add a flowchart image here
    st.image('resale_process_navigator_flowchart.png')

# Main Navigation
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Affordability Calculator", "Filtered Resale Flats", "HDB Resale Process Navigator", "About Us", "Methodology"])
    
    if page == "Home":
        st.title("Welcome to the HDB Resale Assistant")
        st.write("Use the sidebar to navigate through the app.")
    
    elif page == "Affordability Calculator":
        affordability_calculator()
    
    elif page == "Filtered Resale Flats":
        filtered_resale_flats()
    
    elif page == "HDB Resale Process Navigator":
        resale_process_navigator()
    
    elif page == "About Us":
        about_us_page()
    
    elif page == "Methodology":
        methodology_page()

if __name__ == "__main__":
    # Initialize session state variables
    if 'calculated' not in st.session_state:
        st.session_state.calculated = False

    main()
