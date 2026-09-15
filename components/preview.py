from html import escape

import streamlit as st
import streamlit.components.v1 as components

def render_preview(asset: dict) -> None:
    asset_type = asset["asset_type"]

    st.caption(
        "Preview estrutural. O renderer visual avançado será implementado depois."
    )

    if asset_type == "banner_memed":
        _render_banner(asset)

    elif asset_type == "article_pharmacist":
        _render_article(asset)

    elif asset_type == "flyer":
        _render_flyer(asset)


def _render_banner(asset: dict) -> None:
    content = asset["content"]

    metrics_html = ""

    for block in content.get("evidence_blocks", []):
        metrics_html += f"""
        <div class="metric-card">
            <div class="metric">{escape(block.get("metric", ""))}</div>
            <div>{escape(block["message"])}</div>
        </div>
        """

    html = f"""
    <style>
        .banner {{
            background: linear-gradient(135deg, #05623b, #07864c);
            padding: 42px;
            border-radius: 22px;
            color: white;
            min-height: 430px;
            font-family: Arial, sans-serif;
        }}

        .banner h1 {{
            color: #ffd735;
            font-size: 42px;
            line-height: 1.05;
            max-width: 800px;
        }}

        .banner .subtitle {{
            font-size: 20px;
            max-width: 750px;
            margin-bottom: 30px;
        }}

        .metric-container {{
            display: flex;
            gap: 18px;
            margin-top: 25px;
            margin-bottom: 35px;
        }}

        .metric-card {{
            background: rgba(255, 255, 255, 0.12);
            padding: 20px;
            border-radius: 16px;
            flex: 1;
        }}

        .metric {{
            color: #ffd735;
            font-size: 38px;
            font-weight: bold;
        }}

        .product {{
            border-top: 2px solid rgba(255,255,255,.3);
            padding-top: 20px;
            font-size: 22px;
            font-weight: bold;
        }}

        .disclaimer {{
            opacity: .65;
            font-size: 11px;
            margin-top: 25px;
        }}
    </style>

    <div class="banner">
        <h1>{escape(content["headline"])}</h1>

        <div class="subtitle">
            {escape(content.get("subheadline", ""))}
        </div>

        <div class="metric-container">
            {metrics_html}
        </div>

        <div class="product">
            {escape(content.get("product_message", ""))}
        </div>

        <p>{escape(content.get("cta", ""))}</p>

        <div class="disclaimer">
            {escape(content.get("disclaimer", ""))}
        </div>
    </div>
    """

    components.html(
        html,
        height=600,
        scrolling=False,
    )


def _render_article(asset: dict) -> None:
    content = asset["content"]

    st.title(content["headline"])

    if content.get("subheadline"):
        st.markdown(f"*{content['subheadline']}*")

    for section in content.get("sections", []):
        st.markdown(f"### {section['title']}")
        st.write(section["text"])

    if content.get("key_points"):
        st.markdown("### Principais pontos")

        for item in content["key_points"]:
            st.markdown(f"- {item}")

    if content.get("cta"):
        st.info(content["cta"])

    if content.get("disclaimer"):
        st.caption(content["disclaimer"])


def _render_flyer(asset: dict) -> None:
    content = asset["content"]

    points = "".join(
        f"<div class='point'>{escape(point)}</div>"
        for point in content.get("key_points", [])
    )

    sections = "".join(
        f"""
        <h3>{escape(section['title'])}</h3>
        <p>{escape(section['text'])}</p>
        """
        for section in content.get("sections", [])
    )

    html = f"""
    <style>
        .flyer {{
            background: linear-gradient(180deg, #087245, #045c38);
            padding: 45px;
            border-radius: 24px;
            color: white;
            max-width: 850px;
            margin: auto;
        }}

        .flyer h1 {{
            color: #ffd735;
            font-size: 40px;
        }}

        .flyer h3 {{
            color: #ffd735;
            margin-top: 30px;
        }}

        .point {{
            background: rgba(255,255,255,.1);
            border-radius: 12px;
            padding: 14px;
            margin-bottom: 10px;
        }}

        .product {{
            margin-top: 35px;
            border-top: 2px solid rgba(255,255,255,.3);
            padding-top: 22px;
            font-size: 20px;
            font-weight: bold;
        }}
    </style>

    <div class="flyer">
        <h1>{escape(content["headline"])}</h1>

        <p>{escape(content.get("subheadline", ""))}</p>

        {sections}

        <div>
            {points}
        </div>

        <div class="product">
            {escape(content.get("product_message", ""))}
        </div>

        <p>{escape(content.get("cta", ""))}</p>
    </div>
    """

    components.html(
        html,
        height=750,
        scrolling=False,
    )