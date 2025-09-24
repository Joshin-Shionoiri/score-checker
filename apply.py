import streamlit as st
import pandas as pd
import datetime

st.title("📝 電子出願システム")

# 出願モード切り替え
if "apply_mode" not in st.session_state:
    st.session_state.apply_mode = False

if not st.session_state.apply_mode:
    if st.button("出願する"):
        st.session_state.apply_mode = True

if st.session_state.apply_mode:
    st.subheader("受験者情報を入力してください")

    with st.form("application_form"):
        name = st.text_input("氏名")
        dob = st.date_input("生年月日", value=datetime.date(2005, 1, 1))
        email = st.text_input("メールアドレス")
        exam_date = st.date_input("希望試験日", value=datetime.date(2025, 10, 1))
        location = st.selectbox("希望試験会場", ["東京", "大阪", "名古屋", "福岡"])
        password = st.text_input("照会用パスワード", type="password")
        submitted = st.form_submit_button("出願する")

        if submitted:
            try:
                existing = pd.read_csv("scores.csv")
                last_id = existing["examId"].str.extract(r'(\d+)').dropna().astype(int).max()[0]
                new_id = f"A{last_id+1:05d}"
            except:
                new_id = "A00001"

            new_row = pd.DataFrame([{
                "examId": new_id,
                "name": name,
                "dob": dob.strftime("%Y-%m-%d"),
                "password": password,
                "score": "",
                "result": "",
                "pdf": ""
            }])

            try:
                df = pd.read_csv("scores.csv")
                df = pd.concat([df, new_row], ignore_index=True)
            except FileNotFoundError:
                df = new_row

            df.to_csv("scores.csv", index=False)
            st.success(f"出願が完了しました！あなたの受験番号は {new_id} です")
