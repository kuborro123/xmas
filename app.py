import streamlit as st

st.set_page_config(page_title="Prezent dla taty 🎄", page_icon="🎁", layout="centered")

YOUTUBE_URL = "https://youtu.be/xDuLuKzKc2I"
LIVES_START = 3

# --- Pytania (15 szt.) ---
QUESTIONS = [
    {
        "q": "Kim tata jest z zawodu?",
        "options": ["Lekarzem", "Farmaceutą", "Pielęgniarzem", "Chemikiem"],
        "answer": "Farmaceutą",
        "hint": "Recepty tak, diagnozy nie 💊",
    },
    {
        "q": "W którym miesiącu tata się urodził?",
        "options": ["Styczeń", "Luty", "Marzec", "Grudzień"],
        "answer": "Styczeń",
        "hint": "Zimno było ❄️",
    },
    {
        "q": "W którym roku tata się urodził?",
        "options": ["1969", "1970", "1971", "1972"],
        "answer": "1971",
        "hint": "Początek lat 70.",
    },
    {
        "q": "Ile dzieci ma tata?",
        "options": ["1", "2", "3", "4"],
        "answer": "3",
        "hint": "Pełna drużyna 👨‍👩‍👧‍👦",
    },
    {
        "q": "Co jest dla taty najważniejsze?",
        "options": ["Praca", "Sport", "Rodzina", "Samochody"],
        "answer": "Rodzina",
        "hint": "❤️",
    },
    {
        "q": "Ironman to zawody składające się z:",
        "options": ["Biegu", "Pływania i biegu", "Pływania, roweru i biegu", "Siłowni i biegu"],
        "answer": "Pływania, roweru i biegu",
        "hint": "Trzy dyscypliny 💪",
    },
    {
        "q": "Której dyscypliny NIE ma w Ironmanie?",
        "options": ["Pływanie", "Rower", "Bieg", "Siłownia"],
        "answer": "Siłownia",
        "hint": "To triathlon 😉",
    },
    {
        "q": "Co oznacza skrót BMW?",
        "options": ["Berlin Motor Works", "Bayerische Motoren Werke", "British Motor Wheels", "Bavarian Machine Works"],
        "answer": "Bayerische Motoren Werke",
        "hint": "Niemcy 🇩🇪",
    },
    {
        "q": "Jak nazywa się napęd, z którego BMW słynie najbardziej?",
        "options": ["Na przednie koła", "Na tylne koła", "Na gąsienice", "Na jedną oś tylko w zakrętach"],
        "answer": "Na tylne koła",
        "hint": "RWD 😉",
    },
    {
        "q": "W którym roku człowiek wylądował na Księżycu?",
        "options": ["1965", "1969", "1972", "1980"],
        "answer": "1969",
        "hint": "Apollo 11 🌕",
    },
    {
        "q": "W którym roku Polska weszła do Unii Europejskiej?",
        "options": ["1999", "2004", "2007", "2012"],
        "answer": "2004",
        "hint": "1 maja 🇵🇱🇪🇺",
    },
    {
        "q": "Które miasto było stolicą Polski przed Warszawą?",
        "options": ["Gniezno", "Kraków", "Wrocław", "Poznań"],
        "answer": "Kraków",
        "hint": "Wawel 👑",
    },
    {
        "q": "Ile stopni ma kąt prosty?",
        "options": ["45", "90", "180", "360"],
        "answer": "90",
        "hint": "Litera „L” 📐",
    },
    {
        "q": "Ile to jest 7 × 8?",
        "options": ["54", "56", "58", "64"],
        "answer": "56",
        "hint": "Tabliczka mnożenia 😄",
    },
    {
        "q": "Jeśli masz 3 życia i stracisz 2, to ile zostaje?",
        "options": ["0", "1", "2", "3"],
        "answer": "1",
        "hint": "Proste 😉",
    },
]

# --- Session state init ---
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "lives" not in st.session_state:
    st.session_state.lives = LIVES_START
if "passed" not in st.session_state:
    st.session_state.passed = False
if "locked" not in st.session_state:
    st.session_state.locked = False

def reset():
    st.session_state.idx = 0
    st.session_state.lives = LIVES_START
    st.session_state.passed = False
    st.session_state.locked = False

st.title("🎁 Prezent świąteczny dla taty")
st.caption("Odpowiedz na 15 pytań. Masz 3 życia. Powodzenia! 🎄")

col1, col2, col3 = st.columns(3)
col1.metric("Pytanie", f"{min(st.session_state.idx + 1, len(QUESTIONS))}/{len(QUESTIONS)}")
col2.metric("Życia", "❤️" * st.session_state.lives if st.session_state.lives > 0 else "—")
col3.button("Zacznij od nowa", on_click=reset)

st.divider()

# --- Jeśli wygrana: pokazuj film z YouTube ---
if st.session_state.passed:
    st.success("Brawo! 🎉 Oto film!")
    st.video(YOUTUBE_URL)
    st.link_button("▶️ Otwórz film w YouTube", YOUTUBE_URL, use_container_width=True)
    st.balloons()
    st.stop()

# --- Jeśli przegrana ---
if st.session_state.locked:
    st.error("Koniec żyć 😅 Kliknij „Zacznij od nowa” i spróbuj jeszcze raz.")
    st.stop()

# --- Quiz ---
q = QUESTIONS[st.session_state.idx]
st.subheader(q["q"])
choice = st.radio("Wybierz odpowiedź:", q["options"], index=None)

c1, c2 = st.columns([1, 1])
submit = c1.button("✅ Zatwierdź", use_container_width=True)
hint_btn = c2.button("💡 Podpowiedź", use_container_width=True)

if hint_btn:
    st.info(q.get("hint", "Brak podpowiedzi."))

if submit:
    if choice is None:
        st.warning("Wybierz odpowiedź 😉")
        st.stop()

    if choice == q["answer"]:
        st.success("Dobrze! ✅")
        st.session_state.idx += 1
        if st.session_state.idx >= len(QUESTIONS):
            st.session_state.passed = True
        st.rerun()
    else:
        st.session_state.lives -= 1
        st.error("Nie tym razem ❌")
        if st.session_state.lives <= 0:
            st.session_state.locked = True
        st.rerun()
