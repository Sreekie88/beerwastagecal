import streamlit as st

# Set page configuration
st.set_page_config(page_title="Beer Wastage Calculator", page_icon="🍺", layout="centered")

st.title("🍺 Beer Wastage & Cost Calculator")
st.markdown("Track line cleaning losses, volumetric waste, and associated labor costs for your venue.")

# --- SIDEBAR: GLOBAL SETTINGS ---
st.sidebar.header("Step 1: Global Cost Settings")
cost_per_pint = st.sidebar.number_input("Average Cost per Pint ($)", min_value=0.0, value=6.50, step=0.10)
hourly_labor_rate = st.sidebar.number_input("Hourly Labor Rate ($/hr)", min_value=0.0, value=15.00, step=0.50)

st.header("Step 2: Tap & Line Configuration")

# Standard US beer line volume approximation (3/16" ID line = ~0.01 pints per foot)
PINTS_PER_FOOT = 0.01

# Initialize unique counter to guarantee safe tracking IDs
if 'tap_counter' not in st.session_state:
    st.session_state.tap_counter = 1

# Initialize the taps tracking dictionary if it doesn't exist
if 'taps_dict' not in st.session_state:
    st.session_state.taps_dict = {
        0: {"name": "Tap 1", "length": 20.0, "labor_hours": 0.5}
    }

# Callback functions to safely handle data modifications
def add_tap():
    next_id = st.session_state.tap_counter
    st.session_state.taps_dict[next_id] = {
        "name": f"Tap {next_id + 1}", 
        "length": 20.0, 
        "labor_hours": 0.5
    }
    st.session_state.tap_counter += 1

def remove_tap(tap_id):
    if len(st.session_state.taps_dict) > 1:
        del st.session_state.taps_dict[tap_id]

# --- RENDER TAP INPUTS ---
# We loop over a static copy of keys to prevent runtime alteration errors
for tap_id in list(st.session_state.taps_dict.keys()):
    tap = st.session_state.taps_dict[tap_id]
    
    with st.expander(f"📋 {tap['name']}", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.session_state.taps_dict[tap_id]['name'] = st.text_input(
                "Tap Name/Beer", value=tap['name'], key=f"name_{tap_id}"
            )
        with col2:
            st.session_state.taps_dict[tap_id]['length'] = st.number_input(
                "Line Length (Feet)", min_value=0.0, value=tap['length'], key=f"len_{tap_id}"
            )
        with col3:
            st.session_state.taps_dict[tap_id]['labor_hours'] = st.number_input(
                "Labor (Hours)", min_value=0.0, value=tap['labor_hours'], step=0.1, key=f"lab_{tap_id}"
            )
            
        if len(st.session_state.taps_dict) > 1:
            st.button("Delete Tap", key=f"del_{tap_id}", on_click=remove_tap, args=(tap_id,))

st.button("➕ Add Another Tap", on_click=add_tap)

# --- CALCULATIONS ---
total_line_length = 0.0
total_labor_hours = 0.0
total_pints_wasted = 0.0

for tap_id, tap_data in st.session_state.taps_dict.items():
    total_line_length += tap_data['length']
    total_labor_hours += tap_data['labor_hours']
    total_pints_wasted += tap_data['length'] * PINTS_PER_FOOT

# Financial metrics
beer_waste_cost = total_pints_wasted * cost_per_pint
labor_cost = total_labor_hours * hourly_labor_rate
total_financial_loss = beer_waste_cost + labor_cost

st.markdown("---")
st.header("📊 Wastage Summary (Per Clean Cycle)")

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric(label="Total Pints Wasted", value=f"{total_pints_wasted:.2f} pts")
with col_b:
    st.metric(label="Beer Value Lost", value=f"${beer_waste_cost:.2f}")
with col_c:
    st.metric(label="Labor Cost", value=f"${labor_cost:.2f}")

st.subheader(f"Total Cost per Clean: :red[${total_financial_loss:.2f}]")

with st.info("ℹ️ Methodology Note"):
    st.write(
        f"Calculations assume a standard **3/16\" Inside Diameter (ID)** beer line, which holds approximately **0.01 pints per foot** "
        f"of product. If your lines are entirely flushed and dumped during cleaning, a total of **{total_pints_wasted:.2f} pints** "
        f"is lost across all **{len(st.session_state.taps_dict)} tap(s)**."
    )
