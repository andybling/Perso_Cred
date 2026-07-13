# =====================================================================
# 🏦 SEGAH-CREDIT - Application de Simulation et Pilotage
# Version : V4.0 (fusion des modules salaire & prêt avec logging & admin)
# =====================================================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import os

# =====================================================================
# 🎨 CONFIGURATION GÉNÉRALE
# =====================================================================

st.set_page_config(
    page_title="SEGAH-CREDIT",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Design System
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
USAGE_LOG_FILE = "usage_logs_segah.csv"


# =====================================================================
# 🔐 SÉCURITÉ SIMPLE PAR HASH SHA-256
# =====================================================================

def hash_password(password: str) -> str:
    """Retourne le hash SHA-256 d'un mot de passe."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# Utilisateurs pré-définis avec leurs rôles et modules accessibles
# Les mots de passe sont hashés (ex: admin123, rh2025, credit2025)
USERS = {
    "admin": {
        "password_hash": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",  # admin123
        "role": "Administrateur",
        "modules": ["salary", "loan", "admin"]
    },
    "rh": {
        "password_hash": "d3cdbaa6c5cbb1e4f64fec97a5893749b456b29b2ceda7e4e0c87a46936f8f8c",  # rh2025
        "role": "Ressources Humaines",
        "modules": ["salary"]
    },
    "credit": {
        "password_hash": "7d1b9e06b2a13184a94a9391b85f61f990b14d3454650ec429a2146dc448bea7",  # credit2025
        "role": "Analyste Crédit",
        "modules": ["loan"]
    },
}


def verify_password(username: str, password: str) -> bool:
    """Vérifie si le mot de passe correspond au hash stocké."""
    if username not in USERS:
        return False
    return hash_password(password) == USERS[username]["password_hash"]


# =====================================================================
# 🎨 CSS GLOBAL UX/UI
# =====================================================================

def apply_custom_css():
    """Applique le style CSS personnalisé à l'application."""
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

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {SG_BLACK} 0%, {SG_DARK_GRAY} 100%);
    }}

    [data-testid="stSidebar"] * {{
        color: white !important;
    }}

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

    .dataframe {{
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }}

    .stNumberInput>div>div>input, .stSelectbox>div>div>select, .stDateInput>div>div>input {{
        border-radius: 10px;
        border: 2px solid {SG_GRAY};
        padding: 12px;
        transition: all 0.3s ease;
        font-size: 1em;
    }}
    
    .stNumberInput>div>div>input:focus, .stSelectbox>div>div>select:focus, .stDateInput>div>div>input:focus {{
        border-color: {SG_RED};
        box-shadow: 0 0 0 3px rgba(230, 0, 40, 0.15);
        transform: scale(1.02);
    }}

    </style>
    """, unsafe_allow_html=True)


# =====================================================================
# 🧠 SESSION STATE
# =====================================================================

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


# =====================================================================
# 📈 TRACKING USAGE & KPI
# =====================================================================

def init_usage_tracking():
    """Crée le fichier CSV de logs s'il n'existe pas."""
    if not os.path.exists(USAGE_LOG_FILE):
        df = pd.DataFrame(columns=[
            "timestamp",
            "date",
            "username",
            "role",
            "event_type",
            "module",
            "details"
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


# =====================================================================
# 🔐 LOGIN / LOGOUT
# =====================================================================

def login_page():
    """Affiche la page de connexion."""
    st.markdown("""
    <div class="login-shell">
        <div class="login-logo">🏦</div>
        <div class="login-title">SEGAH-CREDIT</div>
        <div class="login-subtitle">Portail sécurisé de simulation et pilotage d’usage</div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 1.4, 1])
    with col_center:
        username = st.text_input(
            "👤 Identifiant",
            placeholder="Entrez votre identifiant",
            key="login_username"
        )
        password = st.text_input(
            "🔒 Mot de passe",
            type="password",
            placeholder="Entrez votre mot de passe",
            key="login_password"
        )
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
            - **admin** / `admin123` : accès complet
            - **rh** / `rh2025` : accès simulation salaire
            - **credit** / `credit2025` : accès simulation prêt
            """)


def logout():
    """Déconnecte l'utilisateur et réinitialise la session."""
    log_event("logout", "auth", "Déconnexion utilisateur")
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_role = None
    st.session_state.user_modules = []
    st.session_state.session_started_at = None
    st.rerun()


# =====================================================================
# 🧮 UTILITAIRES MÉTIER
# =====================================================================

def format_fcfa(value):
    """Formate un nombre en FCFA avec espaces comme séparateurs de milliers."""
    return f"{value:,.0f} FCFA".replace(",", " ")


def calcul_revenu_annuel(salaire_net, mois):
    """Calcule le revenu annuel net."""
    return salaire_net * mois


def calcul_surcout_credit(encours, taux_actuel, taux_nouveau):
    """Calcule le surcoût mensuel dû à la différence de taux d'intérêt."""
    diff = (taux_nouveau - taux_actuel) / 100
    return (encours * diff) / 12


def calcul_salaire_equivalent(revenu_annuel, mois_nouveau):
    """Calcule le salaire mensuel équivalent pour un nombre de mois donné."""
    if mois_nouveau <= 0:
        return 0
    return revenu_annuel / mois_nouveau


def calculate_constant_payment(loan_amount, annual_rate, duration_months):
    """
    Calcule la mensualité constante (amortissement + intérêts + assurance)
    selon la formule de l'annuité constante.
    """
    if loan_amount <= 0 or duration_months <= 0:
        return 0
    monthly_rate = annual_rate / 12
    if annual_rate == 0:
        return loan_amount / duration_months
    payment = loan_amount * (
        monthly_rate * (1 + monthly_rate) ** duration_months
    ) / ((1 + monthly_rate) ** duration_months - 1)
    return payment


# Groupes de clients basés sur le revenu mensuel (pour le taux d'endettement max)
INCOME_GROUPS = [
    {'max_income': 250000, 'group': 'Groupe<250', 'max_ratio': 0.33, 'color': '#10B981'},
    {'max_income': 450000, 'group': 'Groupe<400', 'max_ratio': 0.35, 'color': '#3B82F6'},
    {'max_income': 1000000, 'group': 'Groupe<1000', 'max_ratio': 0.40, 'color': '#8B5CF6'},
    {'max_income': 2000000, 'group': 'Groupe<2000', 'max_ratio': 0.42, 'color': '#F59E0B'},
    {'max_income': float('inf'), 'group': 'Groupe de +2000', 'max_ratio': 0.45, 'color': '#E60028'}
]


def get_client_group(income):
    """Détermine le groupe du client selon son revenu."""
    for group_info in INCOME_GROUPS:
        if income <= group_info["max_income"]:
            return group_info
    return INCOME_GROUPS[-1]


def get_risk_assessment(debt_ratio, max_ratio):
    """
    Évalue le niveau de risque en fonction du taux d'endettement par rapport au maximum.
    Retourne (niveau, emoji, classe CSS).
    """
    if debt_ratio <= max_ratio * 0.85:
        return "FAIBLE", "🟢", "badge-green"
    elif debt_ratio <= max_ratio:
        return "MODÉRÉ", "🟡", "badge-orange"
    else:
        return "ÉLEVÉ", "🔴", "badge-red"


def calculate_amortization_schedule_constant(
    loan_amount,
    interest_rate,
    insurance_rate,
    duration_years,
    first_date
):
    """
    Génère le tableau d'amortissement avec mensualité constante,
    incluant intérêts, assurance et TPS (10%).
    """
    duration_months = duration_years * 12
    tps_rate = 0.10
    global_rate = interest_rate + insurance_rate
    monthly_payment_ht = calculate_constant_payment(
        loan_amount,
        global_rate,
        duration_months
    )
    schedule = []
    remaining_capital = loan_amount

    for month in range(1, duration_months + 1):
        payment_date = first_date + timedelta(days=30 * (month - 1))
        interest = remaining_capital * (interest_rate / 12)
        insurance = remaining_capital * (insurance_rate / 12)
        principal = monthly_payment_ht - interest - insurance

        if month == duration_months:
            principal = remaining_capital
            monthly_payment_ht = principal + interest + insurance

        tps = monthly_payment_ht * tps_rate
        monthly_payment_ttc = monthly_payment_ht + tps

        remaining_capital -= principal

        schedule.append({
            "N°": month,
            "Date": payment_date.strftime("%d/%m/%Y"),
            "Principal": round(principal, 2),
            "Intérêts": round(interest, 2),
            "Assurance": round(insurance, 2),
            "Sous-total HT": round(monthly_payment_ht, 2),
            "TPS (10%)": round(tps, 2),
            "Mensualité TTC": round(monthly_payment_ttc, 2),
            "Capital Restant": round(max(0, remaining_capital), 2)
        })

    return pd.DataFrame(schedule)


# =====================================================================
# 💼 MODULE 1 : SIMULATION SALAIRE & MOBILITÉ
# =====================================================================

def module_simulation_salaire():
    """
    Module de simulation du salaire minimum à négocier lors d'une mobilité.
    Reprend l'affichage détaillé du premier code (métriques, recommandations, barres de progression).
    """
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
            step=5000,
            help="Prime mensuelle de scolarité."
        )

    with col2:
        st.markdown("### 🎯 Nouveau poste")
        mois_nouveau = st.number_input(
            "Nombre de mois payés/an au nouveau poste",
            value=13,
            min_value=12,
            max_value=24,
            help="Nombre de mois de salaire sur le nouveau poste."
        )
        encours_credit = st.number_input(
            "Encours crédit restant",
            value=35900000,
            step=100000,
            help="Montant restant du crédit."
        )

    with col3:
        st.markdown("### 🏦 Conditions crédit")
        taux_act = st.number_input(
            "Taux actuel privilégié (%)",
            value=3.5,
            step=0.1,
            help="Taux d'intérêt actuel (privilège employeur)."
        )
        taux_new = st.number_input(
            "Nouveau taux estimé (%)",
            value=10.0,
            step=0.1,
            help="Taux d'intérêt après mobilité (sans privilège)."
        )
        cotis_total = st.number_input(
            "Cotisations / avantages employeur mensuels",
            value=379356,
            step=1000,
            help="Total des cotisations sociales mensuelles."
        )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if st.button("🔍 CALCULER LA SIMULATION", use_container_width=True):
        # Enregistrement de l'événement
        log_event(
            "simulation_salary",
            "salary",
            f"Salaire={salaire_net}; Mois_actuels={mois_actuels}; Mois_nouveau={mois_nouveau}; Encours={encours_credit}"
        )

        # --- Calculs ---
        revenu_annuel = calcul_revenu_annuel(salaire_net, mois_actuels)
        surcout = calcul_surcout_credit(encours_credit, taux_act, taux_new)
        salaire_equiv = calcul_salaire_equivalent(revenu_annuel, mois_nouveau)
        perte_mois = (mois_actuels - mois_nouveau) * salaire_net
        salaire_min_base = salaire_equiv + surcout
        # On intègre la prime de scolarité et les cotisations dans le package recommandé
        salaire_min_with_cotis = salaire_min_base + cotis_total + prime_scolarite
        impact_mensuel = perte_mois / 12
        ecart_percentage = ((salaire_min_with_cotis - salaire_net) / salaire_net) * 100

        # --- Affichage des métriques ---
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

        # --- Salaires recommandés ---
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

            # Barre de progression de l'augmentation nécessaire
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

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # --- Analyse détaillée ---
        st.markdown('<p class="section-header">📈 Analyse détaillée</p>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 📉 Pertes")
            st.write(f"- Mois perdus : **{mois_actuels - mois_nouveau}**")
            st.write(f"- Impact mensuel moyen : **{format_fcfa(impact_mensuel)}**")
            st.write(f"- Prime scolarité : **{format_fcfa(prime_scolarite)} / mois**")

        with col2:
            st.markdown("### 💸 Surcoûts")
            st.write(f"- Surcoût crédit mensuel : **{format_fcfa(surcout)}**")
            st.write(f"- Surcoût crédit annuel : **{format_fcfa(surcout * 12)}**")
            st.write(f"- Écart de taux : **{taux_new - taux_act:.1f}%**")

        with col3:
            st.markdown("### ✅ Actions prioritaires")
            st.write("1. Négocier le package complet.")
            st.write("2. Sécuriser le crédit.")
            st.write("3. Documenter les avantages perdus.")
            st.write("4. Prévoir un bonus de mobilité.")


# =====================================================================
# 💳 MODULE 2 : SIMULATION PRÊT PERSONNEL
# =====================================================================

def module_simulation_pret():
    """
    Module de simulation de prêt avec mensualité constante.
    Reprend l'affichage détaillé du premier code (métriques, recommandations, barres de progression,
    répartition des coûts, tableau d'amortissement, téléchargement CSV).
    """
    st.markdown("""
    <div class="sg-header">
        <h1>💳 Simulateur de Prêt Personnel</h1>
        <p>Calculez la mensualité constante, le coût du crédit et le taux d'endettement.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-header">📋 Paramètres du prêt</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 💰 Montant & revenus")
        client_income = st.number_input(
            "Revenu mensuel net",
            value=1500000,
            step=50000,
            help="Votre revenu mensuel net."
        )
        loan_amount = st.number_input(
            "Montant du prêt",
            value=10000000,
            step=100000,
            help="Montant emprunté."
        )

    with col2:
        st.markdown("### ⏱️ Durée & taux")
        duration_years = st.slider(
            "Durée du prêt en années",
            1, 30, 7,
            help="Durée de remboursement."
        )
        interest_rate = st.number_input(
            "Taux d'intérêt annuel (%)",
            value=3.5,
            step=0.1,
            help="Taux d'intérêt nominal."
        ) / 100
        insurance_rate = st.number_input(
            "Taux d'assurance annuel (%)",
            value=1.1,
            step=0.1,
            help="Taux d'assurance décès-invalidité."
        ) / 100

    with col3:
        st.markdown("### 📅 Première échéance")
        first_date = st.date_input(
            "Date du premier prélèvement",
            value=datetime.now().date()
        )

        # Affichage du groupe client
        if client_income > 0:
            group_info = get_client_group(client_income)
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,{group_info['color']},{group_info['color']}dd);
                        padding:18px;border-radius:16px;margin-top:15px;color:white;text-align:center;">
                <div style="font-size:1.1em;font-weight:900;">{group_info['group']}</div>
                <div style="font-size:1.45em;font-weight:900;">
                    Ratio max : {group_info['max_ratio'] * 100:.0f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if st.button("🔍 CALCULER LE PRÊT", use_container_width=True):
        # Enregistrement de l'événement
        log_event(
            "simulation_loan",
            "loan",
            f"Revenu={client_income}; Montant={loan_amount}; Durée={duration_years}; Taux={interest_rate*100:.2f}; Assurance={insurance_rate*100:.2f}"
        )

        if loan_amount <= 0 or client_income <= 0:
            st.warning("⚠️ Veuillez renseigner un montant de prêt et un revenu mensuel.")
            return

        # --- Calculs ---
        group_info = get_client_group(client_income)
        duration_months = duration_years * 12
        processing_fee = min(loan_amount * 0.015, 150000)  # Frais de dossier plafonnés

        global_rate = interest_rate + insurance_rate
        monthly_payment_ht = calculate_constant_payment(loan_amount, global_rate, duration_months)
        tps_monthly = monthly_payment_ht * 0.10
        monthly_payment_ttc = monthly_payment_ht + tps_monthly

        debt_ratio = (monthly_payment_ttc / client_income) * 100
        max_ratio = group_info["max_ratio"] * 100

        max_payment = client_income * group_info["max_ratio"]
        if global_rate > 0:
            max_loan = (
                max_payment *
                ((1 + global_rate / 12) ** duration_months - 1)
            ) / (
                (global_rate / 12) *
                (1 + global_rate / 12) ** duration_months
            )
        else:
            max_loan = max_payment * duration_months

        risk_level, risk_emoji, risk_class = get_risk_assessment(debt_ratio, max_ratio)

        # Tableau d'amortissement
        schedule = calculate_amortization_schedule_constant(
            loan_amount,
            interest_rate,
            insurance_rate,
            duration_years,
            first_date
        )

        total_paid = schedule["Mensualité TTC"].sum()
        total_interest = schedule["Intérêts"].sum()
        total_insurance = schedule["Assurance"].sum()
        total_tps = schedule["TPS (10%)"].sum()
        total_cost = total_interest + total_insurance + total_tps + processing_fee

        # --- Métriques principales ---
        st.markdown('<p class="section-header">📊 Résultats de la simulation</p>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Mensualité TTC</div>
                <div class="metric-value">{format_fcfa(monthly_payment_ttc)}</div>
                <p class="metric-subtitle">Inclut TPS estimée à 10%</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total à rembourser</div>
                <div class="metric-value">{format_fcfa(total_paid)}</div>
                <p class="metric-subtitle">Hors frais initiaux</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Coût total crédit</div>
                <div class="metric-value">{format_fcfa(total_cost)}</div>
                <p class="metric-subtitle">Intérêts + assurance + TPS + frais</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Taux d'endettement</div>
                <div class="metric-value">{risk_emoji} {debt_ratio:.1f}%</div>
                <p class="metric-subtitle">{risk_level} • Max {max_ratio:.0f}%</p>
            </div>
            """, unsafe_allow_html=True)

        # Barre de progression de l'endettement
        progress_color_1 = SG_GREEN if debt_ratio <= max_ratio * 0.85 else SG_ORANGE if debt_ratio <= max_ratio else "#EF4444"
        progress_color_2 = "#059669" if debt_ratio <= max_ratio * 0.85 else "#D97706" if debt_ratio <= max_ratio else "#DC2626"
        progress_width = min((debt_ratio / max_ratio) * 100, 100)

        st.markdown(f"""
        <div style="margin:24px 0;">
            <p style="font-weight:900;">
                Endettement : {debt_ratio:.1f}% / {max_ratio:.0f}% autorisé
            </p>
            <div class="progress-bar">
                <div class="progress-fill" 
                     style="width:{progress_width}%;background:linear-gradient(90deg,{progress_color_1},{progress_color_2});">
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # --- Détails du prêt ---
        col_left, col_right = st.columns([1, 1.2])

        with col_left:
            st.markdown('<p class="section-header">💡 Détails du prêt</p>', unsafe_allow_html=True)

            details = [
                ("💰 Capital emprunté", format_fcfa(loan_amount)),
                ("📊 Taux intérêt", f"{interest_rate * 100:.2f}% / an"),
                ("🛡️ Taux assurance", f"{insurance_rate * 100:.2f}% / an"),
                ("📈 Taux global", f"{global_rate * 100:.2f}% / an"),
                ("💼 Frais de dossier", format_fcfa(processing_fee)),
                ("📅 Durée", f"{duration_years} ans / {duration_months} mois"),
                ("🏦 Groupe client", f"{group_info['group']}"),
            ]

            for label, value in details:
                st.markdown(f"""
                <div style="background:white;padding:13px;border-radius:13px;margin-bottom:9px;
                            border-left:4px solid {SG_RED};
                            display:flex;justify-content:space-between;
                            box-shadow:0 4px 12px rgba(0,0,0,0.06);">
                    <span style="font-weight:800;color:#333;">{label}</span>
                    <span style="font-weight:900;color:{SG_RED};">{value}</span>
                </div>
                """, unsafe_allow_html=True)

        with col_right:
            st.markdown('<p class="section-header">📈 Analyse & recommandations</p>', unsafe_allow_html=True)

            if debt_ratio <= max_ratio * 0.85:
                st.success(f"""
                **✅ DOSSIER EXCELLENT**

                Le taux d'endettement de **{debt_ratio:.1f}%** est largement inférieur au maximum autorisé de **{max_ratio:.0f}%**.

                - Capacité restante mensuelle : **{format_fcfa(max_payment - monthly_payment_ttc)}**
                - Capacité théorique estimée : **{format_fcfa(max_loan)}**
                """)
            elif debt_ratio <= max_ratio:
                st.warning(f"""
                **⚠️ DOSSIER ACCEPTABLE MAIS À SURVEILLER**

                Le taux d'endettement de **{debt_ratio:.1f}%** reste dans la limite de **{max_ratio:.0f}%**, mais avec une marge réduite.

                Recommandations :
                - allonger la durée si possible ;
                - augmenter l'apport ;
                - vérifier la stabilité des revenus ;
                - limiter les crédits parallèles.
                """)
            else:
                excess = monthly_payment_ttc - max_payment
                reduced_loan = max_loan * 0.95
                st.error(f"""
                **❌ DOSSIER À RISQUE**

                Le taux d'endettement de **{debt_ratio:.1f}%** dépasse la limite de **{max_ratio:.0f}%**.

                - Dépassement mensuel : **{format_fcfa(excess)}**
                - Montant cible prudent : **{format_fcfa(reduced_loan)}**
                """)

            # Répartition des coûts
            st.markdown("### 📊 Répartition des coûts")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Intérêts", f"{total_interest / total_paid * 100:.1f}%", format_fcfa(total_interest))
            with col_b:
                st.metric("Assurance", f"{total_insurance / total_paid * 100:.1f}%", format_fcfa(total_insurance))
            with col_c:
                st.metric("TPS", f"{total_tps / total_paid * 100:.1f}%", format_fcfa(total_tps))

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # --- Tableau d'amortissement ---
        st.markdown('<p class="section-header">📋 Tableau d’amortissement détaillé</p>', unsafe_allow_html=True)

        display_df = schedule.copy()
        money_cols = [
            "Principal",
            "Intérêts",
            "Assurance",
            "Sous-total HT",
            "TPS (10%)",
            "Mensualité TTC",
            "Capital Restant"
        ]
        for col in money_cols:
            display_df[col] = display_df[col].apply(lambda x: format_fcfa(x))

        st.dataframe(display_df, use_container_width=True, height=450)

        # Téléchargement CSV
        csv = schedule.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Télécharger le tableau d'amortissement",
            data=csv,
            file_name=f"tableau_amortissement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )


# =====================================================================
# 🛡️ MODULE 3 : ADMIN KPI (Dashboard d'usage)
# =====================================================================

def module_admin_kpi():
    """
    Module d'administration affichant les indicateurs d'usage,
    les connexions, les simulations et les logs.
    """
    st.markdown("""
    <div class="admin-hero">
        <h1>🛡️ Administration & KPI d’usage</h1>
        <p>Suivi quotidien de l’adoption, des connexions, des simulations et de l’activité utilisateur.</p>
    </div>
    """, unsafe_allow_html=True)

    df = load_usage_logs()

    if df.empty:
        st.info("Aucune donnée d’usage disponible pour le moment.")
        return

    today = datetime.now().date()

    st.markdown('<p class="section-header">🎛️ Filtres d’analyse</p>', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        selected_period = st.selectbox(
            "Période",
            ["Aujourd'hui", "7 derniers jours", "30 derniers jours", "Tout l'historique"]
        )

    with col_f2:
        selected_user = st.selectbox(
            "Utilisateur",
            ["Tous"] + sorted(df["username"].dropna().unique().tolist())
        )

    with col_f3:
        selected_module = st.selectbox(
            "Module",
            ["Tous"] + sorted(df["module"].dropna().unique().tolist())
        )

    df_filtered = df.copy()

    if selected_period == "Aujourd'hui":
        df_filtered = df_filtered[df_filtered["date"] == today]
    elif selected_period == "7 derniers jours":
        start_date = today - timedelta(days=7)
        df_filtered = df_filtered[df_filtered["date"] >= start_date]
    elif selected_period == "30 derniers jours":
        start_date = today - timedelta(days=30)
        df_filtered = df_filtered[df_filtered["date"] >= start_date]

    if selected_user != "Tous":
        df_filtered = df_filtered[df_filtered["username"] == selected_user]

    if selected_module != "Tous":
        df_filtered = df_filtered[df_filtered["module"] == selected_module]

    total_events = len(df_filtered)
    total_logins = len(df_filtered[df_filtered["event_type"] == "login_success"])
    active_users = df_filtered["username"].nunique()
    salary_sims = len(df_filtered[df_filtered["event_type"] == "simulation_salary"])
    loan_sims = len(df_filtered[df_filtered["event_type"] == "simulation_loan"])
    total_sims = salary_sims + loan_sims
    errors = len(df_filtered[df_filtered["event_type"].str.contains("error", na=False)])

    st.markdown('<p class="section-header">📌 KPI principaux</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Utilisateurs actifs</div>
            <div class="kpi-number">{active_users}</div>
            <div class="kpi-caption">Sur la période filtrée</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Connexions réussies</div>
            <div class="kpi-number">{total_logins}</div>
            <div class="kpi-caption">Accès authentifiés</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Simulations totales</div>
            <div class="kpi-number">{total_sims}</div>
            <div class="kpi-caption">Salaire + prêt</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Erreurs suivies</div>
            <div class="kpi-number">{errors}</div>
            <div class="kpi-caption">Tentatives échouées ou incidents</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown('<p class="section-header">📅 Usage jour par jour</p>', unsafe_allow_html=True)

    if not df_filtered.empty:
        daily_usage = (
            df_filtered
            .groupby(["date", "event_type"])
            .size()
            .reset_index(name="volume")
        )
        pivot_daily = daily_usage.pivot_table(
            index="date",
            columns="event_type",
            values="volume",
            aggfunc="sum",
            fill_value=0
        )
        st.line_chart(pivot_daily)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
        st.markdown("### 🧭 Répartition par module")
        module_usage = df_filtered["module"].value_counts().reset_index()
        module_usage.columns = ["Module", "Volume"]
        if not module_usage.empty:
            st.bar_chart(module_usage.set_index("Module"))
        else:
            st.info("Aucune donnée module.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
        st.markdown("### 👤 Usage par utilisateur")
        user_usage = df_filtered["username"].value_counts().reset_index()
        user_usage.columns = ["Utilisateur", "Volume"]
        if not user_usage.empty:
            st.bar_chart(user_usage.set_index("Utilisateur"))
        else:
            st.info("Aucune donnée utilisateur.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown('<p class="section-header">📋 Journal détaillé des événements</p>', unsafe_allow_html=True)

    display_logs = df_filtered.sort_values("timestamp", ascending=False).copy()
    if not display_logs.empty:
        display_logs["timestamp"] = display_logs["timestamp"].astype(str)
        st.dataframe(display_logs, use_container_width=True, height=420)

        csv = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Télécharger les logs filtrés",
            data=csv,
            file_name=f"usage_logs_segah_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("Aucun événement disponible avec ces filtres.")


# =====================================================================
# 🧭 SIDEBAR & NAVIGATION
# =====================================================================

def render_sidebar():
    """Affiche la barre latérale avec les infos utilisateur et la déconnexion."""
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center;padding:22px;
                    background:rgba(255,255,255,0.10);
                    border-radius:18px;margin-bottom:20px;">
            <div style="font-size:3em;margin-bottom:10px;">👤</div>
            <div style="font-size:1.2em;font-weight:900;">SEGAH-SG-{st.session_state.username}</div>
            <div style="opacity:0.88;margin-top:5px;">{st.session_state.user_role}</div>
            <div style="font-size:0.82em;margin-top:8px;opacity:0.72;">
                Session : {st.session_state.session_started_at}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        if st.button("🚪 DÉCONNEXION", use_container_width=True):
            logout()

        st.markdown("---")

        st.markdown(f"""
        <div style="text-align:center;opacity:0.75;font-size:0.86em;margin-top:30px;">
            <p><strong>{APP_NAME}</strong> {APP_VERSION}</p>
            <p>Simulation • Crédit • KPI</p>
            <p>© 2026</p>
        </div>
        """, unsafe_allow_html=True)


def render_top_header():
    """Affiche l'en-tête principal avec le nom de l'application et l'heure."""
    st.markdown(f"""
    <div class="top-hero">
        <h1>🏦 {APP_NAME} — Interface V4</h1>
        <p>
            Bienvenue <strong>{st.session_state.username}</strong> • 
            {st.session_state.user_role} • 
            {datetime.now().strftime('%d/%m/%Y %H:%M')}
        </p>
    </div>
    """, unsafe_allow_html=True)


# =====================================================================
# 🚀 MAIN APPLICATION
# =====================================================================

def main():
    """Point d'entrée principal de l'application."""
    apply_custom_css()
    init_session_state()
    init_usage_tracking()

    if not st.session_state.authenticated:
        login_page()
        return

    render_sidebar()
    render_top_header()

    # Déterminer les modules accessibles
    available_modules = []
    if "salary" in st.session_state.user_modules:
        available_modules.append("💼 Simulation Salaire")
    if "loan" in st.session_state.user_modules:
        available_modules.append("💳 Simulation Prêt")
    if "admin" in st.session_state.user_modules:
        available_modules.append("🛡️ Administration KPI")

    if len(available_modules) > 1:
        tabs = st.tabs(available_modules)
        for i, tab in enumerate(tabs):
            with tab:
                if available_modules[i] == "💼 Simulation Salaire":
                    module_simulation_salaire()
                elif available_modules[i] == "💳 Simulation Prêt":
                    module_simulation_pret()
                elif available_modules[i] == "🛡️ Administration KPI":
                    module_admin_kpi()
    else:
        if "salary" in st.session_state.user_modules:
            module_simulation_salaire()
        elif "loan" in st.session_state.user_modules:
            module_simulation_pret()
        elif "admin" in st.session_state.user_modules:
            module_admin_kpi()

    # Pied de page
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center;color:#666;font-size:0.9em;padding:18px;">
        <p>🏦 <strong>{APP_NAME} {APP_VERSION}</strong> • Application confidentielle • Tous droits réservés</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
