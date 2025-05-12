import os
import streamlit as st
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# OpenAI APIキーの取得（Colabで設定済み）
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI APIキーが設定されていません。環境変数を確認してください。")
    st.stop()

# LLM要約関数の定義
def generate_summary(story_title, expert_choice):
    # Web検索
    search = DuckDuckGoSearchRun()
    search_results = search.run(f"{story_title} 童話 あらすじ")

    if not search_results or not search_results.strip():
        return "検索結果が見つかりませんでした。別の題名を試してください。"

    # 専門家に応じたプロンプトの作成
    if expert_choice == "心理学者":
        prompt = PromptTemplate(
            input_variables=["story_title", "web_content"],
            template="""
以下は「{story_title}」という童話についてWebから集めた情報です。
これを基に、心理学者として、登場人物の心理状態や感情の動きについて焦点を当てて、小学生にもわかりやすく要約してください。
おじいさんの博士のような口調で説明してください。

情報:
{web_content}

要約:
"""
        )
    elif expert_choice == "教育学者":
        prompt = PromptTemplate(
            input_variables=["story_title", "web_content"],
            template="""
以下は「{story_title}」という童話についてWebから集めた情報です。
これを基に、教育学者として、子どもたちにとって学びやすいポイントや教訓を強調し、小学生にもわかりやすく要約してください。
お姉さんの口調で説明してください。

情報:
{web_content}

要約:
"""
        )





    # GPT-4で要約実行
    try:
        llm = ChatOpenAI(model="gpt-4", temperature=0.7, openai_api_key=openai_api_key)
        chain = LLMChain(llm=llm, prompt=prompt)
        summary = chain.run({"story_title": story_title, "web_content": search_results})
        return summary
    except Exception as e:
        return f"要約の生成中にエラーが発生しました: {e}"

import streamlit as st
import os

# カスタムCSSで背景と文字色を変更
st.markdown(
    """
    <style>
    /* 全体の背景と文字色 */
    html, body, .stApp {
        background-color: white;
        color: black;
    }

    /* 入力フォームの背景と文字色 */
    input {
        background-color: #f0f0f0 !important;
        color: black !important;
        border-radius: 5px;
        padding: 0.5em;
    }

    /* ラジオボタンの文字色を黒に */
    .stRadio > label, .stRadio div {
        color: black !important;
    }

    /* ボタンの背景色を淡いグレーに強制上書き */
    button {
        background-color: #e0e0e0 !important;
        color: black !important;
        border: none;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        transition: background-color 0.3s ease, transform 0.2s ease;
    }

    /* ボタンホバー演出 */
    button:hover {
        background-color: #d5d5d5 !important;
        transform: scale(1.03);
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# タイトルと説明文
st.title("📚 童話要約アプリ")
st.markdown("### 🎉 童話の世界を、専門家がやさしく解説！")
st.write("このアプリは、童話の題名を入力すると、Webから情報を検索し、心理学者や教育学者の視点で小学生にもわかりやすい要約を生成します。")

# 親しみやすいイラスト風の区切り線
st.markdown("---")
st.markdown("🖋️ **まずは、知りたい童話のタイトルを入力してみよう！**")

# 入力フォーム
story_title = st.text_input("🔍 童話の題名を入力してください", "")

# 専門家の選択（ラジオボタン）
expert_choice = st.radio("🧠 どんな先生に説明してもらう？", ("心理学者", "教育学者"))

# 実行ボタン
if st.button("✨ 要約する！"):
    if not story_title.strip():
        st.error("題名を入力してください。")
    else:
        # （ここで generate_summary() を呼び出して表示）
        with st.spinner("童話を検索してまとめているよ..."):
            summary = generate_summary(story_title, expert_choice)
        st.subheader("📖 要約結果")
        with st.expander("🔽 ここをクリックしてみよう！"):
            st.write(summary)

