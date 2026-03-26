import gradio as gr
from modules.auth_gradio import login_fn


# ===== MOCK FUNCTIONS =====
def download_ui():
    return "📥 Download module hoạt động"

def chunking_ui():
    return "🧩 Chunking module hoạt động"

def qa_ui():
    return "💬 QA module hoạt động"

def report_ui():
    return "📊 Report module hoạt động"


# ===== MAIN APP =====
def main_app(username, role):
    return f"""
### 🎉 Xin chào {username}
👤 **Role:** `{role}`  
---
🚀 Chọn tab bên dưới để sử dụng hệ thống
"""


# ===== LOGIN =====
def handle_login(u, p):
    msg, ok, username, role, groups, menus = login_fn(u, p)

    if ok:
        return (
            msg,
            username,
            role,
            menus,
            gr.update(visible=False),
            gr.update(visible=True),
        )

    return (
        msg,
        None,
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
        None,
        gr.update(visible=True),
        gr.update(visible=False),
        "⚠️ Vui lòng đăng nhập"
    )


# ===== APP =====
with gr.Blocks() as app:

    state_user = gr.State(None)
    state_role = gr.State(None)
    state_menus = gr.State(None)

    gr.Markdown("""
# 📚 Hệ thống RAG Pháp Luật  
### 🚀 Retrieval Augmented Generation System
---
""")

    # ===== LOGIN =====
    with gr.Row():
        gr.Column(scale=1)

        with gr.Column(scale=2, min_width=400) as login_box:
            gr.Markdown("## 🔐 Đăng nhập")

            username = gr.Textbox(label="Tên tài khoản", placeholder="admin")
            password = gr.Textbox(label="Mật khẩu", type="password")

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

        # ===== TABS (ĐÚNG CHUẨN) =====
        with gr.Tabs():

            # ===== DOWNLOAD =====
            with gr.Tab("📥 Download"):
                gr.Markdown("## 📥 Module Download")

                download_output = gr.Markdown("👉 Nhấn nút để chạy")
                gr.Button("🚀 Run Download").click(
                    download_ui, None, download_output
                )

            # ===== CHUNKING =====
            with gr.Tab("🧩 Chunking"):
                gr.Markdown("## 🧩 Chunking")

                chunk_output = gr.Markdown("👉 Nhấn nút để chạy")
                gr.Button("🚀 Run Chunking").click(
                    chunking_ui, None, chunk_output
                )

            # ===== QA =====
            with gr.Tab("💬 QA"):
                gr.Markdown("## 💬 QA")

                qa_output = gr.Markdown("👉 Nhấn nút để chạy")
                gr.Button("🚀 Run QA").click(
                    qa_ui, None, qa_output
                )

            # ===== REPORT =====
            with gr.Tab("📊 Report"):
                gr.Markdown("## 📊 Report")

                report_output = gr.Markdown("👉 Nhấn nút để chạy")
                gr.Button("🚀 Run Report").click(
                    report_ui, None, report_output
                )

    # ===== EVENTS =====
    login_btn.click(
        handle_login,
        inputs=[username, password],
        outputs=[login_msg, state_user, state_role, state_menus, login_box, app_box]
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
        outputs=[login_msg, state_user, state_role, state_menus, login_box, app_box, main_output]
    )


app.launch(theme=gr.themes.Soft())
