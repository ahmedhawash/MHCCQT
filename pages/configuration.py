import os
import streamlit as st
import pandas as pd
from datetime import datetime


# Delete file in path
def delete_existing_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)

# Save df as CSV


def save_dataframe(df, folder_path, filename):
    file_path = os.path.join(folder_path, filename)
    df.to_csv(file_path, index=False)

####################


st.title("Configuration")

questions_tab, tab2, tab3 = st.tabs(["Questions", "Agents", "QA Coaches"])

# Questions tab

# Questions Path
SAVE_QUESTIONS_PATH = "data/questions"

current_questions_csv_path = os.path.join(
    SAVE_QUESTIONS_PATH, os.listdir(SAVE_QUESTIONS_PATH)[0])
current_questions_df = pd.read_csv(current_questions_csv_path)


with questions_tab:

    st.markdown("# Questions")

    st.markdown("## Upload Questions")

    uploaded_file = st.file_uploader(
        "Choose a file", type="csv", key="questions")
    if uploaded_file is not None:
        try:
            questions_df = pd.read_csv(uploaded_file)

            # 1. Remove completely empty rows
            questions_df = questions_df.dropna(how="all")

            # 2. Validate columns
            expected_columns = ["Number", "Question", "Weight"]
            if list(questions_df.columns) != expected_columns:
                st.error(
                    "CSV must have exactly these columns: Number, Question, Weight")
                st.stop()

            # 3. Convert Number and Weight to numeric
            questions_df["Number"] = pd.to_numeric(
                questions_df["Number"], errors="coerce")
            questions_df["Weight"] = pd.to_numeric(
                questions_df["Weight"], errors="coerce")

            # 4. Check for invalid numbers
            if questions_df["Number"].isnull().any() or questions_df["Weight"].isnull().any():
                st.error("Number and Weight columns must contain only numbers")
                st.stop()

            # 5. Validate sum of weights
            weight_sum = questions_df["Weight"].sum()
            if weight_sum != 100:
                st.error(f"Sum of Weight must be 100 (current: {weight_sum})")
                st.stop()

            # 6. Validate row count matches max Number
            row_count = len(questions_df)
            max_number = int(questions_df["Number"].max())

            if row_count != max_number:
                st.error(
                    f"Row count ({row_count}) must match max Number ({max_number})"
                )
                st.stop()

            # If all checks pass
            st.success("CSV file is valid ✅")
            st.table(questions_df)

            current_time = datetime.now()
            current_time = current_time.strftime("%Y%m%d%H%M%S")

            delete_existing_files(SAVE_QUESTIONS_PATH)
            save_dataframe(questions_df, SAVE_QUESTIONS_PATH,
                           f"questions_{current_time}.csv")
            st.success("File saved successfully")

        except Exception as e:
            st.error("Failed to read CSV file")
            st.text(e)

    st.markdown("## Current Questions")
    st.table(current_questions_df)


# Agents tab
with tab2:

    SAVE_AGENTS_PATH = "data/agents"
    current_agents_csv_path = os.path.join(
        SAVE_AGENTS_PATH, os.listdir(SAVE_AGENTS_PATH)[0])
    current_agents_df = pd.read_csv(current_agents_csv_path)

    st.markdown("# Agents")
    st.markdown("## Upload Agents List")

    agents = st.file_uploader("Choose a file", type="csv", key="agents")
    if agents is not None:
        try:
            agents_df = pd.read_csv(agents)

            # 1. Remove completely empty rows
            agents_df = agents_df.dropna(how="all")

            # 2. Validate columns
            expected_columns = ["ID", "Agent Name"]
            if list(agents_df.columns) != expected_columns:
                st.error(
                    "CSV must have exactly these columns: ID, Agent Name")
                st.stop()
            # 3. Convert ID to numeric
            agents_df["ID"] = pd.to_numeric(
                agents_df["ID"], errors="coerce")
            # 4. Check for invalid numbers
            if agents_df["ID"].isnull().any():
                st.error("ID column must contain only numbers")
                st.stop()

            # If all checks pass
            st.success("CSV file is valid ✅")
            st.table(agents_df)

            delete_existing_files(SAVE_AGENTS_PATH)
            save_dataframe(agents_df, SAVE_AGENTS_PATH,
                           f"agents.csv")
            st.success("File saved successfully")

        except Exception as e:
            st.error("Failed to read CSV file")

    st.markdown("## Current Agents List")
    st.table(current_agents_df)

# Coaches tab
with tab3:

    SAVE_COACHES_PATH = "data/coaches"
    current_coaches_csv_path = os.path.join(
        SAVE_COACHES_PATH, os.listdir(SAVE_COACHES_PATH)[0])
    current_coaches_df = pd.read_csv(current_coaches_csv_path)

    st.markdown("# QA Coaches")
    st.markdown("## Upload Coaches List")

    coaches = st.file_uploader("Choose a file", type="csv", key="coaches")
    if coaches is not None:
        try:
            coaches_df = pd.read_csv(coaches)

            # 1. Remove completely empty rows
            coaches_df = coaches_df.dropna(how="all")

            # 2. Validate columns
            expected_columns = ["ID", "Coach Name"]
            if list(coaches_df.columns) != expected_columns:
                st.error(
                    "CSV must have exactly these columns: ID, Agent Name")
                st.stop()
            # 3. Convert ID to numeric
            coaches_df["ID"] = pd.to_numeric(
                coaches_df["ID"], errors="coerce")
            # 4. Check for invalid numbers
            if coaches_df["ID"].isnull().any():
                st.error("ID column must contain only numbers")
                st.stop()

            # If all checks pass
            st.success("CSV file is valid ✅")
            st.table(coaches_df)

            delete_existing_files(SAVE_COACHES_PATH)
            save_dataframe(coaches_df, SAVE_COACHES_PATH,
                           f"coaches.csv")
            st.success("File saved successfully")

        except Exception as e:
            st.error("Failed to read CSV file")

    st.markdown("## Current coaches List")
    st.table(current_coaches_df)
