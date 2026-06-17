import streamlit as st

# Set page configuration
st.set_page_config(page_title="Beer Wastage Calculator", page_icon="🍺", layout="centered")

st.title("🍺 Beer Wastage & Cost Calculator")
st.markdown("Track line cleaning losses, volumetric waste, and associated labor costs for your venue.")

st.header("Step 1: Tap & Line Configuration")
st.markdown("Set up your lines and input the retail/cost value per pint *individually* for each tap.")

# Standard UK beer line volume approximation (3/16" ID line = ~0.01 pints per foot)
PINTS_PER_FOOT = 0.01

# Initialize unique counter to guarantee safe tracking IDs
if 'tap_counter' not in st.session_state:
    st.session_state.tap_counter = 1

# Initialize the taps tracking dictionary if it doesn't exist
if 'taps_dict' not in st.session_state:
    st.session_state.taps_dict = {
        0: {"name": "Tap 1", "length": 20.0, "cost_per_pint": 5.50}
    }

# Callback functions to safely handle data modifications
def add_tap():
    next_id = st.session_state.tap_counter
    st.session_state.taps_dict[next_id] = {
        "name": f"Tap {next_id + 1}", 
        "length": 20.0, 
        "cost_per_pint": 5.50
    }
    st.session_state.tap_counter += 1

def remove_tap(tap_id):
    if len(st.session_state.taps_dict) > 1:
        del st.session_state.taps_dict[tap_id]

# --- RENDER TAP INPUTS ---
for tap_id in list(st.session_state.taps_dict.keys()):
    tap = st.session_state.taps_dict[tap_id]
    
    with st.expander(f"📋 {tap['name']}", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.session_state.taps_dict[tap_id]['name'] = st.text_input(
                "Tap/Beer Name", value=tap['name'], key=f"name_{tap_id}"
            )
        with col2:
            st.session_state.taps_dict[tap_id]['length'] = st.number_input(
                "Line Length (Feet)", min_value=0.0, value=tap['length'], key=f"len_{tap_id}"
            )
        with col3:
            st.session_state.taps_dict[tap_id]['cost_per_pint'] = st.number_input(
                "Cost per Pint (£)", min_value=0.0, value=tap['cost_per_pint'], step=0.10, key=f"cost_{tap_id}"
            )
            
        if len(st.session_state.taps_dict) > 1:
            st.button("Delete Tap", key=f"del_{tap_id}", on_click=remove_tap, args=(tap_id,))

st.button("➕ Add Another Tap", on_click=add_tap)

# --- SEPARATE LABOR SECTION ---
st.markdown("---")
st.header("Step 2: Independent Labor Costs")
st.markdown("Record the time spent overall on line cleaning duties, separate from liquid calculations.")

col_lab1, col_lab2 = st.columns(2)
with col_lab1:
    total_labor_hours = st.number_input("Total Labor Allocated (Hours)", min_value=0.0, value=1.5, step=0.25)
with col_lab2:
    hourly_labor_rate = st.number_input("Staff Hourly Rate (£/hr)", min_value=0.0, value=11.54, step=0.10) # Set to standard UK NLW baseline

# --- CALCULATIONS ---
total_pints_wasted = 0.0
beer_waste_cost = 0.0

for tap_id, tap_data in st.session_state.taps_dict.items():
    # Calculate volume for this specific line
    pints_lost_this_line = tap_data['length'] * PINTS_PER_FOOT
    total_pints_wasted += pints_lost_this_line
    
    # Financial calculation using this specific line's designated cost
    beer_waste_cost += pints_lost_this_line * tap_data['cost_per_pint']

# Independent Labor cost math
labor_cost = total_labor_hours * hourly_labor_rate
total_financial_loss = beer_waste_cost + labor_cost

# --- SUMMARY DASHBOARD ---
st.markdown("---")
st.header("📊 Wastage Summary (Per Clean Cycle)")

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric(label="Total Pints Wasted", value=f"{total_pints_wasted:.2f} pts")
with col_b:
    st.metric(label="Beer Value Lost", value=f"£{beer_waste_cost:.2f}")
with col_c:
    st.metric(label="Labor Cost", value=f"£{labor_cost:.2f}")

st.subheader(f"Total Cost per Clean: :red[£{total_financial_loss:.2f}]")

with st.info("ℹ️ Methodology Note"):
    st.write(
        f"Calculations are localized to **£ (GBP)**. Standard **3/16\" ID** python lines hold approx **0.01 pints per foot**. "
        f"Financial liquid loss scales accurately to the specific pricing tier designated per line above."
    )
