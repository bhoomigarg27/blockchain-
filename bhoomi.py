import streamlit as st
import hashlib

# Initialize an empty hospital ledger in session state if not present
if "hospital_ledger_advanced" not in st.session_state:
    st.session_state.hospital_ledger_advanced = {}

def generate_hash(patient_name, treatment, cost, date_of_visit):
    """Generates a unique hash for a patient visit record."""
    data = f"{patient_name}{treatment}{cost}{date_of_visit}"
    return hashlib.sha256(data.encode()).hexdigest()

# Streamlit UI
st.title("🏥 Hospital Ledger System")

# Section to add patient visit
st.header("Add or Update Patient Visit")
with st.form(key="visit_form"):
    patient_name = st.text_input("Enter Patient's Name:")
    treatment = st.text_input("Enter Treatment Received:")
    cost = st.number_input("Enter Cost of Treatment ($):", min_value=0.0, format="%.2f")
    date_of_visit = st.date_input("Enter Date of Visit:")
    
    submit_button = st.form_submit_button(label="Add Visit")

if submit_button and patient_name and treatment:
    # Convert date object to string
    date_str = date_of_visit.strftime("%Y-%m-%d")
    visit_hash = generate_hash(patient_name, treatment, cost, date_str)

    visit = {
        "treatment": treatment,
        "cost": cost,
        "date_of_visit": date_str,
        "visit_hash": visit_hash
    }

    if patient_name not in st.session_state.hospital_ledger_advanced:
        st.session_state.hospital_ledger_advanced[patient_name] = []
        st.success(f"New record added for {patient_name}.")
    else:
        st.success(f"Updated record for {patient_name}.")

    st.session_state.hospital_ledger_advanced[patient_name].append(visit)
    st.write(f"**Visit added:** {treatment} on {date_str} costing ${cost:.2f}")
    st.code(f"Visit Hash: {visit_hash}")

# Section to search for a patient's visits
st.header("🔍 Search Patient Visits")
search_patient = st.text_input("Enter Patient's Name to Search:")

if search_patient:
    if search_patient in st.session_state.hospital_ledger_advanced:
        st.subheader(f"Visit Records for {search_patient}:")
        for visit in st.session_state.hospital_ledger_advanced[search_patient]:
            st.write(f"📅 Date: {visit['date_of_visit']}")
            st.write(f"💉 Treatment: {visit['treatment']}")
            st.write(f"💰 Cost: ${visit['cost']:.2f}")
            st.code(f"Hash: {visit['visit_hash']}")
            st.markdown("---")
    else:
        st.warning(f"Patient {search_patient} not found in the ledger.")
