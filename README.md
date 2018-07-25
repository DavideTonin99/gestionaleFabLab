# Managament for Verona FabLab - Gestionale per Verona FabLab

Project written using Django-framework, html5, css, javascript
Progetto scritto con Django-framework, html5, css, javascript

---

### ESEGUIRE L'APPLICAZIONE IN LOCALE
1. Installare python 3.6 se non è già installato
2. Scaricare il progetto
3. Aprire il file ``gestionale/settings.py``, commentare sotto la linea 33, la parte riguardante il database per la produzione (per heroku) e scommentare la parte del database per locale
4. Aprire una finestra del cmd/terminale ed entrare nella cartella del progetto
5. Eseguire il comando ``pip3 install -r requirements.txt`` per installare tutte le librerie necessarie
6. Eseguire il comando ``python3 manage.py migrate`` per creare il database
7. Eseguire il comando ``python3 manage.py createsuperuser`` per poter accedere alla pagina di admin di Django e all'applicazione
8. Eseguire il comando ``python3 manage.py runserver``
9. Aprire un browser alla pagina ``http://localhost:8000`` o ``http://127.0.0.1:8000``
---


### RUN THE APP LOCALLY
1. Install python 3.6
2. Download the project
3. Open the file `` gestionale / settings.py``, comment under line 33, the part concerning the database for production (for heroku) and discomment the part of the database for local
4. Open a CMD/Terminal window and enter the project folder
5. Run the command ``pip3 install -r requirements.txt`` to install all necessary libraries
6. Run the command ``python3 manage.py migrate`` to create the database
7. Run the command ``python3 manage.py createsuperuser`` to access the Django admin page and to the application
8. Run the command ``python3 manage.py runserver``
9. Open a browser on the page ``http://localhost:8000`` or ``http://127.0.0.1:8000``

---
Davide Tonin, Ettore Forigo
