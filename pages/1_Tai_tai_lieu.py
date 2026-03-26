import gradio as gr
from pathlib import Path
from modules.downloader import batch_download
from modules.auth_gradio import require
from config import DOCUMENT_GROUPS, DOCX_DIR


# ====== FUNCTION: ĐẾM FILE ======
def get_file_stats():
    stats = []
    for grp, cfg in DOCUMENT_GROUPS.items():
        grp_dir = Path(DOCX_DIR) / grp
        count = len(list(grp_dir.glob("*.docx"))) if grp_dir.exists() else 0
        stats.append([grp, count])
    return stats


# ====== FUNCTION: DOWNLOAD ======
def run_download(group, target, delay, logged_in, menus):

    ok, msg = require("download", logged_in, menus)
    if not ok:
        return msg

    cfg = DOCUMENT_GROUPS[group]

    results = batch_download(
        group_name=group,
        id_start=cfg["vbpl_id_range"][0],
        id_end=cfg["vbpl_id_range"][1],
        target=int(target),
        delay=delay,
    )

    return f"""
    ✅ Xong!

    - Đã tải: {results["downloaded"]}
    - Đã có: {results["exists"]}
    - Lỗi: {results["error"]}
    """


# ====== UI ======
def download_tab(state_logged_in, state_menus):

    with gr.Column():

        gr.Markdown("## 📥 Tải tài liệu từ vbpl.vn")
        gr.Markdown("⚠️ Chỉ Admin mới có quyền thực hiện")

        # ===== STATS =====
        stats_btn = gr.Button("🔄 Refresh số liệu")
        stats_table = gr.Dataframe(headers=["Nhóm", "Số file"])

        stats_btn.click(get_file_stats, outputs=stats_table)

        # ===== CONFIG =====
        group = gr.Dropdown(
            list(DOCUMENT_GROUPS.keys()),
            label="Chọn nhóm tài liệu"
        )

        target = gr.Slider(10, 500, value=100, step=10, label="Số văn bản")
        delay = gr.Slider(0.3, 2.0, value=0.6, label="Delay (giây)")

        info_box = gr.Markdown()

        def update_info(g):
            if not g:
                return ""
            cfg = DOCUMENT_GROUPS[g]
            return f"""
            🔎 Quét ID từ **{cfg["vbpl_id_range"][0]:,} → {cfg["vbpl_id_range"][1]:,}**  
            📄 Tải tối đa **{cfg["target_docs"]} file**  
            ⚠️ File đã tồn tại sẽ KHÔNG bị ghi đè
            """

        group.change(update_info, group, info_box)

        # ===== RUN =====
        run_btn = gr.Button("🚀 Bắt đầu tải")
        output = gr.Markdown()

        run_btn.click(
            run_download,
            inputs=[group, target, delay, state_logged_in, state_menus],
            outputs=output
        )

    return None
