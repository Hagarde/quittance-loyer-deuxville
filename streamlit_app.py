import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- FONCTION : GÉNÉRATION DU PDF AVEC DESIGN AMÉLIORÉ ---
def generer_quittance_pro(proprietaire, locataire, adresse, montant_loyer, periode):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 1. Bordure décorative
    pdf.rect(5, 5, 200, 287) # Cadre extérieur
    pdf.rect(7, 7, 196, 283) # Cadre intérieur
    
    # 2. En-tête
    pdf.set_font("Helvetica", 'B', 20)
    pdf.set_text_color(44, 62, 80) # Bleu foncé professionnel
    pdf.cell(0, 20, "QUITTANCE DE LOYER", ln=True, align='C')
    pdf.ln(5)
    
    # 3. Informations Propriétaire & Locataire
    pdf.set_font("Helvetica", 'B', 11)
    pdf.set_text_color(0)
    pdf.cell(95, 10, "PROPRIÉTAIRE :", ln=0)
    pdf.cell(95, 10, "LOCATAIRE :", ln=1)
    
    pdf.set_font("Helvetica", size=11)
    pdf.cell(95, 7, proprietaire, ln=0)
    pdf.cell(95, 7, locataire, ln=1)
    pdf.ln(10)
    
    # 4. Objet de la quittance
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, f" Période : {periode}", ln=1, fill=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 10, f"Adresse du bien : {adresse}")
    pdf.ln(5)

    # 5. Texte légal
    pdf.multi_cell(0, 8, f"Je soussigné(e) {proprietaire}, propriétaire du logement désigné ci-dessus, "
                         f"déclare avoir reçu de la part du locataire M./Mme {locataire}, la somme suivante "
                         f"au titre du paiement du loyer pour la période mentionnée.")
    pdf.ln(10)

    # 6. Tableau des montants (Le côté "Pro")
    total = montant_loyer 
    
    pdf.set_font("Helvetica", 'B', 11)
    # Entête tableau (Correction ici)
    pdf.cell(80, 10, "Désignation", border=1, align='C')
    pdf.cell(50, 10, "Montant (EUR)", border=1, align='C', ln=1) 
    
    # Lignes (Correction ici également)
    pdf.set_font("Helvetica", size=11)
    pdf.cell(80, 10, " Loyer principal", border=1)
    pdf.cell(50, 10, f"{montant_loyer:,.2f} EUR", border=1, align='R', ln=1)
    
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(80, 12, " TOTAL REÇU", border=1)
    pdf.cell(50, 12, f"{total:,.2f} EUR", border=1, align='R', ln=1)
    
    # 7. Signature
    pdf.ln(20)
    pdf.set_font("Helvetica", 'I', 10)
    date_jour = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 10, f"Fait à Paris, le {date_jour}", ln=1, align='R')
    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 11)
    pdf.cell(0, 10, "Signature du Propriétaire", ln=1, align='R')

    return bytes(pdf.output())

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Générateur de Quittance", page_icon="📄")

st.title("📄 Générateur de Quittance de Loyer")
st.info("Remplissez les informations et téléchargez instantanément votre PDF professionnel.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Parties")
    proprio = st.text_input("Votre Nom (Propriétaire)", value="M. Marc Morel")
    locataire = st.text_input("Nom du Locataire", value="Mme Alice Bernard")

with col2:
    st.subheader("💰 Montants")
    loyer = st.number_input("Loyer (€)", value=750.0, step=10.0)

st.subheader("🏠 Détails du bien")
adresse = st.text_area("Adresse complète", value="15 Rue de Rivoli, 75004 Paris")
periode = st.text_input("Mois / Période concernée", value="Mai 2026")

st.divider()

# Génération du PDF en mémoire
pdf_bytes = generer_quittance_pro(proprio, locataire, adresse, loyer, periode)

# Bouton de téléchargement
st.download_button(
    label="📥 Télécharger la Quittance (PDF)",
    data=pdf_bytes,
    file_name=f"Quittance_{locataire.replace(' ', '_')}_{periode.replace(' ', '_')}.pdf",
    mime="application/pdf",
    use_container_width=True
)

st.caption("Le PDF est généré localement dans votre navigateur. Aucune donnée n'est envoyée par mail.")