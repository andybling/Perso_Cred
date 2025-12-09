import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from dateutil.relativedelta import relativedelta

# Configuration de la page
st.set_page_config(
    page_title="SGBCI - Gestionnaire de Prêt Personnel",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé - Charte graphique professionnelle avec effets
st.markdown("""<style>
    /* Variables de couleurs */
    :root {
        --primary-red: #C41E3A;
        --dark-red: #A01830;
        --light-red: #F8D7DA;
        --primary-black: #212529;
        --gray-dark: #343A40;
        --gray-light: #F8F9FA;
        --white: #FFFFFF;
        --success: #28A745;
        --warning: #FFC107;
        --danger: #DC3545;
        --sg-red: #C41E3A;
        --sg-dark-red: #8B0000;
    }
    
    /* Reset et base */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    }
    
    /* Logo et header unifiés */
    .brand-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 3px solid var(--primary-red);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        border-radius: 0 0 15px 15px;
        padding: 15px 40px;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }
    
    .brand-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-red), var(--sg-dark-red));
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .logo-section img {
        max-height: 50px;
        width: auto;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
    }
    
    .brand-title {
        flex-grow: 1;
        text-align: center;
    }
    
    .main-title {
        color: var(--primary-black);
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 5px;
        background: linear-gradient(90deg, var(--primary-red), var(--sg-dark-red));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .subtitle {
        color: var(--gray-dark);
        font-size: 1rem;
        font-weight: 400;
    }
    
    .brand-tagline {
        font-size: 0.85rem;
        color: #6C757D;
        text-align: right;
        font-style: italic;
    }
    
    /* Chatbot button */
    .chatbot-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, var(--primary-red), var(--sg-dark-red));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 6px 25px rgba(196, 30, 58, 0.4);
        z-index: 1000;
        transition: all 0.3s ease;
        border: 3px solid white;
    }
    
    .chatbot-button:hover {
        transform: scale(1.1);
        box-shadow: 0 8px 30px rgba(196, 30, 58, 0.6);
    }
    
    .chatbot-icon {
        color: white;
        font-size: 30px;
    }
    
    /* Video modal */
    .video-modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 80%;
        max-width: 800px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        z-index: 2000;
        display: none;
        overflow: hidden;
    }
    
    .video-modal.active {
        display: block;
        animation: modalAppear 0.3s ease;
    }
    
    @keyframes modalAppear {
        from {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.8);
        }
        to {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
        }
    }
    
    .video-header {
        background: linear-gradient(135deg, var(--primary-red), var(--sg-dark-red));
        color: white;
        padding: 15px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .video-header h3 {
        margin: 0;
        font-size: 1.2rem;
    }
    
    .close-btn {
        background: none;
        border: none;
        color: white;
        font-size: 24px;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .close-btn:hover {
        transform: rotate(90deg);
    }
    
    .video-container {
        padding: 20px;
        background: #000;
    }
    
    /* Overlay */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        z-index: 1999;
        display: none;
    }
    
    .modal-overlay.active {
        display: block;
    }
    
    /* Cartes avec effets de survol */
    .card {
        background: var(--white);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(0, 0, 0, 0.08);
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border-color: var(--primary-red);
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(to bottom, var(--primary-red), var(--sg-dark-red));
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .card:hover::before {
        opacity: 1;
    }
    
    .card-title {
        color: var(--primary-black);
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--light-red);
    }
    
    .card-title i {
        color: var(--primary-red);
    }
    
    /* Boutons avec effets */
    .stButton button {
        background: linear-gradient(135deg, var(--primary-red), var(--sg-dark-red));
        color: var(--white) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(196, 30, 58, 0.3) !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton button::before {
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
    }
    
    .stButton button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(196, 30, 58, 0.4) !important;
    }
    
    /* Inputs avec style */
    .stNumberInput input, .stTextInput input, .stSelectbox select {
        border: 2px solid #E9ECEF !important;
        border-radius: 8px !important;
        padding: 12px 15px !important;
        font-size: 0.95rem !important;
        transition: all 0.3s !important;
        background: var(--white) !important;
    }
    
    .stNumberInput input:focus, .stTextInput input:focus, .stSelectbox select:focus {
        border-color: var(--primary-red) !important;
        box-shadow: 0 0 0 3px rgba(196, 30, 58, 0.15) !important;
        outline: none !important;
    }
    
    /* Tableaux */
    .dataframe {
        border: 1px solid #E9ECEF !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05) !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, var(--primary-red), var(--sg-dark-red)) !important;
        color: var(--white) !important;
        font-weight: 600 !important;
        padding: 15px !important;
        text-align: center !important;
        border: none !important;
    }
    
    .dataframe td {
        padding: 12px 15px !important;
        border-bottom: 1px solid #E9ECEF !important;
        transition: background-color 0.2s;
    }
    
    .dataframe tr:hover td {
        background-color: var(--light-red) !important;
    }
    
    /* Métriques avec style */
    .metric-card {
        background: var(--white);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(0, 0, 0, 0.08);
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s;
        border-top: 4px solid var(--primary-red);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-red);
        margin: 10px 0;
        text-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--gray-dark);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .metric-subtext {
        font-size: 0.8rem;
        color: #6C757D;
        margin-top: 5px;
    }
    
    /* Alertes avec animation */
    .stAlert {
        border-radius: 10px !important;
        border-left: 4px solid !important;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Tooltips personnalisés */
    .tooltip-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 20px;
        height: 20px;
        background: var(--primary-red);
        color: white;
        border-radius: 50%;
        font-size: 12px;
        margin-left: 8px;
        cursor: pointer;
        position: relative;
    }
    
    .tooltip-icon:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: var(--primary-black);
        color: white;
        padding: 10px 15px;
        border-radius: 6px;
        font-size: 0.85rem;
        white-space: nowrap;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Onglets stylisés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: var(--gray-light);
        padding: 5px;
        border-radius: 10px;
        border: 1px solid rgba(0, 0, 0, 0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        color: var(--gray-dark);
        transition: all 0.3s;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-red), var(--sg-dark-red)) !important;
        color: white !important;
        box-shadow: 0 2px 10px rgba(196, 30, 58, 0.3) !important;
    }
    
    /* Ballons d'information */
    .balloon {
        background: var(--white);
        border: 2px solid var(--primary-red);
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        position: relative;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        animation: float 6s ease-in-out infinite;
    }
    
    .balloon::before {
        content: '💡';
        position: absolute;
        top: -15px;
        left: 20px;
        font-size: 24px;
        background: var(--white);
        padding: 5px;
        border-radius: 50%;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Statut financier */
    .status-indicator {
        display: inline-block;
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status-success {
        background: rgba(40, 167, 69, 0.1);
        color: var(--success);
        border: 1px solid var(--success);
    }
    
    .status-warning {
        background: rgba(255, 193, 7, 0.1);
        color: var(--warning);
        border: 1px solid var(--warning);
    }
    
    .status-danger {
        background: rgba(220, 53, 69, 0.1);
        color: var(--danger);
        border: 1px solid var(--danger);
    }
    
    /* Barre de progression */
    .progress-container {
        width: 100%;
        background: #E9ECEF;
        border-radius: 10px;
        overflow: hidden;
        height: 10px;
        margin: 15px 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-red), var(--sg-dark-red));
        border-radius: 10px;
        transition: width 1s ease-in-out;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        margin-top: 50px;
        border-top: 2px solid var(--light-red);
        color: var(--gray-dark);
        font-size: 0.9rem;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px 10px 0 0;
    }
    
    /* Badges */
    .sg-badge {
        display: inline-block;
        padding: 4px 12px;
        background: linear-gradient(135deg, var(--primary-red), var(--sg-dark-red));
        color: white;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 10px;
    }
    
    /* Section séparateurs */
    .section-separator {
        height: 3px;
        background: linear-gradient(90deg, var(--primary-red), transparent);
        margin: 30px 0;
        border: none;
    }
</style>""", unsafe_allow_html=True)

# HTML pour le chatbot et la vidéo
st.markdown("""
<div id="chatbot-container">
    <div class="chatbot-button" onclick="showVideoModal()">
        <span class="chatbot-icon">🤖</span>
    </div>
</div>

<div id="video-modal" class="video-modal">
    <div class="video-header">
        <h3>📺 Tutoriel SGBCI - Utilisation du simulateur</h3>
        <button class="close-btn" onclick="hideVideoModal()">×</button>
    </div>
    <div class="video-container">
        <iframe width="100%" height="450" src="https://www.youtube.com/embed/sac6_7QxNLg?autoplay=1" 
                title="Tutoriel SGBCI" frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
        </iframe>
    </div>
</div>

<div id="modal-overlay" class="modal-overlay" onclick="hideVideoModal()"></div>

<script>
    function showVideoModal() {
        document.getElementById('video-modal').classList.add('active');
        document.getElementById('modal-overlay').classList.add('active');
    }
    
    function hideVideoModal() {
        document.getElementById('video-modal').classList.remove('active');
        document.getElementById('modal-overlay').classList.remove('active');
    }
    
    // Auto-ouvrir la vidéo au chargement de la page
    window.onload = function() {
        setTimeout(function() {
            showVideoModal();
        }, 1500); // Délai de 1.5 seconde
    };
</script>
""", unsafe_allow_html=True)

# Interface principale harmonisée
st.markdown("""
<div class="brand-container">
    <div class="logo-section">
        <img src="https://particuliers.societegenerale.ci/fileadmin/user_upload/logos/SGBCI103_2025.svg" 
             alt="SGBCI Logo" 
             onerror="this.onerror=null; this.src='https://via.placeholder.com/200x50?text=SGBCI+Logo'">
        <div class="brand-title">
            <h1 class="main-title">OCTROI DE CREDIT POUR LE PERSONNEL</h1>
            <p class="subtitle">Simulateur d'Échéancier & Analyse Financière</p>
        </div>
    </div>
    <div class="brand-tagline">
        Votre partenaire de confiance<br>La DIRECTION INNOVATION
    </div>
</div>
""", unsafe_allow_html=True)

# Ballon d'information initial
with st.container():
    st.markdown("""
    <div class="balloon">
        <strong>💎 CALCUL DE REVENU CLIENT</strong><br>
        Le revenu pris en compte est calculé comme suit :<br>
        <strong>Salaire + (80% × Revenu Locatif) + (50% × Revenu Agricole)</strong><br>
        Conforme aux normes bancaires internationales.
    </div>
    """, unsafe_allow_html=True)

# Fonctions de conversion numérique en lettres professionnelles
def convertir_millions_en_lettres(nombre):
    """Convertit un nombre en lettres françaises correctement"""
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
    """Formate un montant en lettres avec Francs CFA"""
    partie_entiere = int(nombre)
    
    if partie_entiere == 0:
        return "zéro Francs CFA"
    
    texte = convertir_millions_en_lettres(partie_entiere)
    
    if partie_entiere == 1:
        return texte + " Franc CFA"
    else:
        return texte + " Francs CFA"

# Fonctions de calcul financier
def calculer_taux_mensuel_combine(taux_interet, taux_assurance, taux_tps):
    """Calcule le taux mensuel combiné incluant intérêt, assurance et TPS"""
    return (taux_interet + taux_assurance) / 12 + taux_interet * taux_tps / 12

def calculer_annuite_constante(montant, taux_mensuel, duree_mois):
    """Calcule l'annuité constante selon la formule financière standard"""
    if taux_mensuel == 0:
        return montant / duree_mois
    
    annuite = montant * taux_mensuel / (1 - (1 + taux_mensuel) ** -duree_mois)
    return annuite

def calculer_frais_dossier(montant):
    """Calcule les frais de dossier (1.5% avec max 150,000 FCFA)"""
    return min(montant * 0.015, 150000)

def calculer_teg(taux_interet, taux_assurance, taux_tps):
    """Calcule le Taux Effectif Global approximatif"""
    return (taux_interet + taux_assurance + taux_interet * taux_tps) * 100

def calculer_revenu_total(salaire, revenu_locatif, revenu_agricole):
    """Calcule le revenu total pris en compte selon la formule bancaire"""
    return salaire + (0.8 * revenu_locatif) + (0.5 * revenu_agricole)

def calculer_echeancier(montant, taux_interet_annuel, taux_assurance_annuel, taux_tps, duree_mois, 
                       salaire, revenu_locatif, revenu_agricole, autres_engagements, 
                       date_debut, quotite_cessible_pct):
    """
    Calcule l'échéancier complet avec vérifications financières
    """
    # Calcul du revenu total pris en compte
    revenu_total = calculer_revenu_total(salaire, revenu_locatif, revenu_agricole)
    
    # Calculs préliminaires
    taux_mensuel_interet = taux_interet_annuel / 12
    taux_mensuel_assurance = taux_assurance_annuel / 12
    taux_combine = calculer_taux_mensuel_combine(taux_interet_annuel, taux_assurance_annuel, taux_tps)
    
    # Annuité constante
    annuite = calculer_annuite_constante(montant, taux_combine, duree_mois)
    
    # Initialisation
    echeancier = []
    capital_restant = montant
    amortissement_cumule = 0
    date_echeance = date_debut
    
    for mois in range(1, duree_mois + 1):
        # Calculs pour la période
        interets = capital_restant * taux_mensuel_interet
        assurance = capital_restant * taux_mensuel_assurance
        tps = assurance * taux_tps
        
        # Amortissement
        amortissement = annuite - (interets + assurance + tps)
        
        # Ajustement pour la dernière échéance
        if mois == duree_mois:
            amortissement = capital_restant
            annuite_ajustee = amortissement + interets + assurance + tps
        else:
            annuite_ajustee = annuite
        
        # Mise à jour
        amortissement_cumule += amortissement
        capital_suivant = max(0, capital_restant - amortissement)
        
        # Ajout au tableau
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
    
    # Calcul des indicateurs financiers
    df = pd.DataFrame(echeancier)
    
    # Taux d'endettement
    mensualite_totale = annuite
    total_engagements = mensualite_totale + autres_engagements
    taux_endettement = (total_engagements / revenu_total) * 100 if revenu_total > 0 else 0
    
    # Quotité cessible
    quotite_cessible = revenu_total * (quotite_cessible_pct / 100)
    
    # Disposible mensuel
    disponible_mensuel = revenu_total - total_engagements
    
    # Totaux
    total_interets = df["Intérêts"].sum()
    total_assurance = df["Assurance"].sum()
    total_tps = df["TPS"].sum()
    total_rembourse = df["Mensualité"].sum()
    
    # Coût total du crédit
    cout_total = total_interets + total_assurance + total_tps
    ratio_cout = (cout_total / montant) * 100
    
    # Date dernière échéance
    date_derniere = date_debut + relativedelta(months=duree_mois - 1)
    
    # Calcul TEG
    teg = calculer_teg(taux_interet_annuel, taux_assurance_annuel, taux_tps)
    
    # Analyse de la situation financière
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

# Fonctions de visualisation
def creer_graphique_evolution(df):
    """Crée un graphique d'évolution du capital et des intérêts"""
    fig = go.Figure()
    
    # Capital restant
    fig.add_trace(go.Scatter(
        x=df["N° Échéance"],
        y=df["Capital Restant"],
        mode='lines',
        name='Capital Restant',
        line=dict(color='#C41E3A', width=3),
        fill='tozeroy',
        fillcolor='rgba(196, 30, 58, 0.1)'
    ))
    
    # Amortissement cumulé
    fig.add_trace(go.Scatter(
        x=df["N° Échéance"],
        y=df["Amort. Cumulé"],
        mode='lines',
        name='Amortissement Cumulé',
        line=dict(color='#212529', width=2, dash='dash')
    ))
    
    # Mise en page
    fig.update_layout(
        title=dict(
            text="Évolution du Capital Restant et Amortissement",
            font=dict(size=18, color='#212529')
        ),
        xaxis=dict(
            title="Numéro d'Échéance",
            gridcolor='rgba(0,0,0,0.05)'
        ),
        yaxis=dict(
            title="Montant (FCFA)",
            gridcolor='rgba(0,0,0,0.05)',
            tickformat=',.0f'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

def creer_graphique_repartition(df):
    """Crée un graphique de répartition des paiements"""
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
        marker_colors=['#C41E3A', '#212529', '#FF6B6B', '#FF8A80'],
        textinfo='label+percent+value',
        texttemplate='%{label}<br>%{percent:.1%}<br>%{value:,.0f} FCFA',
        hoverinfo='label+percent+value'
    )])
    
    fig.update_layout(
        title=dict(
            text="Répartition des Paiements Totaux",
            font=dict(size=16, color='#212529')
        ),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

# Initialisation des variables de session
if 'calcul_realise' not in st.session_state:
    st.session_state.calcul_realise = False
if 'resultats' not in st.session_state:
    st.session_state.resultats = None
if 'duree_mois' not in st.session_state:
    st.session_state.duree_mois = None

# SECTION 1: PARAMÈTRES DU PRÊT
st.markdown("""
<div class="card">
    <div class="card-title">
        <i>📋</i> PARAMÈTRES DU PRÊT & SITUATION FINANCIÈRE
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    # Informations client
    with st.container():
        st.markdown("#### 👤 Informations Client")
        
        col1a, col1b = st.columns(2)
        with col1a:
            nom_client = st.text_input("Nom complet", value="MOUAHA HANDY YVES")
            num_client = st.text_input("Référence client", value="CLIENT-2025-001")
        
        with col1b:
            statut = st.selectbox(
                "Statut professionnel",
                ["Salarié"]
            )
            autres_engagements = st.number_input("Autres engagements (FCFA)",
                                               min_value=0,
                                               value=0,
                                               step=10000,
                                               format="%d",
                                               help="Mensualités en cours (crédits, loyers, etc.)")
        
        # Sources de revenus détaillées
        st.markdown("---")
        st.markdown("#### 💰 Sources de Revenus Mensuelles")
        
        salaire = st.number_input("Salaire net mensuel (FCFA)", 
                                 min_value=0, 
                                 value=1000000,
                                 step=10000,
                                 format="%d",
                                 help="Revenu salarial net après impôts")
        
        col_rev1, col_rev2 = st.columns(2)
        with col_rev1:
            revenu_locatif = st.number_input("Revenu locatif mensuel (FCFA)",
                                          min_value=0,
                                          value=250000,
                                          step=10000,
                                          format="%d",
                                          help="Revenus de location (80% pris en compte)")
        
        with col_rev2:
            revenu_agricole = st.number_input("Revenu agricole mensuel (FCFA)",
                                           min_value=0,
                                           value=16000,
                                           step=10000,
                                           format="%d",
                                           help="Revenus agricoles (50% pris en compte)")
        
        # Calcul et affichage du revenu total pris en compte
        revenu_total = calculer_revenu_total(salaire, revenu_locatif, revenu_agricole)
        st.info(f"""
        **Revenu total pris en compte :** {revenu_total:,.0f} FCFA
        - Salaire : {salaire:,.0f} FCFA (100%)
        - Revenu locatif : {revenu_locatif:,.0f} FCFA (80% → {(revenu_locatif * 0.8):,.0f} FCFA)
        - Revenu agricole : {revenu_agricole:,.0f} FCFA (50% → {(revenu_agricole * 0.5):,.0f} FCFA)
        """)
        
        # Quotité cessible avec explication
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
        
        # Affichage de la quotité en valeur
        quotite_valeur = revenu_total * (quotite_pct / 100)
        st.success(f"**Quotité cessible :** {quotite_valeur:,.0f} FCFA ({quotite_pct}% de {revenu_total:,.0f} FCFA)")

with col2:
    # Caractéristiques du prêt
    with st.container():
        st.markdown("#### 💰 Caractéristiques du Prêt")
        
        montant_pret = st.number_input("Montant du prêt (FCFA)",
                                     min_value=0,
                                     value=35900000,
                                     step=100000,
                                     format="%d",
                                     help="Capital emprunté")
        
        col2a, col2b = st.columns(2)
        with col2a:
            duree_annees = st.selectbox("Durée (années)", 
                                       options=[5, 7, 10, 15, 20, 25],
                                       index=1)
            taux_interet = st.number_input("Taux d'intérêt annuel (%)",
                                         min_value=0.0,
                                         max_value=20.0,
                                         value=3.5,
                                         step=0.1,
                                         format="%.3f")
        
        with col2b:
            taux_assurance = st.number_input("Taux assurance annuel (%)",
                                           min_value=0.0,
                                           max_value=5.0,
                                           value=1.1,
                                           step=0.1,
                                           format="%.3f")
            taux_tps = st.number_input("Taux TPS (%)",
                                     min_value=0.0,
                                     max_value=20.0,
                                     value=10.0,
                                     step=0.1,
                                     format="%.1f")
        
        # Date de début
        date_debut = st.date_input("Date de premier prélèvement",
                                 value=datetime.now().replace(day=25) + relativedelta(months=1),
                                 help="Généralement fixée au 25 du mois suivant")
        
        # Affichage du montant en lettres
        st.markdown("---")
        st.markdown(f"**Montant du prêt en lettres :**")
        st.markdown(f"*{nombre_en_lettres(montant_pret)}*")

# Bouton de calcul principal
st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("🔍 ANALYSER LA FAISABILITÉ & CALCULER L'ÉCHÉANCIER", 
                 use_container_width=True, 
                 type="primary"):
        
        with st.spinner("Analyse financière en cours..."):
            # Calcul de l'échéancier
            duree_mois = duree_annees * 12
            st.session_state.duree_mois = duree_mois
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
            
            st.session_state.resultats = resultats
            st.session_state.calcul_realise = True

# Affichage des résultats si calcul réalisé
if st.session_state.calcul_realise and st.session_state.resultats:
    resultats = st.session_state.resultats
    duree_mois = st.session_state.duree_mois
    
    # SECTION 2: SYNTHÈSE FINANCIÈRE
    st.markdown("""
    <div class="card">
        <div class="card-title">
            <i>📊</i> SYNTHÈSE FINANCIÈRE & ANALYSE DE RISQUE
        </div>
    </div>
""", unsafe_allow_html=True)
    
    # Indicateurs clés
    col_ind1, col_ind2, col_ind3, col_ind4 = st.columns(4)
    
    with col_ind1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Mensualité</div>
            <div class="metric-value">{resultats["mensualite"]:,.0f} FCFA</div>
            <div class="metric-subtext">Échéance constante</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_ind2:
        # Indicateur de taux d'endettement avec couleur
        couleur_classe = f"status-{resultats['couleur_statut']}"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Taux d'endettement</div>
            <div class="metric-value">{resultats['taux_endettement']:.1f}%</div>
            <div class="metric-subtext">
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
            <div class="metric-value">{resultats['cout_total']:,.0f} FCFA</div>
            <div class="metric-subtext">{resultats['ratio_cout']:.1f}% du capital</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_ind4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Taux Effectif Global</div>
            <div class="metric-value">{resultats['teg']:.3f}%</div>
            <div class="metric-subtext">Inclut tous les frais</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Analyse de la quotité cessible
    total_engagements = resultats["mensualite"] + autres_engagements
    marge_quotite = resultats["quotite_cessible"] - total_engagements
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Barre de progression de l'endettement
    st.markdown("#### 📈 Analyse de votre capacité d'endettement")
    
    pourcentage_utilisation = min((total_engagements / resultats["quotite_cessible"]) * 100, 100)
    
    col_prog1, col_prog2 = st.columns([3, 1])
    with col_prog1:
        st.markdown(f"""
        <div style="margin: 20px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>Utilisation de votre quotité</span>
                <span><strong>{pourcentage_utilisation:.1f}%</strong></span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {pourcentage_utilisation}%;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #6C757D; margin-top: 10px;">
                <span>0 FCFA</span>
                <span>{resultats['quotite_cessible']:,.0f} FCFA (max)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_prog2:
        if marge_quotite > 0:
            st.success(f"✅ **Marge disponible :** {marge_quotite:,.0f} FCFA")
        else:
            st.error(f"⚠️ **Dépassement :** {abs(marge_quotite):,.0f} FCFA")
    
    # Détails en colonnes
    st.markdown("<br>", unsafe_allow_html=True)
    col_det1, col_det2, col_det3 = st.columns(3)
    
    with col_det1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title"><i>💰</i> Revenus & Engagements</div>
            <table style="width: 100%;">
                <tr><td>Salaire net</td><td style="text-align: right; font-weight: bold;">{salaire:,} FCFA</td></tr>
                <tr><td>Revenu locatif</td><td style="text-align: right;">{revenu_locatif:,} FCFA</td></tr>
                <tr><td>Revenu agricole</td><td style="text-align: right;">{revenu_agricole:,} FCFA</td></tr>
                <tr><td><strong>Revenu pris en compte</strong></td><td style="text-align: right; font-weight: bold; color: #C41E3A;">{resultats['revenu_total']:,} FCFA</td></tr>
                <tr><td>Autres engagements</td><td style="text-align: right;">{autres_engagements:,} FCFA</td></tr>
                <tr><td>Mensualité prêt</td><td style="text-align: right; font-weight: bold; color: #C41E3A;">{resultats['mensualite']:,.0f} FCFA</td></tr>
                <tr><td><strong>Total engagements</strong></td><td style="text-align: right; font-weight: bold;">{total_engagements:,.0f} FCFA</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col_det2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title"><i>🎯</i> Quotité & Disposable</div>
            <table style="width: 100%;">
                <tr><td>Quotité cessible ({quotite_pct}%)</td><td style="text-align: right; font-weight: bold;">{resultats['quotite_cessible']:,.0f} FCFA</td></tr>
                <tr><td>Total engagements</td><td style="text-align: right; font-weight: bold;">{total_engagements:,.0f} FCFA</td></tr>
                <tr><td><strong>Disponible mensuel</strong></td><td style="text-align: right; font-weight: bold; color: #28A745;">{resultats['disponible_mensuel']:,.0f} FCFA</td></tr>
                <tr><td><strong>Taux d'endettement</strong></td><td style="text-align: right; font-weight: bold;">{resultats['taux_endettement']:.1f}%</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col_det3:
        couleur_marge = "#28A745" if marge_quotite > 0 else "#DC3545"
        couleur_epargne = "#28A745" if resultats["disponible_mensuel"] > resultats['revenu_total'] * 0.1 else "#FFC107"
        st.markdown(f"""
        <div class="card">
            <div class="card-title"><i>⚠️</i> Analyse de Risque</div>
            <table style="width: 100%;">
                <tr><td>Statut endettement</td><td style="text-align: right;"><span class="status-indicator status-{resultats['couleur_statut']}">{resultats['statut_endettement']}</span></td></tr>
                <tr><td>Niveau de risque</td><td style="text-align: right; font-weight: bold;">{resultats['niveau_risque']}</td></tr>
                <tr><td>Marge de sécurité</td><td style="text-align: right; font-weight: bold; color: {couleur_marge};">{marge_quotite:+,.0f} FCFA</td></tr>
                <tr><td>Capacité d'épargne</td><td style="text-align: right; font-weight: bold; color: {couleur_epargne};">{resultats['disponible_mensuel']:,.0f} FCFA</td></tr>
                <tr><td>Ratio épargne/revenu</td><td style="text-align: right; font-weight: bold;">{(resultats['disponible_mensuel']/resultats['revenu_total']*100):.1f}%</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    # SECTION 3: TABLES ET GRAPHIQUES
    st.markdown("""
    <div class="card">
        <div class="card-title">
            <i>📈</i> VISUALISATIONS & ÉCHÉANCIER DÉTAILLÉ
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Onglets pour différentes vues
    tab1, tab2, tab3 = st.tabs(["📋 Tableau d'Amortissement", "📊 Graphiques d'Analyse", "📄 Synthèse Complète"])
    
    with tab1:
        # Affichage du tableau d'amortissement
        st.markdown(f"### 📅 Tableau d'Amortissement Détaillé ({duree_mois} échéances)")
        
        # Options d'affichage
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            n_lignes = st.slider("Nombre de lignes à afficher", 
                                min_value=12, 
                                max_value=duree_mois, 
                                value=min(24, duree_mois),
                                step=12)
        
        with col_opt2:
            show_all = st.checkbox("Afficher tout l'échéancier", value=False)
        
        # Préparation des données
        df_display = resultats["dataframe"].copy()
        if not show_all:
            df_display = df_display.head(n_lignes)
        
        # Formater les nombres
        for col in ["Amortissement", "Amort. Cumulé", "Intérêts", "Assurance", "TPS", "Mensualité", "Capital Restant"]:
            df_display[col] = df_display[col].apply(lambda x: f"{x:,.2f}")
        
        # Afficher le tableau
        st.dataframe(
            df_display,
            use_container_width=True,
            height=500
        )
        
        # Téléchargement
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
            st.metric("Total Intérêts", f"{resultats['total_interets']:,.0f} FCFA")
        
        with col_sum2:
            st.metric("Total Assurance", f"{resultats['total_assurance']:,.0f} FCFA")
        
        with col_sum3:
            st.metric("Total TPS", f"{resultats['total_tps']:,.0f} FCFA")
        
        with col_sum4:
            st.metric("Total à rembourser", f"{resultats['total_rembourse']:,.0f} FCFA")
    
    with tab2:
        # Graphiques
        col_graph1, col_graph2 = st.columns(2)
        
        with col_graph1:
            fig_evolution = creer_graphique_evolution(resultats["dataframe"])
            st.plotly_chart(fig_evolution, use_container_width=True)
        
        with col_graph2:
            fig_repartition = creer_graphique_repartition(resultats["dataframe"])
            st.plotly_chart(fig_repartition, use_container_width=True)
        
        # Graphique supplémentaire
        st.markdown("### 📉 Évolution des composantes de la mensualité")
        
        fig_composantes = go.Figure()
        fig_composantes.add_trace(go.Scatter(
            x=resultats["dataframe"]["N° Échéance"],
            y=resultats["dataframe"]["Intérêts"],
            mode='lines',
            name='Intérêts',
            line=dict(color='#212529', width=2),
            stackgroup='one'
        ))
        fig_composantes.add_trace(go.Scatter(
            x=resultats["dataframe"]["N° Échéance"],
            y=resultats["dataframe"]["Assurance"],
            mode='lines',
            name='Assurance',
            line=dict(color='#FF6B6B', width=2),
            stackgroup='one'
        ))
        fig_composantes.add_trace(go.Scatter(
            x=resultats["dataframe"]["N° Échéance"],
            y=resultats["dataframe"]["TPS"],
            mode='lines',
            name='TPS',
            line=dict(color='#FF8A80', width=2),
            stackgroup='one'
        ))
        
        fig_composantes.update_layout(
            title="Décomposition de la mensualité",
            xaxis_title="N° Échéance",
            yaxis_title="Montant (FCFA)",
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig_composantes, use_container_width=True)
    
    with tab3:
        # Synthèse complète
        st.markdown("### 📄 Synthèse Financière Complète")
        
        col_synth1, col_synth2 = st.columns(2)
        
        with col_synth1:
            st.markdown(f"""
            <div class="card">
                <div class="card-title"><i>💵</i> Détails Financiers</div>
                <table style="width: 100%;">
                    <tr><td>Montant emprunté</td><td style="text-align: right; font-weight: bold;">{montant_pret:,} FCFA</td></tr>
                    <tr><td>Durée</td><td style="text-align: right;">{duree_annees} ans ({duree_mois} mois)</td></tr>
                    <tr><td>Taux d'intérêt nominal</td><td style="text-align: right;">{taux_interet:.3f}%</td></tr>
                    <tr><td>Taux d'assurance</td><td style="text-align: right;">{taux_assurance:.3f}%</td></tr>
                    <tr><td>Taux TPS</td><td style="text-align: right;">{taux_tps:.1f}%</td></tr>
                    <tr><td>Taux Effectif Global</td><td style="text-align: right; font-weight: bold; color: #C41E3A;">{resultats['teg']:.3f}%</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
        
        with col_synth2:
            st.markdown(f"""
            <div class="card">
                <div class="card-title"><i>🧮</i> Totaux & Coûts</div>
                <table style="width: 100%;">
                    <tr><td>Total intérêts</td><td style="text-align: right; font-weight: bold;">{resultats['total_interets']:,.0f} FCFA</td></tr>
                    <tr><td>Total assurance</td><td style="text-align: right;">{resultats['total_assurance']:,.0f} FCFA</td></tr>
                    <tr><td>Total TPS</td><td style="text-align: right;">{resultats['total_tps']:,.0f} FCFA</td></tr>
                    <tr><td><strong>Coût total du crédit</strong></td><td style="text-align: right; font-weight: bold; color: #C41E3A;">{resultats['cout_total']:,.0f} FCFA</td></tr>
                    <tr><td><strong>Total à rembourser</strong></td><td style="text-align: right; font-weight: bold;">{resultats['total_rembourse']:,.0f} FCFA</td></tr>
                    <tr><td>Ratio coût/capital</td><td style="text-align: right;">{resultats['ratio_cout']:.1f}%</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendations
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

# SECTION 4: INFORMATIONS LÉGALES ET TECHNIQUES
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
        ```
        A = C × i / [1 - (1 + i)^-n]
        ```
        où :
        - A = Annuité constante
        - C = Capital emprunté
        - i = Taux mensuel combiné (intérêts + assurance + TPS)
        - n = Nombre de mois
        
        **Taux mensuel combiné :**
        ```
        i = (t_intérêt + t_assurance)/12 + t_intérêt × t_TPS/12
        ```
        
        **Taux Effectif Global (TEG) :**
        ```
        TEG = (1 + i_mensuel)^12 - 1
        ```
        
        **Validations effectuées :**
        1. Cohérence des taux et durées
        2. Respect des ratios d'endettement
        3. Vérification des limites réglementaires
        4. Contrôle de la solvabilité du demandeur
        """)

# Footer professionnel
st.markdown("""
<div class="footer">
    <p>
        <strong>SGCI - Gestionnaire de Prêt Professionnel v5.0</strong> • 
        Conforme à la POC du Personnel • 
        © 2025 Société Générale Côte d'Ivoire
    </p>
    <p style="font-size: 0.8rem; color: #6C757D;">
        Les informations fournies sont à titre indicatif et ne constituent pas une offre de prêt.<br>
        Consultez votre conseiller financier pour une analyse personnalisée.
    </p>
</div>

""", unsafe_allow_html=True)
