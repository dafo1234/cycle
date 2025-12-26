import streamlit as st
import math
from collections import Counter

# Configuration de la page
st.set_page_config(page_title="Décomposition en facteurs premiers", layout="centered")

st.title("Décomposition d'un entier en facteurs premiers")
st.write("Saisissez un entier et obtenez sa décomposition en produit de nombres premiers.")

def prime_factors(n: int):
    """Retourne la liste des facteurs premiers de n (avec répétitions)."""
    factors = []
    # Gestion des signes
    if n < 0:
        factors.append(-1)
        n = -n
    # Gestion des cas particuliers
    if n in (0, 1):
        return factors

    # Extraire les facteurs 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Extraire les facteurs impairs
    f = 3
    while f * f <= n:
        while n % f == 0:
            factors.append(f)
            n //= f
        f += 2

    # Si il reste un facteur premier > 1
    if n > 1:
        factors.append(n)

    return factors

def factors_to_string(factors):
    """Produit sous forme a × b × c."""
    if not factors:
        return "—"
    return " × ".join(str(x) for x in factors)

def factors_to_powers(factors):
    """Forme canonique avec puissances, ex: 2^3 × 3 × 5."""
    if not factors:
        return "—"
    counts = Counter(factors)
    # Placer -1 en tête s'il existe, puis trier le reste
    parts = []
    if counts.get(-1):
        parts.append("-1")
        del counts[-1]
    for p in sorted(counts):
        exp = counts[p]
        parts.append(f"{p}^{exp}" if exp > 1 else f"{p}")
    return " × ".join(parts)

# Entrée utilisateur
n = st.number_input(
    "Entier à décomposer",
    min_value=-10**9,
    max_value=10**9,
    step=1,
    format="%d",
    help="Entrez un entier entre −10^9 et 10^9."
)

if st.button("Décomposer"):
    # Cas particuliers
    if n == 0:
        st.info("0 n'a pas de décomposition en facteurs premiers (tout nombre divise 0).")
    elif n == 1:
        st.info("1 n'a pas de facteurs premiers (par convention).")
    else:
        factors = prime_factors(int(n))
        produit = factors_to_string(factors)
        puissances = factors_to_powers(factors)

        st.subheader("Résultat")
        st.write(f"**Nombre saisi:** {int(n)}")
        st.write(f"**Produit de facteurs:** {produit}")
        st.write(f"**Forme avec puissances:** {puissances}")

        # Petite visualisation des multiplicité des facteurs (hors -1)
        counts = Counter([f for f in factors if f != -1])
        if counts:
            st.subheader("Multiplicités des facteurs")
            # Conversion pour un bar chart simple
            chart_data = {
                "Facteur": list(map(str, sorted(counts.keys()))),
                "Multiplicité": [counts[k] for k in sorted(counts.keys())],
            }
            st.bar_chart(chart_data, x="Facteur", y="Multiplicité")
