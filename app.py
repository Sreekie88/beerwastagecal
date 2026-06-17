import streamlit as str

# Set page configuration
st.set_page_config(page_title="Beer Wastage Calculator", page_icon="🍺", layout="centered")

st.title("🍺 Beer Wastage & Cost Calculator")
st.markdown("Track line cleaning losses, volumetric waste, and associated labor costs for your venue.")

st.sidebar.header("Step 1: Global Cost Settings")
cost_per_pint = st.sidebar.number_input("Average Cost per Pint ($)", min_value=0.0, value=6.50, step=0.10)
hourly_labor_rate = st.sidebar.number_input("Hourly Labor Rate ($/hr)", min_value=0.0, value=15.00, step=0.50)

st.header("Step 2: Tap & Line Configuration")

# Standard US beer line volume approximation: 
# 3/16" ID vinyl line holds roughly 0.16 fluid ounces per foot. 
# 1 Pint = 16 fluid ounces. 
# Formula: Pints per foot = 0.16 / 16 = 0.01 pints/foot.
PINTS_PER_FOOT = 0.01

# Initialize session state to keep track of taps dynamically
if 'taps' not in st.session_state:
    st.session_state.taps = [{"name": "Tap 1", "length": 20.0, "labor_hours": 0.5}]

# Functions to modify tap list
def add_tap():
    tap_num = len(st.session_state.taps) + 1
    st.session_state.taps.append({"name": f"Tap {tap_num}", "length": 20.0, "labor_hours": 0.5})

def remove_tap(index):
    if len(st.session_state.taps) > 1:
        st.session_state.taps.pop(index)
        st.rerun()

# Render inputs for each tap
for i, tap in enumerate(st.session_state.taps):
    with st.expander(f"📋 {tap['name']}", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.session_state.taps[i]['name'] = st.text_input(f"Tap Name/Beer", value=tap['name'], key=f"name_{i}")
        with col2:
            st.session_state.taps[i]['length'] = st.number_input(f"Line Length (Feet)", min_value=0.0, value=tap['length'], key=f"len_{i}")
        with col3:
            st.session_state.taps[i]['labor_hours'] = st.number_input(f"Labor (Hours)", min_value=0.0, value=tap['labor_hours'], step=0.1, key=f"lab_{i}")
            
        if len(st.session_state.taps) > 1:
            st.button("Delete Tap", key=f"del_{i}", on_click=remove_tap, args=(i,))

st.button("➕ Add Another Tap", on_click=add_tap)

# --- CALCULATIONS ---
total_line_length = 0.0
total_labor_hours = 0.0
total_pints_wasted = 0.0

for tap in st.session_state.taps:
    total_line_length += tap['length']
    total_labor_hours += tap['labor_hours']
    # Calculate volume trapped in the lines for this tap
    total_pints_wasted += tap['length'] * PINTS_PER_FOOT

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

# Contextual breakdown breakdown
with st.info("ℹ️ Methodology Note"):
    st.write(
        f"Calculations assume a standard **3/16\" Inside Diameter (ID)** beer line, which holds approximately **0.01 pints per foot** "
        f"of product. If your lines are entirely flushed and dumped during cleaning, a total of **{total_pints_wasted:.2f} pints** "
        f"is lost across all **{len(st.session_state.taps)} tap(s)**."
    )
