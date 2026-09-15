import streamlit as st


STEPS = {
    1: {
        "number": "01",
        "eyebrow": "ETAPA 01",
        "title": "Source & Opportunities",
    },
    2: {
        "number": "02",
        "eyebrow": "ETAPA 02",
        "title": "AI Draft & Claims",
    },
    3: {
        "number": "03",
        "eyebrow": "ETAPA 03",
        "title": "Initial Asset",
    },
    4: {
        "number": "04",
        "eyebrow": "ETAPA 04",
        "title": "Refine with Prompt",
    },
    5: {
        "number": "05",
        "eyebrow": "ETAPA 05",
        "title": "Review & Approval",
    },
}


def init_stepper():
    if "current_step" not in st.session_state:
        st.session_state.current_step = 1


def set_step(step: int):
    st.session_state.current_step = step


def render_stepper():
    current = st.session_state.current_step

    cols = st.columns(5, gap="small")

    for step, data in STEPS.items():
        with cols[step - 1]:

            state_class = (
                "active"
                if step == current
                else "completed"
                if step < current
                else "inactive"
            )

            st.html(
                f"""
                <div class="workflow-step {state_class}">
                    <div class="workflow-step-number">
                        {data["number"]}
                    </div>

                    <div class="workflow-step-copy">
                        <div class="workflow-step-eyebrow">
                            {data["eyebrow"]}
                        </div>

                        <div class="workflow-step-title">
                            {data["title"]}
                        </div>
                    </div>
                </div>
                """
            )


def render_navigation(
    can_advance: bool = True,
):
    current = st.session_state.current_step

    left, _, right = st.columns(
        [1, 4, 1]
    )

    with left:
        if current > 1:
            if st.button(
                "← Voltar",
                use_container_width=True,
            ):
                set_step(current - 1)
                st.rerun()

    with right:
        if current < 5:
            if st.button(
                "Avançar →",
                type="primary",
                disabled=not can_advance,
                use_container_width=True,
            ):
                set_step(current + 1)
                st.rerun()