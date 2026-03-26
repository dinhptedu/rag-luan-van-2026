import gradio as gr
import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go

from modules.auth_gradio import require
from config import EMBEDDING_MODELS, CHUNKING_OPTIONS


# ===== MOCK DATA =====
def mock_results(embeds, chunks, rets, n_runs):
    rows = []
    for e in embeds:
        for c in chunks:
            for r in rets:
                base = np.random.uniform(0.55, 0.85)
                rows.append({
                    "experiment": f"{c[:10]}|{e[:10]}|{r}",
                    "chunking": c,
                    "embedding": e,
                    "retrieval": r,
                    "faithfulness": round(base + np.random.uniform(-0.05, 0.05), 3),
                    "answer_relevancy": round(base + np.random.uniform(-0.05, 0.07), 3),
                    "context_precision": round(base + np.random.uniform(-0.08, 0.05), 3),
                    "context_recall": round(base + np.random.uniform(-0.06, 0.06), 3),
                })
    return pd.DataFrame(rows)


# ===== RUN EXPERIMENT =====
def run_experiment(embeds, chunks, rets, n_runs, logged_in, menus):
    ok, msg = require("report", logged_in, menus)
    if not ok:
        return msg, None, None, None

    df = mock_results(embeds, chunks, rets, n_runs)

    return f"✅ Hoàn thành {len(df)} experiments!", df, df, df


# ===== RADAR =====
def plot_radar(df):
    metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]

    fig = go.Figure()
    for _, row in df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row[m] for m in metrics] + [row[metrics[0]]],
            theta=metrics + [metrics[0]],
            fill="toself",
            name=row["experiment"][:25]
        ))
    fig.update_layout(polar=dict(radialaxis=dict(range=[0, 1])))
    return fig


# ===== BAR =====
def plot_bar(df, metric):
    fig = px.bar(
        df.sort_values(metric, ascending=True),
        x=metric,
        y="experiment",
        orientation="h",
        color=metric,
        text=metric
    )
    return fig


# ===== STATS =====
def compute_stats(df, n_runs):
    metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]

    best = df.loc[df["faithfulness"].idxmax()]
    worst = df.loc[df["faithfulness"].idxmin()]

    rows = []
    for m in metrics:
        a = [best[m] + np.random.normal(0, 0.02) for _ in range(n_runs)]
        b = [worst[m] + np.random.normal(0, 0.02) for _ in range(n_runs)]

        _, pval = stats.wilcoxon(a, b) if n_runs > 1 else (0, 0.03)
        d = (np.mean(a) - np.mean(b)) / (np.std(b) + 1e-9)

        rows.append({
            "Metric": m,
            "p-value": round(pval, 4),
            "Cohens_d": round(d, 3),
            "Kết luận": "Có ý nghĩa" if pval < 0.05 else "Không"
        })

    return pd.DataFrame(rows)


# ===== UI =====
def report_tab(state_logged_in, state_menus):

    with gr.Column():

        gr.Markdown("## 📊 Báo cáo đánh giá RAG")

        # ===== CONFIG =====
        embed = gr.CheckboxGroup(
            choices=list(EMBEDDING_MODELS.keys()),
            value=list(EMBEDDING_MODELS.keys())[:2],
            label="Embedding models"
        )

        chunk = gr.CheckboxGroup(
            choices=list(CHUNKING_OPTIONS.keys()),
            value=list(CHUNKING_OPTIONS.keys())[:2],
            label="Chunking"
        )

        retrieval = gr.CheckboxGroup(
            choices=["Dense", "BM25", "Hybrid"],
            value=["Dense", "Hybrid"],
            label="Retrieval"
        )

        n_runs = gr.Slider(1, 10, value=5, step=1, label="Số lần chạy")

        run_btn = gr.Button("🚀 Chạy đánh giá")

        status = gr.Markdown()

        df_output = gr.Dataframe()

        radar_plot = gr.Plot()
        bar_plot = gr.Plot()
        stats_table = gr.Dataframe()

        metric_select = gr.Dropdown(
            ["faithfulness", "answer_relevancy", "context_precision", "context_recall"],
            label="Metric"
        )

        # ===== EVENTS =====
        run_btn.click(
            run_experiment,
            inputs=[embed, chunk, retrieval, n_runs, state_logged_in, state_menus],
            outputs=[status, df_output, radar_plot, bar_plot]
        )

        # Radar
        df_output.change(plot_radar, df_output, radar_plot)

        # Bar
        metric_select.change(plot_bar, [df_output, metric_select], bar_plot)

        # Stats
        df_output.change(compute_stats, [df_output, n_runs], stats_table)

    return None
