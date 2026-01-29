import gekko
m = gekko.GEKKO()

x1 = m.Var(value=0, lb=0, name='x1')
x2 = m.Var(value=0, lb=0, name='x2')
x3 = m.Var(value=0, lb=0, name='x3')

def calculate_FonctionX(x1, x2, x3):
  # Ecrire ici la fonction objective
  #===========================================================
    return 4*x1**2 + 2*x2**2 - x3**2 + 2*x1*x3 - 2*x1 + 5*x2
  #===========================================================

variables = [x1, x2, x3]

# Contraintes du problème à écrire ici :
#=============================================================
m.Equation(x1 + x2 + x3 == 4)
m.Equation(2*x1**2 + x1*x2 == 2)
m.Equation(x1 + 2*x2 == 6)
#=============================================================

# Changer en fonction du problème à minimiser (Minimize) /
# maximiser (Maximize) :
#=============================================================
m.Minimize(calculate_FonctionX(x1, x2, x3))
#=============================================================

m.solve(disp=False)

print("="*80)
print('Valeurs des variables minimisées')
print("="*80)

for var in variables:
    print(f'{var.name} = {var.value[0]}')

x1 = x1.value[0]
x2 = x2.value[0]
x3 = x3.value[0]

FonctionX = calculate_FonctionX(x1, x2, x3)

print("="*80)
print('Fonction minimisée avec les variables')
print("="*80)
print(f'f(x) = {FonctionX}')