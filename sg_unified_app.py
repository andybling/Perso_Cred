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
    page_title="Société Générale - Finance Hub",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Couleurs Société Générale
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
    #"admin": {"password": "admin123", "role": "Administrateur", "modules": ["salary", "loan"]},
    "rh": {"password": "rh2025", "role": "Ressources Humaines", "modules": ["salary"]}#,"credit": {"password": "credit2024", "role": "Analyste Crédit", "modules": ["loan"]},
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
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="sg-logo">🏦</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align: center; color: #E60028; font-weight: 800; font-size: 2.2em;">Société Générale</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; margin-bottom: 40px; font-size: 1.1em;">Finance Hub - Portail Sécurisé</p>', unsafe_allow_html=True)
    
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
        <b>👨‍💼 Administrateur:</b><br>
        • Identifiant: <code>admin</code> | Mot de passe: <code>admin123</code><br><br>
        
        <b>👤 Ressources Humaines:</b><br>
        • Identifiant: <code>rh</code> | Mot de passe: <code>rh2024</code><br><br>
        
        <b>💳 Analyste Crédit:</b><br>
        • Identifiant: <code>credit</code> | Mot de passe: <code>credit2024</code>
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

        # Footer
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9em; padding: 20px;">
            <p>🏦 <strong>Société Générale</strong> • Application confidentielle • Tous droits réservés</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()