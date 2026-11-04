import hmac
import os

import streamlit as st


st.set_page_config(page_title="Bytecode Institute", page_icon="B")
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(ellipse at top, #17253a 0%, #0e1117 55%);
    }
    .block-container {
        max-width: 760px;
        padding-top: 3rem;
    }
    .brand {
        color: #f2f5fa;
        font-size: 2rem;
        font-weight: 750;
        letter-spacing: .12em;
        text-align: center;
    }
    .brand span {
        color: #48c6b5;
    }
    .tagline {
        color: #aab5c5;
        margin: .35rem 0 1.6rem;
        text-align: center;
    }
    div[data-testid="stForm"] {
        background: rgba(18, 24, 34, .82);
        border: 1px solid #293447;
        border-radius: 14px;
        padding: 1.4rem;
    }
    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background: #168f83;
        border-color: #168f83;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="brand">BYTECODE <span>INSTITUTE</span></div>'
    '<div class="tagline">Learn, build, and grow together.</div>',
    unsafe_allow_html=True,
)

demo_email = os.getenv("BYTECODE_LOGIN_EMAIL", "").strip().lower()
demo_password = os.getenv("BYTECODE_LOGIN_PASSWORD", "")
demo_role = os.getenv("BYTECODE_LOGIN_ROLE", "Trainer")
if "accounts" not in st.session_state:
    st.session_state.accounts = {}
    if demo_email and demo_password:
        st.session_state.accounts[demo_email] = {
            "name": "Bytecode member",
            "password": demo_password,
            "role": demo_role,
        }

if "signed_in" in st.session_state:
    st.success(f"Welcome, {st.session_state.signed_in['name']}!")
    st.write(f"Role: **{st.session_state.signed_in['role']}**")
    if st.button("Log out"):
        del st.session_state.signed_in
        st.rerun()
else:
    login_tab, register_tab = st.tabs(["Login", "Register"])
    roles = ["Student", "Trainer", "Faculty"]

    with login_tab:
        st.subheader("Welcome back")
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Your role", roles, index=1)
            login_submitted = st.form_submit_button(
                "Log in", type="primary", use_container_width=True
            )

        if login_submitted:
            account = st.session_state.accounts.get(email.strip().lower())
            if (
                account
                and hmac.compare_digest(account["password"], password)
                and account["role"] == role
            ):
                st.session_state.signed_in = account
                st.rerun()
            else:
                st.error("Those login details don't match an account and role.")

        if not demo_email or not demo_password:
            st.caption(
                "To enable the demo account, set BYTECODE_LOGIN_EMAIL and "
                "BYTECODE_LOGIN_PASSWORD in PowerShell before starting the app."
            )

    with register_tab:
        st.subheader("Create your account")
        with st.form("register_form"):
            name = st.text_input("Name", placeholder="Your name")
            new_email = st.text_input("Email", placeholder="you@example.com")
            new_password = st.text_input(
                "Password", type="password", placeholder="Choose a password"
            )
            confirm_password = st.text_input(
                "Confirm password", type="password"
            )
            new_role = st.selectbox("Choose your role", roles, key="register_role")
            register_submitted = st.form_submit_button(
                "Create account", type="primary", use_container_width=True
            )

        if register_submitted:
            normalized_email = new_email.strip().lower()
            if not name.strip() or not normalized_email or not new_password:
                st.error("Please fill in every field.")
            elif "@" not in normalized_email or " " in normalized_email:
                st.error("Enter a valid email address.")
            elif new_password != confirm_password:
                st.error("The passwords don't match.")
            elif normalized_email in st.session_state.accounts:
                st.error("An account with that email already exists.")
            else:
                st.session_state.accounts[normalized_email] = {
                    "name": name.strip(),
                    "password": new_password,
                    "role": new_role,
                }
                st.success("Account created. You can now log in.")
