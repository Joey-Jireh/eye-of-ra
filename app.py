
import streamlit as st
import pandas as pd
import ast
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Eye of Ra 👁️",
    page_icon="👁️",
    layout="wide"
)

@st.cache_data
def load_data():
    scored = pd.read_csv("/content/eye_of_ra_scored_contracts_v2.csv")
    return scored

scored = load_data()

def parse_list(val):
    if isinstance(val, list):
        return val
    try:
        return ast.literal_eval(val)
    except:
        return []

# ── SIDEBAR ──
st.sidebar.image("https://flagcdn.com/w80/gh.png", width=60)
st.sidebar.title("👁️ Eye of Ra")
st.sidebar.markdown("AI Procurement Fraud Detection for Ghana")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", [
    "📊 Overview",
    "🔴 Flagged Contracts",
    "🏛️ Entity Scorecards",
    "🔍 Contract Deep Dive"
])
st.sidebar.markdown("---")
st.sidebar.markdown("Built on Ghana PPA & Auditor-General data")
st.sidebar.markdown("Grounded in Public Procurement Act 663")

# ── PAGE 1: OVERVIEW ──
if page == "📊 Overview":
    st.title("👁️ Eye of Ra — Procurement Fraud Detection")
    st.markdown("### Ghana AI Summit 2026 | Real Data. Real Flags. Real Accountability.")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Contracts Scanned", "262")
    col2.metric("Fraud Detected", "87%", "20 of 23 confirmed")
    col3.metric("🔴 Escalate", str(len(scored[scored["tier"] == "🔴 ESCALATE"])))
    col4.metric("False Positives", "0", "in ESCALATE tier")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        tier_counts = scored["tier"].value_counts()
        fig = px.pie(
            values=tier_counts.values,
            names=tier_counts.index,
            title="Risk Tier Distribution — All 262 Contracts",
            color=tier_counts.index,
            color_discrete_map={
                "🔴 ESCALATE": "#d32f2f",
                "🟡 REVIEW": "#f9a825",
                "🟢 MONITOR": "#388e3c"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fraud = scored[scored["fraud_label"] == 1]
        escalate_n = len(fraud[fraud["tier"] == "🔴 ESCALATE"])
        review_n = len(fraud[fraud["tier"] == "🟡 REVIEW"])
        monitor_n = len(fraud[fraud["tier"] == "🟢 MONITOR"])
        fig2 = go.Figure(go.Bar(
            x=["🔴 ESCALATE\n(caught)", "🟡 REVIEW\n(caught)", "🟢 MONITOR\n(missed)"],
            y=[escalate_n, review_n, monitor_n],
            marker_color=["#d32f2f", "#f9a825", "#388e3c"],
            text=[escalate_n, review_n, monitor_n],
            textposition="outside"
        ))
        fig2.update_layout(
            title="23 Confirmed Fraud Contracts — Detection Breakdown",
            yaxis_title="Number of Contracts",
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Score Distribution — Fraud vs Clean")
    fig3 = px.histogram(
        scored, x="composite_score", color="fraud_label",
        nbins=30,
        color_discrete_map={0: "#388e3c", 1: "#d32f2f"},
        labels={"fraud_label": "Fraud", "composite_score": "Composite Risk Score"},
        title="Risk Score Distribution"
    )
    fig3.add_vline(x=50, line_dash="dash", line_color="#d32f2f", annotation_text="ESCALATE threshold")
    fig3.add_vline(x=35, line_dash="dash", line_color="#f9a825", annotation_text="REVIEW threshold")
    st.plotly_chart(fig3, use_container_width=True)

# ── PAGE 2: FLAGGED CONTRACTS ──
elif page == "🔴 Flagged Contracts":
    st.title("🔴 Flagged Contracts")
    st.markdown("Contracts in ESCALATE and REVIEW tiers — sorted by risk score.")
    st.markdown("---")

    tier_filter = st.multiselect(
        "Filter by tier:",
        options=["🔴 ESCALATE", "🟡 REVIEW", "🟢 MONITOR"],
        default=["🔴 ESCALATE", "🟡 REVIEW"]
    )

    filtered = scored[scored["tier"].isin(tier_filter)].sort_values("composite_score", ascending=False)
    st.markdown(f"**{len(filtered)} contracts shown**")
    st.dataframe(
        filtered[["entity", "supplier", "composite_score", "tier", "fraud_label"]].reset_index(drop=True),
        use_container_width=True
    )

# ── PAGE 3: ENTITY SCORECARDS ──
elif page == "🏛️ Entity Scorecards":
    st.title("🏛️ Entity Integrity Scorecards")
    st.markdown("Search any procurement entity and see their full risk profile.")
    st.markdown("---")

    entity_list = sorted(scored["entity"].unique())
    selected_entity = st.selectbox("Select an entity:", entity_list)

    entity_contracts = scored[scored["entity"] == selected_entity]
    max_score = entity_contracts["composite_score"].max()
    fraud_count = entity_contracts["fraud_label"].sum()
    total = len(entity_contracts)
    escalate_count = len(entity_contracts[entity_contracts["tier"] == "🔴 ESCALATE"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Contracts", total)
    col2.metric("Max Risk Score", f"{max_score:.1f}")
    col3.metric("Confirmed Fraud", int(fraud_count))
    col4.metric("Escalated", escalate_count)

    st.markdown("---")
    st.markdown("### All contracts for this entity:")
    st.dataframe(
        entity_contracts[["supplier", "composite_score", "tier", "fraud_label"]]
        .sort_values("composite_score", ascending=False)
        .reset_index(drop=True),
        use_container_width=True
    )

# ── PAGE 4: CONTRACT DEEP DIVE ──
elif page == "🔍 Contract Deep Dive":
    st.title("🔍 Contract Deep Dive")
    st.markdown("Select any contract for a full risk breakdown.")
    st.markdown("---")

    contract_idx = st.selectbox(
        "Select contract:",
        options=scored.index.tolist(),
        format_func=lambda i: f"#{i} — {scored.loc[i, 'entity'][:50]} | Score: {scored.loc[i, 'composite_score']}"
    )

    row = scored.loc[contract_idx]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Entity:** {row['entity']}")
        st.markdown(f"**Supplier:** {row['supplier']}")
        st.markdown(f"**Composite Score:** {row['composite_score']}")
        st.markdown(f"**Tier:** {row['tier']}")
        st.markdown(f"**Fraud Confirmed:** {'✅ Yes' if row['fraud_label'] == 1 else '⬜ No'}")

    with col2:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=row["composite_score"],
            title={"text": "Risk Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#d32f2f" if row["composite_score"] >= 50 else "#f9a825" if row["composite_score"] >= 35 else "#388e3c"},
                "steps": [
                    {"range": [0, 35], "color": "#e8f5e9"},
                    {"range": [35, 50], "color": "#fff9c4"},
                    {"range": [50, 100], "color": "#ffebee"}
                ],
                "threshold": {"line": {"color": "black", "width": 4}, "thickness": 0.75, "value": row["composite_score"]}
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### Flags raised:")
    flags = parse_list(row["flags"])
    if flags:
        for f in flags:
            st.markdown(f"• {f}")
    else:
        st.markdown("No flags raised.")

    st.markdown("### Legal citations:")
    citations = parse_list(row["legal_citations"])
    if citations:
        for c in citations:
            st.markdown(f"• {c}")
    else:
        st.markdown("No citations.")

    st.markdown("### Top SHAP drivers:")
    shap_items = parse_list(row["shap_top3"])
    if shap_items:
        for s in shap_items:
            st.markdown(f"• {s}")
    else:
        st.markdown("No SHAP data.")
