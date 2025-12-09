import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import base64
from io import BytesIO

# ═══════════════════════════════════════════════════════════════
# 🎨 CONFIGURATION & DESIGN SYSTEM
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="CHURN",
    page_icon="😒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Couleurs MOUAHA HANDY YVES
SG_RED = "#E60028"
SG_BLACK = "#000000"
SG_WHITE = "#FFFFFF"
SG_GRAY = "#F5F5F5"
SG_DARK_GRAY = "#333333"
SG_LIGHT_RED = "#FFF0F0"

def apply_custom_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .main {{
        background: linear-gradient(135deg, {SG_WHITE} 0%, {SG_GRAY} 100%);
        animation: fadeIn 0.8s ease-in;
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
        from {{ transform: translateX(30px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    
    @keyframes glow {{
        0%, 100% {{ box-shadow: 0 0 20px rgba(230, 0, 40, 0.3); }}
        50% {{ box-shadow: 0 0 40px rgba(230, 0, 40, 0.6); }}
    }}
    
    @keyframes shimmer {{
        0% {{ background-position: -1000px 0; }}
        100% {{ background-position: 1000px 0; }}
    }}
    
    /* Login Container */
    .login-container {{
        background: white;
        border-radius: 25px;
        padding: 60px 50px;
        box-shadow: 0 25px 80px rgba(0,0,0,0.2);
        max-width: 480px;
        margin: 60px auto;
        animation: slideIn 0.6s ease-out;
        border-top: 5px solid {SG_RED};
        position: relative;
        overflow: hidden;
    }}
    
    .login-container::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(230, 0, 40, 0.05), transparent);
        animation: shimmer 3s infinite;
    }}
    
    /* Main Header */
    .sg-header {{
        background: linear-gradient(135deg, {SG_BLACK} 0%, {SG_DARK_GRAY} 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 35px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.25);
        animation: slideIn 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }}
    
    .sg-header::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(230, 0, 40, 0.15), transparent);
        animation: shine 4s infinite;
    }}
    
    @keyframes shine {{
        0% {{ transform: translateX(-100%) translateY(-100%) rotate(45deg); }}
        100% {{ transform: translateX(100%) translateY(100%) rotate(45deg); }}
    }}
    
    .sg-header h1 {{
        margin: 0;
        font-weight: 800;
        font-size: 2.5em;
        position: relative;
        z-index: 1;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }}
    
    .sg-header p {{
        margin: 12px 0 0 0;
        opacity: 0.95;
        font-size: 1.15em;
        position: relative;
        z-index: 1;
        font-weight: 300;
    }}
    
    /* Cards */
    .metric-card {{
        background: white;
        border-radius: 18px;
        padding: 28px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 5px solid {SG_RED};
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideInRight 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(230, 0, 40, 0.03), transparent);
        transition: left 0.5s;
    }}
    
    .metric-card:hover::before {{
        left: 100%;
    }}
    
    .metric-card:hover {{
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 50px rgba(230, 0, 40, 0.25);
        border-left-width: 8px;
    }}
    
    .metric-value {{
        font-size: 2.2em;
        font-weight: 800;
        color: {SG_RED};
        margin: 12px 0;
        letter-spacing: -1px;
    }}
    
    .metric-label {{
        color: {SG_DARK_GRAY};
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
        opacity: 0.8;
    }}
    
    .metric-subtitle {{
        color: #666;
        font-size: 0.85em;
        margin-top: 5px;
        font-weight: 500;
    }}
    
    /* Info Cards */
    .info-card {{
        background: linear-gradient(135deg, {SG_LIGHT_RED} 0%, white 100%);
        border-radius: 15px;
        padding: 20px;
        border: 2px solid rgba(230, 0, 40, 0.1);
        margin: 15px 0;
        transition: all 0.3s ease;
    }}
    
    .info-card:hover {{
        border-color: {SG_RED};
        box-shadow: 0 5px 20px rgba(230, 0, 40, 0.15);
    }}
    
    .info-card-title {{
        font-weight: 700;
        color: {SG_RED};
        font-size: 1.1em;
        margin-bottom: 8px;
    }}
    
    /* Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, {SG_RED} 0%, #B00020 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 35px;
        font-weight: 700;
        font-size: 1.05em;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 6px 20px rgba(230, 0, 40, 0.35);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        position: relative;
        overflow: hidden;
    }}
    
    .stButton>button::before {{
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }}
    
    .stButton>button:hover::before {{
        width: 300px;
        height: 300px;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(230, 0, 40, 0.5);
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {SG_BLACK} 0%, {SG_DARK_GRAY} 100%);
    }}
    
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] .stButton>button {{
        background: linear-gradient(135deg, {SG_RED} 0%, #B00020 100%);
        border: 2px solid white;
    }}
    
    /* Input Fields */
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
    
    /* Tables */
    .dataframe {{
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        font-size: 0.9em;
    }}
    
    .dataframe thead tr th {{
        background: {SG_BLACK} !important;
        color: white !important;
        font-weight: 700;
        padding: 18px 12px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85em;
    }}
    
    .dataframe tbody tr:hover {{
        background: rgba(230, 0, 40, 0.08) !important;
        transform: scale(1.01);
        transition: all 0.2s ease;
    }}
    
    .dataframe tbody td {{
        padding: 14px 12px !important;
        border-bottom: 1px solid #f0f0f0 !important;
    }}
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 15px;
        background: white;
        border-radius: 15px;
        padding: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 10px;
        padding: 12px 25px;
        font-weight: 700;
        transition: all 0.3s ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {SG_RED} !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(230, 0, 40, 0.3);
    }}
    
    /* Success/Warning Messages */
    .stSuccess, .stWarning, .stInfo, .stError {{
        border-radius: 12px;
        padding: 18px;
        animation: slideIn 0.5s ease-out;
        border-left: 5px solid;
        font-weight: 500;
    }}
    
    /* Logo Animation */
    .sg-logo {{
        font-size: 4em;
        text-align: center;
        margin-bottom: 25px;
        animation: pulse 2.5s infinite;
        filter: drop-shadow(0 5px 15px rgba(230, 0, 40, 0.3));
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.08); }}
    }}
    
    /* Section Divider */
    .section-divider {{
        height: 4px;
        background: linear-gradient(90deg, transparent, {SG_RED}, transparent);
        margin: 40px 0;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(230, 0, 40, 0.3);
    }}
    
    /* Progress Bar */
    .progress-bar {{
        height: 8px;
        background: {SG_GRAY};
        border-radius: 10px;
        overflow: hidden;
        margin: 15px 0;
    }}
    
    .progress-fill {{
        height: 100%;
        background: linear-gradient(90deg, {SG_RED}, #FF4D4D);
        border-radius: 10px;
        transition: width 1s ease;
        box-shadow: 0 0 10px rgba(230, 0, 40, 0.5);
    }}
    
    /* Risk Badge */
    .risk-badge {{
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9em;
        margin: 5px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15);
    }}
    
    .risk-low {{
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
    }}
    
    .risk-medium {{
        background: linear-gradient(135deg, #F59E0B, #D97706);
        color: white;
    }}
    
    .risk-high {{
        background: linear-gradient(135deg, #EF4444, #DC2626);
        color: white;
    }}
    
    /* Section Headers */
    .section-header {{
        font-size: 1.4em;
        font-weight: 800;
        color: {SG_BLACK};
        margin: 25px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid {SG_RED};
        display: inline-block;
    }}
    
    /* Tooltips */
    .tooltip {{
        position: relative;
        display: inline-block;
        cursor: help;
        color: {SG_RED};
        font-weight: 700;
    }}
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 🔐 AUTHENTICATION SYSTEM
# ═══════════════════════════════════════════════════════════════

USERS = {
    "admin": {"password": "admin123", "role": "Administrateur", "modules": ["salary", "loan"]},
    "rh": {"password": "rh2025", "role": "Ressources Humaines", "modules": ["salary"]},
    "credit": {"password": "credit2025", "role": "Analyste Crédit", "modules": ["loan"]},
}

def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_modules' not in st.session_state:
        st.session_state.user_modules = []

def login_page():
    st.markdown('<div class="sg-logo">🤷‍♂️</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align: center; color: #E60028; font-weight: 800; font-size: 2.2em;">CHURN</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; margin-bottom: 40px; font-size: 1.1em;">CHURN - Portail Sécurisé</p>', unsafe_allow_html=True)
    
    username = st.text_input("👤 Identifiant", placeholder="Entrez votre identifiant", key="login_username")
    password = st.text_input("🔒 Mot de passe", type="password", placeholder="Entrez votre mot de passe", key="login_password")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 SE CONNECTER", width='stretch'):
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.user_role = USERS[username]["role"]
                st.session_state.user_modules = USERS[username]["modules"]
                st.success("✅ Connexion réussie!")
                st.rerun()
            else:
                st.error("❌ Identifiant ou mot de passe incorrect")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.expander("📋 Comptes de démonstration", expanded=False):
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
        <b>👤 Ressources Humaines:</b><br>
        • Identifiant: <code>rh</code> | Mot de passe: <code>rh2025</code><br><br>
        </div>
        """, unsafe_allow_html=True)

def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_role = None
    st.session_state.user_modules = []
    st.rerun()

# ═══════════════════════════════════════════════════════════════
# 📊 MODULE 1: SIMULATION SALAIRE
# ═══════════════════════════════════════════════════════════════

def calcul_revenu_annuel(salaire_net, mois):
    return salaire_net * mois

def calcul_surcout_credit(encours, taux_actuel, taux_nouveau):
    diff = (taux_nouveau - taux_actuel) / 100
    return (encours * diff) / 12

def calcul_salaire_equivalent(revenu_annuel, mois_nouveau):
    return revenu_annuel / mois_nouveau

def module_simulation_salaire():
    st.markdown('<div class="sg-header"><h1>💼 Simulation Salaire & Mobilité RH</h1><p>Calculez le salaire minimum à négocier lors d\'une mobilité professionnelle</p></div>', unsafe_allow_html=True)
    
    # Section Inputs avec amélioration UX
    st.markdown('<p class="section-header">📋 Informations de Base</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 💰 Situation Actuelle")
        salaire_net = st.number_input("Salaire net mensuel (FCFA)", value=1008071, step=10000, help="Votre salaire mensuel net actuel")
        mois_actuels = st.number_input("Mois payés/an", value=17, min_value=12, max_value=24, help="Nombre de mois de salaire par an (incluant primes)")
        prime_scolarite = st.number_input("Prime scolarité (FCFA)", value=60000, step=5000, help="Prime mensuelle de scolarité")
    
    with col2:
        st.markdown("### 🎯 Nouveau Poste")
        mois_nouveau = st.number_input("Mois payés/an (nouveau)", value=13, min_value=12, max_value=24, help="Nombre de mois au nouveau poste")
        encours_credit = st.number_input("Encours crédit (FCFA)", value=35900000, step=100000, help="Montant restant du crédit")
    
    with col3:
        st.markdown("### 🏦 Conditions Crédit")
        taux_act = st.number_input("Taux actuel (%)", value=3.5, step=0.1, help="Taux d'intérêt actuel (privilège employeur)")
        taux_new = st.number_input("Taux après mobilité (%)", value=10.0, step=0.1, help="Nouveau taux sans privilège")
        cotis_total = st.number_input("Cotisations employeur (FCFA)", value=379356, step=1000, help="Total cotisations sociales mensuelles")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    if st.button("🔍 CALCULER LA SIMULATION", width='stretch'):
        # Calculs
        revenu_annuel = calcul_revenu_annuel(salaire_net, mois_actuels)
        surcout = calcul_surcout_credit(encours_credit, taux_act, taux_new)
        salaire_equiv = calcul_salaire_equivalent(revenu_annuel, mois_nouveau)
        perte_mois = (mois_actuels - mois_nouveau) * salaire_net
        salaire_min_base = salaire_equiv + surcout
        salaire_min_with_cotis = salaire_min_base + cotis_total
        
        # Impact mensuel moyen
        impact_mensuel = perte_mois / 12
        
        st.markdown('<p class="section-header">📊 Résultats de la Simulation</p>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-label">Revenu Annuel Actuel</div>
                <div class="metric-value">{revenu_annuel:,.0f}</div>
                <p class="metric-subtitle">FCFA • Base de calcul</p>
            </div>''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-label">Salaire Équivalent</div>
                <div class="metric-value">{salaire_equiv:,.0f}</div>
                <p class="metric-subtitle">FCFA/mois • Sur {mois_nouveau} mois</p>
            </div>''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-label">Surcoût Crédit</div>
                <div class="metric-value">+{surcout:,.0f}</div>
                <p class="metric-subtitle">FCFA/mois • Différence taux</p>
            </div>''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-label">Perte Annuelle</div>
                <div class="metric-value">-{perte_mois:,.0f}</div>
                <p class="metric-subtitle">FCFA • {mois_actuels - mois_nouveau} mois perdus</p>
            </div>''', unsafe_allow_html=True)
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            st.markdown('<p class="section-header">💰 Salaires Minimum Recommandés</p>', unsafe_allow_html=True)
            
            st.markdown(f'''<div class="info-card">
                <div class="info-card-title">🎯 Niveau 1 : Compensation de Base</div>
                <div style="font-size: 1.8em; font-weight: 800; color: #E60028; margin: 10px 0;">
                    {salaire_min_base:,.0f} FCFA/mois
                </div>
                <p style="color: #666;">Inclut le salaire équivalent + surcoût crédit</p>
            </div>''', unsafe_allow_html=True)
            
            st.markdown(f'''<div class="info-card">
                <div class="info-card-title">⭐ Niveau 2 : Package Complet (Recommandé)</div>
                <div style="font-size: 1.8em; font-weight: 800; color: #E60028; margin: 10px 0;">
                    {salaire_min_with_cotis:,.0f} FCFA/mois
                </div>
                <p style="color: #666;">Inclut compensation des cotisations employeur</p>
            </div>''', unsafe_allow_html=True)
            
            # Barre de progression pour visualiser l'écart
            ecart_percentage = ((salaire_min_with_cotis - salaire_net) / salaire_net) * 100
            st.markdown(f'''
            <div style="margin-top: 20px;">
                <p style="font-weight: 600; color: #333;">Augmentation nécessaire : <span style="color: #E60028; font-size: 1.2em; font-weight: 800;">+{ecart_percentage:.1f}%</span></p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {min(ecart_percentage, 100)}%;"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<p class="section-header">🎯 Recommandations RH</p>', unsafe_allow_html=True)
            
            recommendations = [
                ("💼 Package Global", "Négocier un package net-à-net incluant tous les avantages"),
                ("🏥 Santé", "Maintien couverture santé ou compensation équivalente"),
                ("🏦 Crédit", "Refinancement avant mobilité ou indemnité de rachat"),
                ("🎁 Mobilité", "Bonus de mobilité pour compenser la perte de mois"),
                ("📋 Fiscal", "Clause de neutralité fiscale pour 12-18 mois"),
                ("💰 Retraite", "Compensation cotisations retraite CNPS/CRRAE")
            ]
            
            for emoji_title, desc in recommendations:
                st.markdown(f'''
                <div style="background: white; padding: 12px; border-radius: 10px; margin-bottom: 10px; 
                            border-left: 3px solid #E60028; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                    <div style="font-weight: 700; color: #E60028; margin-bottom: 3px;">{emoji_title}</div>
                    <div style="font-size: 0.9em; color: #666;">{desc}</div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Analyse détaillée
        st.markdown('<p class="section-header">📈 Analyse d\'Impact Détaillée</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📉 Pertes")
            st.markdown(f"- **Mois perdus:** {mois_actuels - mois_nouveau} mois")
            st.markdown(f"- **Impact mensuel:** {impact_mensuel:,.0f} FCFA")
            st.markdown(f"- **Prime scolarité:** {prime_scolarite:,.0f} FCFA/mois")
            st.markdown(f"- **Cotisations:** {cotis_total:,.0f} FCFA/mois")
        
        with col2:
            st.markdown("### 💸 Surcoûts")
            st.markdown(f"- **Crédit mensuel:** +{surcout:,.0f} FCFA")
            st.markdown(f"- **Crédit annuel:** +{surcout * 12:,.0f} FCFA")
            st.markdown(f"- **Écart taux:** {taux_new - taux_act:.1f}%")
        
        with col3:
            st.markdown("### ✅ Actions Prioritaires")
            st.markdown("1. **Négociation package**")
            st.markdown("2. **Refinancement crédit**")
            st.markdown("3. **Clause santé**")
            st.markdown("4. **Bonus mobilité**")

# ═══════════════════════════════════════════════════════════════
# 💳 MODULE 2: SIMULATION PRÊT (Mensualité Constante)
# ═══════════════════════════════════════════════════════════════

# Groupes basés sur le REVENU client (et non le montant du prêt)
INCOME_GROUPS = [
    {'max_income': 250000, 'group': 'Groupe 1', 'max_ratio': 0.35, 'color': '#10B981'},
    {'max_income': 450000, 'group': 'Groupe 2', 'max_ratio': 0.37, 'color': '#3B82F6'},
    {'max_income': 1000000, 'group': 'Groupe 3', 'max_ratio': 0.40, 'color': '#8B5CF6'},
    {'max_income': 2000000, 'group': 'Groupe 4', 'max_ratio': 0.42, 'color': '#F59E0B'},
    {'max_income': float('inf'), 'group': 'Groupe 5', 'max_ratio': 0.45, 'color': '#E60028'}
]

def get_client_group(income):
    """Détermine le groupe du client basé sur son revenu"""
    for group_info in INCOME_GROUPS:
        if income <= group_info['max_income']:
            return group_info
    return INCOME_GROUPS[-1]

def calculate_constant_payment(loan_amount, annual_rate, duration_months):
    """Calcule la mensualité CONSTANTE selon la formule standard"""
    if loan_amount <= 0 or annual_rate <= 0 or duration_months <= 0:
        return 0
    
    monthly_rate = annual_rate / 12
    
    # Formule de l'annuité constante: M = C * [i(1+i)^n] / [(1+i)^n - 1]
    payment = loan_amount * (monthly_rate * (1 + monthly_rate)**duration_months) / ((1 + monthly_rate)**duration_months - 1)
    
    return payment

def calculate_amortization_schedule_constant(loan_amount, interest_rate, insurance_rate, duration_years, first_date):
    """Calcule le tableau d'amortissement avec MENSUALITÉ CONSTANTE"""
    
    duration_months = duration_years * 12
    tps_rate = 0.10  # 10% TPS
    
    # Taux global (intérêt + assurance)
    global_rate = interest_rate + insurance_rate
    
    # Calcul de la mensualité CONSTANTE (capital + intérêts + assurance)
    monthly_payment_base = calculate_constant_payment(loan_amount, global_rate, duration_months)
    
    schedule = []
    remaining_capital = loan_amount
    
    for month in range(1, duration_months + 1):
        # Date de paiement
        payment_date = first_date + timedelta(days=30 * (month - 1))
        
        # Intérêts sur le capital restant
        interest = remaining_capital * (interest_rate / 12)
        
        # Assurance sur le capital restant
        insurance = remaining_capital * (insurance_rate / 12)
        
        # Amortissement (capital remboursé) = mensualité base - intérêts - assurance
        principal = monthly_payment_base - interest - insurance
        
        # Ajustement pour le dernier mois (éviter les arrondis négatifs)
        if month == duration_months:
            principal = remaining_capital
            monthly_payment_base = principal + interest + insurance
        
        # TPS sur le total
        tps = monthly_payment_base * tps_rate
        
        # Mensualité totale TTC
        total_payment = monthly_payment_base + tps
        
        # Mise à jour du capital restant
        remaining_capital -= principal
        
        schedule.append({
            'N°': month,
            'Date': payment_date.strftime('%d/%m/%Y'),
            'Principal': round(principal, 2),
            'Intérêts': round(interest, 2),
            'Assurance': round(insurance, 2),
            'Sous-total HT': round(monthly_payment_base, 2),
            'TPS (10%)': round(tps, 2),
            'Mensualité TTC': round(total_payment, 2),
            'Capital Restant': round(max(0, remaining_capital), 2)
        })
    
    return pd.DataFrame(schedule)

def get_risk_assessment(debt_ratio, max_ratio):
    """Évalue le niveau de risque"""
    if debt_ratio <= max_ratio * 0.85:
        return "FAIBLE", "🟢", "risk-low"
    elif debt_ratio <= max_ratio:
        return "MODÉRÉ", "🟡", "risk-medium"
    else:
        return "ÉLEVÉ", "🔴", "risk-high"

def module_simulation_pret():
    st.markdown('<div class="sg-header"><h1>💳 Simulateur de Prêt Personnel</h1><p>Calculez votre capacité d\'emprunt avec mensualités constantes et groupe basé sur revenus</p></div>', unsafe_allow_html=True)
    
    # Section Inputs
    st.markdown('<p class="section-header">📋 Paramètres du Prêt</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 💰 Montant & Revenus")
        client_income = st.number_input("💵 Revenu mensuel net (FCFA)", value=1500000, step=50000, 
                                       help="Votre revenu mensuel net - détermine votre groupe")
        loan_amount = st.number_input("🏦 Montant du prêt (FCFA)", value=10000000, step=100000,
                                     help="Montant que vous souhaitez emprunter")
    
    with col2:
        st.markdown("### ⏱️ Durée & Taux")
        duration_years = st.slider("📅 Durée du prêt (années)", 1, 30, 7,
                                   help="Durée de remboursement en années")
        interest_rate = st.number_input("📊 Taux d'intérêt annuel (%)", value=3.5, step=0.1,
                                       help="Taux d'intérêt annuel nominal") / 100
        insurance_rate = st.number_input("🛡️ Taux d'assurance annuel (%)", value=1.1, step=0.1,
                                        help="Taux d'assurance décès-invalidité") / 100
    
    with col3:
        st.markdown("### 📅 Première Échéance")
        first_date = st.date_input("🗓️ Date du 1er prélèvement", value=datetime.now().date(),
                                   help="Date de début des remboursements")
        
        # Affichage du groupe client
        if client_income > 0:
            group_info = get_client_group(client_income)
            st.markdown(f'''
            <div style="background: linear-gradient(135deg, {group_info['color']}, {group_info['color']}dd); 
                        padding: 15px; border-radius: 12px; margin-top: 15px; color: white; text-align: center;">
                <div style="font-size: 1.1em; font-weight: 700; margin-bottom: 5px;">
                    {group_info['group']}
                </div>
                <div style="font-size: 1.4em; font-weight: 800;">
                    Ratio max: {group_info['max_ratio']*100:.0f}%
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    if st.button("🔍 CALCULER LE PRÊT", width='stretch'):
        if loan_amount > 0 and client_income > 0:
            
            # Détermination du groupe
            group_info = get_client_group(client_income)
            
            # Calcul des valeurs
            duration_months = duration_years * 12
            processing_fee = min(loan_amount * 0.015, 150000)
            
            # Calcul de la mensualité CONSTANTE
            global_rate = interest_rate + insurance_rate
            monthly_payment_base = calculate_constant_payment(loan_amount, global_rate, duration_months)
            tps = monthly_payment_base * 0.10
            monthly_payment_total = monthly_payment_base
            
            # Taux d'endettement
            debt_ratio = (monthly_payment_total / client_income) * 100
            max_ratio = group_info['max_ratio'] * 100
            
            # Capacité d'emprunt théorique
            max_payment = client_income * group_info['max_ratio']
            max_loan = (max_payment * ((1 + global_rate/12)**duration_months - 1)) / (global_rate/12 * (1 + global_rate/12)**duration_months)
            
            # Évaluation du risque
            risk_level, risk_emoji, risk_class = get_risk_assessment(debt_ratio, max_ratio)
            
            # Génération du tableau d'amortissement
            schedule = calculate_amortization_schedule_constant(loan_amount, interest_rate, insurance_rate, duration_years, first_date)
            
            total_paid = schedule['Mensualité TTC'].sum()
            total_interest = schedule['Intérêts'].sum()
            total_insurance = schedule['Assurance'].sum()
            total_tps = schedule['TPS (10%)'].sum()
            total_cost = total_interest + total_insurance + total_tps
            
            # Section Résultats
            st.markdown('<p class="section-header">📊 Résultats de la Simulation</p>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f'''<div class="metric-card">
                    <div class="metric-label">Mensualité Constante</div>
                    <div class="metric-value">{monthly_payment_total:,.0f}</div>
                    <p class="metric-subtitle">FCFA • Sur {duration_months} mois</p>
                </div>''', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'''<div class="metric-card">
                    <div class="metric-label">Total à Rembourser</div>
                    <div class="metric-value">{total_paid:,.0f}</div>
                    <p class="metric-subtitle">FCFA • Capital + coûts</p>
                </div>''', unsafe_allow_html=True)
            
            with col3:
                st.markdown(f'''<div class="metric-card">
                    <div class="metric-label">Coût Total du Crédit</div>
                    <div class="metric-value">{total_cost:,.0f}</div>
                    <p class="metric-subtitle">FCFA • Intérêts + assurance + TPS</p>
                </div>''', unsafe_allow_html=True)
            
            with col4:
                st.markdown(f'''<div class="metric-card">
                    <div class="metric-label">Taux d'Endettement</div>
                    <div class="metric-value">{risk_emoji} {debt_ratio:.1f}%</div>
                    <p class="metric-subtitle">{risk_level} • Max {max_ratio:.0f}%</p>
                </div>''', unsafe_allow_html=True)
            
            # Barre de progression endettement
            st.markdown(f'''
            <div style="margin: 25px 0;">
                <p style="font-weight: 700; font-size: 1.1em; color: #333; margin-bottom: 10px;">
                    Taux d'endettement : {debt_ratio:.1f}% / {max_ratio:.0f}% maximum pour votre groupe
                </p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {min(debt_ratio/max_ratio*100, 100)}%; 
                         background: linear-gradient(90deg, {'#10B981' if debt_ratio <= max_ratio*0.85 else '#F59E0B' if debt_ratio <= max_ratio else '#EF4444'}, 
                         {'#059669' if debt_ratio <= max_ratio*0.85 else '#D97706' if debt_ratio <= max_ratio else '#DC2626'});"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            
            # Détails et Analyse
            col1, col2 = st.columns([1, 1.2])
            
            with col1:
                st.markdown('<p class="section-header">💡 Détails du Prêt</p>', unsafe_allow_html=True)
                
                details = [
                    ("💰 Capital emprunté", f"{loan_amount:,.0f} FCFA"),
                    ("📊 Taux d'intérêt", f"{interest_rate*100:.2f}% / an"),
                    ("🛡️ Taux d'assurance", f"{insurance_rate*100:.2f}% / an"),
                    ("📈 Taux global", f"{global_rate*100:.2f}% / an"),
                    ("💼 Frais de dossier", f"{processing_fee:,.0f} FCFA"),
                    ("📅 Durée", f"{duration_years} ans ({duration_months} mois)"),
                    ("🏦 Groupe client", f"{group_info['group']} (revenu: {client_income:,.0f} FCFA)"),
                ]
                
                for label, value in details:
                    st.markdown(f'''
                    <div style="background: white; padding: 12px; border-radius: 10px; margin-bottom: 8px;
                                border-left: 3px solid #E60028; display: flex; justify-content: space-between;">
                        <span style="font-weight: 600; color: #333;">{label}</span>
                        <span style="font-weight: 700; color: #E60028;">{value}</span>
                    </div>
                    ''', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<p class="section-header">📈 Analyse & Recommandations</p>', unsafe_allow_html=True)
                
                # Évaluation du dossier
                if debt_ratio <= max_ratio * 0.85:
                    st.success(f"""
                    **✅ DOSSIER EXCELLENT**
                    
                    Votre taux d'endettement ({debt_ratio:.1f}%) est largement en dessous du maximum autorisé ({max_ratio:.0f}%).
                    
                    💰 **Capacité restante:** {max_payment - monthly_payment_total:,.0f} FCFA/mois
                    
                    📊 **Vous pourriez emprunter jusqu'à:** {max_loan:,.0f} FCFA
                    """)
                elif debt_ratio <= max_ratio:
                    st.warning(f"""
                    **⚠️ DOSSIER ACCEPTABLE**
                    
                    Votre taux d'endettement ({debt_ratio:.1f}%) est proche du maximum ({max_ratio:.0f}%).
                    
                    💡 **Recommandations:**
                    - Envisager une durée plus longue pour réduire la mensualité
                    - Augmenter l'apport personnel si possible
                    - Vérifier la stabilité de vos revenus
                    """)
                else:
                    excess = monthly_payment_total - max_payment
                    reduced_loan = max_loan * 0.95  # 95% de la capacité max
                    
                    st.error(f"""
                    **❌ DOSSIER À RISQUE**
                    
                    Votre taux d'endettement ({debt_ratio:.1f}%) dépasse le maximum autorisé ({max_ratio:.0f}%).
                    
                    ⚠️ **Dépassement:** {excess:,.0f} FCFA/mois
                    
                    💡 **Solutions:**
                    - Réduire le montant à {reduced_loan:,.0f} FCFA
                    - Augmenter la durée à {duration_years + 2} ans
                    - Ajouter un co-emprunteur
                    """)
                
                # Répartition des coûts
                st.markdown("### 📊 Répartition des Coûts")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    pct_interest = (total_interest / total_paid) * 100
                    st.metric("Intérêts", f"{pct_interest:.1f}%", f"{total_interest:,.0f} FCFA")
                with col_b:
                    pct_insurance = (total_insurance / total_paid) * 100
                    st.metric("Assurance", f"{pct_insurance:.1f}%", f"{total_insurance:,.0f} FCFA")
                with col_c:
                    pct_tps = (total_tps / total_paid) * 100
                    st.metric("TPS", f"{pct_tps:.1f}%", f"{total_tps:,.0f} FCFA")
            
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            
            # Tableau d'amortissement
            st.markdown('<p class="section-header">📋 Tableau d\'Amortissement Détaillé</p>', unsafe_allow_html=True)
            
            # Formatage du DataFrame pour l'affichage
            display_df = schedule.copy()
            for col in ['Principal', 'Intérêts', 'Assurance', 'Sous-total HT', 'TPS (10%)', 'Mensualité TTC', 'Capital Restant']:
                display_df[col] = display_df[col].apply(lambda x: f"{x:,.2f} FCFA")
            
            st.dataframe(display_df, width='stretch', height=450)
            
            # Résumé du tableau
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.info(f"**📊 Échéances:** {len(schedule)}")
            with col2:
                st.info(f"**💰 Intérêts totaux:** {total_interest:,.0f} FCFA")
            with col3:
                st.info(f"**🛡️ Assurance totale:** {total_insurance:,.0f} FCFA")
            with col4:
                st.info(f"**📄 TPS total:** {total_tps:,.0f} FCFA")
            
        else:
            st.warning("⚠️ Veuillez renseigner le montant du prêt ET votre revenu mensuel pour lancer la simulation.")

# ═══════════════════════════════════════════════════════════════
# 🚀 MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════

def main():
    apply_custom_css()
    init_session_state()
    
    if not st.session_state.authenticated:
        login_page()
    else:
        # Sidebar
        with st.sidebar:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 15px; margin-bottom: 20px;">
                <div style="font-size: 3em; margin-bottom: 10px;">👤</div>
                <div style="font-size: 1.2em; font-weight: 700;">{st.session_state.username}</div>
                <div style="opacity: 0.9; margin-top: 5px;">{st.session_state.user_role}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            if st.button("🚪 DÉCONNEXION", width='stretch'):
                logout()
            
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; opacity: 0.7; font-size: 0.85em; margin-top: 30px;">
                <p>MOUAHA HANDY YVES</p>
                <p>CHURN v2.0</p>
                <p>© 2025</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Header principal
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {SG_BLACK}, {SG_RED}); color: white; 
                    padding: 25px 30px; border-radius: 18px; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
            <h2 style="margin: 0; font-weight: 800; font-size: 1.8em;">🏦 MOUAHA HANDY YVES CHURN</h2>
            <p style="margin: 8px 0 0 0; opacity: 0.95; font-size: 1.05em;">
                Bienvenue, <strong>{st.session_state.username}</strong> • {datetime.now().strftime('%A %d %B %Y • %H:%M')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Module Selection avec tabs améliorés
        available_modules = []
        if "salary" in st.session_state.user_modules:
            available_modules.append("💼 Simulation Salaire")
        if "loan" in st.session_state.user_modules:
            available_modules.append("💳 Simulation Prêt")
        
        if len(available_modules) > 1:
            tabs = st.tabs(available_modules)
            
            for i, tab in enumerate(tabs):
                with tab:
                    if available_modules[i] == "💼 Simulation Salaire":
                        module_simulation_salaire()
                    elif available_modules[i] == "💳 Simulation Prêt":
                        module_simulation_pret()
        else:
            if "salary" in st.session_state.user_modules:
                module_simulation_salaire()
            elif "loan" in st.session_state.user_modules:
                module_simulation_pret()
        
        # Footer
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9em; padding: 20px;">
            <p>🏦 <strong>MOUAHA HANDY YVES</strong> • Application confidentielle • Tous droits réservés</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
