import streamlit as st
import gspread
from streamlit_calendar import calendar
from datetime import datetime, timedelta

# Configurarea paginii
st.set_page_config(layout="wide", page_title="Calendar Menstrual Pro", page_icon="🌸")

# ==========================================
# 💅 DESIGN ȘI ASPECT (MACHIAJUL DIGITAL)
# ==========================================
# Ascundem bara de sus și footer-ul Streamlit pentru un aspect de aplicație nativă
st.markdown("""
<style>
    /* Ascundem meniul Streamlit (hamburger) și footer-ul tehnic */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Fundalul general - un roz extrem de deschis, cald și prietenos */
    .stApp {
        background-color: #FAFAFA; 
    }

    /* Stilizarea textelor principale cu o culoare roz-coral caldă */
    h1, h2, h3 {
        color: #D6336C !important;
        font-family: 'Arial', sans-serif;
    }

    /* Design-ul pentru noile carduri cu informații de jos */
    .stMetricCard {
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); /* O umbră fină */
        text-align: center;
        border-top: 6px solid #FF85B3; /* O dungă roz sus */
        margin-bottom: 20px;
    }
    .stMetricCard-label {
        color: #D6336C;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .stMetricCard-value {
        color: #FF1493;
        font-size: 2.2rem;
        font-weight: 800;
    }

    /* Stilizarea butoanelor pentru a fi roz, rotunjite și animate */
    .stButton>button {
        border-radius: 30px !important;
        background-color: #FF85B3 !important; /* Un roz cald */
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 6px rgba(255,133,179,0.3) !important;
        transition: all 0.3s ease 0s;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #FF6699 !important;
        transform: translateY(-2px); /* Efect de ridicare */
        box-shadow: 0 6px 8px rgba(255,133,179,0.4) !important;
    }

    /* Meniurile de selecție și căsuțele de text mai rotunjite */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        border-radius: 15px !important;
        border: 1px solid #FFC0CB !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔒 1. SISTEMUL DE SECURITATE (LACĂTUL)
# ==========================================
if 'autentificat' not in st.session_state:
    st.session_state['autentificat'] = False

if not st.session_state['autentificat']:
    st.title("🔒 Acces Securizat")
    st.write("Aplicația este blocată. Introdu codul PIN pentru a continua.")
    
    parola = st.text_input("Introdu PIN-ul:", type="password")
    
    if st.button("Deblochează"):
        if parola == "1234": # <--- AICI SCHIMBI PIN-UL DORIT!
            st.session_state['autentificat'] = True
            st.rerun() # Reîncarcă pagina pentru a arăta calendarul
        else:
            st.error("PIN incorect!")
            
    # Comanda asta oprește execuția codului de mai jos dacă nu e autentificată
    st.stop() 


# ==========================================
# 🌸 RESTUL APLICAȚIEI (Dacă PIN-ul e corect)
# ==========================================
st.title("🌸 Calendarul Tău Inteligent")

# 1. Conexiunea cu Google 
gc = gspread.service_account(filename='credentials.json')
tabel_menstruatie = gc.open("Date_Calendar").sheet1
tabel_jurnal = gc.open("Date_Calendar").worksheet("Jurnal") 

istoric = tabel_menstruatie.get_all_records()
istoric_jurnal = tabel_jurnal.get_all_records()

# 2. CALCULE MEDII
if istoric:
    durate_ciclu = [int(r['Durata_Ciclu']) for r in istoric if str(r['Durata_Ciclu']).isdigit()]
    medie_ciclu = sum(durate_ciclu) / len(durate_ciclu) if durate_ciclu else 28
    
    durate_menstr = [int(r['Durata_Menstruatie']) for r in istoric if str(r['Durata_Menstruatie']).isdigit()]
    medie_menstr = sum(durate_menstr) / len(durate_menstr) if durate_menstr else 5
else:
    medie_ciclu = 28
    medie_menstr = 5

# 3. GENERARE EVENIMENTE CALENDAR (Mai colorate)
calendar_events = []

# --- A. Evenimentele din Jurnal (Emoji-urile) ---
if istoric_jurnal:
    for rand in istoric_jurnal:
        data_jurnal = str(rand['Data']).split(" ")[0]
        detalii = rand['Intimitate']
        calendar_events.append({
            "title": f"❤️ {detalii}",
            "start": data_jurnal,
            "end": data_jurnal,
            "color": "transparent",
            "textColor": "#D6336C", # Text clar, roz
            "borderColor": "transparent",
            "allDay": True
        })

# --- B. Menstruația (Trecut și Viitor) ---
if istoric:
    # Trecutul
    for r in istoric:
        data_inceput = datetime.strptime(str(r['Data_Inceput']).split(" ")[0], '%Y-%m-%d')
        data_sfarsit = data_inceput + timedelta(days=int(r['Durata_Menstruatie']))
        calendar_events.append({
            "title": "🩸 Menstruație",
            "start": data_inceput.strftime('%Y-%m-%d'),
            "end": data_sfarsit.strftime('%Y-%m-%d'),
            "color": "#FF4B4B",
            "textColor": "white",
            "borderColor": "transparent",
            "allDay": True
        })

    # Viitorul (Predicții pe 4 luni)
    ultima_data_str = str(istoric[-1]['Data_Inceput']).split(" ")[0]
    ultima_data_dt = datetime.strptime(ultima_data_str, '%Y-%m-%d')

    for i in range(1, 5):
        viitoare_menstr_start = ultima_data_dt + timedelta(days=int(medie_ciclu) * i)
        viitoare_menstr_end = viitoare_menstr_start + timedelta(days=int(medie_menstr))
        calendar_events.append({
            "title": "🩸 (Prezis)",
            "start": viitoare_menstr_start.strftime('%Y-%m-%d'),
            "end": viitoare_menstr_end.strftime('%Y-%m-%d'),
            "color": "#FFB6C1", # Roz deschis pentru viitor
            "textColor": "#D6336C",
            "borderColor": "transparent",
            "allDay": True
        })

        ovulatie_max = viitoare_menstr_start - timedelta(days=14)
        calendar_events.append({
            "title": "💎 Ovulație",
            "start": ovulatie_max.strftime('%Y-%m-%d'),
            "end": ovulatie_max.strftime('%Y-%m-%d'),
            "color": "#9370DB", # Mov pentru ovulație
            "textColor": "white",
            "borderColor": "transparent",
            "allDay": True
        })

        feritla_start = ovulatie_max - timedelta(days=3)
        feritla_end = ovulatie_max + timedelta(days=2)
        calendar_events.append({
            "title": "✨ Fertilă",
            "start": feritla_start.strftime('%Y-%m-%d'),
            "end": feritla_end.strftime('%Y-%m-%d'),
            "color": "#E6E6FA", # Lavandă extrem de deschisă
            "textColor": "#9370DB",
            "borderColor": "transparent",
            "allDay": True
        })

# 4. AFIȘARE CALENDAR (În temă luminoasă)
calendar_options = {
    "editable": False,
    "selectable": True,
    "timeZone": "UTC",
    "headerToolbar": {"left": "today prev,next", "center": "title", "right": "dayGridMonth"},
    "initialView": "dayGridMonth",
    # Setăm o înălțime specifică pentru a se încadra mai bine pe ecran
    "height": 550,
}

state = calendar(events=calendar_events, options=calendar_options)

# 5. LOGICA DE SALVARE ȘI ȘTERGERE (Când apasă pe o zi)
if state and "dateClick" in state:
    data_selectata = state["dateClick"]["date"].split("T")[0]
    
    st.divider()
    st.subheader(f"📅 Setări pentru: {data_selectata}")
    
    # Verificăm dacă există deja ceva salvat pe această dată
    are_menstruatie = any(str(r['Data_Inceput']).split(" ")[0] == data_selectata for r in istoric)
    are_jurnal = any(str(r['Data']).split(" ")[0] == data_selectata for r in istoric_jurnal)
    
    col_stanga, col_dreapta = st.columns(2)
    
    # === COLOANA MENSTRUAȚIE ===
    with col_stanga:
        st.markdown("### 🩸 Ciclu Menstrual")
        
        if are_menstruatie:
            st.warning("Ai înregistrat deja o menstruație pe această zi.")
            if st.button("🗑️ Șterge înregistrarea"):
                try:
                    celula = tabel_menstruatie.find(data_selectata, in_column=1)
                    tabel_menstruatie.delete_row(celula.row)
                    st.success("Șters cu succes!")
                    st.rerun()
                except:
                    st.error("Eroare la ștergere.")
        else:
            if st.button(f"Confirmă prima zi"):
                if not istoric:
                    tabel_menstruatie.append_row([data_selectata, 5, 28])
                else:
                    ultima_data_str = str(istoric[-1]['Data_Inceput']).split(" ")[0]
                    u_dt = datetime.strptime(ultima_data_str, '%Y-%m-%d')
                    n_dt = datetime.strptime(data_selectata, '%Y-%m-%d')
                    dif = (n_dt - u_dt).days
                    tabel_menstruatie.append_row([data_selectata, 5, dif])
                st.success("S-a salvat menstruația!")
                st.rerun()

    # === COLOANA JURNAL ===
    with col_dreapta:
        st.markdown("### 📔 Jurnal Zilnic & Intimitate")
        
        if are_jurnal:
            st.info("Ai deja notițe în jurnal pentru această zi.")
            if st.button("🗑️ Șterge jurnalul de azi"):
                try:
                    celula = tabel_jurnal.find(data_selectata, in_column=1)
                    tabel_jurnal.delete_row(celula.row)
                    st.success("Jurnal șters!")
                    st.rerun()
                except:
                    st.error("Eroare la ștergere.")
        else:
            optiuni = st.multiselect(
                "Cum a fost ziua ta?",
                ["❤️ Protejat", "🔥 Neprotejat", "📈 Libidou ridicat", "💊 Am luat pastila", "🍷 Am băut un pahar", "😭 Sensibilă", "😫 Crampe"]
            )
            if st.button("Salvează în Jurnal"):
                if optiuni:
                    text_salvat = ", ".join(optiuni)
                    tabel_jurnal.append_row([data_selectata, text_salvat])
                    st.success("Jurnalul a fost actualizat!")
                    st.rerun()
                else:
                    st.warning("Te rog selectează măcar o opțiune înainte să salvezi.")

# 6. STATUS JOS (ACUM VIZIBIL!)
if istoric:
    st.divider()
    st.markdown("### 📊 Informații bazate pe istoricul tău")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div class='stMetricCard'>
                <div class='stMetricCard-label'>Media Ciclului tău</div>
                <div class='stMetricCard-value'>{int(medie_ciclu)} zile</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class='stMetricCard'>
                <div class='stMetricCard-label'>Durata Sângerării</div>
                <div class='stMetricCard-value'>{int(medie_menstr)} zile</div>
            </div>
        """, unsafe_allow_html=True)