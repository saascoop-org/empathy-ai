import json
from html import escape

import streamlit as st
import streamlit.components.v1 as components
from pydantic import ValidationError

from empathy_engine.errors import EmpathyEngineError
from empathy_engine.config import load_settings
from empathy_engine.i18n.language import (
    LANGUAGE_LABELS,
    SUPPORTED_UI_LANGUAGES,
    detect_language_from_accept_language,
    detect_language_from_locale,
    detect_language_from_timezone,
    translate,
)
from empathy_engine.operations import get_local_runtime_status
from empathy_engine.presentation.alterity_map import compose_interaction_with_alterity_map
from empathy_engine.presentation.demo_scenarios import (
    demo_scenario_options,
    get_demo_scenario,
)
from empathy_engine.presentation.learning_diary import (
    diary_entry_title,
    display_bridge_for_language,
    display_feedback_for_language,
    extract_diary_interaction,
)
from empathy_engine.presentation.result_presenter import ResultPresenter
from empathy_engine.safety.logging import configure_safe_logging
from empathy_engine.security.demo_token import DemoTokenError, validate_demo_token
from empathy_engine.storage.interaction_store import InteractionStore
from empathy_engine.use_cases.analyze_interaction import (
    AnalyzeInteractionCommand,
    AnalyzeInteractionUseCase,
)

st.set_page_config(
    page_title="EmpathyAI Cognitive Mediator",
    page_icon="🧠",
    layout="wide",
    # The controlled demo is frequently opened from phones during judging/testing.
    # Starting collapsed keeps Streamlit's sidebar from covering the first screen,
    # while preserving access through Streamlit's native sidebar toggle.
    initial_sidebar_state="collapsed",
)

configure_safe_logging()

st.markdown(
    """
    <style>
        :root {
            --empathy-teal: #17aeb6;
            --empathy-teal-dark: #0d7f88;
            --empathy-coral: #ff705f;
            --empathy-coral-dark: #bf4a3d;
            --empathy-amber: #ffb45f;
            --empathy-lavender: #bf87f2;
            --empathy-ink: #18333b;
            --empathy-muted: #607179;
            --empathy-line: #dcebee;
            --empathy-surface: #ffffff;
            --empathy-wash: #f6fbfb;
        }

        .stApp {
            background:
                linear-gradient(135deg, rgba(23, 174, 182, 0.08), rgba(255, 112, 95, 0.07) 48%, rgba(191, 135, 242, 0.07)),
                var(--empathy-wash);
            color: var(--empathy-ink);
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff, #f2fbfb);
            border-right: 1px solid var(--empathy-line);
        }

        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label {
            color: var(--empathy-ink);
        }

        .empathy-hero {
            display: grid;
            grid-template-columns: minmax(160px, 220px) 1fr;
            gap: 2rem;
            align-items: center;
            margin-bottom: 1.25rem;
            padding: 1.3rem 0 1.6rem;
            border-bottom: 1px solid rgba(23, 174, 182, 0.18);
        }

        .empathy-logo-shell {
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .empathy-kicker {
            margin: 0 0 0.45rem;
            color: var(--empathy-teal-dark);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0;
            text-transform: uppercase;
        }

        .empathy-title {
            margin: 0;
            color: var(--empathy-ink);
            font-size: clamp(2.25rem, 5vw, 4.4rem);
            line-height: 1;
            font-weight: 760;
            letter-spacing: 0;
        }

        .empathy-subtitle {
            max-width: 720px;
            margin: 0.85rem 0 0;
            color: var(--empathy-muted);
            font-size: 1.12rem;
            line-height: 1.55;
        }

        .empathy-band {
            margin: 0.8rem 0 1.25rem;
            padding: 1rem 1.1rem;
            border-left: 5px solid var(--empathy-coral);
            background: rgba(255, 255, 255, 0.78);
            box-shadow: 0 14px 38px rgba(24, 51, 59, 0.06);
        }

        .empathy-panel {
            padding: 1.15rem;
            border: 1px solid var(--empathy-line);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.88);
            box-shadow: 0 12px 32px rgba(24, 51, 59, 0.06);
        }

        .empathy-section-title {
            margin: 0 0 0.7rem;
            color: var(--empathy-ink);
            font-size: 1.05rem;
            font-weight: 750;
        }

        .empathy-step-label {
            margin: 1.2rem 0 0.25rem;
            color: var(--empathy-teal-dark);
            font-size: 0.84rem;
            font-weight: 750;
            letter-spacing: 0;
            text-transform: uppercase;
        }

        .empathy-result-accent {
            height: 4px;
            width: 100%;
            margin: 1.4rem 0 1rem;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--empathy-teal), var(--empathy-lavender), var(--empathy-coral));
        }

        .stTextArea textarea {
            border: 1px solid rgba(23, 174, 182, 0.32);
            border-radius: 8px;
            background: #ffffff;
            color: var(--empathy-ink);
        }

        .stTextArea textarea::placeholder,
        [data-testid="stCaptionContainer"],
        .stCaptionContainer {
            color: #595959 !important;
            opacity: 1 !important;
        }

        .stTextArea textarea:focus,
        .stAudioInput:focus-within,
        .stCheckbox:focus-within,
        .stRadio:focus-within,
        .stExpander:focus-within,
        .stTextInput:focus-within,
        .stButton > button:focus-visible,
        [data-baseweb="select"] > div:focus-within {
            border-color: var(--empathy-teal) !important;
            box-shadow: 0 0 0 3px rgba(23, 174, 182, 0.16) !important;
            outline: 2px solid transparent !important;
        }

        .stButton > button[kind="primary"] {
            border: 0;
            background: linear-gradient(90deg, var(--empathy-teal-dark), var(--empathy-coral-dark));
            color: #ffffff;
            font-weight: 750;
            min-height: 3rem;
        }

        .stButton > button[kind="primary"]:hover {
            filter: saturate(1.06) brightness(0.98);
            color: #ffffff;
        }

        .stButton:has(button[kind="primary"]) {
            position: sticky;
            bottom: 0.75rem;
            z-index: 20;
            padding: 0.55rem 0;
            background: linear-gradient(180deg, rgba(246, 251, 251, 0), rgba(246, 251, 251, 0.96) 32%);
        }

        div[data-testid="stAlert"] {
            border-radius: 8px;
        }

        .empathy-bridge-card {
            margin: 1rem 0 0.65rem;
            padding: 1.25rem 1.35rem;
            border: 1px solid rgba(23, 174, 182, 0.28);
            border-left: 6px solid var(--empathy-teal);
            border-radius: 8px;
            background: #ffffff;
            box-shadow: 0 14px 32px rgba(24, 51, 59, 0.08);
        }

        .empathy-bridge-label {
            margin: 0 0 0.65rem;
            color: var(--empathy-teal-dark);
            font-weight: 750;
        }

        .empathy-bridge-text {
            margin: 0;
            color: var(--empathy-ink);
            font-size: 1.12rem;
            line-height: 1.65;
        }

        h3 {
            color: var(--empathy-ink);
        }

        @media (max-width: 760px) {
            .stApp {
                overflow-x: hidden;
            }

            .block-container {
                width: 100%;
                max-width: 100%;
                padding-top: 1rem;
                padding-left: 0.85rem;
                padding-right: 0.85rem;
                padding-bottom: 5rem;
            }

            .empathy-hero {
                grid-template-columns: 1fr;
                gap: 1rem;
                margin-bottom: 1rem;
                padding-top: 0.75rem;
                padding-bottom: 1rem;
                text-align: center;
            }

            .empathy-logo-shell img {
                max-width: 120px;
            }

            .empathy-subtitle {
                margin-left: auto;
                margin-right: auto;
                font-size: 1rem;
                line-height: 1.45;
            }

            .empathy-band,
            .empathy-panel,
            .empathy-bridge-card {
                padding: 0.9rem;
            }

            .empathy-title {
                font-size: clamp(2rem, 13vw, 3.1rem);
            }

            .empathy-section-title {
                font-size: 1rem;
                line-height: 1.35;
            }

            .empathy-step-label {
                margin-top: 1rem;
                font-size: 0.78rem;
            }

            .stTextArea textarea {
                min-height: 7rem;
                font-size: 1rem;
            }

            .stButton > button,
            .stDownloadButton > button {
                width: 100%;
                min-height: 2.85rem;
                white-space: normal;
            }

            [data-baseweb="select"] > div {
                min-height: 2.75rem;
            }

            .stButton:has(button[kind="primary"]) {
                bottom: 0;
                padding-bottom: 0.75rem;
            }
        }

        /* Mobile and tablet users should land directly in the task flow.
           The sidebar remains available through Streamlit's built-in toggle,
           but the main content keeps the full viewport width on first load. */
        @media (max-width: 1024px) {
            section[data-testid="stSidebar"] {
                box-shadow: 8px 0 28px rgba(24, 51, 59, 0.12);
            }

            .block-container {
                padding-left: max(0.85rem, env(safe-area-inset-left));
                padding-right: max(0.85rem, env(safe-area-inset-right));
            }

            div[data-testid="column"] {
                min-width: 0;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

try:
    settings = load_settings()
except (ValueError, ValidationError) as error:
    st.error(f"Invalid application configuration: {error}")
    st.stop()


def enforce_demo_token_access(settings):
    demo_token_secret = getattr(settings, "demo_token_secret", "")
    demo_token_ttl_seconds = getattr(settings, "demo_token_ttl_seconds", 300)

    if not demo_token_secret and "demo_token" in st.query_params:
        del st.query_params["demo_token"]
        return
    if not demo_token_secret:
        return
    if st.session_state.get("demo_token_validated"):
        return

    token = st.query_params.get("demo_token", "")
    try:
        validate_demo_token(
            token,
            demo_token_secret,
            max_ttl_seconds=demo_token_ttl_seconds,
        )
    except DemoTokenError:
        st.error(
            "This controlled demo link is missing, expired, or invalid. "
            "Please relaunch the demo from the landing page."
        )
        st.stop()

    st.session_state["demo_token_validated"] = True
    if "demo_token" in st.query_params:
        del st.query_params["demo_token"]


enforce_demo_token_access(settings)


def render_session_timeout_guard(settings):
    timeout_ms = getattr(settings, "session_timeout_ms", 180_000)
    warning_ms = min(getattr(settings, "session_timeout_warning_ms", 150_000), timeout_ms)
    expired_url = getattr(settings, "session_expired_url", "/session-expired.html")

    components.html(
        f"""
        <script>
          (() => {{
            const timeoutMs = {json.dumps(timeout_ms)};
            const warningMs = {json.dumps(warning_ms)};
            const expiredUrl = {json.dumps(expired_url)};
            const parentWindow = window.parent || window;
            let parentDocument = document;
            try {{
              parentDocument = parentWindow.document || document;
            }} catch (error) {{
              parentDocument = document;
            }}
            const humanEvents = [
              "pointermove",
              "pointerdown",
              "mousemove",
              "mousedown",
              "keydown",
              "keyup",
              "click",
              "scroll",
              "wheel",
              "touchstart",
              "touchmove"
            ];
            let warningTimer = null;
            let expirationTimer = null;
            let watchdogTimer = null;
            let lastHumanActivity = Date.now();
            let expired = false;
            const previousGuard = parentWindow.__empathyInactivityTimeoutGuard;

            if (previousGuard && typeof previousGuard.destroy === "function") {{
              previousGuard.destroy();
            }}

            function ensureWarning() {{
              let warning = parentDocument.getElementById("empathy-session-warning");
              if (warning) {{
                return warning;
              }}

              warning = parentDocument.createElement("div");
              warning.id = "empathy-session-warning";
              warning.setAttribute("role", "status");
              warning.setAttribute("aria-live", "polite");
              warning.textContent = "Session will expire soon due to inactivity. This controlled demo uses automatic session shutdown to minimize infrastructure and environmental costs.";
              warning.style.cssText = [
                "position: fixed",
                "right: 24px",
                "bottom: 24px",
                "z-index: 2147483647",
                "max-width: 420px",
                "border: 1px solid rgba(13, 127, 136, 0.32)",
                "border-left: 6px solid #0d7f88",
                "border-radius: 8px",
                "background: #ffffff",
                "color: #18333b",
                "box-shadow: 0 18px 42px rgba(24, 51, 59, 0.18)",
                "font: 600 14px/1.45 system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
                "padding: 14px 16px",
                "display: none"
              ].join(";");
              parentDocument.body.appendChild(warning);
              return warning;
            }}

            function hideWarning() {{
              const warning = parentDocument.getElementById("empathy-session-warning");
              if (warning) {{
                warning.style.display = "none";
              }}
            }}

            function showWarning() {{
              ensureWarning().style.display = "block";
            }}

            function expireSession() {{
              if (expired) {{
                return;
              }}
              expired = true;
              destroy();
              try {{
                parentWindow.location.replace(expiredUrl);
              }} catch (error) {{
                window.location.replace(expiredUrl);
              }}
            }}

            function checkInactivity() {{
              if (expired) {{
                return;
              }}
              const idleMs = Date.now() - lastHumanActivity;
              if (idleMs >= timeoutMs) {{
                expireSession();
                return;
              }}
              if (idleMs >= warningMs) {{
                showWarning();
              }}
            }}

            function resetTimers() {{
              if (expired) {{
                return;
              }}
              lastHumanActivity = Date.now();
              hideWarning();
              clearTimeout(warningTimer);
              clearTimeout(expirationTimer);
              warningTimer = setTimeout(showWarning, warningMs);
              expirationTimer = setTimeout(expireSession, timeoutMs);
            }}

            function destroy() {{
              clearTimeout(warningTimer);
              clearTimeout(expirationTimer);
              clearInterval(watchdogTimer);
              humanEvents.forEach((eventName) => {{
                parentDocument.removeEventListener(eventName, resetTimers, true);
                parentWindow.removeEventListener(eventName, resetTimers, true);
              }});
              if (parentWindow.__empathyInactivityTimeoutGuard === guard) {{
                delete parentWindow.__empathyInactivityTimeoutGuard;
              }}
            }}

            const guard = {{ destroy }};
            parentWindow.__empathyInactivityTimeoutGuard = guard;
            ensureWarning();
            humanEvents.forEach((eventName) => {{
              parentDocument.addEventListener(eventName, resetTimers, true);
              parentWindow.addEventListener(eventName, resetTimers, true);
            }});
            resetTimers();
            watchdogTimer = setInterval(checkInactivity, 1000);
          }})();
        </script>
        """,
        height=1,
    )


render_session_timeout_guard(settings)


def resolve_initial_ui_language() -> str:
    context_locale = detect_language_from_locale(getattr(st.context, "locale", None))
    if context_locale:
        return context_locale

    accept_language = None
    headers = getattr(st.context, "headers", None)
    if headers:
        accept_language = headers.get("accept-language")

    header_language = detect_language_from_accept_language(accept_language)
    if header_language:
        return header_language

    timezone_language = detect_language_from_timezone(
        getattr(st.context, "timezone", None)
    )
    if timezone_language:
        return timezone_language

    return "en"


initial_language = resolve_initial_ui_language()
st.session_state.setdefault("selected_ui_language", initial_language)

selected_language = st.session_state["selected_ui_language"]
t = lambda key: translate(selected_language, key)

language_columns = st.columns([0.68, 0.32], vertical_alignment="center")
with language_columns[1]:
    # The sidebar starts collapsed for mobile, so language switching must stay
    # visible in the main flow for multilingual demo testers.
    selected_language = st.selectbox(
        t("ui_language"),
        SUPPORTED_UI_LANGUAGES,
        index=SUPPORTED_UI_LANGUAGES.index(selected_language),
        format_func=lambda language: LANGUAGE_LABELS[language],
        key="selected_ui_language",
        label_visibility="visible",
    )

t = lambda key: translate(selected_language, key)

store = InteractionStore()
presenter = ResultPresenter()

FORM_FIELD_KEYS = (
    "alterity_user_profile",
    "alterity_other_profile",
    "alterity_context_factors",
    "alterity_repair_supports",
    "interaction",
)
SCENARIO_TO_FORM_FIELD = {
    "user_profile": "alterity_user_profile",
    "other_profile": "alterity_other_profile",
    "context_factors": "alterity_context_factors",
    "repair_supports": "alterity_repair_supports",
    "interaction": "interaction",
}

for field_key in FORM_FIELD_KEYS:
    st.session_state.setdefault(field_key, "")


def render_copy_button(text: str):
    copy_label = t("copy_response")
    components.html(
        f"""
        <button
            style="
                border: 1px solid #17aeb6;
                border-radius: 8px;
                background: #ffffff;
                color: #0d7f88;
                cursor: pointer;
                font: 600 14px system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                padding: 9px 13px;
            "
            onclick='navigator.clipboard.writeText({json.dumps(text)})'
            aria-label="{copy_label}"
        >
            {copy_label}
        </button>
        """,
        height=48,
    )


def render_learning_diary():
    st.markdown(
        f'<div class="empathy-section-title">{t("learning_diary_heading")}</div>',
        unsafe_allow_html=True,
    )
    st.caption(t("learning_diary_intro"))

    diary_records = store.list(limit=20)
    if diary_records:
        query = st.text_input(
            t("learning_diary_search"),
            placeholder=t("learning_diary_search_placeholder"),
        ).strip().lower()
        matched_records = []
        for diary_record in diary_records:
            stored_record = store.get(diary_record.id)
            result_json = stored_record.result_json if stored_record else {}
            display_record = presenter.present(result_json, selected_language)
            response = display_record.get("response", {})
            learning = display_record.get("learning", {})
            bridge_message = response.get("bridge_message", "")
            reflection_question = learning.get("reflection_question", "")
            diary_interaction = extract_diary_interaction(
                diary_record.anonymized_interaction
            )
            title = diary_entry_title(
                diary_record.anonymized_interaction,
                diary_record.created_at,
                selected_language,
                getattr(st.context, "timezone", None),
            )
            searchable = " ".join(
                [
                    title,
                    diary_interaction,
                    bridge_message,
                    reflection_question,
                    diary_record.feedback or "",
                ]
            ).lower()
            if query and query not in searchable:
                continue
            matched_records.append(
                (
                    diary_record,
                    title,
                    diary_interaction,
                    bridge_message,
                    reflection_question,
                )
            )

        if not matched_records:
            st.info(t("learning_diary_no_results"))
            return

        for (
            diary_record,
            title,
            diary_interaction,
            bridge_message,
            reflection_question,
        ) in matched_records:
            with st.expander(title, expanded=False):
                st.caption(t("learning_diary_privacy_note"))
                st.write(t("learning_diary_interaction"))
                st.write(diary_interaction)

                if bridge_message:
                    st.write(t("learning_diary_bridge"))
                    st.write(display_bridge_for_language(bridge_message, selected_language))

                if reflection_question:
                    st.write(t("learning_diary_reflection"))
                    st.write(reflection_question)

                st.caption(
                    t("learning_diary_feedback").format(
                        feedback=display_feedback_for_language(
                            diary_record.feedback,
                            selected_language,
                        )
                    )
                )
                if st.button(
                    t("delete_diary_entry"),
                    key=f"delete-diary-entry-{diary_record.id}",
                ):
                    store.delete(diary_record.id)
                    st.success(t("diary_entry_deleted"), icon=":material/check_circle:")
                    st.rerun()
    else:
        st.info(t("learning_diary_empty"))


st.markdown(
    f"""
    <div class="empathy-kicker">{t("product_kicker")}</div>
    <h1 class="empathy-title">EmpathyAI</h1>
    <p class="empathy-subtitle">{t("subtitle")}</p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="empathy-band">
        {t("intro")}
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(t("notice"))

with st.expander(t("local_status"), expanded=False):
    status = get_local_runtime_status(settings)
    ollama_status = t("status_available") if status.ollama_available else t("status_unavailable")
    st.text(f"{t('status_model')}: {status.model}")
    st.text(f"Ollama: {ollama_status}")
    st.text(f"{t('status_processing_language')}: {status.processing_language}")
    st.text(f"{t('status_database')}: {status.database_path}")

st.markdown(
    f'<div class="empathy-section-title">{t("demo_scenario_heading")}</div>',
    unsafe_allow_html=True,
)
st.caption(t("demo_scenario_intro"))
scenario_options = demo_scenario_options(selected_language)
scenario_lookup = dict(scenario_options)
selected_scenario = st.selectbox(
    t("demo_scenario_select"),
    [scenario_id for scenario_id, _ in scenario_options],
    format_func=lambda scenario_id: scenario_lookup[scenario_id],
)
if st.button(t("load_demo_scenario")):
    scenario = get_demo_scenario(selected_scenario, selected_language)
    for scenario_key, field_key in SCENARIO_TO_FORM_FIELD.items():
        st.session_state[field_key] = scenario[scenario_key]
    st.success(t("demo_scenario_loaded"), icon=":material/check_circle:")

st.markdown(
    f'<div class="empathy-section-title">{t("alterity_heading")}</div>',
    unsafe_allow_html=True,
)
st.caption(t("alterity_intro"))

st.markdown(f'<div class="empathy-step-label">{t("step_user_context")}</div>', unsafe_allow_html=True)
alterity_user_profile = st.text_area(
    t("alterity_user_profile"),
    height=96,
    placeholder=t("alterity_user_profile_placeholder"),
    help=t("alterity_help"),
    key="alterity_user_profile",
)

st.markdown(f'<div class="empathy-step-label">{t("step_other_context")}</div>', unsafe_allow_html=True)
alterity_other_profile = st.text_area(
    t("alterity_other_profile"),
    height=96,
    placeholder=t("alterity_other_profile_placeholder"),
    help=t("alterity_help"),
    key="alterity_other_profile",
)

st.markdown(f'<div class="empathy-step-label">{t("step_context_factors")}</div>', unsafe_allow_html=True)
alterity_context_factors = st.text_area(
    t("alterity_context_factors"),
    height=96,
    placeholder=t("alterity_context_factors_placeholder"),
    help=t("alterity_help"),
    key="alterity_context_factors",
)

alterity_repair_supports = st.text_area(
    t("alterity_repair_supports"),
    height=96,
    placeholder=t("alterity_repair_supports_placeholder"),
    help=t("alterity_help"),
    key="alterity_repair_supports",
)

st.markdown(f'<div class="empathy-step-label">{t("step_interaction")}</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="empathy-section-title">{t("audio_input_heading")}</div>',
    unsafe_allow_html=True,
)
st.caption(t("audio_input_intro"))
audio_note = st.audio_input(
    t("audio_input_label"),
    help=t("audio_input_help"),
)
if audio_note is not None:
    st.info(t("audio_input_received"))

interaction = st.text_area(
    t("interaction_label"),
    height=220,
    placeholder=t("interaction_placeholder"),
    help=t("interaction_help"),
    key="interaction",
)

st.markdown(f'<div class="empathy-section-title">{t("save_to_diary_heading")}</div>', unsafe_allow_html=True)
store_consent = st.checkbox(
    t("save_to_diary"),
    value=False,
    help=t("save_to_diary_help"),
)
st.caption(t("save_to_diary_note"))

feedback = st.radio(
    t("feedback"),
    t("feedback_options"),
    horizontal=True,
    index=None,
    help=t("feedback_help"),
)

if st.button(t("analyze"), type="primary", use_container_width=True):
    if not interaction.strip():
        st.warning(t("missing_interaction"))
    else:
        alterity_map = {
            "user_profile": alterity_user_profile,
            "other_profile": alterity_other_profile,
            "context_factors": alterity_context_factors,
            "repair_supports": alterity_repair_supports,
        }
        interaction_for_analysis = compose_interaction_with_alterity_map(
            interaction,
            alterity_map,
        )
        with st.spinner(t("spinner")):
            try:
                use_case = AnalyzeInteractionUseCase()
                analysis = use_case.execute(
                    AnalyzeInteractionCommand(
                        interaction=interaction_for_analysis,
                        output_language="auto",
                        language_detection_text=interaction,
                        store_consent=store_consent,
                        feedback=feedback,
                    )
                )
            except EmpathyEngineError as error:
                st.error(str(error))
                st.stop()
            result = analysis.workflow_result
            display_result = analysis.display_result

        st.success(t("success"), icon=":material/check_circle:")

        if not display_result["safety"]["safe"]:
            st.warning(display_result["safety"]["guidance"])

        st.markdown('<div class="empathy-result-accent"></div>', unsafe_allow_html=True)

        bridge_text = display_bridge_for_language(
            display_result["response"]["bridge_message"],
            selected_language,
        )
        st.markdown(t("bridge_heading"))
        st.markdown(
            f"""
            <div class="empathy-bridge-card">
                <p class="empathy-bridge-label">{t("bridge_card_label")}</p>
                <p class="empathy-bridge-text">{escape(bridge_text)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_copy_button(bridge_text)

        context_tab, perspective_tab, learning_tab, privacy_tab = st.tabs(
            [
                t("result_tab_context"),
                t("result_tab_perspectives"),
                t("result_tab_learning"),
                t("result_tab_privacy"),
            ]
        )

        with context_tab:
            st.write(
                display_result["context"].get("interaction_summary")
                or t("context_text")
            )
            st.caption(
                t("language_note").format(
                    user_language=LANGUAGE_LABELS[result["language"]["user_language"]]
                )
            )

        with perspective_tab:
            st.write(t("for_user"))
            st.write(display_result["translation"]["translation_for_user"])
            st.write(t("for_other"))
            st.write(display_result["translation"]["translation_for_other_person"])

        with learning_tab:
            st.write(display_result["learning"]["reflection_question"])

        with privacy_tab:
            if store_consent:
                st.info(t("stored").format(record_id=analysis.stored_record_id))
            else:
                st.info(t("not_stored"))
                if st.button(t("save_after_analysis")):
                    saved_record_id = store.save(
                        result["interaction"],
                        result,
                        feedback,
                    )
                    st.success(
                        t("saved_after_analysis").format(
                            record_id=saved_record_id
                        ),
                        icon=":material/check_circle:",
                    )
                    st.rerun()

st.markdown('<div class="empathy-result-accent"></div>', unsafe_allow_html=True)
render_learning_diary()
