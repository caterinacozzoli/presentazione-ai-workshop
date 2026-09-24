#!/usr/bin/env python3
"""
auth.py — Google OAuth2 one-time setup
Run once: python3 scripts/auth.py
Then run: python3 scripts/write_gdoc.py
"""

import os
import json
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/documents']
TOKEN_FILE = os.path.expanduser('~/.gdoc_token.json')
CREDS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')

def authenticate():
    creds = None

    # Check for existing token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Refresh or get new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("✅ Token rinnovato automaticamente.")
        else:
            if not os.path.exists(CREDS_FILE):
                print(f"""
❌ File credentials.json non trovato in: {CREDS_FILE}

Segui questi passaggi (5 minuti):
1. Vai su: https://console.cloud.google.com/apis/credentials
2. Crea un progetto (o usa uno esistente)
3. Abilita l'API: https://console.cloud.google.com/apis/library/docs.googleapis.com
4. Clicca "Crea credenziali" → "OAuth 2.0 Client ID" → "App desktop"
5. Scarica il JSON e salvalo come: {CREDS_FILE}
6. Riavvia questo script.
""")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            print("🌐 Apertura browser per autorizzazione Google...")
            creds = flow.run_local_server(port=0)
            print("✅ Autenticazione completata!")

        # Save token for future use
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())

    return creds

if __name__ == '__main__':
    creds = authenticate()
    print(f"✅ Autenticato. Token salvato in: {TOKEN_FILE}")
    print("Ora puoi eseguire: python3 scripts/write_gdoc.py")
