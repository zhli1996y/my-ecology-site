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
   # 新增100句功能生态学/生物多样性领域论文句式

    # Introduction 部分 (25句)
    {"section": "Introduction", "intent": "强调功能多样性与生态系统功能的关系", "sentence": "The relationship between **biodiversity** and **ecosystem functioning** has emerged as a central theme in ecology, yet the role of **functional trait diversity** remains poorly quantified."},
    {"section": "Introduction", "intent": "指出物种丰富度与功能组成的研究差距", "sentence": "Although many studies have examined the effects of **species richness** on productivity, fewer have considered how **functional composition** mediates these relationships."},
    {"section": "Introduction", "intent": "描述全球变化对群落性状分布的影响", "sentence": "Global environmental changes, such as **climate warming** and **land-use intensification**, are expected to alter **community trait distributions**, with cascading effects on ecosystem processes."},
    {"section": "Introduction", "intent": "强调性状生态学理论框架的实证需求", "sentence": "Recent advances in **trait-based ecology** have provided a framework for predicting species responses to environmental gradients, but empirical tests remain scarce."},
    {"section": "Introduction", "intent": "讨论物种共存机制的重要性", "sentence": "Understanding the mechanisms underlying **species coexistence** is crucial for predicting biodiversity loss under global change scenarios."},
    {"section": "Introduction", "intent": "提出功能冗余假说", "sentence": "The **functional redundancy** hypothesis posits that multiple species can perform similar roles, thereby buffering ecosystems against species loss."},
    {"section": "Introduction", "intent": "强调种内性状变异的研究不足", "sentence": "Despite growing recognition of the importance of **intraspecific trait variation**, most studies still rely on species mean trait values, potentially overlooking key ecological dynamics."},
    {"section": "Introduction", "intent": "讨论入侵物种的性状新颖性", "sentence": "Invasive species often possess **novel traits** that allow them to outcompete native species, yet the role of **trait novelty** in invasion success is not fully understood."},
    {"section": "Introduction", "intent": "指出BEF关系的生态系统普适性问题", "sentence": "The **biodiversity-ecosystem functioning** (BEF) relationship has been extensively studied in grasslands, but its generality across other ecosystems, such as forests or aquatic systems, remains unclear."},
    {"section": "Introduction", "intent": "定义功能性状", "sentence": "Functional traits, defined as morphological, physiological, or phenological characteristics that affect fitness, offer a mechanistic link between organisms and ecosystem processes."},
    {"section": "Introduction", "intent": "指出多驱动因子相互作用的研究空白", "sentence": "One key knowledge gap is how **multiple global change drivers** interact to affect **functional diversity** and, in turn, ecosystem multifunctionality."},
    {"section": "Introduction", "intent": "讨论质量比假说", "sentence": "The **mass ratio hypothesis** suggests that ecosystem properties are primarily determined by the traits of dominant species, but this idea has rarely been tested under field conditions."},
    {"section": "Introduction", "intent": "强调性状权衡在群落组装中的作用", "sentence": "Recent theoretical work highlights the importance of **trait trade-offs** in shaping community assembly, yet empirical evidence is limited."},
    {"section": "Introduction", "intent": "描述生物多样性丧失对功能多样性的影响", "sentence": "Biodiversity loss may lead to a decline in **functional diversity**, which could impair ecosystem stability and resilience."},
    {"section": "Introduction", "intent": "强调性状-环境关系的重要性", "sentence": "Understanding the **trait-environment relationships** is essential for predicting community responses to environmental change."},
    {"section": "Introduction", "intent": "讨论功能多样性度量的争议", "sentence": "While the concept of **functional diversity** has gained traction, its measurement and interpretation remain subject to debate."},
    {"section": "Introduction", "intent": "讨论系统发育多样性的局限性", "sentence": "The role of **phylogenetic diversity** as a proxy for functional diversity has been questioned, given that traits may not be evolutionarily conserved."},
    {"section": "Introduction", "intent": "强调物种周转和性状周转的重要性", "sentence": "In the context of global change, it is critical to assess how **species turnover** and **trait turnover** contribute to changes in ecosystem functioning."},
    {"section": "Introduction", "intent": "指出入侵物种功能性状研究不足", "sentence": "Despite the prevalence of **invasive species**, we lack a comprehensive understanding of how their **functional traits** mediate their impacts on native communities."},
    {"section": "Introduction", "intent": "描述群落性状组成对干扰的响应", "sentence": "Ecosystem responses to disturbances, such as fire or herbivory, are likely mediated by the **functional trait composition** of the community."},
    {"section": "Introduction", "intent": "讨论生态记忆的概念", "sentence": "The concept of **ecological memory** suggests that past community composition influences current ecosystem functioning, but the trait-based mechanisms remain elusive."},
    {"section": "Introduction", "intent": "强调地下性状研究不足", "sentence": "Recent studies have begun to integrate **belowground traits**, such as root morphology and mycorrhizal associations, into functional ecology, yet data are still sparse."},
    {"section": "Introduction", "intent": "讨论植物功能型的全球格局", "sentence": "Global patterns of **plant functional types** have been mapped, but the underlying drivers of these patterns are not fully resolved."},
    {"section": "Introduction", "intent": "提出保险假说", "sentence": "The **insurance hypothesis** proposes that biodiversity buffers ecosystems against environmental fluctuations, but the role of **functional trait diversity** in this context needs further exploration."},
    {"section": "Introduction", "intent": "指出预测群落性状变化的挑战", "sentence": "One of the fundamental challenges in ecology is to predict how changes in **community trait composition** will affect ecosystem processes under novel environmental conditions."},

    # Methods 部分 (25句)
    {"section": "Methods", "intent": "描述功能性状测量方法", "sentence": "We measured a suite of **functional traits** related to resource acquisition, including specific leaf area, leaf nitrogen content, and wood density, following standardized protocols."},
    {"section": "Methods", "intent": "描述群落加权平均性状计算", "sentence": "Community-weighted mean traits were calculated as the average trait value weighted by the relative abundance of each species."},
    {"section": "Methods", "intent": "描述功能多样性指数计算", "sentence": "Functional diversity indices, including functional richness, evenness, and divergence, were computed using the **FD** package in R."},
    {"section": "Methods", "intent": "描述线性混合模型的应用", "sentence": "To assess the effects of environmental gradients on trait variation, we employed **linear mixed-effects models** with site as a random factor."},
    {"section": "Methods", "intent": "描述物种选择标准", "sentence": "Species were selected to represent a gradient of **functional distinctiveness**, based on their position in a multivariate trait space."},
    {"section": "Methods", "intent": "描述种内性状变异的量化", "sentence": "We quantified **intraspecific trait variation** by measuring traits on multiple individuals per species across environmental gradients."},
    {"section": "Methods", "intent": "描述结构方程模型的使用", "sentence": "Structural equation modeling was used to partition the direct and indirect effects of **climate variables** on **ecosystem productivity** via changes in functional composition."},
    {"section": "Methods", "intent": "描述非线性关系的检验", "sentence": "To test for **nonlinear relationships**, we fitted generalized additive models with smoothing splines."},
    {"section": "Methods", "intent": "描述物种周转与种内变异的分解", "sentence": "We assessed the relative importance of **species turnover** vs. **intraspecific trait variation** in driving community-level trait shifts using a variation partitioning approach."},
    {"section": "Methods", "intent": "描述系统发育树的构建", "sentence": "Phylogenetic relationships among species were reconstructed using a **molecular phylogeny**, and phylogenetic diversity metrics were calculated."},
    {"section": "Methods", "intent": "描述元分析方法", "sentence": "We conducted a **meta-analysis** of published studies to synthesize the effects of [Driver] on [Response] across different ecosystems."},
    {"section": "Methods", "intent": "描述功能多样性的实验操纵", "sentence": "To manipulate functional diversity, we assembled experimental communities with varying levels of **trait dissimilarity** while controlling for species richness."},
    {"section": "Methods", "intent": "描述环境变量的测量", "sentence": "Environmental variables, including soil nutrients, temperature, and precipitation, were measured at each site following standard methods."},
    {"section": "Methods", "intent": "描述主成分分析的应用", "sentence": "We used **principal component analysis** to reduce the dimensionality of trait data and identify major axes of trait variation."},
    {"section": "Methods", "intent": "描述响应-效应性状框架", "sentence": "The **response-effect trait framework** was applied to distinguish traits that determine species responses to the environment from those that affect ecosystem functioning."},
    {"section": "Methods", "intent": "描述生态系统多功能性的量化", "sentence": "We quantified ecosystem multifunctionality by integrating multiple functions, such as biomass production, nutrient cycling, and water regulation, using averaging or threshold-based approaches."},
    {"section": "Methods", "intent": "描述第四角分析", "sentence": "To examine the **trait-environment relationship**, we performed a fourth-corner analysis, which tests for associations between species traits and environmental variables."},
    {"section": "Methods", "intent": "描述零模型的使用", "sentence": "We used **null models** to test whether observed functional diversity deviated from random expectations, accounting for species richness."},
    {"section": "Methods", "intent": "描述性状数据来源", "sentence": "Trait data were obtained from existing databases, such as TRY, and complemented with field measurements."},
    {"section": "Methods", "intent": "描述贝叶斯层次模型", "sentence": "We employed **Bayesian hierarchical models** to account for uncertainty in trait estimates and to model complex ecological processes."},
    {"section": "Methods", "intent": "描述入侵物种影响的分析", "sentence": "To assess the effects of **invasive species** on functional diversity, we compared invaded and uninvaded plots using paired t-tests or permutational multivariate analysis of variance."},
    {"section": "Methods", "intent": "描述生态系统功能的测量", "sentence": "We measured **ecosystem functions** at peak biomass, including aboveground net primary productivity, litter decomposition rates, and soil respiration."},
    {"section": "Methods", "intent": "描述群落组装过程的推断", "sentence": "The **community assembly** processes were inferred by comparing observed patterns of trait dispersion with null models, distinguishing between environmental filtering and limiting similarity."},
    {"section": "Methods", "intent": "描述环境梯度采样设计", "sentence": "We collected data along **environmental gradients** to capture a wide range of conditions and to test for threshold responses."},
    {"section": "Methods", "intent": "描述空间自相关的处理", "sentence": "To account for spatial autocorrelation, we included spatial covariates in our models or used generalized least squares with a spatial correlation structure."},

    # Results 部分 (25句)
    {"section": "Results", "intent": "描述功能多样性与生产力的正相关", "sentence": "Functional diversity was positively correlated with ecosystem productivity, but this relationship plateaued at high diversity levels."},
    {"section": "Results", "intent": "发现资源获取与保守性状的权衡", "sentence": "We found a significant **trade-off** between resource acquisition and conservation traits across species, consistent with the leaf economics spectrum."},
    {"section": "Results", "intent": "描述群落加权性状沿环境梯度的变化", "sentence": "Community-weighted mean traits shifted along the environmental gradient, with more acquisitive traits prevailing under high resource availability."},
    {"section": "Results", "intent": "强调种内变异对模型预测的改进", "sentence": "The inclusion of **intraspecific trait variation** improved model predictions of community responses to warming by 20%."},
    {"section": "Results", "intent": "描述功能冗余在干扰下的变化", "sentence": "Our results revealed that **functional redundancy** was high in undisturbed sites, but decreased significantly following disturbance."},
    {"section": "Results", "intent": "发现物种丰富度通过功能多样性影响多功能性", "sentence": "The effects of **species richness** on multifunctionality were mediated by functional diversity, supporting the idea that trait diversity is a key mechanism."},
    {"section": "Results", "intent": "描述入侵物种的性状优势", "sentence": "Invasive species exhibited higher specific leaf area and lower wood density compared to native species, conferring a competitive advantage."},
    {"section": "Results", "intent": "发现生产力对干旱强度的单峰响应", "sentence": "The relationship between **drought intensity** and productivity was unimodal, with peak productivity at intermediate drought levels."},
    {"section": "Results", "intent": "检测到氮添加与功能多样性的交互作用", "sentence": "We detected a significant interaction between **nitrogen addition** and **functional diversity** on decomposition rates, indicating that diversity buffers against nutrient enrichment effects."},
    {"section": "Results", "intent": "发现系统发育多样性与功能多样性弱相关", "sentence": "Phylogenetic diversity was weakly correlated with functional diversity, suggesting that traits are not strongly conserved evolutionarily."},
    {"section": "Results", "intent": "量化物种周转与种内变异的贡献", "sentence": "Species turnover was the main driver of community-level trait changes, accounting for 70% of the variation, while intraspecific variation contributed 30%."},
    {"section": "Results", "intent": "发现多功能性在中等功能均匀度时最大", "sentence": "Ecosystem multifunctionality was maximized at intermediate levels of functional evenness, supporting the **complementarity effect**."},
    {"section": "Results", "intent": "报告模型解释的方差比例", "sentence": "Our models explained 65% of the variance in productivity, with climate and functional composition as the strongest predictors."},
    {"section": "Results", "intent": "描述入侵群落的性状空间偏移", "sentence": "The **functional trait space** of invaded communities was shifted towards more acquisitive traits, indicating a shift in resource-use strategies."},
    {"section": "Results", "intent": "发现功能多样性低于阈值时功能急剧下降", "sentence": "We observed a threshold response: below a certain level of functional diversity, ecosystem functioning declined sharply."},
    {"section": "Results", "intent": "发现增温效应在贫瘠群落中更强", "sentence": "The effects of **warming** on community traits were stronger in species-poor communities than in species-rich communities, suggesting a buffering effect of biodiversity."},
    {"section": "Results", "intent": "报告根性状与土壤碳无显著关系", "sentence": "Contrary to expectations, we found no significant relationship between **root traits** and soil carbon storage, possibly due to confounding factors."},
    {"section": "Results", "intent": "支持质量比假说", "sentence": "The **mass ratio hypothesis** was supported, as community-weighted mean traits were better predictors of productivity than functional diversity indices."},
    {"section": "Results", "intent": "强调种内变异的重要性", "sentence": "Our results highlight that **intraspecific trait variation** can be as important as species turnover in shaping community trait distributions along environmental gradients."},
    {"section": "Results", "intent": "发现功能多样性与生态系统稳定性正相关", "sentence": "The relationship between **functional diversity** and **ecosystem stability** was positive, with more diverse communities exhibiting lower temporal variability in productivity."},
    {"section": "Results", "intent": "强调固氮物种对生产力的促进作用", "sentence": "We found that **nitrogen-fixing species** disproportionately enhanced ecosystem productivity, underscoring the importance of key functional groups."},
    {"section": "Results", "intent": "描述草食与干旱的交互作用降低性状多样性", "sentence": "The **interaction** between herbivory and drought reduced trait diversity, leading to simplified communities dominated by stress-tolerant species."},
    {"section": "Results", "intent": "证明功能性状比物种分类更能预测响应", "sentence": "Our results demonstrate that **functional traits** are better predictors of species responses to climate change than taxonomic identity alone."},
    {"section": "Results", "intent": "发现系统发育信息无额外预测力", "sentence": "The inclusion of **phylogenetic information** did not improve predictions of ecosystem functioning beyond trait-based models, suggesting that traits capture relevant ecological differences."},
    {"section": "Results", "intent": "描述功能多样性与物种丰富度的空间格局", "sentence": "Spatial patterns of functional diversity mirrored those of species richness, but with notable exceptions in areas with high environmental heterogeneity."},

    # Discussion 部分 (25句)
    {"section": "Discussion", "intent": "为生态位互补假说提供实证支持", "sentence": "Our findings provide empirical support for the **niche complementarity** hypothesis, showing that functionally diverse communities more efficiently use resources."},
    {"section": "Discussion", "intent": "将性状权衡与叶经济谱联系", "sentence": "The observed **trade-off** between acquisitive and conservative traits aligns with the **leaf economics spectrum** and highlights the constraints on plant strategies."},
    {"section": "Discussion", "intent": "讨论系统发育信号弱的原因", "sentence": "The lack of a strong phylogenetic signal in functional traits suggests that **convergent evolution** may have shaped trait distributions across distantly related lineages."},
    {"section": "Discussion", "intent": "强调种内变异在全球变化模型中的重要性", "sentence": "Our results underscore the importance of considering **intraspecific trait variation** in global change models, as it can buffer or amplify community responses."},
    {"section": "Discussion", "intent": "讨论功能冗余的缓冲作用及其脆弱性", "sentence": "The **functional redundancy** observed in undisturbed communities may confer resilience, but this redundancy can be eroded under chronic stress."},
    {"section": "Discussion", "intent": "解释功能多样性的单峰响应", "sentence": "The **unimodal response** of productivity to functional diversity suggests that beyond an optimum, competition may outweigh complementarity."},
    {"section": "Discussion", "intent": "讨论入侵物种对性状空间的改变", "sentence": "Our study demonstrates that **invasive species** with novel traits can alter community trait space, potentially disrupting ecosystem processes."},
    {"section": "Discussion", "intent": "强调多驱动因子相互作用的复杂性", "sentence": "The interaction between **multiple global change drivers** complicates predictions, emphasizing the need for multifactorial experiments."},
    {"section": "Discussion", "intent": "挑战物种丰富度作为功能多样性代理的观点", "sentence": "Our results challenge the assumption that **species richness** alone is a sufficient proxy for functional diversity; instead, trait-based metrics provide more mechanistic insights."},
    {"section": "Discussion", "intent": "支持质量比假说并指出性状变异的作用", "sentence": "The strong relationship between **community-weighted mean traits** and ecosystem functioning supports the **mass ratio hypothesis**, but also highlights the importance of trait variation."},
    {"section": "Discussion", "intent": "提出生态系统管理启示", "sentence": "Our findings have implications for **ecosystem management**, suggesting that maintaining functionally diverse communities can enhance stability and productivity."},
    {"section": "Discussion", "intent": "警告系统发育多样性不能可靠替代功能多样性", "sentence": "The weak correlation between **phylogenetic diversity** and functional diversity indicates that phylogenetic diversity may not reliably capture functional differences, cautioning its use as a surrogate."},
    {"section": "Discussion", "intent": "建议未来研究纳入时间动态", "sentence": "Future studies should incorporate **temporal dynamics** of traits and functions to better understand the mechanisms underlying BEF relationships."},
    {"section": "Discussion", "intent": "指出阈值效应对保护的意义", "sentence": "The observed **threshold effects** suggest that conservation efforts should aim to maintain functional diversity above critical levels to avoid ecosystem degradation."},
    {"section": "Discussion", "intent": "提倡基于性状的方法预测全球变化响应", "sentence": "Our work highlights the need for **trait-based approaches** in predicting ecosystem responses to global change, moving beyond traditional taxonomic measures."},
    {"section": "Discussion", "intent": "讨论种内变异的适应意义", "sentence": "The **intraspecific trait variation** detected along environmental gradients may represent rapid adaptive responses, with implications for species persistence under climate change."},
    {"section": "Discussion", "intent": "参与物种丰富度与功能组成的辩论", "sentence": "Our results contribute to the ongoing debate on the relative importance of **species richness** vs. **functional composition** in driving ecosystem functioning."},
    {"section": "Discussion", "intent": "强调功能性状空间方法的价值", "sentence": "The **functional trait space** approach provides a powerful tool for quantifying community structure and linking it to ecosystem processes."},
    {"section": "Discussion", "intent": "提醒研究结果的生态系统局限性", "sentence": "We caution that our findings are based on a single ecosystem type; further research is needed to test the generality across different biomes."},
    {"section": "Discussion", "intent": "强调功能多样性对多功能性的积极效应", "sentence": "The **positive effects** of functional diversity on multifunctionality reinforce the idea that biodiversity conservation should prioritize functional traits."},
    {"section": "Discussion", "intent": "揭示环境过滤与限制相似性的相对重要性", "sentence": "Our study reveals that **environmental filtering** is the dominant assembly process in harsh environments, while **limiting similarity** becomes more important under benign conditions."},
    {"section": "Discussion", "intent": "讨论草食与干旱交互作用的复杂性", "sentence": "The **interaction** between herbivory and drought highlights the complexity of ecological responses and the need for integrative approaches."},
    {"section": "Discussion", "intent": "呼吁加强地下性状研究", "sentence": "The role of **belowground traits** in ecosystem functioning remains understudied; we advocate for more comprehensive trait measurements including roots and symbionts."},
    {"section": "Discussion", "intent": "提出功能多样性可作为生态系统退化的预警指标", "sentence": "Our findings suggest that **functional diversity** can serve as an early warning indicator of ecosystem degradation before species loss becomes apparent."},
    {"section": "Discussion", "intent": "强调将功能性状整合进预测模型", "sentence": "Ultimately, integrating **functional traits** into predictive models will improve our ability to forecast the consequences of biodiversity loss for ecosystem services."}

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

