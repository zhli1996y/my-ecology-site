import streamlit as st
import pandas as pd
import os
import random
import feedparser

# --- 页面配置 ---
st.set_page_config(page_title="Ecology Writing Hub", layout="wide", page_icon="🌿")

# --- 数据持久化处理 ---
DB_FILE = "my_ecology_phrases.csv"

# 初始化句式库 (内置首批功能生态学高分句式)
default_data = [
    {"section": "Introduction", "intent": "描述功能性状的全球趋势", "sentence": "Global patterns of [Trait A] reveal a fundamental trade-off between **resource acquisition** and **conservation strategies**."},
    {"section": "Introduction", "intent": "强调生物多样性流失的背景", "sentence": "Accelerating biodiversity loss has sparked intense interest in how **functional redundancy** buffers ecosystems against environmental stochasticity."},
    {"section": "Introduction", "intent": "指出研究空白（入侵生态学）", "sentence": "Despite extensive research, the mechanisms by which **invasive congeners** bypass biotic resistance remain poorly understood."},
    {"section": "Methods", "intent": "描述物种选取标准", "sentence": "Species were selected based on their **functional distinctiveness** and their dominance within the local community."},
    {"section": "Methods", "intent": "描述统计模型选择", "sentence": "We employed **piecewise structural equation modeling** to partition the direct and indirect effects of [Factor X] on [Function Y]."},
    {"section": "Results", "intent": "描述非线性响应", "sentence": "Our results demonstrate that ecosystem productivity exhibits a **unimodal response** to functional diversity gradients."},
    {"section": "Results", "intent": "描述交互作用的显著性", "sentence": "The interaction between **nitrogen deposition** and **drought severity** significantly modulated the trait-expression of [Species Z]."},
    {"section": "Discussion", "intent": "将结果与经典理论联系", "sentence": "These findings are consistent with the **mass ratio hypothesis**, suggesting that biomass is driven by the traits of the dominant species."},
    {"section": "Discussion", "intent": "阐述全球变化下的生态意义", "sentence": "Our study underscores the importance of considering **intra-specific trait variation** when predicting ecosystem responses to global warming."},
    {"section": "Discussion", "intent": "提出未来的研究方向", "sentence": "Future research should integrate **below-ground functional traits** to provide a more holistic view of carbon cycling."},
    # ... 此处可继续添加至200组
]

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        df = pd.DataFrame(default_data)
        df.to_csv(DB_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# 加载数据
if 'phrase_df' not in st.session_state:
    st.session_state.phrase_df = load_data()

# --- 界面设计 ---
st.title("🌿 功能生态学写作进化站")

tab1, tab2, tab3 = st.tabs(["📡 前沿精读 (RSS)", "🃏 碎片化背诵 (Anki模式)", "📔 我的句式库管理"])

# --- Tab 1: RSS 阅读 ---
with tab1:
    st.subheader("📡 CNS & Ecology 实时动态")
    jr_rss = {
        "Nature Ecology & Evolution": "https://www.nature.com/natecolevol.rss",
        "Science Latest": "https://www.science.org/rss/news_current.xml",
        "Ecology Letters": "https://onlinelibrary.wiley.com/rss/journal/10.1111/(ISSN)1461-0248",
        "Global Change Biology": "https://onlinelibrary.wiley.com/rss/journal/10.1111/(ISSN)1365-2486"
    }
    selected = st.selectbox("订阅频道", list(jr_rss.keys()))
    feed = feedparser.parse(jr_rss[selected])
    for entry in feed.entries[:5]:
        with st.expander(f"📖 {entry.title}"):
            st.write(entry.summary if 'summary' in entry else "No summary available.")
            st.markdown(f"[阅读原文]({entry.link})")

# --- Tab 2: 背诵模式 ---
with tab2:
    st.subheader("🃏 碎片化复习")
    # 从库中随机选一行
    if st.button("🔄 换一个句式"):
        st.session_state.random_idx = random.randint(0, len(st.session_state.phrase_df)-1)
    
    if 'random_idx' not in st.session_state:
        st.session_state.random_idx = 0
    
    row = st.session_state.phrase_df.iloc[st.session_state.random_idx]
    
    st.info(f"**【{row['section']}】写作意图：{row['intent']}**")
    
    if st.checkbox("👁️ 查看高分句式 (标准表达)"):
        st.success(row['sentence'])
        st.caption("提示：你可以试着在纸上模仿这个结构写一个关于你研究方向的句子。")

# --- Tab 3: 录入与存储 ---
with tab3:
    st.subheader("📔 个人句式沉淀")
    st.write("在这里录入你阅读时发现的精彩句式，它们将永久保存。")
    
    with st.form("new_phrase"):
        c1, c2 = st.columns(2)
        with c1:
            sec = st.selectbox("段落位置", ["Abstract", "Introduction", "Methods", "Results", "Discussion"])
        with c2:
            intent = st.text_input("逻辑意图 (如：描述环境梯度)")
        
        sentence = st.text_area("高分句式 (建议把具体物种名用 [Species] 代替，方便复用)")
        
        if st.form_submit_button("💾 永久保存"):
            new_row = pd.DataFrame([{"section": sec, "intent": intent, "sentence": sentence}])
            st.session_state.phrase_df = pd.concat([st.session_state.phrase_df, new_row], ignore_index=True)
            save_data(st.session_state.phrase_df)
            st.success("数据已持久化存储！")

    st.divider()
    st.subheader("🔍 库内搜索与导出")
    search_q = st.text_input("搜索意图关键词")
    filtered_df = st.session_state.phrase_df[st.session_state.phrase_df['intent'].str.contains(search_q, case=False)]
    st.dataframe(filtered_df, use_container_width=True)
    
    # 导出按钮
    csv = st.session_state.phrase_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 下载完整句式库 (.csv)", data=csv, file_name="my_ecology_phrases.csv")
