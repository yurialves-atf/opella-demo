import streamlit as st


def render_section_header(
    number: int,
    title: str,
    description: str = "",
):
    description_html = ""

    if description:
        description_html = f"""
        <div class="opella-section-description">
            {description}
        </div>
        """

    html = f"""
    <div class="opella-section-header">
        <div class="opella-section-number">
            {number:02d}
        </div>

        <div class="opella-section-content">
            <div class="opella-section-title">
                {title}
            </div>

            {description_html}
        </div>
    </div>
    """

    st.html(html)