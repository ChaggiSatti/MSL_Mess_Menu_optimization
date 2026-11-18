# Mess Menu Optimisation Platform (MSL304: Managing Operations)

An interactive decision-support tool using **Two-Stage Mathematical Programming (Linear & Integer Linear Programming)** with the **PuLP CBC Solver** to generate cost-optimal, variety-aware, and nutritionally balanced mess menus for student hostels.

---

## Authors & Course
- **Sahil Raj** (2024EE10550)
- **Aditya Vikram** (2024ME21122)
- **Ayush Lekurwale** (2023MT10087)
- **Course**: MSL304: Managing Operations, IIT Delhi

---

## Features
1. **Executive Impact Summary**:
   - Compare manual menu (₹155/day) vs optimised roster (₹129/day).
   - Dynamic annual savings calculator: **₹39 Lakhs/year** for 500 students.
   - Guaranteed ICMR 2020 RDA nutritional compliance (2,320 kcal, 93g protein).

2. **Stage 1 (Continuous LP)**:
   - Solves the single-day minimum cost baseline in `< 0.05 seconds`.
   - Category cost breakdown and nutrient fulfillment gauges.

3. **Stage 2 (7-Day ILP Variety Roster)**:
   - 140 binary decision variables ($y_{id}$) ensuring no dish repeats more than 3 times a week.
   - Daily nutritional targets and food-group coverage satisfied every day.
   - Interactive daily cost distribution (Mon–Sun).
   - One-click export to CSV.

4. **Sensitivity Analysis**:
   - Interactive Calorie vs Cost curve (1,800 to 2,500 kcal).
   - Computes shadow prices / marginal cost per 100 kcal (~₹7/100 kcal).

5. **Live Food Database & Wholesale Price Editor**:
   - Interactive data table of 20 Indian mess dishes based on NIN (2016) values.
   - Customisable wholesale prices and vegetarian filters.

---

## How to Run

### Method 1: Double-click launcher
Double-click `run_app.bat` inside `G:\mess_menu_optimizer\`.

### Method 2: Command Line
```bash
cd G:\mess_menu_optimizer
streamlit run app.py
```
Then open `http://localhost:8501` in your browser.

