import streamlit as st
from config import USERS, ROLE_MENUS, DOCUMENT_GROUPS

def login():
    if st.session_state.get('logged_in'):
        return True
    st.title('Dang nhap He thong RAG')
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input('Ten tai khoan')
        password = st.text_input('Mat khau', type='password')
        if st.button('Dang nhap', type='primary', use_container_width=True):
            user = USERS.get(username)
            if user and user['password'] == password:
                st.session_state.update({
                    'logged_in': True,
                    'username': username,
                    'role': user['role'],
                    'groups': user['groups'],
                    'menus': ROLE_MENUS[user['role']],
                })
                st.rerun()
            else:
                st.error('Sai tai khoan hoac mat khau')
    return False

def require(feature):
    if not st.session_state.get('logged_in'):
        st.error('Vui long dang nhap truoc')
        st.stop()
    if feature not in st.session_state.get('menus', []):
        st.error('Ban khong co quyen truy cap chuc nang nay')
        st.stop()

def get_allowed_groups():
    groups = st.session_state.get('groups', [])
    if 'all' in groups:
        return list(DOCUMENT_GROUPS.keys())
    return groups

def sidebar_user():
    with st.sidebar:
        role = st.session_state.get('role','')
        uname = st.session_state.get('username','')
        badge = 'ADMIN' if role=='admin' else 'GUEST'
        st.markdown(f'**{badge}: {uname}**')
        if role == 'guest':
            st.caption('Nhom: ' + ', '.join(get_allowed_groups()))
        st.divider()
        if st.button('Dang xuat', use_container_width=True):
            for k in list(st.session_state): del st.session_state[k]
            st.rerun()
