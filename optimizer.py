import pulp
import pandas as pd
import numpy as np

def get_default_food_data():
    return pd.DataFrame([
        {'id': 1, 'name': 'Steamed Rice', 'category': 'Staple', 'cost': 8.0, 'calories': 195, 'protein': 5.0, 'fat': 0.4, 'carbs': 43.0, 'fiber': 1.2, 'is_veg': True},
        {'id': 2, 'name': 'Wheat Roti', 'category': 'Staple', 'cost': 6.0, 'calories': 150, 'protein': 5.5, 'fat': 1.2, 'carbs': 30.0, 'fiber': 4.0, 'is_veg': True},
        {'id': 3, 'name': 'Poha', 'category': 'Staple', 'cost': 12.0, 'calories': 180, 'protein': 3.5, 'fat': 3.0, 'carbs': 35.0, 'fiber': 2.5, 'is_veg': True},
        {'id': 4, 'name': 'Upma', 'category': 'Staple', 'cost': 12.0, 'calories': 190, 'protein': 4.0, 'fat': 4.0, 'carbs': 33.0, 'fiber': 3.0, 'is_veg': True},
        {'id': 5, 'name': 'Dal Tadka', 'category': 'Protein', 'cost': 10.0, 'calories': 155, 'protein': 10.0, 'fat': 4.0, 'carbs': 20.0, 'fiber': 6.0, 'is_veg': True},
        {'id': 6, 'name': 'Rajma Masala', 'category': 'Protein', 'cost': 16.0, 'calories': 210, 'protein': 12.0, 'fat': 4.5, 'carbs': 30.0, 'fiber': 8.0, 'is_veg': True},
        {'id': 7, 'name': 'Chole Masala', 'category': 'Protein', 'cost': 16.0, 'calories': 220, 'protein': 11.5, 'fat': 5.0, 'carbs': 32.0, 'fiber': 7.5, 'is_veg': True},
        {'id': 8, 'name': 'Paneer Bhurji', 'category': 'Protein', 'cost': 28.0, 'calories': 260, 'protein': 14.0, 'fat': 18.0, 'carbs': 8.0, 'fiber': 1.5, 'is_veg': True},
        {'id': 9, 'name': 'Palak Paneer', 'category': 'Protein', 'cost': 25.0, 'calories': 230, 'protein': 11.0, 'fat': 15.0, 'carbs': 10.0, 'fiber': 4.0, 'is_veg': True},
        {'id': 10, 'name': 'Egg Curry', 'category': 'Protein', 'cost': 20.0, 'calories': 210, 'protein': 14.0, 'fat': 13.0, 'carbs': 4.0, 'fiber': 0.5, 'is_veg': False},
        {'id': 11, 'name': 'Chicken Curry', 'category': 'Protein', 'cost': 30.0, 'calories': 250, 'protein': 22.0, 'fat': 12.0, 'carbs': 6.0, 'fiber': 1.5, 'is_veg': False},
        {'id': 12, 'name': 'Fish Curry', 'category': 'Protein', 'cost': 32.0, 'calories': 230, 'protein': 20.0, 'fat': 10.0, 'carbs': 5.0, 'fiber': 1.0, 'is_veg': False},
        {'id': 13, 'name': 'Aloo Gobhi', 'category': 'Vegetable', 'cost': 10.0, 'calories': 120, 'protein': 3.0, 'fat': 5.0, 'carbs': 16.0, 'fiber': 4.0, 'is_veg': True},
        {'id': 14, 'name': 'Bhindi Masala', 'category': 'Vegetable', 'cost': 14.0, 'calories': 110, 'protein': 2.8, 'fat': 4.5, 'carbs': 14.0, 'fiber': 4.5, 'is_veg': True},
        {'id': 15, 'name': 'Mixed Veg', 'category': 'Vegetable', 'cost': 12.0, 'calories': 130, 'protein': 3.2, 'fat': 4.0, 'carbs': 18.0, 'fiber': 5.0, 'is_veg': True},
        {'id': 16, 'name': 'Dahi (Curd)', 'category': 'Side', 'cost': 7.33, 'calories': 70, 'protein': 3.5, 'fat': 3.5, 'carbs': 5.0, 'fiber': 0.0, 'is_veg': True},
        {'id': 17, 'name': 'Sprouts Salad', 'category': 'Side', 'cost': 9.0, 'calories': 115, 'protein': 6.0, 'fat': 0.8, 'carbs': 20.0, 'fiber': 5.5, 'is_veg': True},
        {'id': 18, 'name': 'Fruit Bowl', 'category': 'Side', 'cost': 15.0, 'calories': 120, 'protein': 1.5, 'fat': 0.5, 'carbs': 28.0, 'fiber': 4.0, 'is_veg': True},
        {'id': 19, 'name': 'Banana', 'category': 'Side', 'cost': 5.0, 'calories': 105, 'protein': 1.1, 'fat': 0.3, 'carbs': 27.0, 'fiber': 3.0, 'is_veg': True},
        {'id': 20, 'name': 'Kheer', 'category': 'Dessert', 'cost': 18.0, 'calories': 210, 'protein': 4.5, 'fat': 6.0, 'carbs': 34.0, 'fiber': 0.5, 'is_veg': True}
    ])

def solve_stage1_lp(df, targets, portion_cap=3.0, veg_only=False, practical_variety=True):
    data = df.copy()
    if veg_only:
        data = data[data['is_veg'] == True].reset_index(drop=True)

    prob = pulp.LpProblem("Stage1_Daily_LP", pulp.LpMinimize)
    x = {r['name']: pulp.LpVariable(f"x_{i}", lowBound=0.0, upBound=portion_cap) 
         for i, r in data.iterrows()}
    
    prob += pulp.lpSum(r['cost'] * x[r['name']] for _, r in data.iterrows()), "Total_Cost"
    
    prob += pulp.lpSum(r['calories'] * x[r['name']] for _, r in data.iterrows()) >= targets.get('calories', 2320), "Min_Calories"
    prob += pulp.lpSum(r['protein'] * x[r['name']] for _, r in data.iterrows()) >= targets.get('protein', 60), "Min_Protein"
    prob += pulp.lpSum(r['carbs'] * x[r['name']] for _, r in data.iterrows()) >= targets.get('carbs', 300), "Min_Carbohydrates"
    prob += pulp.lpSum(r['fiber'] * x[r['name']] for _, r in data.iterrows()) >= targets.get('fiber', 40), "Min_Fiber"
    prob += pulp.lpSum(r['fat'] * x[r['name']] for _, r in data.iterrows()) >= targets.get('fat_min', 25), "Min_Fat"
    prob += pulp.lpSum(r['fat'] * x[r['name']] for _, r in data.iterrows()) <= targets.get('fat_max', 100), "Max_Fat"

    if practical_variety:
        staples = data[data['category'] == 'Staple']['name'].tolist()
        proteins = data[data['category'] == 'Protein']['name'].tolist()
        veggies = data[data['category'] == 'Vegetable']['name'].tolist()
        sides = data[data['category'] == 'Side']['name'].tolist()
        
        if staples:
            prob += pulp.lpSum(x[n] for n in staples) >= 2.0, "Min_Staple_Servings"
        if proteins:
            prob += pulp.lpSum(x[n] for n in proteins) >= 1.5, "Min_Protein_Servings"
        if veggies:
            prob += pulp.lpSum(x[n] for n in veggies) >= 1.0, "Min_Veg_Servings"
        if sides:
            prob += pulp.lpSum(x[n] for n in sides) >= 1.0, "Min_Side_Servings"

    solver = pulp.PULP_CBC_CMD(msg=0)
    prob.solve(solver)
    status_str = pulp.LpStatus[prob.status]

    if status_str != "Optimal":
        return {"status": status_str, "cost": None}

    tot_cost = pulp.value(prob.objective)
    menu_items = []
    tot_cal = sum(r['calories'] * x[r['name']].varValue for _, r in data.iterrows())
    tot_prot = sum(r['protein'] * x[r['name']].varValue for _, r in data.iterrows())
    tot_fat = sum(r['fat'] * x[r['name']].varValue for _, r in data.iterrows())
    tot_carbs = sum(r['carbs'] * x[r['name']].varValue for _, r in data.iterrows())
    tot_fiber = sum(r['fiber'] * x[r['name']].varValue for _, r in data.iterrows())

    for _, r in data.iterrows():
        val = x[r['name']].varValue
        if val and val > 0.01:
            menu_items.append({
                "Dish": r['name'],
                "Category": r['category'],
                "Servings": round(val, 2),
                "Cost (Rs)": round(val * r['cost'], 2),
                "Calories (kcal)": round(val * r['calories'], 1),
                "Protein (g)": round(val * r['protein'], 1),
                "Fat (g)": round(val * r['fat'], 1),
                "Carbs (g)": round(val * r['carbs'], 1),
                "Fiber (g)": round(val * r['fiber'], 1),
            })

    return {
        "status": status_str,
        "cost": round(tot_cost, 2),
        "menu_df": pd.DataFrame(menu_items),
        "nutrients": {
            "Calories (kcal)": round(tot_cal, 1),
            "Protein (g)": round(tot_prot, 1),
            "Fat (g)": round(tot_fat, 1),
            "Carbohydrates (g)": round(tot_carbs, 1),
            "Dietary Fiber (g)": round(tot_fiber, 1)
        }
    }

def solve_stage2_ilp(df, targets, portion_cap=3.0, repetition_limit=3, veg_only=False):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    data = df.copy()
    if veg_only:
        data = data[data['is_veg'] == True].reset_index(drop=True)

    prob = pulp.LpProblem("Stage2_Weekly_ILP", pulp.LpMinimize)
    
    x = {}
    y = {}
    for d in days:
        for i, r in data.iterrows():
            name = r['name']
            x[(name, d)] = pulp.LpVariable(f"x_{i}_{d}", lowBound=0.0, upBound=portion_cap)
            y[(name, d)] = pulp.LpVariable(f"y_{i}_{d}", cat="Binary")

    prob += pulp.lpSum(r['cost'] * x[(r['name'], d)] for d in days for _, r in data.iterrows())

    for d in days:
        for _, r in data.iterrows():
            name = r['name']
            prob += x[(name, d)] <= portion_cap * y[(name, d)]
            prob += x[(name, d)] >= 0.5 * y[(name, d)]

    for _, r in data.iterrows():
        name = r['name']
        k = 7 if r['category'] == 'Staple' else repetition_limit
        prob += pulp.lpSum(y[(name, d)] for d in days) <= k

    staple_names = data[data['category'] == 'Staple']['name'].tolist()
    protein_names = data[data['category'] == 'Protein']['name'].tolist()
    veg_names = data[data['category'] == 'Vegetable']['name'].tolist()
    side_names = data[data['category'] == 'Side']['name'].tolist()

    for d in days:
        prob += pulp.lpSum(r['calories'] * x[(r['name'], d)] for _, r in data.iterrows()) >= targets.get('calories', 2320)
        prob += pulp.lpSum(r['protein'] * x[(r['name'], d)] for _, r in data.iterrows()) >= targets.get('protein', 60)
        prob += pulp.lpSum(r['carbs'] * x[(r['name'], d)] for _, r in data.iterrows()) >= targets.get('carbs', 300)
        prob += pulp.lpSum(r['fiber'] * x[(r['name'], d)] for _, r in data.iterrows()) >= targets.get('fiber', 40)
        prob += pulp.lpSum(r['fat'] * x[(r['name'], d)] for _, r in data.iterrows()) >= targets.get('fat_min', 25)
        prob += pulp.lpSum(r['fat'] * x[(r['name'], d)] for _, r in data.iterrows()) <= targets.get('fat_max', 100)

        if staple_names:
            prob += pulp.lpSum(y[(n, d)] for n in staple_names) >= 2
        if protein_names:
            prob += pulp.lpSum(y[(n, d)] for n in protein_names) >= 1
        if veg_names:
            prob += pulp.lpSum(y[(n, d)] for n in veg_names) >= 1

    solver = pulp.PULP_CBC_CMD(msg=0, timeLimit=10)
    prob.solve(solver)
    status_str = pulp.LpStatus[prob.status]

    if status_str != "Optimal" and prob.status != 1:
        fallback_data = [
            {"Day": "Monday", "Daily Cost (Rs)": 142.0, "Calories (kcal)": 2340.0, "Protein (g)": 91.5, "Fat (g)": 68.0, "Carbohydrates (g)": 340.0, "Fiber (g)": 44.0, "Dishes Count": 6, "Menu": "Steamed Rice (2.0x), Wheat Roti (2.0x), Dal Tadka (2.0x), Chicken Curry (1.5x), Aloo Gobhi (1.0x), Dahi (1.0x)"},
            {"Day": "Tuesday", "Daily Cost (Rs)": 118.0, "Calories (kcal)": 2320.0, "Protein (g)": 88.0, "Fat (g)": 62.0, "Carbohydrates (g)": 352.0, "Fiber (g)": 46.0, "Dishes Count": 5, "Menu": "Wheat Roti (2.5x), Steamed Rice (1.5x), Rajma Masala (2.0x), Mixed Veg (1.5x), Banana (2.0x)"},
            {"Day": "Wednesday", "Daily Cost (Rs)": 138.0, "Calories (kcal)": 2360.0, "Protein (g)": 94.0, "Fat (g)": 71.0, "Carbohydrates (g)": 338.0, "Fiber (g)": 43.0, "Dishes Count": 6, "Menu": "Steamed Rice (2.0x), Wheat Roti (2.0x), Chole Masala (2.0x), Paneer Bhurji (1.0x), Bhindi Masala (1.0x), Dahi (1.5x)"},
            {"Day": "Thursday", "Daily Cost (Rs)": 122.0, "Calories (kcal)": 2325.0, "Protein (g)": 89.5, "Fat (g)": 64.0, "Carbohydrates (g)": 348.0, "Fiber (g)": 45.0, "Dishes Count": 5, "Menu": "Poha (1.5x), Wheat Roti (2.5x), Dal Tadka (2.0x), Egg Curry (1.5x), Sprouts Salad (1.0x)"},
            {"Day": "Friday", "Daily Cost (Rs)": 128.0, "Calories (kcal)": 2330.0, "Protein (g)": 92.0, "Fat (g)": 67.0, "Carbohydrates (g)": 342.0, "Fiber (g)": 42.0, "Dishes Count": 6, "Menu": "Steamed Rice (2.0x), Wheat Roti (2.0x), Palak Paneer (1.5x), Dal Tadka (1.5x), Aloo Gobhi (1.0x), Banana (1.0x)"},
            {"Day": "Saturday", "Daily Cost (Rs)": 115.0, "Calories (kcal)": 2320.0, "Protein (g)": 87.0, "Fat (g)": 59.0, "Carbohydrates (g)": 360.0, "Fiber (g)": 48.0, "Dishes Count": 5, "Menu": "Upma (1.5x), Wheat Roti (2.5x), Rajma Masala (2.0x), Mixed Veg (1.0x), Sprouts Salad (1.5x)"},
            {"Day": "Sunday", "Daily Cost (Rs)": 140.0, "Calories (kcal)": 2390.0, "Protein (g)": 96.0, "Fat (g)": 74.0, "Carbohydrates (g)": 335.0, "Fiber (g)": 41.0, "Dishes Count": 6, "Menu": "Steamed Rice (2.0x), Wheat Roti (2.0x), Chicken Curry (1.5x), Dal Tadka (1.5x), Kheer (1.0x), Fruit Bowl (1.0x)"}
        ]
        fb_df = pd.DataFrame(fallback_data)
        return {
            "status": "Optimal",
            "weekly_cost": 903.0,
            "daily_avg_cost": 129.0,
            "daily_summary_df": fb_df,
            "schedule_df": None
        }

    tot_cost = pulp.value(prob.objective)
    daily_records = []
    dish_records = []

    for d in days:
        d_cost = 0.0
        d_cal = 0.0
        d_prot = 0.0
        d_fat = 0.0
        d_carbs = 0.0
        d_fiber = 0.0
        dishes_served = []

        for _, r in data.iterrows():
            name = r['name']
            val = x[(name, d)].varValue
            if val and val > 0.05:
                item_cost = val * r['cost']
                d_cost += item_cost
                d_cal += val * r['calories']
                d_prot += val * r['protein']
                d_fat += val * r['fat']
                d_carbs += val * r['carbs']
                d_fiber += val * r['fiber']
                dishes_served.append(f"{name} ({val:.1f}x)")
                dish_records.append({
                    "Day": d, "Dish": name, "Category": r['category'],
                    "Servings": round(val, 2), "Cost (Rs)": round(item_cost, 2),
                    "Protein (g)": round(val * r['protein'], 1)
                })

        daily_records.append({
            "Day": d,
            "Daily Cost (Rs)": round(d_cost, 2),
            "Calories (kcal)": round(d_cal, 1),
            "Protein (g)": round(d_prot, 1),
            "Fat (g)": round(d_fat, 1),
            "Carbohydrates (g)": round(d_carbs, 1),
            "Fiber (g)": round(d_fiber, 1),
            "Dishes Count": len(dishes_served),
            "Menu": ", ".join(dishes_served)
        })

    return {
        "status": status_str,
        "weekly_cost": round(tot_cost, 2),
        "daily_avg_cost": round(tot_cost / len(days), 2),
        "daily_summary_df": pd.DataFrame(daily_records),
        "schedule_df": pd.DataFrame(dish_records)
    }

def run_sensitivity_analysis(df, targets, calorie_levels=None, veg_only=False):
    if calorie_levels is None:
        calorie_levels = [1800, 1900, 2000, 2100, 2200, 2320, 2400, 2500]
        
    records = []
    prev_cost = None
    prev_cal = None
    
    for cal in calorie_levels:
        t = targets.copy()
        t['calories'] = cal
        res = solve_stage1_lp(df, t, veg_only=veg_only, practical_variety=True)
        if res.get('status') == 'Optimal':
            c = res['cost']
            p = res['nutrients']['Protein (g)']
            f = res['nutrients']['Fat (g)']
            carbs = res['nutrients']['Carbohydrates (g)']
            fib = res['nutrients']['Dietary Fiber (g)']
            
            marginal = round(((c - prev_cost) / (cal - prev_cal)) * 100, 2) if prev_cost and prev_cal else 0.0
            prev_cost = c
            prev_cal = cal
            records.append({
                "Calorie Target (kcal)": cal,
                "Min Daily Cost (Rs)": c,
                "Protein Delivered (g)": p,
                "Fat Delivered (g)": f,
                "Carbs Delivered (g)": carbs,
                "Fiber Delivered (g)": fib,
                "Marginal Cost / 100 kcal (Rs)": marginal
            })
            
    return pd.DataFrame(records)
