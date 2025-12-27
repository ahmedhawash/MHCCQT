import streamlit as st
import pandas as pd

st.title("Get Started")
st.header("Quality Results", divider="red")

st.markdown("## Recent Evaluations")

import os
import pandas as pd

RESULTS_DIR = "data/results"

# List all result CSV files
result_files = [
    f for f in os.listdir(RESULTS_DIR)
    if f.endswith(".csv") and "_results_" in f
]

# Extract question timestamps
question_timestamps = [
    f.split("_results_")[0] for f in result_files
]

# Get the most recent questions timestamp
latest_questions_timestamp = max(question_timestamps)

# Lates timestamp files
latest_result_files = [
    f for f in result_files
    if f.startswith(latest_questions_timestamp)
]

# 5. Load and combine
dfs = []
for file in latest_result_files:
    path = os.path.join(RESULTS_DIR, file)
    dfs.append(pd.read_csv(path))

results_df = pd.concat(dfs, ignore_index=True)

results_df = results_df.sort_values(by='result_id', ascending=False)


st.data_editor(results_df, disabled=True)

st.markdown("## Average Score / Agent")
avg_score_agent = results_df.pivot_table(
    index=["agent_name"],
    values=["total_score"],
    aggfunc="mean"
)


st.bar_chart(avg_score_agent, sort="-total_score")
