# HejJakube
Osobní asistent ovládaný mikrofonem volaný příkazem "Hej Jakube".

Záklaní (první) funkce:
- přečtení datumu a času
- předpověd počasí
- přečtení prvních X vět z wikipedie

Využítí služeb:
- Google API - překlad zvuku na text
- SAPI5 (použití implementováno v pyttsx3) - tvoření hlasové odpovědi
- Wit.ai - analyzování textu (zahrnutý klíč k předtrénovanému modelu)
- weatherapi.com - zjišťování počasí

# Instalace:
1. Nainstalovat všechny potřebné knihovny `pip install -r requierements.txt`
2. Přidat model hlasu **Jakub** `Nastavení > Čas a jazyk > Řeč > Přidat hlasy > Čeština`
3. Spustit .reg soubor (případně modifikovat registry ručně), pro změnu `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens\MSTTS_V110_csCZ_Jakub` na `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_csCZ_Jakub`
4. Vytvořit si účet a získat API key na https://www.weatherapi.com a zadat daný klíč na místo `[key]` v `main.py`
5. Spustit aplikaci `python main.py`
