import os
import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------- LOAD DATA --------------------

# Helper to avoid errors if folders are empty
def get_first_csv(path):
    files = [f for f in os.listdir(path) if f.endswith('.csv')]
    return os.path.join(path, files[0]) if files else None

SAVE_COACHES_PATH = "data/coaches"
SAVE_AGENTS_PATH = "data/agents"
SAVE_QUESTIONS_PATH = "data/questions"

# Ensure directories exist
for p in [SAVE_COACHES_PATH, SAVE_AGENTS_PATH, SAVE_QUESTIONS_PATH]:
    os.makedirs(p, exist_ok=True)

current_coaches_df = pd.read_csv(get_first_csv(SAVE_COACHES_PATH))
current_agents_df = pd.read_csv(get_first_csv(SAVE_AGENTS_PATH))

q_path = get_first_csv(SAVE_QUESTIONS_PATH)
current_questions_df = pd.read_csv(q_path)
questions_timestamp = os.path.basename(q_path).replace("questions_", "").replace(".csv", "")

# -------------------- SESSION STATE --------------------

# Using dictionary syntax to avoid AttributeErrors
if "locked" not in st.session_state:
    st.session_state["locked"] = False

if "has_submitted" not in st.session_state:
    st.session_state["has_submitted"] = False

if "form_id" not in st.session_state:
    st.session_state["form_id"] = 0

# -------------------- UI --------------------

st.title("Quality Tracker")

# The form_id ensures that when we click 'New Entry', the entire UI is destroyed and rebuilt fresh
with st.form(key=f"quality_form_{st.session_state['form_id']}", clear_on_submit=False):

    col1, col2 = st.columns(2)

    with col1:
        coach = st.selectbox(
            "Coach Name",
            options=current_coaches_df.to_dict("records"),
            format_func=lambda x: x["Coach Name"],
            index=None,
            placeholder="Select Coach Name",
            disabled=st.session_state["locked"],
            key="coach_selector"
        )

        agent = st.selectbox(
            "Agent Name",
            options=current_agents_df.to_dict("records"),
            format_func=lambda x: x["Agent Name"],
            index=None,
            placeholder="Select Agent Name",
            disabled=st.session_state["locked"],
            key="agent_selector"
        )

    with col2:
        monitoring_date = st.date_input(
            "Monitoring Date", value=None, disabled=st.session_state["locked"], key="m_date"
        )
        transaction_date = st.date_input(
            "Transaction Date", value=None, disabled=st.session_state["locked"], key="t_date"
        )

    st.divider()

    answers = []
    max_score = current_questions_df["Weight"].sum()

    for _, row in current_questions_df.iterrows():
        qn = int(row["Number"])
        qt = row["Question"]
        qw = int(row["Weight"])

        # Create unique key for radio
        q_key = f"q{qn}"

        answer = st.radio(
            f"**Q{qn}. {qt}**",
            ["Yes", "No"],
            index=None,
            horizontal=True,
            key=q_key,
            disabled=st.session_state["locked"],
        )

        score = qw if answer == "Yes" else 0
        st.markdown(f"**Weight:** {qw} | **Score:** {score}")
        st.divider()
        answers.append(answer)

    reviewer_comments = st.text_area(
        "Comments", disabled=st.session_state["locked"], key="comm_text"
    )

    submit_clicked = st.form_submit_button(
        "Submit", disabled=st.session_state["locked"]
    )

# -------------------- SUBMISSION LOGIC --------------------

if submit_clicked and not st.session_state["has_submitted"]:
    errors = []
    if coach is None: errors.append("Coach is required")
    if agent is None: errors.append("Agent is required")
    if monitoring_date is None: errors.append("Monitoring date is required")
    if transaction_date is None: errors.append("Transaction date is required")
    if any(a is None for a in answers): errors.append("All questions must be answered")

    if errors:
        for e in errors:
            st.error(e)
    else:
        # LOCK IMMEDIATELY
        st.session_state["locked"] = True
        st.session_state["has_submitted"] = True
        st.rerun()

# -------------------- SAVE DATA --------------------

if st.session_state["has_submitted"]:
    # Calculate scores from session state keys
    total_score = 0
    for _, row in current_questions_df.iterrows():
        val = st.session_state.get(f"q{int(row['Number'])}")
        if val == "Yes":
            total_score += int(row["Weight"])
    
    normalized_score = round((total_score / max_score) * 100, 2)

    if "already_saved" not in st.session_state or not st.session_state["already_saved"]:
        result_id = datetime.now().strftime("%Y%m%d%H%M%S")
        result_date = datetime.now().strftime("%Y%m%d")

        result_data = {
            "result_id": result_id,
            "coach_id": st.session_state["coach_selector"]["ID"],
            "coach_name": st.session_state["coach_selector"]["Coach Name"],
            "agent_id": st.session_state["agent_selector"]["ID"],
            "agent_name": st.session_state["agent_selector"]["Agent Name"],
            "monitoring_date": st.session_state["m_date"],
            "transaction_date": st.session_state["t_date"],
            "total_score": total_score,
            "normalized_score": normalized_score,
            "reviewer_comments": st.session_state["comm_text"],
        }

        for row in current_questions_df.itertuples():
            qn = int(row.Number)
            ans_val = st.session_state[f"q{qn}"]
            result_data[f"Q{qn}_answer"] = ans_val
            result_data[f"Q{qn}_score"] = row.Weight if ans_val == "Yes" else 0

        RESULTS_PATH = "data/results"
        os.makedirs(RESULTS_PATH, exist_ok=True)
        results_filename = f"{questions_timestamp}_results_{result_date}.csv"
        results_path = os.path.join(RESULTS_PATH, results_filename)

        pd.DataFrame([result_data]).to_csv(
            results_path, mode="a", header=not os.path.exists(results_path), index=False,
        )
        st.session_state["already_saved"] = True

    st.success(f"Submission successful ✅ | Score: {normalized_score}%")

    # -------------------- NEW ENTRY (RESET) --------------------
    # """
    # if st.button("New Entry"):
    #     # 1. Update form ID to force a total UI reset
    #     st.session_state["form_id"] += 1
        
    #     # 2. Reset flow flags
    #     st.session_state["locked"] = False
    #     st.session_state["has_submitted"] = False
    #     st.session_state["already_saved"] = False
        
    #     # 3. Clear all widget keys from session state
    #     for key in list(st.session_state.keys()):
    #         if key.startswith("q") or key in ["coach_selector", "agent_selector", "m_date", "t_date", "comm_text"]:
    #             del st.session_state[key]
        
    #     st.rerun()
    # """

    if st.button("New Entry"):
        st.markdown("""
            <meta http-equiv="refresh" content="0; url='/quality_tracker'" />
            """, unsafe_allow_html=True
    )