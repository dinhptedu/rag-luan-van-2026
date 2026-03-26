import gradio as gr
from modules.auth_gradio import login_fn

def main_app(username, role):
    return f"Xin chào {username} — Role: {role}"

with gr.Blocks() as app:

    state_user = gr.State(None)
    state_role = gr.State(None)

    gr.Markdown("# 🔐 Đăng nhập hệ thống")

    username = gr.Textbox(label="Tên tài khoản")
    password = gr.Textbox(label="Mật khẩu", type="password")
    login_btn = gr.Button("Đăng nhập")

    output = gr.Markdown()

    def handle_login(u, p):
        ok, role = login_fn(u, p)
        if ok:
            return f"✅ Login thành công: {u}", u, role
        return "❌ Sai tài khoản", None, None

    login_btn.click(
        handle_login,
        inputs=[username, password],
        outputs=[output, state_user, state_role]
    )

    gr.Markdown("## 📊 Hệ thống RAG")

    main_output = gr.Markdown()

    def load_main(u, r):
        if not u:
            return "⚠️ Vui lòng đăng nhập"
        return main_app(u, r)

    app.load(load_main, [state_user, state_role], main_output)

app.launch()
