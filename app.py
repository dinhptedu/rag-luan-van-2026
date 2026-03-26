import gradio as gr
from modules.auth_gradio import login_fn


# ===== MOCK FUNCTIONS (để test UI trước) =====
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

    # ===== STATE =====
    state_user = gr.State(None)
    state_role = gr.State(None)
    state_menus = gr.State(None)

    # ===== HEADER =====
    gr.Markdown("""
# 📚 Hệ thống RAG Pháp Luật  
### 🚀 Retrieval Augmented Generation System
---
""")

    # ===== LOGIN UI =====
    with gr.Row():
        gr.Column(scale=1)

        with gr.Column(scale=2, min_width=400) as login_box:
            gr.Markdown("## 🔐 Đăng nhập")

            username = gr.Textbox(label="Tên tài khoản", placeholder="admin")
            password = gr.Textbox(label="Mật khẩu", type="password")

            login_btn = gr.Button("🚀 Đăng nhập", variant="primary")
            login_msg = gr.Markdown()

        gr.Column(scale=1)

    # ===== MAIN UI =====
    with gr.Column(visible=False) as app_box:

        with gr.Row():
            with gr.Column(scale=8):
                user_info = gr.Markdown()

            with gr.Column(scale=1):
                logout_btn = gr.Button("Đăng xuất")

        gr.Markdown("---")

        main_output = gr.Markdown()

        # ===== TABS =====
    with gr.Tab("📥 Download"):
    
        gr.Markdown("## 📥 Module Download")
    
        download_output = gr.Markdown("👉 Nhấn nút để chạy")
    
        download_btn = gr.Button("🚀 Run Download")
    
        download_btn.click(
            download_ui,
            inputs=None,
            outputs=download_output
        )

    with gr.Tab("🧩 Chunking"):
    
        gr.Markdown("## 🧩 Chunking")
    
        chunk_output = gr.Markdown("👉 Nhấn nút để chạy")
    
        chunk_btn = gr.Button("🚀 Run Chunking")
    
        chunk_btn.click(
            chunking_ui,
            None,
            chunk_output
        )

    with gr.Tab("🧩 Chunking"):
    
        gr.Markdown("## 🧩 Chunking")
    
        chunk_output = gr.Markdown("👉 Nhấn nút để chạy")
    
        chunk_btn = gr.Button("🚀 Run Chunking")
    
        chunk_btn.click(
            chunking_ui,
            None,
            chunk_output
        )

    with gr.Tab("💬 QA"):

    gr.Markdown("## 💬 QA")

    qa_output = gr.Markdown("👉 Nhấn nút để chạy")

    qa_btn = gr.Button("🚀 Run QA")

    qa_btn.click(
        qa_ui,
        None,
        qa_output
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
