import streamlit as st
import gekko
import numpy as np
import pandas as pd
import traceback

st.set_page_config(
    page_title="Solveur d'Optimisation GEKKO",
    layout="wide"
)

st.title("Solveur d'Optimisation Non Linéaire")
st.markdown("*Résolvez vos problèmes d'optimisation avec GEKKO*")

# Sidebar pour les exemples
with st.sidebar:
    st.header("Exemples prédéfinis")

    exemple = st.selectbox(
        "Choisir un exemple:",
        ["Personnalisé", "Exemple 1 (cours)", "Exemple 2 (simple)", "Exemple 3 (complexe)"]
    )

    st.markdown("---")
    st.markdown("### Syntaxe")
    st.markdown("""
    **Variables:** `x1`, `x2`, `x3`, ...

    **Opérateurs:**
    - Addition: `+`
    - Soustraction: `-`
    - Multiplication: `*`
    - Division: `/`
    - Puissance: `**`

    **Exemples:**
    - `2*x1**2 + x2`
    - `x1*x2 - 4*x1`
    - `x1**2 + 5*x2`
    """)

# Charger les exemples
if exemple == "Exemple 1 (cours)":
    default_vars = 3
    default_obj = "2*x1**2 + 2*x2**2 + x3**2 - 2*x1*x2 - 4*x1 - 6*x2"
    default_constraints = ["x1 + x2 + x3 == 2", "x1**2 + 5*x2 == 5"]
    default_bounds = [(0, None), (0, None), (0, None)]
    default_type = "Minimiser"
elif exemple == "Exemple 2 (simple)":
    default_vars = 2
    default_obj = "(x1-3)**2 + (x2-2)**2"
    default_constraints = ["x1 + x2 <= 5"]
    default_bounds = [(0, None), (0, None)]
    default_type = "Minimiser"
elif exemple == "Exemple 3 (complexe)":
    default_vars = 3
    default_obj = "4*x1**2 + 2*x2**2 - x3**2 + 2*x1*x3 - 2*x1 + 5*x2"
    default_constraints = ["x1 + x2 + x3 == 4", "2*x1**2 + x1*x2 == 2", "x1 + 2*x2 == 6"]
    default_bounds = [(0, None), (0, None), (0, None)]
    default_type = "Minimiser"
else:
    default_vars = 3
    default_obj = "x1**2 + x2**2 + x3**2"
    default_constraints = ["x1 + x2 + x3 == 1"]
    default_bounds = [(0, None), (0, None), (0, None)]
    default_type = "Minimiser"

# Configuration du problème
st.header("Configuration du problème")

col1, col2 = st.columns([1, 1])

with col1:
    num_vars = st.number_input(
        "Nombre de variables",
        min_value=1,
        max_value=10,
        value=default_vars,
        help="Nombre de variables de décision (x1, x2, ...)"
    )

    obj_type = st.radio(
        "Type d'optimisation",
        ["Minimiser", "Maximiser"],
        index=0 if default_type == "Minimiser" else 1,
        horizontal=True
    )

with col2:
    st.markdown("### Variables disponibles")
    vars_display = ", ".join([f"x{i + 1}" for i in range(num_vars)])
    st.info(f"{vars_display}")

# Fonction objective
st.markdown("### Fonction objective")
objective_function = st.text_area(
    f"Fonction à {obj_type.lower()}:",
    value=default_obj,
    height=80,
    help="Entrez votre fonction objective en utilisant x1, x2, x3, etc."
)

# Contraintes
st.markdown("### Contraintes")

num_constraints = st.number_input(
    "Nombre de contraintes",
    min_value=0,
    max_value=20,
    value=len(default_constraints),
    help="Nombre de contraintes d'égalité ou d'inégalité"
)

constraints = []
for i in range(num_constraints):
    default_val = default_constraints[i] if i < len(default_constraints) else ""
    constraint = st.text_input(
        f"Contrainte {i + 1}",
        value=default_val,
        help="Format: expression == valeur, expression <= valeur, ou expression >= valeur"
    )
    if constraint:
        constraints.append(constraint)

# Bornes des variables
st.markdown("### Bornes des variables")

with st.expander("Configurer les bornes (optionnel)"):
    bounds = []
    cols = st.columns(num_vars)

    for i in range(num_vars):
        with cols[i]:
            st.markdown(f"**x{i + 1}**")

            lower_bound = st.number_input(
                f"Min x{i + 1}",
                value=float(default_bounds[i][0]) if default_bounds[i][0] is not None else 0.0,
                key=f"lb_{i}"
            )

            use_upper = st.checkbox(f"Max x{i + 1}", key=f"ub_check_{i}")

            if use_upper:
                upper_bound = st.number_input(
                    f"Valeur max x{i + 1}",
                    value=10.0,
                    key=f"ub_{i}"
                )
                bounds.append((lower_bound, upper_bound))
            else:
                bounds.append((lower_bound, None))

# Bouton de résolution
st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    solve_button = st.button("Résoudre", type="primary", use_container_width=True)

if solve_button:
    try:
        with st.spinner("Résolution en cours..."):
            # Créer le modèle GEKKO
            m = gekko.GEKKO(remote=False)
            m.options.SOLVER = 3  # IPOPT

            # Créer les variables
            variables = []
            for i in range(num_vars):
                lb = bounds[i][0] if i < len(bounds) else 0
                ub = bounds[i][1] if i < len(bounds) and bounds[i][1] is not None else None

                if ub is not None:
                    var = m.Var(value=lb, lb=lb, ub=ub, name=f'x{i + 1}')
                else:
                    var = m.Var(value=lb, lb=lb, name=f'x{i + 1}')
                variables.append(var)

            # Créer un dictionnaire pour l'évaluation
            var_dict = {f'x{i + 1}': variables[i] for i in range(num_vars)}

            # Définir la fonction objective
            obj_expr = eval(objective_function, {"__builtins__": {}}, var_dict)

            # Ajouter les contraintes
            for constraint in constraints:
                if '==' in constraint:
                    left, right = constraint.split('==')
                    left_expr = eval(left.strip(), {"__builtins__": {}}, var_dict)
                    right_val = eval(right.strip(), {"__builtins__": {}}, var_dict)
                    m.Equation(left_expr == right_val)
                elif '<=' in constraint:
                    left, right = constraint.split('<=')
                    left_expr = eval(left.strip(), {"__builtins__": {}}, var_dict)
                    right_val = eval(right.strip(), {"__builtins__": {}}, var_dict)
                    m.Equation(left_expr <= right_val)
                elif '>=' in constraint:
                    left, right = constraint.split('>=')
                    left_expr = eval(left.strip(), {"__builtins__": {}}, var_dict)
                    right_val = eval(right.strip(), {"__builtins__": {}}, var_dict)
                    m.Equation(left_expr >= right_val)

            # Optimiser
            if obj_type == "Minimiser":
                m.Minimize(obj_expr)
            else:
                m.Maximize(obj_expr)

            # Résoudre
            m.solve(disp=False)

            # Afficher les résultats
            st.success("Problème résolu avec succès!")

            st.markdown("---")
            st.header("Résultats")

            # Tableau des variables
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("### Valeurs des variables")

                results_data = []
                for i, var in enumerate(variables):
                    results_data.append({
                        "Variable": f"x{i + 1}",
                        "Valeur": f"{var.value[0]:.6f}"
                    })

                df_results = pd.DataFrame(results_data)
                st.dataframe(df_results, use_container_width=True, hide_index=True)

            with col2:
                st.markdown("### Fonction objective")

                # Calculer la valeur de la fonction objective
                var_values = {f'x{i + 1}': variables[i].value[0] for i in range(num_vars)}
                obj_value = eval(objective_function, {"__builtins__": {}}, var_values)

                st.metric(
                    label=f"f(x) {obj_type.lower()}ée",
                    value=f"{obj_value:.6f}"
                )

            # Vérification des contraintes
            st.markdown("### Vérification des contraintes")

            constraint_check = []
            for i, constraint in enumerate(constraints):
                try:
                    if '==' in constraint:
                        left, right = constraint.split('==')
                        left_val = eval(left.strip(), {"__builtins__": {}}, var_values)
                        right_val = eval(right.strip(), {"__builtins__": {}}, var_values)
                        satisfied = abs(left_val - right_val) < 1e-5
                        constraint_check.append({
                            "Contrainte": constraint,
                            "Gauche": f"{left_val:.6f}",
                            "Droite": f"{right_val:.6f}",
                            "Respectée": "OK" if satisfied else "Pas OK"
                        })
                    elif '<=' in constraint:
                        left, right = constraint.split('<=')
                        left_val = eval(left.strip(), {"__builtins__": {}}, var_values)
                        right_val = eval(right.strip(), {"__builtins__": {}}, var_values)
                        satisfied = left_val <= right_val + 1e-5
                        constraint_check.append({
                            "Contrainte": constraint,
                            "Gauche": f"{left_val:.6f}",
                            "Droite": f"{right_val:.6f}",
                            "Respectée": "OK" if satisfied else "Pas OK"
                        })
                    elif '>=' in constraint:
                        left, right = constraint.split('>=')
                        left_val = eval(left.strip(), {"__builtins__": {}}, var_values)
                        right_val = eval(right.strip(), {"__builtins__": {}}, var_values)
                        satisfied = left_val >= right_val - 1e-5
                        constraint_check.append({
                            "Contrainte": constraint,
                            "Gauche": f"{left_val:.6f}",
                            "Droite": f"{right_val:.6f}",
                            "Respectée": "OK" if satisfied else "Pas OK"
                        })
                except:
                    constraint_check.append({
                        "Contrainte": constraint,
                        "Gauche": "Erreur",
                        "Droite": "Erreur",
                        "Respectée": "!"
                    })

            if constraint_check:
                df_constraints = pd.DataFrame(constraint_check)
                st.dataframe(df_constraints, use_container_width=True, hide_index=True)

            # Code Python généré
            st.markdown("---")
            st.markdown("### Code Python équivalent")

            code = f"""import gekko

m = gekko.GEKKO()

# Créer les variables
"""
            for i in range(num_vars):
                lb = bounds[i][0] if i < len(bounds) else 0
                ub = bounds[i][1] if i < len(bounds) and bounds[i][1] is not None else None

                if ub is not None:
                    code += f"x{i + 1} = m.Var(value={lb}, lb={lb}, ub={ub}, name='x{i + 1}')\n"
                else:
                    code += f"x{i + 1} = m.Var(value={lb}, lb={lb}, name='x{i + 1}')\n"

            code += f"\n# Fonction objective\n"
            code += f"obj = {objective_function}\n\n"

            code += "# Contraintes\n"
            for constraint in constraints:
                code += f"m.Equation({constraint})\n"

            code += f"\n# Optimiser\n"
            if obj_type == "Minimiser":
                code += f"m.Minimize(obj)\n"
            else:
                code += f"m.Maximize(obj)\n"

            code += "\nm.solve(disp=False)\n\n"
            code += "# Afficher les résultats\n"
            for i in range(num_vars):
                code += f"print(f'x{i + 1} = {{x{i + 1}.value[0]}}')\n"

            st.code(code, language="python")

    except Exception as e:
        st.error(f"Erreur lors de la résolution: {str(e)}")
        with st.expander("Détails de l'erreur"):
            st.code(traceback.format_exc())

