import streamlit as st
from modules.auth import login, sidebar_user

st.set_page_config(
    page_title="RAG Hoi Dap Van Ban Phap Luat",
    page_icon="scales",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Kiem tra dang nhap
if not login():
    st.stop()

# Hien thi info user o sidebar
sidebar_user()

# Trang chu
role = st.session_state.get('role', 'guest')

st.title('He Thong Hoi Dap Van Ban Phap Luat')
st.markdown(f"Xin chao **{st.session_state.get('username')}** — Role: `{role}`")
st.info('Chon chuc nang o menu ben trai de bat dau.')
