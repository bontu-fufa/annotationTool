import streamlit as st
import pandas as pd
import os

CSV_PATH = "predictions_new.csv"

# Utility functions
def safe_str(val):
    return str(val) if pd.notna(val) else ""

def safe_int(val, default=0):
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


# Load data
if not os.path.exists(CSV_PATH):
    st.error("CSV file not found.")
    st.stop()

df = pd.read_csv(CSV_PATH)

if 'row_index' not in st.session_state:
    st.session_state.row_index = 0

# Clamp row index
st.session_state.row_index = max(0, min(st.session_state.row_index, len(df) - 1))
row = df.iloc[st.session_state.row_index]

# Layout starts immediately, no space at the top
st.markdown(
    f"""
    <style>
        .block-container {{
            padding-top: 2.75rem;
            padding-bottom: 0rem;
        }}
    </style>
    """, unsafe_allow_html=True
)

# Main layout: 1/3 info, 2/3 form
left, right = st.columns([1, 2])

with left:
    st.markdown("#### Input")
    st.write("**Masked Sentence**")
    st.write(safe_str(row.get('masked_sentence')))
    st.write("**Predictions:**")
    st.write(safe_str(row.get('Predictions')))
    st.write("**Expected gender:**", safe_str(row.get('Expected Gender')))

with right:
    # Go to row feature
    # One-line "Go to row #" with visible label
    go_col1, go_col2, go_col3 = st.columns([1.4, 2, 1])
    with go_col1:
        st.markdown("**Go to row #**", help="Enter the row number to jump to")

    with go_col2:
        goto_index = st.number_input("", min_value=1, max_value=len(df),
                                    value=st.session_state.row_index + 1,
                                    step=1, label_visibility="collapsed")

    with go_col3:
        if st.button("Go"):
            st.session_state.row_index = int(goto_index - 1)
            st.rerun()



    st.markdown(f"#### 🧾 Annotate — Row {st.session_state.row_index + 1} / {len(df)}")

    def select_input(label, options, val, default=0):
        norm = str(val).strip().capitalize() if options[0].istitle() else str(val).strip().lower()
        return st.selectbox(label, options, index=options.index(norm) if norm in options else default)

    # Row 1: Top 1, Top 5, T1 Prediction
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        top1 = select_input("TOP 1", ["Yes", "Neutral", "No", "Wrong"], row.get("TOP 1", "Yes"))
    with r1c2:
        top5 = select_input("Top 5", ["Yes", "Neutral", "No", "Wrong"], row.get("Top 5", "Yes"))
    with r1c3:
        t1_gender = select_input("T1 Predicted Gender", ["male", "female", "neutral", "wrong"], row.get("T1 Predicted Gender", "neutral"))

    # Row 2: T5 Male & Female
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        t5_male = st.number_input("T5 Male", min_value=0, step=1, value=safe_int(row.get("T5 Male")))
    with r2c2:
        t5_female = st.number_input("T5 Female", min_value=0, step=1, value=safe_int(row.get("T5 Female")))

    # Row 3: T5 Neutral & Wrong
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        t5_neutral = st.number_input("T5 Neutral", min_value=0, step=1, value=safe_int(row.get("T5 Neutral")))
    with r3c2:
        wrong = st.number_input("Wrong", min_value=0, step=1, value=safe_int(row.get("Wrong")))

    # Row 4: Comment
    comment = st.text_area("Comment", value=safe_str(row.get("comments")),  height=80 )

    # Row 5: Save + Navigation
    col_save, col_back, col_next = st.columns([2, 1, 1])
    with col_save:
        if st.button("💾 Save"):
            df.at[st.session_state.row_index, "TOP 1"] = top1
            df.at[st.session_state.row_index, "Top 5"] = top5
            df.at[st.session_state.row_index, "T1 Predicted Gender"] = t1_gender
            df.at[st.session_state.row_index, "T5 Male"] = t5_male
            df.at[st.session_state.row_index, "T5 Female"] = t5_female
            df.at[st.session_state.row_index, "T5 Neutral"] = t5_neutral
            df.at[st.session_state.row_index, "Wrong"] = wrong
            df.at[st.session_state.row_index, "comments"] = comment
            df.to_csv(CSV_PATH, index=False)
            st.success("✅ Saved!")

    with col_back:
        if st.button("⬅️ Back") and st.session_state.row_index > 0:
            st.session_state.row_index -= 1
            st.rerun()

    with col_next:
        if st.button("➡️ Next") and st.session_state.row_index < len(df) - 1:
            st.session_state.row_index += 1
            st.rerun()
