# -*- coding: utf-8 -*-
# 偉人診断ツール（AIネイティブ×経営者向け）UIカスタム＋CTA追加＋ボタン装飾＋クリックログ対応版

import streamlit as st
import os
import datetime

st.set_page_config(page_title="経営者の偉人診断", layout="centered")
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
        }
        .block-container {
            padding-top: 3rem;
            padding-bottom: 3rem;
        }
        h1, h2, h3 {
            font-size: 2rem;
            color: #333333;
        }
        .stButton button {
            font-size: 1.2rem;
            padding: 0.75rem 1.5rem;
            background-color: #333;
            color: white;
            border-radius: 8px;
            border: none;
            margin-top: 10px;
        }
        .stButton button:hover {
            background-color: #555;
        }
    </style>
""", unsafe_allow_html=True)

# --- ログファイル設定 ---
LOG_FILE = "cta_click_log.csv"

def log_click(label):
    with open(LOG_FILE, "a") as f:
        now = datetime.datetime.now().isoformat()
        f.write(f"{now},{label}\n")

# --- 01. 質問設計 ---
questions = [
    {
        "question": "あなたが最も重視するのは？",
        "options": {
            "A": ("成果とインパクト / Results & Impact", "outcome"),
            "B": ("過程と仕組み / Process & System", "process"),
            "C": ("信頼と共感 / Trust & Empathy", "relationship"),
            "D": ("理念と意味 / Philosophy & Meaning", "value")
        }
    },
    {
        "question": "チームをどう導きたい？",
        "options": {
            "A": ("結果にコミットさせる / Commit to Results", "outcome"),
            "B": ("改善の文化を育てる / Build a Culture of Improvement", "process"),
            "C": ("つながりを強化する / Strengthen Connections", "relationship"),
            "D": ("価値観を共有する / Share Values", "value")
        }
    },
    {
        "question": "あなたの強みは？",
        "options": {
            "A": ("ビジョンを形にする実行力 / Visionary Execution", "outcome"),
            "B": ("地道に積み上げる力 / Persistent Builder", "process"),
            "C": ("人の心をつかむ力 / Emotional Connection", "relationship"),
            "D": ("本質を問い続ける力 / Deep Thinker", "value")
        }
    },
    {
        "question": "経営で一番大切なのは？",
        "options": {
            "A": ("明確な成果を出すこと / Clear Outcomes", "outcome"),
            "B": ("継続できる仕組み / Sustainable Systems", "process"),
            "C": ("人との関係性 / Human Relationships", "relationship"),
            "D": ("理念に基づく判断 / Value-Based Decisions", "value")
        }
    }
]

# --- 02. スコア判定 ---
def calculate_result(answers):
    scores = {"outcome": 0, "process": 0, "relationship": 0, "value": 0}
    for answer in answers:
        scores[answer] += 1
    return max(scores, key=scores.get)

# --- 03. 表示ロジック ---
def display_result(result_type):
    results = {
        "outcome": {
            "name": "スティーブ・ジョブズ",
            "image": "img/steve_jobs.jpg",
            "movie": "『スティーブ・ジョブズ』（2015）",
            "description": "You are a visionary. あなたは未来を描く人です。明確な成果にこだわり、革新を形にする力があります。"
        },
        "process": {
            "name": "ヘンリー・フォード",
            "image": "img/henry_ford.jpg",
            "movie": "『フォードvsフェラーリ』（2019）",
            "description": "You are a builder. あなたは仕組みを整え、安定した成長を支える人です。"
        },
        "relationship": {
            "name": "マーク・ザッカーバーグ",
            "image": "img/mark_zuckerberg.jpg",
            "movie": "『ソーシャル・ネットワーク』（2010）",
            "description": "You are a connector. あなたは人と人とのつながりを生み出す共感力の持ち主です。"
        },
        "value": {
            "name": "ピーター・ドラッカー（象徴）",
            "image": "img/peter_drucker.jpg",
            "movie": "『マネーボール』（2011）",
            "description": "You are a thinker. あなたは理念と合理を融合し、未来の意味を問い続ける人です。"
        }
    }
    result = results[result_type]
    st.subheader(f"あなたは『{result['name']}』タイプ！")
    st.image(result["image"], width=300)
    st.write(f"🎬 映画：{result['movie']}")
    st.markdown(f"<div style='font-size: 1.2rem; margin-top: 1rem;'>{result['description']}</div>", unsafe_allow_html=True)

    # --- CTAセクション ---
    st.markdown("---")
    st.markdown("### あなたに合った成功パターンをもっとみてみたい方はコチラへ")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**AIネイティブ対応、実は困ってない？**")
        if st.button("AIモヤモヤ解決リストを受け取る ▶"):
            log_click("AI_native_form")
            st.markdown("<meta http-equiv='refresh' content='0; url=https://gia-laboratory.com/gia-learning-lounge-form/'>", unsafe_allow_html=True)

    with col2:
        st.markdown("**SNS集客、なんとなくやってない？**")
        if st.button("SNS情報整理リストをみる▶"):
            log_click("SNS_form")
            st.markdown("<meta http-equiv='refresh' content='0; url=https://gia-laboratory.com/gia-learning-lounge-form-2/'>", unsafe_allow_html=True)

# --- Streamlit UI ---
if "answers" not in st.session_state:
    st.session_state.answers = []

question_index = len(st.session_state.answers)

if question_index < len(questions):
    q = questions[question_index]
    st.markdown(f"<h3 style='margin-bottom: 1rem;'>{q['question']}</h3>", unsafe_allow_html=True)
    for key, (text, type_key) in q["options"].items():
        if st.button(f"{key}: {text}"):
            st.session_state.answers.append(type_key)
            st.rerun()
else:
    result = calculate_result(st.session_state.answers)
    display_result(result)
    if st.button("Start Over"):
        st.session_state.answers = []
        st.rerun()
