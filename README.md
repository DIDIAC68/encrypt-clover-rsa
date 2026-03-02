# 🔐 Clover RSA Encryption

Este repositório contém um script em Python para **criptografar dados de cartões de crédito** usando **RSA com PKCS1_OAEP** e enviá-los para a **API de tokenização da Clover**, retornando um token criptografado em rsa.

---

## 🚀 Funcionalidades

- 🔒 Criptografa PAN (Primary Account Number) com chave pública da Clover
- 📡 Envia os dados criptografados para a API oficial da Clover para gerar token
- 📁 Suporta entrada em lote a partir de arquivo `cards.txt`
- ⚙️ Baseado em `requests` + `pycryptodome`

---

## 📂 Estrutura do Projeto
encrypt-clover-rsa/
├── CloverEncrypt.py # Classe principal de criptografia RSA
├── cards.txt # Lista de cartões no formato: número|mês|ano|cvv
├── README.md # Este arquivo

Instale as bibliotecas necessárias com:
pip install requests pycryptodome

📌 Observações
Os dados são criptografados com a chave pública oficial da Clover (extraída via https://checkout.clover.com/assets/keys.json).

A criptografia é feita no padrão PKCS#1 OAEP com SHA-1, conforme exigido pela API da Clover.

🛡️ Segurança
Este projeto é apenas para fins educacionais e de integração. Nunca armazene ou compartilhe informações reais de cartão de crédito sem estar em conformidade com as normas PCI DSS.

📄 Licença
Este projeto está sob a licença MIT. Sinta-se livre para usar, modificar e contribuir.

🛠️ Tecnologias: Python, RSA, API, Criptografia, Clover
