import streamlit as st
import pandas as pd

st.title("📊 成績照会システム")

option = st.radio("操作を選択してください", ["照会する", "登録する"])

df = pd.read_csv("scores.csv")

if option == "照会する":
    st.subheader("受験者照会フォーム")
    examId = st.text_input("受験番号")
    name = st.text_input("氏名")
    dob = st.text_input("生年月日")
    password = st.text_input("パスワード", type="password")

    if st.button("照会する"):
        match = df[
            (df["examId"] == examId) &
            (df["name"] == name) &
            (df["dob"] == dob) &
            (df["password"] == password)
        ]
        if not match.empty:
            st.success("照会成功！")
            st.write(f"得点: {match.iloc[0]['score']}")
            st.write(f"判定: {match.iloc[0]['result']}")
            st.markdown(f"[PDFリンクはこちら]({match.iloc[0]['pdf']})")
        else:
            st.error("照会情報が一致しません。")

elif option == "登録する":
    st.subheader("管理者ログイン")
    admin_pass = st.text_input("管理者パスワード", type="password")
    if admin_pass == "admin1234":
        st.success("ログイン成功！")
        with st.form("登録フォーム"):
            examId = st.text_input("受験番号")
            name = st.text_input("氏名")
            dob = st.text_input("生年月日")
            password = st.text_input("パスワード")
            score = st.text_input("得点")
            result = st.text_input("判定")
            pdf = st.text_input("PDFリンク")
            submitted = st.form_submit_button("登録する")
            if submitted:
                new_row = pd.DataFrame([{
                    "examId": examId,
                    "name": name,
                    "dob": dob,
                    "password": password,
                    "score": score,
                    "result": result,
                    "pdf": pdf
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv("scores.csv", index=False)
                st.success("登録完了！")
    else:
        st.warning("パスワードが間違っています。")
