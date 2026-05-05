import streamlit as st
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import os

# --- FONCTION : GÉNÉRATION DU PDF ---
def generer_quittance_pdf(nom_locataire, adresse, montant, date_mois):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # En-tête
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="QUITTANCE DE LOYER", ln=True, align='C')
    pdf.ln(10)
    
    # Corps du document
    pdf.set_font("Arial", size=12)
    texte = (
        f"Je soussigné(e), Propriétaire, déclare avoir reçu de :\n"
        f"M./Mme {nom_locataire}\n\n"
        f"La somme de {montant} euros, au titre du loyer et des charges \n"
        f"pour le mois de {date_mois}, concernant le logement situé au :\n"
        f"{adresse}\n\n"
        f"Cette quittance annule tous les reçus donnés précédemment pour \n"
        f"le même mois.\n\n"
        f"Fait pour valoir ce que de droit."
    )
    pdf.multi_cell(0, 10, txt=texte)
    
    # Sauvegarde temporaire du fichier
    nom_fichier = "quittance_temp.pdf"
    pdf.output(nom_fichier)
    return nom_fichier

# --- FONCTION : ENVOI DE L'EMAIL ---
def envoyer_email(email_destinataire, fichier_pdf, email_expediteur, mdp_app):
    msg = EmailMessage()
    msg['Subject'] = 'Votre quittance de loyer'
    msg['From'] = email_expediteur
    msg['To'] = email_destinataire
    msg.set_content("Bonjour,\n\nVeuillez trouver ci-joint votre quittance de loyer pour ce mois.\n\nCordialement,")

    # Pièce jointe
    with open(fichier_pdf, 'rb') as f:
        pdf_data = f.read()
    
    msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='Quittance_de_loyer.pdf')

    # Connexion SMTP (Exemple configuré pour Gmail)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_expediteur, mdp_app)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Erreur lors de l'envoi de l'e-mail : {e}")
        return False

# --- INTERFACE STREAMLIT ---
st.title("📄 Générateur et Envoi de Quittance de Loyer")

st.markdown("Remplissez les champs ci-dessous. Certains sont pré-remplis pour vous faire gagner du temps.")

# Utilisation d'un formulaire pour regrouper les actions
with st.form("formulaire_quittance"):
    st.subheader("Informations de la quittance")
    
    # Champs pré-remplis via le paramètre 'value'
    nom_locataire = st.text_input("Nom du locataire", value="Jean Dupont")
    adresse = st.text_area("Adresse du bien", value="10 Rue de la Paix, 75000 Paris")
    montant = st.number_input("Montant (en €)", value=850.00, step=10.00)
    date_mois = st.text_input("Mois concerné", value="Mai 2026")
    
    st.subheader("Informations d'envoi")
    email_destinataire = st.text_input("Email du locataire", value="locataire@exemple.com")
    
    # Pour la sécurité, il vaut mieux stocker ces informations dans st.secrets en production
    email_expediteur = st.text_input("Votre Email (Expéditeur Gmail)")
    mdp_app = st.text_input("Votre Mot de Passe d'Application", type="password", help="Utilisez un mot de passe d'application, pas votre mot de passe classique.")
    
    bouton_soumettre = st.form_submit_button("Générer et Envoyer")

# --- TRAITEMENT APRÈS SOUMISSION ---
if bouton_soumettre:
    if not email_expediteur or not mdp_app:
        st.warning("Veuillez renseigner votre email et votre mot de passe d'application.")
    else:
        with st.spinner("Génération du PDF et envoi de l'e-mail en cours..."):
            # 1. Générer le PDF
            fichier_pdf = generer_quittance_pdf(nom_locataire, adresse, montant, date_mois)
            
            # 2. Envoyer l'e-mail
            succes = envoyer_email(email_destinataire, fichier_pdf, email_expediteur, mdp_app)
            
            # 3. Nettoyer le fichier temporaire et afficher le résultat
            if os.path.exists(fichier_pdf):
                os.remove(fichier_pdf)
                
            if succes:
                st.success(f"✅ La quittance a été générée et envoyée avec succès à {email_destinataire} !")