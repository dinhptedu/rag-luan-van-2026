import gradio as gr
from modules.auth_gradio import login_fn


# ===== MAIN APP =====
def main_app(username, role):
    return f"""
### 🎉 Xin chào {username}

👤 **Role:** `{role}`  

---
🚀 Chọn chức năng để bắt đầu hệ thống RAG
"""


# ===== LOGIN HANDLER =====
def handle_login(u, p):
    msg, ok, username, role, groups, menus = login_fn(u, p)

    if ok:
        return (
            msg,
            username,
            role,
            gr.update(visible=False),
            gr.update(visible=True),
        )

    return (
        msg,
        None,
        None,
        gr.update(visible=True),
        gr.update(visible=False),
    )


# ===== LOGOUT =====
def handle_logout():
    return (
        "🔓 Đã đăng xuất",
        None,
        None,
        gr.update(visible=True),
        gr.update(visible=False),
        "⚠️ Vui lòng đăng nhập"
    )


# ===== APP =====
with gr.Blocks() as app:

    # ===== STATE =====
    state_user = gr.State(None)
    state_role = gr.State(None)

    # ===== HEADER =====
    gr.Markdown("""
# 📚 Hệ thống RAG Pháp Luật  
### 🚀 Retrieval Augmented Generation System
---
""")

    # ===== LOGIN BOX (CENTER) =====
    with gr.Row():
        gr.Column(scale=1)

        with gr.Column(scale=2, min_width=400) as login_box:

            gr.Markdown("## 🔐 Đăng nhập hệ thống")

            username = gr.Textbox(
                label="Tên tài khoản",
                placeholder="admin"
            )

            password = gr.Textbox(
                label="Mật khẩu",
                type="password"
            )

            login_btn = gr.Button("🚀 Đăng nhập", variant="primary")
            login_msg = gr.Markdown()

        gr.Column(scale=1)

    # ===== MAIN APP =====
    with gr.Column(visible=False) as app_box:

        with gr.Row():
            with gr.Column(scale=8):
                user_info = gr.Markdown()

            with gr.Column(scale=1):
                logout_btn = gr.Button("Đăng xuất")

        gr.Markdown("---")

        main_output = gr.Markdown()

        # Dashboard placeholder
        gr.Markdown("### 📊 Dashboard RAG")
        gr.Markdown("👉 Các chức năng sẽ hiển thị tại đây")

    # ===== EVENTS =====
    login_btn.click(
        handle_login,
        inputs=[username, password],
        outputs=[login_msg, state_user, state_role, login_box, app_box]
    ).then(
        main_app,
        inputs=[state_user, state_role],
        outputs=main_output
    ).then(
        lambda u, r: f"👤 **{u}** | `{r}`",
        inputs=[state_user, state_role],
        outputs=user_info
    )

    logout_btn.click(
        handle_logout,
        inputs=[],
        outputs=[login_msg, state_user, state_role, login_box, app_box, main_output]
    )


# ⚠️ Theme đặt ở launch (compatible mọi version)
app.launch(theme=gr.themes.Soft())
