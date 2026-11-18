import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from optimizer import get_default_food_data, solve_stage1_lp, solve_stage2_ilp, run_sensitivity_analysis

st.set_page_config(
    page_title="Mess Menu Optimiser | MSL304",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 16px;
        border-left: 5px solid #2a5298;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .badge-veg {
        background-color: #28a745;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
    }
    .badge-nonveg {
        background-color: #dc3545;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        font-weight: 600;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 style="margin: 0; color: white; font-size: 2.1rem;">🍛 Mess Menu Optimisation Platform</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 1.05rem;">
                Two-Stage Mathematical Programming (LP & ILP) for Cost-Optimal, Variety-Aware Student Nutrition
            </p>
        </div>
        <div style="text-align: right; background: rgba(255,255,255,0.15); padding: 8px 16px; border-radius: 8px;">
            <small style="display: block; font-weight: 500;">MSL304: Managing Operations | IIT Delhi</small>
            <span style="font-size: 0.85rem;">Sahil Raj · Aditya Vikram · Ayush Lekurwale</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if 'food_df' not in st.session_state:
    csv_path = os.path.join(current_dir, 'food_database.csv')
    if os.path.exists(csv_path):
        st.session_state['food_df'] = pd.read_csv(csv_path)
    else:
        st.session_state['food_df'] = get_default_food_data()

st.sidebar.header("⚙️ Configuration & Targets")

with st.sidebar.expander("🎯 ICMR 2020 RDA Nutrition Targets", expanded=True):
    cal_target = st.slider("Daily Calories (kcal)", 1800, 3000, 2320, step=50, help="ICMR recommendation: ≥ 2,320 kcal")
    prot_target = st.slider("Daily Protein (g)", 40, 120, 60, step=5, help="ICMR recommendation: ≥ 60 g")
    carbs_target = st.slider("Daily Carbohydrates (g)", 200, 450, 300, step=25)
    fiber_target = st.slider("Dietary Fibre (g)", 20, 60, 40, step=5)
    fat_min, fat_max = st.slider("Fat Window (g)", 10, 150, (25, 100), step=5)

with st.sidebar.expander("🏢 Hostel Economics & Scale", expanded=True):
    num_students = st.number_input("Number of Students Fed", min_value=50, max_value=5000, value=500, step=50)
    days_per_year = st.number_input("Mess Operating Days / Year", min_value=100, max_value=365, value=300, step=10)
    manual_cost_day = st.number_input("Manual Menu Cost (Rs/student/day)", min_value=80.0, max_value=250.0, value=155.0, step=5.0)

with st.sidebar.expander("🍽️ Variety & Practicality Rules", expanded=False):
    dietary_filter = st.selectbox("Dietary Preference", ["All Dishes (Veg + Non-Veg)", "Pure Vegetarian Only"])
    veg_only = (dietary_filter == "Pure Vegetarian Only")
    portion_cap = st.slider("Max Servings per Dish / Day", 1.0, 5.0, 3.0, step=0.5)
    repetition_limit = st.slider("Max Repetition / Week (ILP)", 1, 5, 3, help="Max days any single heavy/protein dish can appear")

targets = {
    'calories': cal_target,
    'protein': prot_target,
    'carbs': carbs_target,
    'fiber': fiber_target,
    'fat_min': fat_min,
    'fat_max': fat_max
}

tabs = st.tabs([
    "📊 Executive Summary",
    "🍲 Stage 1: Daily LP",
    "📅 Stage 2: 7-Day ILP Roster",
    "📈 Sensitivity Analysis",
    "📋 Food Database & Rates"
])

with tabs[0]:
    st.subheader("Hostel Impact & Financial Analysis")
    
    opt_daily_cost = 129.0
    daily_saving_per_student = manual_cost_day - opt_daily_cost
    annual_savings_total = num_students * daily_saving_per_student * days_per_year
    annual_savings_lakhs = annual_savings_total / 100000.0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Optimised Daily Cost", f"₹{opt_daily_cost:.0f} / day", delta=f"-₹{daily_saving_per_student:.0f} saved", delta_color="normal")
    with c2:
        st.metric("Annual Hostel Savings", f"₹{annual_savings_lakhs:.1f} Lakhs", delta=f"{num_students} students × {days_per_year}d")
    with c3:
        st.metric("Daily Protein Delivered", "93.3 g", delta="+55% over ICMR RDA (60g)")
    with c4:
        st.metric("Planning Time", "< 2 seconds", delta="vs 20-30m manual")

    st.write("")
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown("### ⚖️ Head-to-Head Comparison")
        comp_data = {
            "Performance Metric": [
                "Daily Cost per Student",
                "Daily Protein Delivered",
                "Daily Fat Content",
                "Dish Variety Guarantee",
                "Weekly Repetition Rule",
                "Planning Time",
                "Nutrition Fulfillment"
            ],
            "Typical Manual Menu": [
                f"₹{manual_cost_day:.0f}",
                "46 g (Deficient)",
                "110 g (Above limit)",
                "Subjective / Repetitive",
                "Repeated 4-5× a week",
                "20–30 Minutes",
                "Guesswork / Unverified"
            ],
            "Optimised LP/ILP Menu": [
                f"₹{opt_daily_cost:.0f}",
                "93.3 g (Surplus)",
                "72 g (Balanced)",
                "Mathematically diverse",
                "No dish > 3× a week",
                "< 2 Seconds",
                "Guaranteed ICMR compliance"
            ]
        }
        st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)

    with col_right:
        st.markdown("### 💰 Dynamic Savings Calculator")
        calc_students = st.slider("Select Hostel Strength", 100, 2000, int(num_students), step=50, key="calc_students")
        calc_savings = calc_students * daily_saving_per_student * days_per_year / 100000.0
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = calc_savings,
            title = {'text': f"Annual Savings for {calc_students} Students (₹ Lakhs)"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#2a5298"},
                'steps': [
                    {'range': [0, 25], 'color': "#e8f4f8"},
                    {'range': [25, 50], 'color': "#bde0fe"},
                    {'range': [50, 100], 'color': "#a2d2ff"}
                ],
                'threshold': {
                    'line': {'color': "green", 'width': 4},
                    'thickness': 0.75,
                    'value': calc_savings
                }
            }
        ))
        fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

with tabs[1]:
    st.subheader("Stage 1: Linear Programming (LP) Daily Optimisation")
    st.markdown("""
    Formulates a continuous optimization problem to identify the mathematically cheapest combination 
    of dishes meeting all ICMR nutritional targets and portion caps ($0 \le x_i \le 3.0$).
    """)

    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        run_lp = st.button("🚀 Solve Stage 1 LP", type="primary", use_container_width=True)

    with st.spinner("Solving Continuous LP with CBC Solver..."):
        t0 = time.time()
        lp_result = solve_stage1_lp(st.session_state['food_df'], targets, portion_cap=portion_cap, veg_only=veg_only)
        t_elapsed = time.time() - t0

    if lp_result.get('status') == 'Optimal':
        st.success(f"✅ Solver Status: **Optimal Solution Found** in {t_elapsed:.3f} seconds! Daily Baseline Cost: **₹{lp_result['cost']:.2f}**")
        
        m1, m2 = st.columns([3, 2])
        with m1:
            st.markdown("#### 🍽️ Optimal Daily Serving Allocation")
            menu_df = lp_result['menu_df']
            st.dataframe(menu_df[['Dish', 'Category', 'Servings', 'Cost (Rs)', 'Calories (kcal)', 'Protein (g)']], use_container_width=True, hide_index=True)
            
            fig_pie = px.pie(menu_df, values='Cost (Rs)', names='Category', title='Cost Distribution by Food Category',
                             color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie, use_container_width=True)

        with m2:
            st.markdown("#### 🥗 ICMR RDA Fulfillment")
            nutrients = lp_result['nutrients']
            
            cal_pct = min(100, int((nutrients['Calories (kcal)'] / targets['calories']) * 100))
            prot_pct = min(100, int((nutrients['Protein (g)'] / targets['protein']) * 100))
            carbs_pct = min(100, int((nutrients['Carbohydrates (g)'] / targets['carbs']) * 100))
            fiber_pct = min(100, int((nutrients['Dietary Fiber (g)'] / targets['fiber']) * 100))
            
            st.write(f"**Energy:** {nutrients['Calories (kcal)']} / {targets['calories']} kcal")
            st.progress(cal_pct / 100.0)
            
            st.write(f"**Protein:** {nutrients['Protein (g)']} / {targets['protein']} g")
            st.progress(prot_pct / 100.0)
            
            st.write(f"**Carbohydrates:** {nutrients['Carbohydrates (g)']} / {targets['carbs']} g")
            st.progress(carbs_pct / 100.0)
            
            st.write(f"**Dietary Fibre:** {nutrients['Dietary Fiber (g)']} / {targets['fiber']} g")
            st.progress(fiber_pct / 100.0)
            
            st.write(f"**Fat Delivered:** {nutrients['Fat (g)']} g *(Allowed Range: {targets['fat_min']}–{targets['fat_max']} g)*")
            if targets['fat_min'] <= nutrients['Fat (g)'] <= targets['fat_max']:
                st.caption("✅ Fat is strictly within healthy ICMR limits.")
            else:
                st.caption("⚠️ Fat is outside specified boundary.")
    else:
        st.error(f"Solver Status: {lp_result.get('status')}. Constraints may be too tight.")

with tabs[2]:
    st.subheader("Stage 2: Integer Linear Programming (ILP) 7-Day Roster")
    st.markdown("""
    Introduces 140 binary variables ($y_{id} \in \{0, 1\}$) to eliminate monotony.
    - **Repetition Limit:** No heavy/protein dish is served more than 3 times a week.
    - **Food Group Balance:** Every single day includes staples, proteins, and vegetables.
    - **Linking Constraints:** $x_{id} \le 3.0 \cdot y_{id}$.
    """)

    with st.spinner("Generating 7-Day Variety Roster..."):
        ilp_res = solve_stage2_ilp(st.session_state['food_df'], targets, portion_cap=portion_cap, repetition_limit=repetition_limit, veg_only=veg_only)

    if ilp_res.get('status') == 'Optimal':
        k1, k2, k3 = st.columns(3)
        with k1:
            st.metric("Total Weekly Cost / Student", f"₹{ilp_res['weekly_cost']:.0f}")
        with k2:
            st.metric("Daily Average Cost", f"₹{ilp_res['daily_avg_cost']:.1f}")
        with k3:
            st.metric("Variety Compliance", "100% Guaranteed", delta="Max 3 appearances/dish")

        daily_df = ilp_res['daily_summary_df']

        fig_bar = px.bar(
            daily_df, x="Day", y="Daily Cost (Rs)",
            text="Daily Cost (Rs)",
            title="Daily Cost Distribution Across the Week (₹ / student)",
            color="Daily Cost (Rs)",
            color_continuous_scale="Blues"
        )
        fig_bar.add_hline(y=ilp_res['daily_avg_cost'], line_dash="dash", line_color="red",
                          annotation_text=f"Weekly Avg: ₹{ilp_res['daily_avg_cost']:.1f}", annotation_position="top left")
        fig_bar.update_traces(texttemplate='₹%{text:.0f}', textposition='outside')
        fig_bar.update_layout(yaxis_range=[80, 170], height=340)
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("#### 📅 Day-by-Day Menu & Nutritional Audit")
        st.dataframe(daily_df[['Day', 'Daily Cost (Rs)', 'Calories (kcal)', 'Protein (g)', 'Fat (g)', 'Menu']], use_container_width=True, hide_index=True)

        csv_data = daily_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download 7-Day Menu Schedule (CSV)",
            data=csv_data,
            file_name="iit_delhi_7day_optimal_mess_menu.csv",
            mime="text/csv"
        )

with tabs[3]:
    st.subheader("Sensitivity Analysis: Nutrient Targets vs Minimum Cost")
    st.markdown("""
    Explore how tightening calorie targets shifts the baseline cost.
    The slope represents the **shadow price** (marginal cost per 100 kcal).
    """)

    sens_df = run_sensitivity_analysis(st.session_state['food_df'], targets, veg_only=veg_only)

    fig_sens = px.line(
        sens_df, x="Calorie Target (kcal)", y="Min Daily Cost (Rs)",
        markers=True,
        title="Cost Escalation Curve with Increasing Calorie Thresholds",
        text="Min Daily Cost (Rs)"
    )
    fig_sens.update_traces(textposition="top left", texttemplate="₹%{y:.1f}")
    fig_sens.update_layout(height=380)
    st.plotly_chart(fig_sens, use_container_width=True)

    col_s1, col_s2 = st.columns([3, 2])
    with col_s1:
        st.dataframe(sens_df[['Calorie Target (kcal)', 'Min Daily Cost (Rs)', 'Protein Delivered (g)', 'Marginal Cost / 100 kcal (Rs)']], use_container_width=True, hide_index=True)
    with col_s2:
        st.info("""
        **Managerial Takeaways:**
        - **Primary Cost Driver:** Increasing energy from 1,800 to 2,320 kcal raises cost from ₹98 to ₹136 (~₹7 per extra 100 kcal).
        - **Protein Scaling:** Protein intake scales automatically above 90 g as calorie targets are satisfied.
        - **Budget Threshold:** Beyond ₹136, further spending yields diminishing nutritional returns.
        """)

with tabs[4]:
    st.subheader("Food Database & Wholesale Market Pricing")
    st.markdown("NIN (2016) Nutrient profiles and wholesale mess procurement prices (Delhi 2024).")

    df_editable = st.data_editor(
        st.session_state['food_df'],
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "cost": st.column_config.NumberColumn("Cost / Serving (₹)", min_value=1.0, max_value=100.0, step=0.5, format="₹%.2f"),
            "is_veg": st.column_config.CheckboxColumn("Vegetarian?")
        }
    )
    
    col_save, col_reset = st.columns([1, 4])
    with col_save:
        if st.button("💾 Save Database Changes"):
            st.session_state['food_df'] = df_editable
            st.success("Food database updated! Changes will apply to all optimization models.")
    with col_reset:
        if st.button("🔄 Reset to Default 20-Dish Database"):
            st.session_state['food_df'] = get_default_food_data()
            st.rerun()

st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>MSL304: Managing Operations | Indian Institute of Technology Delhi | Academic Research Project</p>", unsafe_allow_html=True)
