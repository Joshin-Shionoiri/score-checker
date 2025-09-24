import streamlit as st
import pandas as pd
import datetime
import uuid
import smtplib  # SendGridなどに置き換え可能

st.title("📝 電子出願システム")

# 出願開始ボタン
if st.button("出願する"):
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
            # 受験番号の自動発番
            try:
                existing = pd.read_csv("scores.csv")
                last_id = existing["examId"].str.extract(r'(\d+)').dropna().astype(int).max()[0]
                new_id = f"A{last_id+1:05d}"
            except:
                new_id = "A00001"

            # データ保存
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

            # メール通知（SendGridなどに置き換え）
            # send_email(email, new_id) ←ここに関数を定義して呼び出し

            st.success(f"出願が完了しました！あなたの受験番号は {new_id} です")
