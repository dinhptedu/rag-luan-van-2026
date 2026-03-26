import gradio as gr
from modules.auth_gradio import login_fn


# ===== MOCK TAB (TẠM THỜI - ĐỂ BẠN THẤY UI HOẠT ĐỘNG) =====
def download_ui():
    return "📥 Module Download (sẽ gắn logic sau)"

def chunking_ui():
    return "🧩 Module Chunking"

def qa_ui():
    return "💬 Module QA"

def report_ui():
    return "📊 Module Report"


# ===== MAIN APP =====
def main_app(username, role):
    return f"""
### 🎉 Xin chào {username}
👤 **Role:** `{role}`  
---
🚀 Chọn chức năng bên dưới
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

    state_user = gr.State(None)
    state_role = gr.State(None)

    # ===== HEADER =====
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

        # 🔥 TAB THỰC SỰ (ĐÂY LÀ PHẦN BẠN THIẾU)
        with gr.Tabs():

            with gr.Tab("📥 Download"):
                download_box = gr.Markdown()
                gr.Button("Load").click(download_ui, None, download_box)

            with gr.Tab("🧩 Chunking"):
                chunk_box = gr.Markdown()
                gr.Button("Load").click(chunking_ui, None, chunk_box)

            with gr.Tab("💬 QA"):
                qa_box = gr.Markdown()
                gr.Button("Load").click(qa_ui, None, qa_box)

            with gr.Tab("📊 Report"):
                report_box = gr.Markdown()
                gr.Button("Load").click(report_ui, None, report_box)

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


app.launch(theme=gr.themes.Soft())
