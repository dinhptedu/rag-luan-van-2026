import gradio as gr
from modules.auth_gradio import login_fn


# ===== MAIN APP =====
def main_app(username, role):
    return f"""
    ## 🎉 Xin chào {username}
    
    👤 Role: **{role}**
    
    👉 Chọn chức năng bên dưới để bắt đầu hệ thống RAG.
    """


# ===== LOGIN HANDLER =====
def handle_login(u, p):
    ok, role = login_fn(u, p)

    if ok:
        return (
            "✅ Đăng nhập thành công",
            u,
            role,
            gr.update(visible=False),   # hide login box
            gr.update(visible=True),    # show app
        )

    return (
        "❌ Sai tài khoản hoặc mật khẩu",
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
with gr.Blocks(theme=gr.themes.Soft(), title="RAG System") as app:

    # ===== STATE =====
    state_user = gr.State(None)
    state_role = gr.State(None)

    # ===== HEADER =====
    gr.Markdown(
        """
        # 📚 Hệ thống RAG Pháp Luật  
        ### 🚀 Retrieval Augmented Generation System
        """
    )

    # ===== LOGIN BOX =====
    with gr.Column(visible=True) as login_box:

        gr.Markdown("## 🔐 Đăng nhập")

        username = gr.Textbox(label="Tên tài khoản", placeholder="admin")
        password = gr.Textbox(label="Mật khẩu", type="password")

        login_btn = gr.Button("Đăng nhập", variant="primary")

        login_msg = gr.Markdown()

    # ===== MAIN APP =====
    with gr.Column(visible=False) as app_box:

        with gr.Row():
            user_info = gr.Markdown()
            logout_btn = gr.Button("Đăng xuất", variant="secondary")

        gr.Markdown("---")

        main_output = gr.Markdown()

        # 👉 chỗ này sau này bạn gắn tabs RAG vào
        gr.Markdown("### 📊 Các chức năng sẽ hiển thị tại đây")

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
        lambda u, r: f"👤 **{u}** | Role: `{r}`",
        inputs=[state_user, state_role],
        outputs=user_info
    )

    logout_btn.click(
        handle_logout,
        inputs=[],
        outputs=[login_msg, state_user, state_role, login_box, app_box, main_output]
    )

app.launch()
