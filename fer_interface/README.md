**`/fer`** - Codurile sursă necesare pentru integrarea modelului în interfață. Cod sursă pentru încarcarea modelului, pentru utilizarea acestuia in aplicație și pentru salvarea log-urilor.

**`/static`** - Conține fișierele statice utilizate în aplicația web. Imagini, fișiere CSS (Cascading Style Sheets), fișiere JavaScript, fișierele necesare in construirea și utilizarea modelului pentru recunoașterea expresiilor faciale.

**`/templates`** - Conține fișierele de șablon HTML utilizate pentru generarea și afișarea paginilor web în cadrul aplicației.

**`app.py`** - Reprezintă fișierul principal care servește ca punct de intrare pentru aplicația Flask. Acesta conține codul necesar pentru definirea și configurarea aplicației Flask, inclusiv rute, view-uri și alte funcționalități specifice aplicației.

**`requirements.txt`** - Este un fișier folosit pentru a specifica bibliotecile externe și dependențele cerute de aplicație.

**_Configurarea aplicației_**

Creează un nou mediu virtual utilizând modulul venv integrat în Python.

`python3 -m venv venv`

Activează mediul virtual, folosind comanda corespunzătoare sistemului de operare:
* Pe Windows: 
    `venv\Scripts\activate.bat`
* Pe macOS/Linux:
    `source venv/bin/activate`

Se instalează pachetele din requirements.txt utilizând comanda pip:

`pip install -r requirements.txt`
