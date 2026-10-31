
import streamlit as st
from ai_engine import extract_meeting_tasks

st.set_page_config(
    page_title="MeetFlow AI",
    page_icon="🎙️",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

if "meeting_text" not in st.session_state:
    st.session_state.meeting_text = ""

if "result" not in st.session_state:
    st.session_state.result = None

if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = []

if "approved" not in st.session_state:
    st.session_state.approved = False


# ---------------- DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: white;
}

.subtitle {
    color: #aab7ca;
    font-size: 16px;
}

div[data-testid="stMetric"] {
    background: #172337;
    padding: 18px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("🎙️ MeetFlow AI")
    st.caption("From conversations to completed actions.")
    st.divider()

    st.write("🏠 Meeting Workspace")
    st.write("📋 Task Dashboard")

    st.caption("Hackathon MVP · 2026")


# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">Meeting to Execution 🚀</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Turn messy meeting conversations into clear, actionable tasks.</div>',
    unsafe_allow_html=True
)

st.divider()


# ---------------- SAMPLE MEETING ----------------

sample_meeting = (
    "We need to finish the website by Friday. "
    "Rahul will handle the frontend. "
    "Priya will complete the backend by Thursday. "
    "I will test the application. "
    "Let's schedule another meeting next Monday."
)

st.subheader("🎤 Capture Your Meeting")

st.write(
    "Speak naturally using Wispr Flow, "
    "or paste your meeting conversation below."
)

if st.button("📝 Load Sample Meeting"):
    st.session_state.meeting_text = sample_meeting

meeting_text = st.text_area(
    "Meeting Conversation",
    key="meeting_text",
    height=200,
    placeholder="Start speaking with Wispr Flow..."
)


# ---------------- AI EXTRACTION ----------------

if st.button(
    "🚀 Extract Action Items",
    type="primary",
    use_container_width=True
):

    if not meeting_text.strip():

        st.warning("Please enter a meeting conversation.")

    else:

        with st.spinner("MeetFlow AI is analysing your meeting..."):

            try:

                result = extract_meeting_tasks(meeting_text)

                # Save AI result
                st.session_state.result = result

                # Reset approval for the new meeting
                st.session_state.approved = False

                # Reset all old task checkbox states
                new_tasks = result.get("tasks", [])

                for i in range(len(new_tasks)):
                    st.session_state[f"task_done_{i}"] = False

                # Reset completion list
                st.session_state.completed_tasks = [
                    False for _ in new_tasks
                ]

                st.success("Meeting successfully analysed!")

            except Exception as e:

                st.error(f"AI extraction failed: {e}")


# ---------------- RESULTS ----------------

result = st.session_state.result

if result:

    tasks = result.get("tasks", [])
    decisions = result.get("decisions", [])
    questions = result.get("open_questions", [])

    # ---------------- METRICS ----------------

    total = len(tasks)

    # Read the latest checkbox values directly
    completed = sum(
        bool(st.session_state.get(f"task_done_{i}", False))
        for i in range(total)
    )

    pending = total - completed

    st.divider()
    st.subheader("📊 Meeting Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Tasks Extracted", total)
    col2.metric("Completed Tasks", completed)
    col3.metric("Pending Tasks", pending)

    st.divider()


    # ---------------- MEETING SUMMARY ----------------

    st.subheader("🧠 Meeting Summary")

    st.write(
        result.get(
            "meeting_summary",
            "No summary available."
        )
    )


    # ---------------- DECISIONS ----------------

    st.subheader("✅ Decisions Made")

    if decisions:

        for decision in decisions:
            st.write(f"• {decision}")

    else:

        st.info("No decisions identified.")

    st.divider()


    # ---------------- HUMAN APPROVAL ----------------

    st.subheader("📋 Review & Approve Tasks")

    if tasks:

        # Before approval, allow editing
        if not st.session_state.approved:

            st.info(
                "Review the AI-generated tasks below. "
                "You can correct owners and deadlines before approval."
            )

            for i, task in enumerate(tasks):

                with st.container(border=True):

                    st.markdown(
                        f"**Task {i + 1}: {task.get('task', 'Untitled')}**"
                    )

                    task["owner"] = st.text_input(
                        "Assigned Owner",
                        value=task.get("owner", "Not specified"),
                        key=f"owner_review_{i}"
                    )

                    task["deadline"] = st.text_input(
                        "Deadline",
                        value=task.get("deadline", "Not specified"),
                        key=f"deadline_review_{i}"
                    )

                    st.write(
                        f"⚡ Priority: {task.get('priority', 'Not specified')}"
                    )

            # Approve all tasks
            if st.button(
                "✅ Approve All Tasks",
                type="primary",
                use_container_width=True
            ):

                st.session_state.approved = True

                st.success("All tasks approved!")

                st.rerun()

        # After approval, show progress tracking
        else:

            st.success(
                "✅ Tasks approved! You can now track their progress."
            )

            for i, task in enumerate(tasks):

                with st.container(border=True):

                    st.markdown(
                        f"**Task {i + 1}: {task.get('task', 'Untitled')}**"
                    )

                    st.write(
                        f"👤 Owner: {task.get('owner', 'Not specified')}"
                    )

                    st.write(
                        f"📅 Deadline: {task.get('deadline', 'Not specified')}"
                    )

                    st.write(
                        f"⚡ Priority: {task.get('priority', 'Not specified')}"
                    )

                    # Checkbox uses Streamlit session state
                    if f"task_done_{i}" not in st.session_state:
                        st.session_state[f"task_done_{i}"] = False

                    done = st.checkbox(
                        "Mark as completed",
                        key=f"task_done_{i}"
                    )

                    # Keep completion list updated
                    st.session_state.completed_tasks[i] = done

    else:

        st.info("No action items were identified.")


    # ---------------- OPEN QUESTIONS ----------------

    st.divider()

    st.subheader("❓ Open Questions")

    if questions:

        for question in questions:
            st.write(f"• {question}")

    else:

        st.info("No unresolved questions identified.")


# ---------------- FOOTER ----------------

st.divider()

st.caption("MeetFlow AI | Built for the Agentic AI Hackathon")
