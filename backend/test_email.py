import smtplib
import os
from dotenv import load_dotenv

print("Cargando variables de entorno...")
load_dotenv()

SENDER_EMAIL = os.environ.get('EMAIL_HOST_USER')
SENDER_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
RECEIVER_EMAIL = SENDER_EMAIL # Nos enviaremos un correo a nosotros mismos

try:
    print(f"Intentando conectar con smtp.gmail.com:587 como {SENDER_EMAIL}...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    
    subject = "Prueba de conexión desde Python"
    body = "Si recibes este correo, la conexión funciona."
    message = f"Subject: {subject}\n\n{body}"
    
    print("Enviando correo...")
    # 👇 CAMBIO REALIZADO AQUÍ para soportar tildes
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.encode('utf-8'))
    server.quit()
    print("¡ÉXITO! El correo se envió correctamente.")

except Exception as e:
    print("\n--- ¡ERROR! ---")
    print(f"No se pudo enviar el correo. El error fue: {e}")