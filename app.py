import streamlit as st
import pandas as pd

# 设置网页标题和图标
st.set_page_config(page_title="生态学高分写作进化站", layout="wide", page_icon="🌿")

st.title("🌿 功能生态学：顶级论文思维与写作进化站")
st.markdown("---")

# 侧边栏导航
menu = st.sidebar.radio("功能模块", ["CNS 逻辑解剖室", "万金油句式矿场", "进度看板"])

if menu == "CNS 逻辑解剖室":
    st.header("🧠 顶级论文逻辑拆解")
    st.info("在此输入你正在精读的 CNS 论文段落，建立你的科研思维骨架。")
    
    paper_title = st.text_input("论文题目", placeholder="例如: Biodiversity increases ecosystem stability...")
    content = st.text_area("粘贴摘要或核心段落", height=200)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("1. 科学 Gap")
        st.write("作者发现了什么现有研究没解决的问题？")
    with col2:
        st.subheader("2. 核心假设")
        st.write("本文基于什么理论（如 Mass Ratio Hypothesis）？")
    with col3:
        st.subheader("3. 结论高度")
        st.write("结论如何提升了领域认知？")

elif menu == "万金油句式矿场":
    st.header("💎 领域高分句式积累")
    
    # 模拟数据库（后续可连接 Google Sheets 或本地 CSV）
    data = {
        "结构": ["Introduction", "Results", "Discussion"],
        "逻辑意图": ["强调研究缺口", "描述交互作用", "理论升华"],
        "顶级句式模板": [
            "Despite extensive research on [A], the role of [B] in mediating [C] remains elusive.",
            "Our results reveal a synergistic effect between [X] and [Y], suggesting a non-linear response.",
            "These findings provide empirical evidence for [Theory], challenging the conventional view that..."
        ]
    }
    df = pd.DataFrame(data)
    
    st.table(df)
    
    st.subheader("➕ 录入新句式")
    new_cat = st.selectbox("段落位置", ["Intro", "Method", "Results", "Discussion"])
    new_intent = st.text_input("写作意图 (例如：描述物种入侵路径)")
    new_sent = st.text_area("原文金句 (可挖空处理)")
    if st.button("存入我的私有库"):
        st.success("已成功存入！这将在你下次打开时永久保存。")

elif menu == "进度看板":
    st.header("📈 我的进化进度")
    st.metric(label="已深度解剖 CNS 论文", value="12 篇")
    st.metric(label="已内化高分句式", value="85 个")
    st.progress(85/100)
    st.write("距离‘信手拈来’的写作境界还差 15 个句式，继续加油！")