import gradio as gr
import json
from pathlib import Path

from modules.auth_gradio import require, get_allowed_groups
from config import VECTOR_DIR, CHUNKING_OPTIONS, GEMINI_API_KEY, LLM_MODEL, TOP_K

import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# ===== CACHE (IMPORTANT) =====
cache = {}

def load_chunks_and_index(group, strategy):
    key = f"{group}_{strategy}"
    if key in cache:
        return cache[key]

    chunk_file = Path(VECTOR_DIR)/group/f'chunks_{strategy.replace(" ","_")}.json'
    if not chunk_file.exists():
        return None, None, None

    with open(chunk_file, encoding="utf-8") as f:
        chunks = json.load(f)

    model = SentenceTransformer("intfloat/multilingual-e5-base")

    texts = [c["text"] for c in chunks]
    embs = model.encode(texts, normalize_embeddings=True)

    index = faiss.IndexFlatIP(embs.shape[1])
    index.add(embs.astype("float32"))

    cache[key] = (chunks, model, index)
    return cache[key]


# ===== QA FUNCTION =====
def ask_question(group, strategy, question, logged_in, menus, groups):

    ok, msg = require("qa", logged_in, menus)
    if not ok:
        return msg, ""

    allowed_groups = get_allowed_groups(groups)
    if group not in allowed_groups:
        return "⛔ Không có quyền truy cập nhóm này", ""

    chunks, embed_model, index = load_chunks_and_index(group, strategy)

    if chunks is None:
        return "❌ Chưa có dữ liệu chunking", ""

    # ===== RETRIEVAL =====
    q_emb = embed_model.encode([question], normalize_embeddings=True)
    _, idxs = index.search(q_emb.astype("float32"), TOP_K)

    context_docs = [chunks[i] for i in idxs[0] if 0 <= i < len(chunks)]

    context_text = "\n\n---\n\n".join(
        [f"[{d['source']}]\n{d['text']}" for d in context_docs]
    )

    # ===== PROMPT =====
    prompt = f"""
Bạn là trợ lý tư vấn pháp luật Việt Nam.
Trả lời ĐÚNG theo nội dung văn bản.

Nếu không có thông tin, nói:
"Tài liệu không có thông tin này."

===VĂN BẢN===
{context_text}
============

Câu hỏi: {question}
Trả lời:
"""

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(LLM_MODEL)

    response = model.generate_content(prompt)
    answer = response.text

    # ===== FORMAT SOURCE =====
    sources = "\n\n".join(
        [f"**{d['source']}** ({d['strategy']})\n{d['text'][:300]}..." for d in context_docs]
    )

    return answer, sources


# ===== UI =====
def qa_tab(state_logged_in, state_menus, state_groups):

    with gr.Column():

        gr.Markdown("## 💬 Hỏi đáp văn bản pháp luật")

        # ===== SELECT =====
        group = gr.Dropdown(label="Nhóm tài liệu")
        strategy = gr.Dropdown(list(CHUNKING_OPTIONS.keys()), label="Chunking")

        def load_groups(groups):
            return gr.update(choices=get_allowed_groups(groups))

        # dynamic load group theo user
        group.change(lambda x: x, group, group)
        
        # ===== QUESTION =====
        question = gr.Textbox(
            label="Nhập câu hỏi",
            lines=3,
            placeholder="Ví dụ: Thời gian thử việc tối đa là bao lâu?"
        )

        ask_btn = gr.Button("🚀 Đặt câu hỏi")

        answer_box = gr.Markdown()
        source_box = gr.Markdown()

        ask_btn.click(
            ask_question,
            inputs=[group, strategy, question, state_logged_in, state_menus, state_groups],
            outputs=[answer_box, source_box]
        )

    return None
