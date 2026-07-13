import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import os
import plotly.graph_objects as go
import plotly.express as px
from dateutil.relativedelta import relativedelta

# ═══════════════════════════════════════════════════════════════
# 🎨 CONFIGURATION GÉNÉRALE
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="SEGAH-CREDIT",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Design System (harmonisé)
SG_RED = "#E60028"
SG_BLACK = "#000000"
SG_WHITE = "#FFFFFF"
SG_GRAY = "#F5F5F5"
SG_DARK_GRAY = "#333333"
SG_LIGHT_RED = "#FFF0F0"
SG_GREEN = "#10B981"
SG_ORANGE = "#F59E0B"
SG_BLUE = "#3B82F6"

APP_NAME = "SEGAH-CREDIT"
APP_VERSION = "V4.0"
USAGE_LOG_FILE = "usage_logs_churn.csv"

# ═══════════════════════════════════════════════════════════════
# 🔐 SÉCURITÉ SIMPLE PAR HASH SHA-256
# ═══════════════════════════════════════════════════════════════

def hash_password(password: str) -> str:
    """Hash un mot de passe avec SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

# Utilisateurs prédéfinis (mots de passe : voir commentaires)
USERS = {
    "admin": {
        "password_hash": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",  # admin2026
        "role": "Administrateur",
        "modules": ["salary", "loan", "admin"]
    },
    "rh": {
        "password_hash": "d3cdbaa6c5cbb1e4f64fec97a5893749b456b29b2ceda7e4e0c87a46936f8f8c",  # rh2026
        "role": "Ressources Humaines",
        "modules": ["salary"]
    },
    "credit": {
        "password_hash": "7d1b9e06b2a13184a94a9391b85f61f990b14d3454650ec429a2146dc448bea7",  # credit2026
        "role": "Analyste Crédit",
        "modules": ["loan"]
    },
}

def verify_password(username: str, password: str) -> bool:
    """Vérifie le couple identifiant/mot de passe."""
    if username not in USERS:
        return False
    return hash_password(password) == USERS[username]["password_hash"]

# ═══════════════════════════════════════════════════════════════
# 🎨 CSS GLOBAL UX/UI (fusion des deux styles)
# ═══════════════════════════════════════════════════════════════

def apply_custom_css():
    """Applique la feuille de style personnalisée."""
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');

    * {{
        font-family: 'Inter', sans-serif;
    }}

    .main {{
        background: linear-gradient(135deg, {SG_WHITE} 0%, {SG_GRAY} 100%);
        animation: fadeIn 0.7s ease-in;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}

    @keyframes slideIn {{
        from {{ transform: translateY(-20px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}

    @keyframes slideInRight {{
        from {{ transform: translateX(25px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}

    @keyframes shimmer {{
        0% {{ background-position: -1000px 0; }}
        100% {{ background-position: 1000px 0; }}
    }}

    /* --- Page de connexion --- */
    .login-shell {{
        max-width: 520px;
        margin: 50px auto;
        background: white;
        border-radius: 28px;
        padding: 44px 42px;
        box-shadow: 0 28px 90px rgba(0,0,0,0.20);
        border-top: 6px solid {SG_RED};
        animation: slideIn 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }}

    .login-shell::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -120%;
        width: 120%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(230,0,40,0.05), transparent);
        animation: shimmer 3.5s infinite;
    }}

    .login-logo {{
        text-align: center;
        font-size: 4em;
        margin-bottom: 8px;
        filter: drop-shadow(0 8px 18px rgba(230,0,40,0.25));
    }}

    .login-title {{
        text-align: center;
        color: {SG_RED};
        font-size: 2.25em;
        font-weight: 900;
        margin-bottom: 5px;
    }}

    .login-subtitle {{
        text-align: center;
        color: #666;
        margin-bottom: 30px;
        font-weight: 500;
    }}

    /* --- En-têtes --- */
    .top-hero {{
        background: linear-gradient(135deg, {SG_BLACK} 0%, {SG_RED} 100%);
        color: white;
        padding: 30px 34px;
        border-radius: 24px;
        margin-bottom: 28px;
        box-shadow: 0 14px 42px rgba(0,0,0,0.22);
        position: relative;
        overflow: hidden;
    }}

    .top-hero h1 {{
        margin: 0;
        font-size: 2em;
        font-weight: 900;
    }}

    .top-hero p {{
        margin: 10px 0 0 0;
        opacity: 0.93;
        font-size: 1.02em;
    }}

    .sg-header {{
        background: linear-gradient(135deg, {SG_BLACK} 0%, {SG_DARK_GRAY} 100%);
        color: white;
        padding: 36px;
        border-radius: 22px;
        margin-bottom: 32px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.22);
        animation: slideIn 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }}

    .sg-header::after {{
        content: '';
        position: absolute;
        right: -80px;
        top: -80px;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: rgba(230,0,40,0.25);
    }}

    .sg-header h1 {{
        margin: 0;
        font-weight: 900;
        font-size: 2.25em;
        position: relative;
        z-index: 1;
    }}

    .sg-header p {{
        margin: 12px 0 0 0;
        opacity: 0.94;
        font-size: 1.08em;
        position: relative;
        z-index: 1;
    }}

    .section-header {{
        font-size: 1.35em;
        font-weight: 900;
        color: {SG_BLACK};
        margin: 26px 0 16px 0;
        padding-bottom: 10px;
        border-bottom: 4px solid {SG_RED};
        display: inline-block;
    }}

    .section-divider {{
        height: 4px;
        background: linear-gradient(90deg, transparent, {SG_RED}, transparent);
        margin: 34px 0;
        border-radius: 8px;
    }}

    /* --- Cartes métriques --- */
    .metric-card, .kpi-card {{
        background: white;
        border-radius: 22px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.10);
        border-left: 6px solid {SG_RED};
        transition: all 0.3s ease;
        animation: slideInRight 0.55s ease-out;
        min-height: 145px;
    }}

    .metric-card:hover, .kpi-card:hover {{
        transform: translateY(-7px);
        box-shadow: 0 22px 50px rgba(230,0,40,0.20);
    }}

    .metric-label, .kpi-title {{
        color: {SG_DARK_GRAY};
        font-size: 0.82em;
        text-transform: uppercase;
        letter-spacing: 1.3px;
        font-weight: 900;
        opacity: 0.82;
    }}

    .metric-value, .kpi-number {{
        font-size: 2.05em;
        font-weight: 900;
        color: {SG_RED};
        margin: 10px 0 4px 0;
        letter-spacing: -0.8px;
    }}

    .metric-subtitle, .kpi-caption {{
        color: #666;
        font-size: 0.86em;
        margin-top: 5px;
        font-weight: 500;
    }}

    /* --- Cartes d'information --- */
    .info-card {{
        background: linear-gradient(135deg, {SG_LIGHT_RED} 0%, white 100%);
        border-radius: 18px;
        padding: 22px;
        border: 2px solid rgba(230,0,40,0.10);
        margin: 14px 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        transition: all 0.25s ease;
    }}

    .info-card:hover {{
        border-color: {SG_RED};
        box-shadow: 0 12px 28px rgba(230,0,40,0.15);
    }}

    .info-card-title {{
        font-weight: 900;
        color: {SG_RED};
        font-size: 1.06em;
        margin-bottom: 8px;
    }}

    /* --- Barres de progression --- */
    .progress-bar {{
        height: 10px;
        background: #ececec;
        border-radius: 99px;
        overflow: hidden;
        margin: 12px 0;
    }}

    .progress-fill {{
        height: 100%;
        background: linear-gradient(90deg, {SG_RED}, #FF4D4D);
        border-radius: 99px;
        transition: width 0.8s ease;
    }}

    /* --- Badges --- */
    .badge-green {{
        display: inline-block;
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 800;
    }}

    .badge-orange {{
        display: inline-block;
        background: linear-gradient(135deg, #F59E0B, #D97706);
        color: white;
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 800;
    }}

    .badge-red {{
        display: inline-block;
        background: linear-gradient(135deg, #EF4444, #DC2626);
        color: white;
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 800;
    }}

    /* --- Boutons --- */
    .stButton > button {{
        background: linear-gradient(135deg, {SG_RED} 0%, #B00020 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 13px 28px;
        font-weight: 900;
        font-size: 0.98em;
        transition: all 0.3s ease;
        box-shadow: 0 7px 20px rgba(230,0,40,0.32);
        letter-spacing: 0.7px;
    }}

    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(230,0,40,0.45);
    }}

    /* --- Sidebar --- */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {SG_BLACK} 0%, {SG_DARK_GRAY} 100%);
    }}

    [data-testid="stSidebar"] * {{
        color: white !important;
    }}

    /* --- Onglets --- */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 12px;
        background: white;
        border-radius: 18px;
        padding: 8px;
        box-shadow: 0 5px 18px rgba(0,0,0,0.08);
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 12px;
        padding: 12px 22px;
        font-weight: 900;
    }}

    .stTabs [aria-selected="true"] {{
        background: {SG_RED} !important;
        color: white !important;
    }}

    /* --- Tableaux --- */
    .dataframe {{
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }}

    /* --- Statuts financiers (ajout) --- */
    .status-indicator {{
        display: inline-block;
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }}
    .status-success {{
        background: rgba(40, 167, 69, 0.1);
        color: #28A745;
        border: 1px solid #28A745;
    }}
    .status-warning {{
        background: rgba(255, 193, 7, 0.1);
        color: #FFC107;
        border: 1px solid #FFC107;
    }}
    .status-danger {{
        background: rgba(220, 53, 69, 0.1);
        color: #DC3545;
        border: 1px solid #DC3545;
    }}

    /* --- Ballon d'information (du premier code) --- */
    .balloon {{
        background: white;
        border: 2px solid {SG_RED};
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        position: relative;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        animation: float 6s ease-in-out infinite;
    }}
    .balloon::before {{
        content: '💡';
        position: absolute;
        top: -15px;
        left: 20px;
        font-size: 24px;
        background: white;
        padding: 5px;
        border-radius: 50%;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }}
    @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}

    /* --- Admin --- */
    .admin-hero {{
        background: linear-gradient(135deg, {SG_BLACK} 0%, {SG_RED} 100%);
        color: white;
        padding: 36px;
        border-radius: 24px;
        margin-bottom: 30px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.24);
        position: relative;
        overflow: hidden;
    }}

    .admin-hero h1 {{
        margin: 0;
        font-size: 2.2em;
        font-weight: 900;
    }}

    .admin-hero p {{
        margin-top: 10px;
        opacity: 0.93;
        font-size: 1.05em;
    }}

    .admin-panel {{
        background: white;
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 8px 28px rgba(0,0,0,0.08);
        margin-top: 18px;
        border-top: 4px solid {SG_RED};
    }}
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 🧠 SESSION STATE
# ═══════════════════════════════════════════════════════════════

def init_session_state():
    """Initialise les variables de session."""
    defaults = {
        "authenticated": False,
        "username": None,
        "user_role": None,
        "user_modules": [],
        "session_started_at": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ═══════════════════════════════════════════════════════════════
# 📈 TRACKING USAGE & KPI
# ═══════════════════════════════════════════════════════════════

def init_usage_tracking():
    """Crée le fichier de logs s'il n'existe pas."""
    if not os.path.exists(USAGE_LOG_FILE):
        df = pd.DataFrame(columns=[
            "timestamp", "date", "username", "role",
            "event_type", "module", "details"
        ])
        df.to_csv(USAGE_LOG_FILE, index=False)

def log_event(event_type: str, module: str = "global", details: str = ""):
    """Enregistre un événement dans le fichier de logs."""
    init_usage_tracking()
    username = st.session_state.get("username") or "anonymous"
    role = st.session_state.get("user_role") or "unknown"
    new_log = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "username": username,
        "role": role,
        "event_type": event_type,
        "module": module,
        "details": details
    }])
    try:
        existing = pd.read_csv(USAGE_LOG_FILE)
        updated = pd.concat([existing, new_log], ignore_index=True)
        updated.to_csv(USAGE_LOG_FILE, index=False)
    except Exception as e:
        st.warning(f"Impossible d'écrire dans le journal d'usage : {e}")

def load_usage_logs():
    """Charge les logs depuis le fichier CSV."""
    init_usage_tracking()
    try:
        df = pd.read_csv(USAGE_LOG_FILE)
        if not df.empty:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
        return df
    except Exception:
        return pd.DataFrame(columns=[
            "timestamp", "date", "username", "role", "event_type", "module", "details"
        ])

# ═══════════════════════════════════════════════════════════════
# 🔐 LOGIN / LOGOUT
# ═══════════════════════════════════════════════════════════════

def login_page():
    """Affiche la page de connexion."""
    st.markdown("""
    <div class="login-shell">
        <div class="login-logo">🏦</div>
        <div class="login-title">SEGAH-CREDIT</div>
        <div class="login-subtitle">Portail sécurisé de simulation et pilotage d'usage</div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 1.4, 1])
    with col_center:
        username = st.text_input("👤 Identifiant", placeholder="Entrez votre identifiant", key="login_username")
        password = st.text_input("🔒 Mot de passe", type="password", placeholder="Entrez votre mot de passe", key="login_password")

        if st.button("🚀 SE CONNECTER", use_container_width=True):
            if verify_password(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.user_role = USERS[username]["role"]
                st.session_state.user_modules = USERS[username]["modules"]
                st.session_state.session_started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_event("login_success", "auth", f"Connexion réussie de {username}")
                st.success("✅ Connexion réussie.")
                st.rerun()
            else:
                log_event("login_error", "auth", f"Tentative échouée pour identifiant : {username}")
                st.error("❌ Identifiant ou mot de passe incorrect.")

        with st.expander("📋 Comptes d'accès au personnel SGCI"):
            st.markdown("""
            - **admin** / `admin2026` : accès complet
            - **rh** / `rh2026` : accès simulation salaire
            - **credit** / `credit2026` : accès simulation prêt
            """)

def logout():
    """Déconnecte l'utilisateur."""
    log_event("logout", "auth", "Déconnexion utilisateur")
    for key in ["authenticated", "username", "user_role", "user_modules", "session_started_at"]:
        st.session_state[key] = None if key != "authenticated" else False
    st.rerun()

# ═══════════════════════════════════════════════════════════════
# 🧮 UTILITAIRES MÉTIER (communs aux deux modules)
# ═══════════════════════════════════════════════════════════════

def format_fcfa(value):
    """Formate un nombre en FCFA avec séparateurs d'espace."""
    return f"{value:,.0f} FCFA".replace(",", " ")

# --- Fonctions du module Salaire (héritées du second code) ---
def calcul_revenu_annuel(salaire_net, mois):
    return salaire_net * mois

def calcul_surcout_credit(encours, taux_actuel, taux_nouveau):
    diff = (taux_nouveau - taux_actuel) / 100
    return (encours * diff) / 12

def calcul_salaire_equivalent(revenu_annuel, mois_nouveau):
    if mois_nouveau <= 0:
        return 0
    return revenu_annuel / mois_nouveau

# --- Fonctions du module Prêt (issues du premier code) ---

def convertir_millions_en_lettres(nombre):
    """Convertit un nombre en lettres françaises (pour les millions)."""
    unites = ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf"]
    dizaines = ["", "dix", "vingt", "trente", "quarante", "cinquante", "soixante", "soixante-dix", "quatre-vingt", "quatre-vingt-dix"]

    if nombre == 0:
        return "zéro"

    def convertir_centaines(num):
        if num < 10:
            return unites[num]
        elif num < 20:
            special = ["dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"]
            return special[num-10]
        elif num < 100:
            d = num // 10
            u = num % 10
            if u == 0:
                if d == 8:
                    return dizaines[d] + "s"
                return dizaines[d]
            elif d == 7 or d == 9:
                return dizaines[d-1] + "-" + convertir_centaines(10 + u)
            else:
                if d == 8:
                    return dizaines[d] + "-" + unites[u]
                return dizaines[d] + ("-" if u == 1 and d != 8 else "-") + unites[u]
        else:
            c = num // 100
            r = num % 100
            if c == 1:
                mot = "cent"
            else:
                mot = unites[c] + " cent"
            if r == 0 and c > 1:
                return mot + "s"
            elif r > 0:
                return mot + " " + convertir_centaines(r)
            return mot

    if nombre < 1000:
        return convertir_centaines(nombre)
    elif nombre < 1000000:
        milliers = nombre // 1000
        reste = nombre % 1000
        if milliers == 1:
            mot = "mille"
        else:
            mot = convertir_centaines(milliers) + " mille"
        if reste > 0:
            return mot + " " + convertir_centaines(reste)
        return mot
    elif nombre < 1000000000:
        millions = nombre // 1000000
        reste = nombre % 1000000
        if millions == 1:
            mot = "un million"
        else:
            mot = convertir_centaines(millions) + " millions"
        if reste > 0:
            return mot + " " + convertir_millions_en_lettres(reste)
        return mot
    else:
        return "nombre trop grand"

def nombre_en_lettres(nombre):
    """Formate un montant en lettres avec Francs CFA."""
    partie_entiere = int(nombre)
    if partie_entiere == 0:
        return "zéro Francs CFA"
    texte = convertir_millions_en_lettres(partie_entiere)
    return texte + (" Franc CFA" if partie_entiere == 1 else " Francs CFA")

def calculer_taux_mensuel_combine(taux_interet, taux_assurance, taux_tps):
    """Calcule le taux mensuel combiné incluant intérêt, assurance et TPS."""
    return (taux_interet + taux_assurance) / 12 + taux_interet * taux_tps / 12

def calculer_annuite_constante(montant, taux_mensuel, duree_mois):
    """Calcule l'annuité constante selon la formule financière standard."""
    if taux_mensuel == 0:
        return montant / duree_mois
    return montant * taux_mensuel / (1 - (1 + taux_mensuel) ** -duree_mois)

def calculer_frais_dossier(montant):
    """Calcule les frais de dossier (1.5% avec max 150 000 FCFA)."""
    return min(montant * 0.015, 150000)

def calculer_teg(taux_interet, taux_assurance, taux_tps):
    """Calcule le Taux Effectif Global approximatif."""
    return (taux_interet + taux_assurance + taux_interet * taux_tps) * 100

def calculer_revenu_total(salaire, revenu_locatif, revenu_agricole):
    """Calcule le revenu total pris en compte selon la formule bancaire."""
    return salaire + (0.8 * revenu_locatif) + (0.5 * revenu_agricole)

def calculer_echeancier(montant, taux_interet_annuel, taux_assurance_annuel, taux_tps, duree_mois,
                       salaire, revenu_locatif, revenu_agricole, autres_engagements,
                       date_debut, quotite_cessible_pct):
    """
    Calcule l'échéancier complet avec vérifications financières.
    Retourne un dictionnaire contenant le DataFrame, des indicateurs et l'analyse de risque.
    """
    # Revenu total pris en compte
    revenu_total = calculer_revenu_total(salaire, revenu_locatif, revenu_agricole)

    # Taux mensuels
    taux_mensuel_interet = taux_interet_annuel / 12
    taux_mensuel_assurance = taux_assurance_annuel / 12
    taux_combine = calculer_taux_mensuel_combine(taux_interet_annuel, taux_assurance_annuel, taux_tps)

    # Annuité constante
    annuite = calculer_annuite_constante(montant, taux_combine, duree_mois)

    # Construction de l'échéancier
    echeancier = []
    capital_restant = montant
    amortissement_cumule = 0
    date_echeance = date_debut

    for mois in range(1, duree_mois + 1):
        interets = capital_restant * taux_mensuel_interet
        assurance = capital_restant * taux_mensuel_assurance
        tps = assurance * taux_tps

        amortissement = annuite - (interets + assurance + tps)
        if mois == duree_mois:
            amortissement = capital_restant
            annuite_ajustee = amortissement + interets + assurance + tps
        else:
            annuite_ajustee = annuite

        amortissement_cumule += amortissement
        capital_suivant = max(0, capital_restant - amortissement)

        echeancier.append({
            "N° Échéance": mois,
            "Date": date_echeance.strftime("%d/%m/%Y"),
            "Amortissement": round(amortissement, 2),
            "Amort. Cumulé": round(amortissement_cumule, 2),
            "Intérêts": round(interets, 2),
            "Assurance": round(assurance, 2),
            "TPS": round(tps, 2),
            "Mensualité": round(annuite_ajustee, 2),
            "Capital Restant": round(capital_suivant, 2)
        })

        capital_restant = capital_suivant
        date_echeance += relativedelta(months=1)

    df = pd.DataFrame(echeancier)

    # Indicateurs
    mensualite_totale = annuite
    total_engagements = mensualite_totale + autres_engagements
    taux_endettement = (total_engagements / revenu_total) * 100 if revenu_total > 0 else 0
    quotite_cessible = revenu_total * (quotite_cessible_pct / 100)
    disponible_mensuel = revenu_total - total_engagements

    total_interets = df["Intérêts"].sum()
    total_assurance = df["Assurance"].sum()
    total_tps = df["TPS"].sum()
    total_rembourse = df["Mensualité"].sum()
    cout_total = total_interets + total_assurance + total_tps
    ratio_cout = (cout_total / montant) * 100
    date_derniere = date_debut + relativedelta(months=duree_mois - 1)
    teg = calculer_teg(taux_interet_annuel, taux_assurance_annuel, taux_tps)

    # Analyse de l'endettement
    if taux_endettement <= 33:
        statut_endettement = "Très bon"
        niveau_risque = "Faible"
        couleur_statut = "success"
    elif taux_endettement <= 42:
        statut_endettement = "Acceptable"
        niveau_risque = "Modéré"
        couleur_statut = "warning"
    else:
        statut_endettement = "Élevé"
        niveau_risque = "Important"
        couleur_statut = "danger"

    return {
        "dataframe": df,
        "mensualite": mensualite_totale,
        "taux_endettement": taux_endettement,
        "quotite_cessible": quotite_cessible,
        "disponible_mensuel": disponible_mensuel,
        "total_interets": total_interets,
        "total_assurance": total_assurance,
        "total_tps": total_tps,
        "total_rembourse": total_rembourse,
        "cout_total": cout_total,
        "ratio_cout": ratio_cout,
        "date_derniere": date_derniere,
        "teg": teg,
        "statut_endettement": statut_endettement,
        "niveau_risque": niveau_risque,
        "couleur_statut": couleur_statut,
        "quotite_max_atteinte": total_engagements >= quotite_cessible,
        "revenu_total": revenu_total
    }

def creer_graphique_evolution(df):
    """Crée un graphique d'évolution du capital restant et de l'amortissement cumulé."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["N° Échéance"],
        y=df["Capital Restant"],
        mode='lines',
        name='Capital Restant',
        line=dict(color=SG_RED, width=3),
        fill='tozeroy',
        fillcolor='rgba(230,0,40,0.1)'
    ))
    fig.add_trace(go.Scatter(
        x=df["N° Échéance"],
        y=df["Amort. Cumulé"],
        mode='lines',
        name='Amortissement Cumulé',
        line=dict(color=SG_BLACK, width=2, dash='dash')
    ))
    fig.update_layout(
        title="Évolution du Capital Restant et Amortissement",
        xaxis_title="N° Échéance",
        yaxis_title="Montant (FCFA)",
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=50, b=50, l=50, r=50)
    )
    return fig

def creer_graphique_repartition(df):
    """Crée un graphique en camembert de répartition des paiements."""
    categories = ['Capital', 'Intérêts', 'Assurance', 'TPS']
    valeurs = [
        df["Amortissement"].sum(),
        df["Intérêts"].sum(),
        df["Assurance"].sum(),
        df["TPS"].sum()
    ]
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=valeurs,
        hole=0.4,
        marker_colors=[SG_RED, SG_BLACK, '#FF6B6B', '#FF8A80'],
        textinfo='label+percent+value',
        texttemplate='%{label}<br>%{percent:.1%}<br>%{value:,.0f} FCFA'
    )])
    fig.update_layout(
        title="Répartition des Paiements Totaux",
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=50, b=50, l=50, r=50)
    )
    return fig

# ═══════════════════════════════════════════════════════════════
# 💼 MODULE 1 : SIMULATION SALAIRE (inchangé)
# ═══════════════════════════════════════════════════════════════

def module_simulation_salaire():
    st.markdown("""
    <div class="sg-header">
        <h1>💼 Simulation Salaire & Mobilité RH</h1>
        <p>Évaluez le salaire minimum à négocier lors d'une mobilité professionnelle.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-header">📋 Informations de base</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 💰 Situation actuelle")
        salaire_net = st.number_input(
            "Salaire net mensuel actuel",
            value=1008071,
            step=10000,
            help="Salaire mensuel net actuel en FCFA."
        )
        mois_actuels = st.number_input(
            "Nombre de mois payés par an",
            value=17,
            min_value=12,
            max_value=24,
            help="Inclure les primes, bonus contractuels et mois additionnels."
        )
        prime_scolarite = st.number_input(
            "Prime scolarité mensuelle",
            value=60000,
            step=5000
        )

    with col2:
        st.markdown("### 🎯 Nouveau poste")
        mois_nouveau = st.number_input(
            "Nombre de mois payés/an au nouveau poste",
            value=13,
            min_value=12,
            max_value=24
        )
        encours_credit = st.number_input(
            "Encours crédit restant",
            value=35900000,
            step=100000
        )

    with col3:
        st.markdown("### 🏦 Conditions crédit")
        taux_act = st.number_input(
            "Taux actuel privilégié (%)",
            value=3.5,
            step=0.1
        )
        taux_new = st.number_input(
            "Nouveau taux estimé (%)",
            value=10.0,
            step=0.1
        )
        cotis_total = st.number_input(
            "Cotisations / avantages employeur mensuels",
            value=379356,
            step=1000
        )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if st.button("🔍 CALCULER LA SIMULATION", use_container_width=True):
        log_event(
            "simulation_salary",
            "salary",
            f"Salaire={salaire_net}; Mois_actuels={mois_actuels}; Mois_nouveau={mois_nouveau}; Encours={encours_credit}"
        )

        revenu_annuel = calcul_revenu_annuel(salaire_net, mois_actuels)
        surcout = calcul_surcout_credit(encours_credit, taux_act, taux_new)
        salaire_equiv = calcul_salaire_equivalent(revenu_annuel, mois_nouveau)
        perte_mois = (mois_actuels - mois_nouveau) * salaire_net
        salaire_min_base = salaire_equiv + surcout
        salaire_min_with_cotis = salaire_min_base + cotis_total + prime_scolarite
        impact_mensuel = perte_mois / 12
        ecart_percentage = ((salaire_min_with_cotis - salaire_net) / salaire_net) * 100

        st.markdown('<p class="section-header">📊 Résultats de la simulation</p>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Revenu annuel actuel</div>
                <div class="metric-value">{format_fcfa(revenu_annuel)}</div>
                <p class="metric-subtitle">Base économique actuelle</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Salaire équivalent</div>
                <div class="metric-value">{format_fcfa(salaire_equiv)}</div>
                <p class="metric-subtitle">Sur {mois_nouveau} mois</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Surcoût crédit</div>
                <div class="metric-value">+{format_fcfa(surcout)}</div>
                <p class="metric-subtitle">Impact mensuel du taux</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Perte annuelle brute</div>
                <div class="metric-value">-{format_fcfa(perte_mois)}</div>
                <p class="metric-subtitle">{mois_actuels - mois_nouveau} mois perdus</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        col_left, col_right = st.columns([1.2, 1])

        with col_left:
            st.markdown('<p class="section-header">💰 Package minimum recommandé</p>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-title">🎯 Niveau 1 — Compensation de base</div>
                <div style="font-size:1.8em;font-weight:900;color:{SG_RED};">
                    {format_fcfa(salaire_min_base)} / mois
                </div>
                <p>Inclut le salaire équivalent et le surcoût crédit.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-title">⭐ Niveau 2 — Package complet recommandé</div>
                <div style="font-size:1.8em;font-weight:900;color:{SG_RED};">
                    {format_fcfa(salaire_min_with_cotis)} / mois
                </div>
                <p>Inclut cotisations, prime scolarité et compensation de base.</p>
            </div>
            """, unsafe_allow_html=True)

            progress_width = min(max(ecart_percentage, 0), 100)

            st.markdown(f"""
            <p style="font-weight:800;color:#333;">
                Augmentation nécessaire :
                <span style="color:{SG_RED};font-size:1.25em;">+{ecart_percentage:.1f}%</span>
            </p>
            <div class="progress-bar">
                <div class="progress-fill" style="width:{progress_width}%;"></div>
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown('<p class="section-header">🎯 Recommandations RH</p>', unsafe_allow_html=True)

            recommendations = [
                ("💼 Package global", "Négocier un net-à-net intégrant tous les avantages."),
                ("🏦 Crédit", "Négocier un refinancement ou une indemnité de différentiel de taux."),
                ("🏥 Santé", "Sécuriser le maintien ou la compensation de la couverture santé."),
                ("🎁 Mobilité", "Prévoir un bonus ponctuel de transition."),
                ("📋 Fiscalité", "Prévoir une clause de neutralité fiscale sur 12 à 18 mois."),
                ("💰 Retraite", "Intégrer l’impact des cotisations retraite et avantages différés."),
            ]

            for title, desc in recommendations:
                st.markdown(f"""
                <div style="background:white;padding:13px;border-radius:13px;margin-bottom:10px;
                            border-left:4px solid {SG_RED};box-shadow:0 4px 12px rgba(0,0,0,0.07);">
                    <div style="font-weight:900;color:{SG_RED};">{title}</div>
                    <div style="font-size:0.92em;color:#666;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 💳 MODULE 2 : SIMULATION PRÊT (version avancée du premier code)
# ═══════════════════════════════════════════════════════════════

def module_simulation_pret():
    st.markdown("""
    <div class="sg-header">
        <h1>💳 Simulateur de Prêt Personnel</h1>
        <p>Analyse complète de solvabilité, échéancier détaillé et recommandations.</p>
    </div>
    """, unsafe_allow_html=True)

    # Ballon d'information (comme dans le premier code)
    st.markdown("""
    <div class="balloon">
        <strong>------💎 CALCUL DE REVENU CLIENT</strong><br>
        Le revenu pris en compte est calculé comme suit :<br>
        <strong>Salaire + (80% × Revenu Locatif) + (50% × Revenu Agricole)</strong><br>
        Conforme à la POC du Personnel validée.
    </div>
    """, unsafe_allow_html=True)

    # SECTION PARAMÈTRES
    st.markdown("""
    <div style="background:white;border-radius:22px;padding:22px;box-shadow:0 8px 28px rgba(0,0,0,0.08);
                margin-bottom:20px;border-left:6px solid #E60028;">
        <div style="font-weight:900;font-size:1.2em;color:#333;margin-bottom:10px;">
            📋 PARAMÈTRES DU PRÊT & SITUATION FINANCIÈRE
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 👤 Informations Client")
        col1a, col1b = st.columns(2)
        with col1a:
            nom_client = st.text_input("Nom complet", value="MOUAHA HANDY YVES")
            num_client = st.text_input("Référence client", value="CLIENT-2025-001")
        with col1b:
            statut = st.selectbox("Statut professionnel", ["Salarié"])
            autres_engagements = st.number_input(
                "Autres engagements (FCFA)",
                min_value=0,
                value=0,
                step=10000,
                format="%d",
                help="Mensualités en cours (crédits, loyers, etc.)"
            )

        st.markdown("---")
        st.markdown("#### 💰 Sources de Revenus Mensuelles")

        salaire = st.number_input(
            "Salaire net mensuel (FCFA)",
            min_value=0,
            value=1000000,
            step=10000,
            format="%d",
            help="Revenu salarial net après impôts"
        )

        col_rev1, col_rev2 = st.columns(2)
        with col_rev1:
            revenu_locatif = st.number_input(
                "Revenu locatif mensuel (FCFA)",
                min_value=0,
                value=250000,
                step=10000,
                format="%d",
                help="Revenus de location (80% pris en compte)"
            )
        with col_rev2:
            revenu_agricole = st.number_input(
                "Revenu agricole mensuel (FCFA)",
                min_value=0,
                value=16000,
                step=10000,
                format="%d",
                help="Revenus agricoles (50% pris en compte)"
            )

        # Revenu total calculé
        revenu_total = calculer_revenu_total(salaire, revenu_locatif, revenu_agricole)
        st.info(f"""
        **Revenu total pris en compte :** {format_fcfa(revenu_total)}
        - Salaire : {format_fcfa(salaire)} (100%)
        - Revenu locatif : {format_fcfa(revenu_locatif)} (80% → {format_fcfa(revenu_locatif * 0.8)})
        - Revenu agricole : {format_fcfa(revenu_agricole)} (50% → {format_fcfa(revenu_agricole * 0.5)})
        """)

        # Quotité cessible
        st.markdown("---")
        st.markdown("#### 🎯 Quotité Cessible")
        quotite_pct = st.slider(
            "Pourcentage maximal d'endettement autorisé (%)",
            min_value=20,
            max_value=50,
            value=42,
            step=1,
            help="Pourcentage de vos revenus pouvant être consacré au remboursement de crédits"
        )
        quotite_valeur = revenu_total * (quotite_pct / 100)
        st.success(f"**Quotité cessible :** {format_fcfa(quotite_valeur)} ({quotite_pct}% de {format_fcfa(revenu_total)})")

    with col2:
        st.markdown("#### 💰 Caractéristiques du Prêt")

        montant_pret = st.number_input(
            "Montant du prêt (FCFA)",
            min_value=0,
            value=35900000,
            step=100000,
            format="%d",
            help="Capital emprunté"
        )

        col2a, col2b = st.columns(2)
        with col2a:
            duree_annees = st.selectbox(
                "Durée (années)",
                options=[5, 7, 10, 15, 20, 25],
                index=1
            )
            taux_interet = st.number_input(
                "Taux d'intérêt annuel (%)",
                min_value=0.0,
                max_value=20.0,
                value=3.5,
                step=0.1,
                format="%.3f"
            )
        with col2b:
            taux_assurance = st.number_input(
                "Taux assurance annuel (%)",
                min_value=0.0,
                max_value=5.0,
                value=1.1,
                step=0.1,
                format="%.3f"
            )
            taux_tps = st.number_input(
                "Taux TPS (%)",
                min_value=0.0,
                max_value=20.0,
                value=10.0,
                step=0.1,
                format="%.1f"
            )

        date_debut = st.date_input(
            "Date de premier prélèvement",
            value=datetime.now().replace(day=25) + relativedelta(months=1),
            help="Généralement fixée au 25 du mois suivant"
        )

        st.markdown("---")
        st.markdown(f"**Montant du prêt en lettres :**")
        st.markdown(f"*{nombre_en_lettres(montant_pret)}*")

    # Bouton de calcul
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🔍 ANALYSER LA FAISABILITÉ & CALCULER L'ÉCHÉANCIER", use_container_width=True, type="primary"):
            # Log de l'événement
            log_event(
                "simulation_loan",
                "loan",
                f"Montant={montant_pret}; Durée={duree_annees}; Taux={taux_interet}; Assurance={taux_assurance}; Revenu={salaire}"
            )

            duree_mois = duree_annees * 12
            with st.spinner("Analyse financière en cours..."):
                resultats = calculer_echeancier(
                    montant=montant_pret,
                    taux_interet_annuel=taux_interet/100,
                    taux_assurance_annuel=taux_assurance/100,
                    taux_tps=taux_tps/100,
                    duree_mois=duree_mois,
                    salaire=salaire,
                    revenu_locatif=revenu_locatif,
                    revenu_agricole=revenu_agricole,
                    autres_engagements=autres_engagements,
                    date_debut=date_debut,
                    quotite_cessible_pct=quotite_pct
                )

                # Stockage en session (pour persistance éventuelle)
                st.session_state['resultats_pret'] = resultats
                st.session_state['duree_mois'] = duree_mois
                st.session_state['duree_annees'] = duree_annees
                st.session_state['montant_pret'] = montant_pret
                st.session_state['taux_interet'] = taux_interet
                st.session_state['taux_assurance'] = taux_assurance
                st.session_state['taux_tps'] = taux_tps
                st.session_state['autres_engagements'] = autres_engagements
                st.session_state['quotite_pct'] = quotite_pct
                st.session_state['calcul_pret_fait'] = True

    # Affichage des résultats si disponible
    if st.session_state.get('calcul_pret_fait', False):
        resultats = st.session_state['resultats_pret']
        duree_mois = st.session_state['duree_mois']
        duree_annees = st.session_state['duree_annees']
        montant_pret = st.session_state['montant_pret']
        taux_interet = st.session_state['taux_interet']
        taux_assurance = st.session_state['taux_assurance']
        taux_tps = st.session_state['taux_tps']
        autres_engagements = st.session_state['autres_engagements']
        quotite_pct = st.session_state['quotite_pct']

        # SECTION SYNTHÈSE FINANCIÈRE
        st.markdown("""
        <div style="background:white;border-radius:22px;padding:22px;box-shadow:0 8px 28px rgba(0,0,0,0.08);
                    margin:30px 0 20px 0;border-left:6px solid #E60028;">
            <div style="font-weight:900;font-size:1.2em;color:#333;margin-bottom:10px;">
                📊 SYNTHÈSE FINANCIÈRE & ANALYSE DE RISQUE
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Métriques principales
        col_ind1, col_ind2, col_ind3, col_ind4 = st.columns(4)

        with col_ind1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Mensualité</div>
                <div class="metric-value">{format_fcfa(resultats['mensualite'])}</div>
                <div class="metric-subtitle">Échéance constante</div>
            </div>
            """, unsafe_allow_html=True)

        with col_ind2:
            couleur_classe = f"status-{resultats['couleur_statut']}"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Taux d'endettement</div>
                <div class="metric-value">{resultats['taux_endettement']:.1f}%</div>
                <div class="metric-subtitle">
                    <span class="status-indicator {couleur_classe}">
                        {resultats['statut_endettement']}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_ind3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Coût total crédit</div>
                <div class="metric-value">{format_fcfa(resultats['cout_total'])}</div>
                <div class="metric-subtitle">{resultats['ratio_cout']:.1f}% du capital</div>
            </div>
            """, unsafe_allow_html=True)

        with col_ind4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Taux Effectif Global</div>
                <div class="metric-value">{resultats['teg']:.3f}%</div>
                <div class="metric-subtitle">Inclut tous les frais</div>
            </div>
            """, unsafe_allow_html=True)

        # Barre de progression de l'endettement
        total_engagements = resultats["mensualite"] + autres_engagements
        marge_quotite = resultats["quotite_cessible"] - total_engagements
        pourcentage_utilisation = min((total_engagements / resultats["quotite_cessible"]) * 100, 100)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📈 Analyse de votre capacité d'endettement")

        col_prog1, col_prog2 = st.columns([3, 1])
        with col_prog1:
            st.markdown(f"""
            <div style="margin: 20px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Utilisation de votre quotité</span>
                    <span><strong>{pourcentage_utilisation:.1f}%</strong></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {pourcentage_utilisation}%;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #6C757D; margin-top: 10px;">
                    <span>0 FCFA</span>
                    <span>{format_fcfa(resultats['quotite_cessible'])} (max)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_prog2:
            if marge_quotite > 0:
                st.success(f"✅ **Marge disponible :** {format_fcfa(marge_quotite)}")
            else:
                st.error(f"⚠️ **Dépassement :** {format_fcfa(abs(marge_quotite))}")

        # Détails en colonnes
        st.markdown("<br>", unsafe_allow_html=True)
        col_det1, col_det2, col_det3 = st.columns(3)

        with col_det1:
            st.markdown(f"""
            <div style="background:white;border-radius:22px;padding:20px;box-shadow:0 8px 28px rgba(0,0,0,0.08);
                        border-left:6px solid #E60028;">
                <div style="font-weight:900;color:#E60028;font-size:1.1em;margin-bottom:15px;">💰 Revenus & Engagements</div>
                <table style="width:100%;">
                    <tr><td>Salaire net</td><td style="text-align:right;font-weight:bold;">{format_fcfa(salaire)}</td></tr>
                    <tr><td>Revenu locatif</td><td style="text-align:right;">{format_fcfa(revenu_locatif)}</td></tr>
                    <tr><td>Revenu agricole</td><td style="text-align:right;">{format_fcfa(revenu_agricole)}</td></tr>
                    <tr><td><strong>Revenu pris en compte</strong></td><td style="text-align:right;font-weight:bold;color:#E60028;">{format_fcfa(resultats['revenu_total'])}</td></tr>
                    <tr><td>Autres engagements</td><td style="text-align:right;">{format_fcfa(autres_engagements)}</td></tr>
                    <tr><td>Mensualité prêt</td><td style="text-align:right;font-weight:bold;color:#E60028;">{format_fcfa(resultats['mensualite'])}</td></tr>
                    <tr><td><strong>Total engagements</strong></td><td style="text-align:right;font-weight:bold;">{format_fcfa(total_engagements)}</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

        with col_det2:
            st.markdown(f"""
            <div style="background:white;border-radius:22px;padding:20px;box-shadow:0 8px 28px rgba(0,0,0,0.08);
                        border-left:6px solid #E60028;">
                <div style="font-weight:900;color:#E60028;font-size:1.1em;margin-bottom:15px;">🎯 Quotité & Disposable</div>
                <table style="width:100%;">
                    <tr><td>Quotité cessible ({quotite_pct}%)</td><td style="text-align:right;font-weight:bold;">{format_fcfa(resultats['quotite_cessible'])}</td></tr>
                    <tr><td>Total engagements</td><td style="text-align:right;font-weight:bold;">{format_fcfa(total_engagements)}</td></tr>
                    <tr><td><strong>Disponible mensuel</strong></td><td style="text-align:right;font-weight:bold;color:#10B981;">{format_fcfa(resultats['disponible_mensuel'])}</td></tr>
                    <tr><td><strong>Taux d'endettement</strong></td><td style="text-align:right;font-weight:bold;">{resultats['taux_endettement']:.1f}%</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

        with col_det3:
            couleur_marge = "#10B981" if marge_quotite > 0 else "#DC3545"
            couleur_epargne = "#10B981" if resultats["disponible_mensuel"] > resultats['revenu_total'] * 0.1 else "#F59E0B"
            st.markdown(f"""
            <div style="background:white;border-radius:22px;padding:20px;box-shadow:0 8px 28px rgba(0,0,0,0.08);
                        border-left:6px solid #E60028;">
                <div style="font-weight:900;color:#E60028;font-size:1.1em;margin-bottom:15px;">⚠️ Analyse de Risque</div>
                <table style="width:100%;">
                    <tr><td>Statut endettement</td><td style="text-align:right;"><span class="status-indicator status-{resultats['couleur_statut']}">{resultats['statut_endettement']}</span></td></tr>
                    <tr><td>Niveau de risque</td><td style="text-align:right;font-weight:bold;">{resultats['niveau_risque']}</td></tr>
                    <tr><td>Marge de sécurité</td><td style="text-align:right;font-weight:bold;color:{couleur_marge};">{format_fcfa(marge_quotite)}</td></tr>
                    <tr><td>Capacité d'épargne</td><td style="text-align:right;font-weight:bold;color:{couleur_epargne};">{format_fcfa(resultats['disponible_mensuel'])}</td></tr>
                    <tr><td>Ratio épargne/revenu</td><td style="text-align:right;font-weight:bold;">{(resultats['disponible_mensuel']/resultats['revenu_total']*100):.1f}%</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

        # SECTION GRAPHIQUES ET TABLEAU
        st.markdown("""
        <div style="background:white;border-radius:22px;padding:22px;box-shadow:0 8px 28px rgba(0,0,0,0.08);
                    margin:30px 0 20px 0;border-left:6px solid #E60028;">
            <div style="font-weight:900;font-size:1.2em;color:#333;margin-bottom:10px;">
                📈 VISUALISATIONS & ÉCHÉANCIER DÉTAILLÉ
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["📋 Tableau d'Amortissement", "📊 Graphiques d'Analyse", "📄 Synthèse Complète"])

        with tab1:
            st.markdown(f"### 📅 Tableau d'Amortissement Détaillé ({duree_mois} échéances)")
            col_opt1, col_opt2 = st.columns(2)
            with col_opt1:
                n_lignes = st.slider("Nombre de lignes à afficher", min_value=12, max_value=duree_mois, value=min(24, duree_mois), step=12)
            with col_opt2:
                show_all = st.checkbox("Afficher tout l'échéancier", value=False)

            df_display = resultats["dataframe"].copy()
            if not show_all:
                df_display = df_display.head(n_lignes)

            # Formater les nombres
            for col in ["Amortissement", "Amort. Cumulé", "Intérêts", "Assurance", "TPS", "Mensualité", "Capital Restant"]:
                df_display[col] = df_display[col].apply(lambda x: f"{x:,.2f}")

            st.dataframe(df_display, use_container_width=True, height=500)

            # Téléchargement CSV
            csv = resultats["dataframe"].to_csv(index=False, sep=';').encode('utf-8')
            st.download_button(
                label="📥 Télécharger l'échéancier complet (CSV)",
                data=csv,
                file_name=f"echeancier_{nom_client.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

            # Résumé du tableau
            st.markdown("#### 📊 Résumé du Tableau d'Amortissement")
            col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
            with col_sum1:
                st.metric("Total Intérêts", format_fcfa(resultats['total_interets']))
            with col_sum2:
                st.metric("Total Assurance", format_fcfa(resultats['total_assurance']))
            with col_sum3:
                st.metric("Total TPS", format_fcfa(resultats['total_tps']))
            with col_sum4:
                st.metric("Total à rembourser", format_fcfa(resultats['total_rembourse']))

        with tab2:
            col_graph1, col_graph2 = st.columns(2)
            with col_graph1:
                fig_evol = creer_graphique_evolution(resultats["dataframe"])
                st.plotly_chart(fig_evol, use_container_width=True)
            with col_graph2:
                fig_rep = creer_graphique_repartition(resultats["dataframe"])
                st.plotly_chart(fig_rep, use_container_width=True)

            st.markdown("### 📉 Évolution des composantes de la mensualité")
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Scatter(
                x=resultats["dataframe"]["N° Échéance"],
                y=resultats["dataframe"]["Intérêts"],
                mode='lines', name='Intérêts', line=dict(color=SG_BLACK, width=2), stackgroup='one'
            ))
            fig_comp.add_trace(go.Scatter(
                x=resultats["dataframe"]["N° Échéance"],
                y=resultats["dataframe"]["Assurance"],
                mode='lines', name='Assurance', line=dict(color='#FF6B6B', width=2), stackgroup='one'
            ))
            fig_comp.add_trace(go.Scatter(
                x=resultats["dataframe"]["N° Échéance"],
                y=resultats["dataframe"]["TPS"],
                mode='lines', name='TPS', line=dict(color='#FF8A80', width=2), stackgroup='one'
            ))
            fig_comp.update_layout(
                title="Décomposition de la mensualité",
                xaxis_title="N° Échéance",
                yaxis_title="Montant (FCFA)",
                hovermode='x unified',
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            st.plotly_chart(fig_comp, use_container_width=True)

        with tab3:
            st.markdown("### 📄 Synthèse Financière Complète")
            col_synth1, col_synth2 = st.columns(2)

            with col_synth1:
                st.markdown(f"""
                <div style="background:white;border-radius:22px;padding:20px;box-shadow:0 8px 28px rgba(0,0,0,0.08);
                            border-left:6px solid #E60028;">
                    <div style="font-weight:900;color:#E60028;font-size:1.1em;margin-bottom:15px;">💵 Détails Financiers</div>
                    <table style="width:100%;">
                        <tr><td>Montant emprunté</td><td style="text-align:right;font-weight:bold;">{format_fcfa(montant_pret)}</td></tr>
                        <tr><td>Durée</td><td style="text-align:right;">{duree_annees} ans ({duree_mois} mois)</td></tr>
                        <tr><td>Taux d'intérêt nominal</td><td style="text-align:right;">{taux_interet:.3f}%</td></tr>
                        <tr><td>Taux d'assurance</td><td style="text-align:right;">{taux_assurance:.3f}%</td></tr>
                        <tr><td>Taux TPS</td><td style="text-align:right;">{taux_tps:.1f}%</td></tr>
                        <tr><td>Taux Effectif Global</td><td style="text-align:right;font-weight:bold;color:#E60028;">{resultats['teg']:.3f}%</td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)

            with col_synth2:
                st.markdown(f"""
                <div style="background:white;border-radius:22px;padding:20px;box-shadow:0 8px 28px rgba(0,0,0,0.08);
                            border-left:6px solid #E60028;">
                    <div style="font-weight:900;color:#E60028;font-size:1.1em;margin-bottom:15px;">🧮 Totaux & Coûts</div>
                    <table style="width:100%;">
                        <tr><td>Total intérêts</td><td style="text-align:right;font-weight:bold;">{format_fcfa(resultats['total_interets'])}</td></tr>
                        <tr><td>Total assurance</td><td style="text-align:right;">{format_fcfa(resultats['total_assurance'])}</td></tr>
                        <tr><td>Total TPS</td><td style="text-align:right;">{format_fcfa(resultats['total_tps'])}</td></tr>
                        <tr><td><strong>Coût total du crédit</strong></td><td style="text-align:right;font-weight:bold;color:#E60028;">{format_fcfa(resultats['cout_total'])}</td></tr>
                        <tr><td><strong>Total à rembourser</strong></td><td style="text-align:right;font-weight:bold;">{format_fcfa(resultats['total_rembourse'])}</td></tr>
                        <tr><td>Ratio coût/capital</td><td style="text-align:right;">{resultats['ratio_cout']:.1f}%</td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)

            # Recommandations
            st.markdown("### 🎯 Recommendations Financières")
            if resultats["quotite_max_atteinte"]:
                st.error("""
                ⚠️ **ATTENTION : VOTRE QUOTITÉ CESSIBLE EST ATTEINTE**

                Nos analyses indiquent que vos engagements totaux atteignent ou dépassent votre quotité cessible.

                **Recommandations :**
                1. Réduisez le montant du prêt demandé
                2. Allongez la durée du prêt pour diminuer la mensualité
                3. Examinez la possibilité de réduire vos autres engagements
                4. Considérez un apport personnel plus important

                **Risques :** Difficultés de remboursement en cas de baisse de revenus.
                """)
            elif resultats["taux_endettement"] > 40:
                st.warning("""
                ⚠️ **SOYEZ VIGILANT : TAUX D'ENDETTEMENT ÉLEVÉ**

                Votre taux d'endettement approche la limite recommandée.

                **Recommandations :**
                1. Assurez-vous d'avoir une épargne de précaution (3-6 mois de revenus)
                2. Prévoyez une marge de sécurité pour les imprévus
                3. Évitez tout nouvel engagement pendant la durée du prêt
                4. Surveillez régulièrement votre budget

                **Conseil :** Maintenez votre épargne à au moins 10% de vos revenus.
                """)
            else:
                st.success("""
                ✅ **SITUATION FINANCIÈRE CONFORME AUX NORMES**

                Votre projet de prêt respecte les critères de solvabilité.

                **Points forts :**
                1. Taux d'endettement dans les limites recommandées
                2. Marge de sécurité financière disponible
                3. Capacité d'épargne préservée

                **Recommandations :**
                - Conservez une épargne de précaution
                - Assurez-vous de la stabilité de vos revenus
                - Pensez au remboursement anticipé pour réduire le coût total
                """)

        # SECTION INFORMATIONS LÉGALES
        with st.expander("📚 Informations Légales & Techniques", expanded=False):
            col_legal1, col_legal2 = st.columns(2)
            with col_legal1:
                st.markdown("""
                ### ⚖️ Mentions Légales

                **Simulateur conforme aux normes :**
                - Calculs basés sur la méthode des annuités constantes
                - Taux Effectif Global calculé selon la réglementation
                - Quotité cessible selon les recommandations du Comité de Bâle

                **Calcul du revenu bancaire :**
                - Salaire : 100% pris en compte
                - Revenu locatif : 80% pris en compte
                - Revenu agricole : 50% pris en compte

                **Formule :** Revenu = Salaire + (0.8 × Revenu Locatif) + (0.5 × Revenu Agricole)

                **Informations importantes :**
                - Ce simulateur fournit des estimations à titre indicatif
                - Les conditions finales sont soumises à l'approbation du comité de crédit
                - Les taux peuvent varier en fonction du profil client
                """)
            with col_legal2:
                st.markdown("""
                ### 🧮 Méthodologie de Calcul

                **Formule d'annuité constante :**
