import gradio as gr
import json
from pathlib import Path

from modules.chunker import read_docx, get_chunks
from modules.auth_gradio import require
from config import DOCUMENT_GROUPS, DOCX_DIR, VECTOR_DIR, CHUNKING_OPTIONS


# ===== FUNCTION: CHUNKING =====
def run_chunking(group, strategy_name, logged_in, menus):

    ok, msg = require("chunking", logged_in, menus)
    if not ok:
        return msg

    strategy_cfg = CHUNKING_OPTIONS[strategy_name]

    grp_dir = Path(DOCX_DIR) / group
    docx_files = list(grp_dir.glob("*.docx")) if grp_dir.exists() else []

    if not docx_files:
        return "❌ Chưa có file DOCX. Hãy tải dữ liệu trước."

    all_chunks = []

    for f in docx_files:
        paras = read_docx(str(f), group)
        all_chunks.extend(get_chunks(paras, strategy_cfg))

    # ===== SAVE =====
    out_dir = Path(VECTOR_DIR) / group
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / f'chunks_{strategy_name.replace(" ","_")}.json'

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(
            [
                {
                    "text": c.text,
                    "source": c.source,
                    "group": c.group,
                    "strategy": c.strategy,
                    "section": c.section,
                }
                for c in all_chunks
            ],
            f,
            ensure_ascii=False,
            indent=2,
        )

    return f"""
    ✅ Chunking hoàn tất

    - Tổng chunks: {len(all_chunks)}
    - File lưu: {out_file}
    """


# ===== UI =====
def chunking_tab(state_logged_in, state_menus):

    with gr.Column():

        gr.Markdown("## 🧩 Chunking & Vector Database")

        # ===== SELECT =====
        group = gr.Dropdown(
            list(DOCUMENT_GROUPS.keys()),
            label="Nhóm tài liệu"
        )

        strategy = gr.Dropdown(
            list(CHUNKING_OPTIONS.keys()),
            label="Chiến lược chunking"
        )

        info_box = gr.Markdown()

        def update_info(s):
            if not s:
                return ""
            cfg = CHUNKING_OPTIONS[s]
            return f"⚙️ Strategy: **{s}**  \nConfig: `{cfg}`"

        strategy.change(update_info, strategy, info_box)

        # ===== RUN =====
        run_btn = gr.Button("🚀 Bắt đầu Chunking")

        output = gr.Markdown()

        run_btn.click(
            run_chunking,
            inputs=[group, strategy, state_logged_in, state_menus],
            outputs=output
        )

    return None
