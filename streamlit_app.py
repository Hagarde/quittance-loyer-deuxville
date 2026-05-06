import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- FONCTION : GÉNÉRATION DU PDF ---
def generer_quittance_pro(proprietaire, locataire, adresse, montant_loyer, periode):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Bordure décorative
    pdf.rect(5, 5, 200, 287)
    pdf.rect(7, 7, 196, 283)
    
    # En-tête
    pdf.set_font("Helvetica", 'B', 20)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 20, "QUITTANCE DE LOYER", ln=True, align='C')
    pdf.ln(5)
    
    # Informations Propriétaire & Locataire
    pdf.set_font("Helvetica", 'B', 11)
    pdf.set_text_color(0)
    pdf.cell(95, 10, "PROPRIÉTAIRE :", ln=0)
    pdf.cell(95, 10, "LOCATAIRE :", ln=1)
    
    pdf.set_font("Helvetica", size=11)
    pdf.cell(95, 7, proprietaire, ln=0)
    pdf.cell(95, 7, locataire, ln=1)
    pdf.ln(10)
    
    # Objet de la quittance
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, f" Période : {periode}", ln=1, fill=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 10, f"Adresse du bien : {adresse}")
    pdf.ln(5)

    # Texte légal
    pdf.multi_cell(0, 8, f"Je soussigné(e) {proprietaire}, propriétaire du logement désigné ci-dessus, "
                         f"déclare avoir reçu de la part du locataire M./Mme {locataire}, la somme suivante "
                         f"au titre du paiement du loyer pour la période mentionnée.")
    pdf.ln(10)

    # Tableau des montants
    total = montant_loyer
    
    pdf.set_font("Helvetica", 'B', 11)
    pdf.cell(80, 10, "Désignation", border=1, align='C')
    pdf.cell(50, 10, "Montant (EUR)", border=1, align='C', ln=1)
    
    pdf.set_font("Helvetica", size=11)
    pdf.cell(80, 10, " Loyer principal", border=1)
    pdf.cell(50, 10, f"{montant_loyer:,.2f} EUR", border=1, align='R', ln=1)
    
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(80, 12, " TOTAL REÇU", border=1)
    pdf.cell(50, 12, f"{total:,.2f} EUR", border=1, align='R', ln=1)
    
    # Signature
    pdf.ln(20)
    pdf.set_font("Helvetica", 'I', 10)
    date_jour = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 10, f"Fait à le {date_jour}", ln=1, align='R')
    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 11)
    pdf.cell(0, 10, "Signature du Propriétaire", ln=1, align='R')

    # --- MÉTHODE DE GÉNÉRATION EN MÉMOIRE (SANS ÉCRIRE SUR LE DISQUE) ---
    try:
        # Essaye la méthode moderne (fpdf2)
        resultat = pdf.output()
        if isinstance(resultat, bytearray):
            return bytes(resultat)
        else:
            return str(resultat).encode('latin-1')
    except Exception:
        # Si erreur, utilise l'ancienne méthode (fpdf classique)
        return pdf.output(dest='S').encode('latin-1')

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Générateur de Quittance", page_icon="📄")

# --- SYSTÈME DE PROFIL PAR MOT DE PASSE ---
st.sidebar.title("🔐 Accès Rapide")
mot_de_passe = st.sidebar.text_input("Mot de passe profil", type="password")

defaut_proprio = ""
defaut_locataire = ""
defaut_adresse = ""
defaut_loyer = 0.0

if mot_de_passe == "secret2026":
    st.sidebar.success("Profil déverrouillé !")
    defaut_proprio = "ORY Jean-Paul et Myriam"
    defaut_locataire = "Blond Mathis et Thiery Mélanie"
    defaut_adresse = "16 Bis Rue St Epvre, 54370 DEUXVILLE"
    defaut_loyer = 900.0
elif mot_de_passe != "":
    st.sidebar.error("Mot de passe incorrect")

# --- INTERFACE PRINCIPALE ---
st.title("📄 Générateur de Quittance de Loyer")
st.info("Remplissez les informations et téléchargez instantanément votre PDF professionnel.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Parties")
    proprio = st.text_input("Votre Nom (Propriétaire)", value=defaut_proprio)
    locataire = st.text_input("Nom du Locataire", value=defaut_locataire)

with col2:
    st.subheader("💰 Montants")
    loyer = st.number_input("Loyer (€)", value=defaut_loyer, step=10.0)

st.subheader("🏠 Détails du bien")
adresse = st.text_area("Adresse complète", value=defaut_adresse)
periode = st.text_input("Mois / Période concernée", value="Mai 2026")

st.divider()

if proprio == "" or locataire == "":
    st.warning("Veuillez remplir au moins les noms du propriétaire et du locataire pour générer la quittance.")
else:
    # 1. On génère le fichier
    pdf_bytes = generer_quittance_pro(proprio, locataire, adresse, loyer, periode)

    # 2. On affiche le diagnostic pour être sûr que ça a marché
    taille = len(pdf_bytes)
    if taille > 0:
        st.success(f"✅ Document prêt ! (Taille générée : {taille} octets)")
        
        # 3. On affiche le bouton seulement si le fichier fait plus de 0 octet
        st.download_button(
            label="📥 Télécharger la Quittance (PDF)",
            data=pdf_bytes,
            file_name=f"Quittance_{locataire.replace(' ', '_')}_{periode.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.error("❌ Erreur critique : Le document généré est vide.")