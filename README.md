# Martina

Codi Python que fa funcionar la Martina, el nostre robot familiar.

Aquest projecte conté el codi Python per controlar el robot Martina.

## 🚀 Getting Started

### 📋 Prerequisits

- Python 3.9 o superior

### 🔧 Instal·lació

1. Clona el repositori:
   ```bash
   git clone https://github.com/mnebot/Martina.git
   ```
2. Entra al directori del projecte:
   ```bash
   cd Martina
   ```
3. Instal·la les dependències:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Usage

Per executar el codi, simplement executa el següent comando:

```bash
python martina.py
```

## 🤝 Contributing

Les contribucions són benvingudes! Si us plau, obre un *issue* per discutir els canvis que vols fer.

## 📝 License

Aquest projecte està sota la llicència MIT. Consulta el fitxer [LICENSE](LICENSE) per a més detalls.

## CI/CD

Aquest projecte utilitza GitHub Actions per automatitzar el desplegament del codi.

### Publicació a PyPI

El workflow `publish-to-pypi.yml` s'encarrega de construir el paquet de Python i publicar-lo a PyPI. Aquest workflow s'executa manualment des de la pestanya "Actions" de GitHub.

### Desplegament a la Raspberry Pi

El workflow `deploy-to-pi.yml` s'encarrega de desplegar la darrera versió del paquet a la Raspberry Pi. Aquest workflow s'executa automàticament cada cop que es fa un `push` a la branca `master` o es pot executar manualment.

El workflow fa els següents passos:
1. S'autentica a la xarxa de Tailscale.
2. Es connecta per SSH a la Raspberry Pi.
3. Instal·la o actualitza el paquet `martinaPI` des de PyPI en un entorn virtual.

---

Taulell de Trello: https://trello.com/b/3mHrU0Km