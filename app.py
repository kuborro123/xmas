import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Prezent dla taty 🎄", page_icon="🎁", layout="centered")

VIDEO_PATH = Path("draft_xmas.mp4")  # wrzuć swój film do folderu obok app.py
LIVES_START = 3

# --- Twoje pytania (edytuj) ---
QUESTIONS = [
    {
        "q": "Jakie jest moje ulubione świąteczne jedzenie?",
        "options": ["Pierogi", "Barszcz", "Karp", "Makowiec"],
        "answer": "Barszcz",
        "hint": "Czerwone i obowiązkowe 😄",
    },
    {
        "q": "W którym miesiącu jest Dzień Ojca w Polsce?",
        "options": ["Maj", "Czerwiec", "Lipiec", "Sierpień"],
        "answer": "Czerwiec",
        "hint": "To nie jest jak w USA 😉",
    },
    {
        "q": "Ile żyć ma ten quiz na starcie?",
        "options": ["1", "2", "3", "5"],
        "answer": "3",
        "hint": "Właśnie widzisz to na ekranie!",
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
    st.session_state.locked = False  # blokada po przegranej

def reset():
    st.session_state.idx = 0
    st.session_state.lives = LIVES_START
    st.session_state.passed = False
    st.session_state.locked = False

st.title("🎁 Prezent świąteczny")
st.caption("Odpowiedz na kilka pytań. Masz 3 życia. Powodzenia! 🎄")

col1, col2, col3 = st.columns(3)
col1.metric("Pytanie", f"{min(st.session_state.idx + 1, len(QUESTIONS))}/{len(QUESTIONS)}")
col2.metric("Życia", "❤️" * st.session_state.lives if st.session_state.lives > 0 else "—")
col3.button("Zacznij od nowa", on_click=reset)

st.divider()

# --- Jeśli wygrana: pokazuj film + pobieranie ---
if st.session_state.passed:
    st.success("Brawo! 🎉 Oto film!")
    if not VIDEO_PATH.exists():
        st.error("Nie widzę pliku film.mp4 w folderze apki. Dodaj go obok app.py.")
        st.stop()

    # Odtwarzanie w apce
    st.video(str(VIDEO_PATH))

    # Pobieranie
    video_bytes = VIDEO_PATH.read_bytes()
    st.download_button(
        "⬇️ Pobierz film",
        data=video_bytes,
        file_name=VIDEO_PATH.name,
        mime="video/mp4",
        use_container_width=True,
    )

    st.stop()

# --- Jeśli przegrana ---
if st.session_state.locked:
    st.error("Koniec żyć 😅 Możesz kliknąć „Zacznij od nowa” i spróbować jeszcze raz.")
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
