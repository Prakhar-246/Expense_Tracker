import json
import streamlit as st
from pathlib import Path
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Syne:wght@700;800&display=swap');

/* Reset & base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background — clean off-white */
.stApp {
    background: #f0f4f8;
    color: #1e293b;
}

/* Sidebar — white card feel */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0;
}
[data-testid="stSidebar"] .stRadio label {
    color: #475569 !important;
    font-size: 0.9rem;
    padding: 6px 0;
}

/* Page title */
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #0d9488 0%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.page-sub {
    color: #94a3b8;
    font-size: 0.88rem;
    margin-bottom: 1.8rem;
}

/* Stat cards */
.stat-row { display: flex; gap: 16px; margin-bottom: 2rem; flex-wrap: wrap; }
.stat-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    flex: 1;
    min-width: 160px;
    box-shadow: 0 1px 4px rgba(15,118,110,0.06);
}
.stat-label {
    font-size: 0.75rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.4rem;
}
.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #1e293b;
}
.stat-accent { color: #0d9488; }

/* Expense table rows */
.exp-row {
    display: flex;
    align-items: center;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    margin-bottom: 0.6rem;
    gap: 12px;
    transition: border-color 0.15s, box-shadow 0.15s;
}
.exp-row:hover { border-color: #0d9488; box-shadow: 0 2px 10px rgba(13,148,136,0.08); }
.exp-id {
    font-size: 0.72rem;
    color: #cbd5e1;
    width: 28px;
    font-weight: 600;
}
.exp-name { flex: 2; font-weight: 500; color: #1e293b; }
.exp-cat {
    flex: 1;
    font-size: 0.78rem;
    color: #0d9488;
    background: #ccfbf1;
    border-radius: 99px;
    padding: 2px 10px;
    text-align: center;
}
.exp-amt {
    flex: 1;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    color: #0f766e;
    text-align: right;
}
.exp-date { flex: 1; font-size: 0.77rem; color: #94a3b8; text-align: right; }

/* Section header */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #0d9488;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #e2e8f0;
}

/* Form card */
.form-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.5rem;
}

/* Streamlit input overrides */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background-color: #f8fafc !important;
    border-color: #cbd5e1 !important;
    color: #1e293b !important;
    border-radius: 8px !important;
}
.stTextInput label, .stNumberInput label, .stSelectbox label, .stDateInput label {
    color: #64748b !important;
    font-size: 0.82rem !important;
    font-weight: 500;
}

/* Button — teal-to-cyan gradient fill */
.stButton > button {
    background: linear-gradient(135deg, #0d9488 0%, #06b6d4 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.4rem !important;
    width: 100%;
    letter-spacing: 0.02em;
    transition: box-shadow 0.2s, filter 0.2s !important;
}
.stButton > button:hover {
    filter: brightness(1.08) !important;
    box-shadow: 0 4px 20px rgba(6,182,212,0.35) !important;
}
.stButton > button:active {
    filter: brightness(0.95) !important;
}

/* Delete buttons — soft red gradient */
[data-testid="stHorizontalBlock"] .stButton:last-child > button {
    background: linear-gradient(135deg, #f43f5e 0%, #fb923c 100%) !important;
    color: #fff !important;
    border: none !important;
    font-size: 0.82rem !important;
}
[data-testid="stHorizontalBlock"] .stButton:last-child > button:hover {
    box-shadow: 0 4px 16px rgba(244,63,94,0.3) !important;
    filter: brightness(1.06) !important;
}

/* Toast / success */
.success-pill {
    background: #f0fdfa;
    border: 1px solid #99f6e4;
    color: #0f766e;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-size: 0.88rem;
    margin-bottom: 1rem;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #94a3b8;
}
.empty-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }

/* Divider */
hr { border-color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Data layer ───────────────────────────────────────────────────────────────
DATABASE = "expense_tracker.json"

def load_data():
    p = Path(DATABASE)
    if p.exists():
        content = p.read_text()
        if content:
            return json.loads(content)
    return {"expenses": []}

def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)

def next_id(data):
    if not data["expenses"]:
        return 1
    return max(e["id"] for e in data["expenses"]) + 1

# ── Session state ─────────────────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = load_data()
if "toast" not in st.session_state:
    st.session_state.toast = None

def data():
    return st.session_state.data

# ── Sidebar nav ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.35rem;font-weight:800;color:#0d9488;padding:1rem 0 1.5rem;">💸 SpendLog</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigate",
        ["📋 All Expenses", "➕ Add Expense", "✏️ Update Expense", "🗑️ Delete Expense", "📊 Summary"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    total = sum(float(e["amount"].replace("$","")) for e in data()["expenses"])
    count = len(data()["expenses"])
    st.markdown(f'<div class="stat-label">Total spent</div><div style="font-family:Syne,sans-serif;font-size:1.4rem;font-weight:700;color:#0d9488;">${total:,.2f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-label" style="margin-top:0.8rem;">Entries</div><div style="font-family:Syne,sans-serif;font-size:1.4rem;font-weight:700;color:#0d9488;">{count}</div>', unsafe_allow_html=True)

# ── Toast ────────────────────────────────────────────────────────────────────
if st.session_state.toast:
    st.markdown(f'<div class="success-pill">✓ {st.session_state.toast}</div>', unsafe_allow_html=True)
    st.session_state.toast = None

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ALL EXPENSES
# ══════════════════════════════════════════════════════════════════════════════
if page == "📋 All Expenses":
    st.markdown('<div class="page-title">All Expenses</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Your complete spending log — tap any entry for details.</div>', unsafe_allow_html=True)

    expenses = data()["expenses"]

    if not expenses:
        st.markdown('<div class="empty-state"><div class="empty-icon">🧾</div><div>No expenses yet.</div><div style="font-size:0.82rem;margin-top:0.3rem;">Add your first one from the sidebar.</div></div>', unsafe_allow_html=True)
    else:
        # Category filter
        cats = sorted(set(e["category"] for e in expenses))
        selected_cats = st.multiselect("Filter by category", cats, default=cats, label_visibility="collapsed",
                                        placeholder="Filter by category…")
        filtered = [e for e in expenses if e["category"] in selected_cats]

        # Stats row
        if filtered:
            famt = [float(e["amount"].replace("$","")) for e in filtered]
            st.markdown(f"""
            <div class="stat-row">
              <div class="stat-card"><div class="stat-label">Total</div><div class="stat-value stat-accent">${sum(famt):,.2f}</div></div>
              <div class="stat-card"><div class="stat-label">Average</div><div class="stat-value">${sum(famt)/len(famt):,.2f}</div></div>
              <div class="stat-card"><div class="stat-label">Largest</div><div class="stat-value">${max(famt):,.2f}</div></div>
              <div class="stat-card"><div class="stat-label">Entries</div><div class="stat-value">{len(filtered)}</div></div>
            </div>
            """, unsafe_allow_html=True)

        # Column headers
        h1, h2, h3, h4, h5 = st.columns([0.5, 3, 2, 1.5, 2])
        h1.markdown('<div style="font-size:0.72rem;color:#94a3b8;font-weight:600;">ID</div>', unsafe_allow_html=True)
        h2.markdown('<div style="font-size:0.72rem;color:#94a3b8;font-weight:600;">NAME</div>', unsafe_allow_html=True)
        h3.markdown('<div style="font-size:0.72rem;color:#94a3b8;font-weight:600;">CATEGORY</div>', unsafe_allow_html=True)
        h4.markdown('<div style="font-size:0.72rem;color:#94a3b8;font-weight:600;text-align:right;">AMOUNT</div>', unsafe_allow_html=True)
        h5.markdown('<div style="font-size:0.72rem;color:#94a3b8;font-weight:600;">DATE</div>', unsafe_allow_html=True)

        for e in filtered:
            c1, c2, c3, c4, c5 = st.columns([0.5, 3, 2, 1.5, 2])
            c1.markdown(f'<div style="color:#cbd5e1;font-size:0.78rem;padding-top:6px;">#{e["id"]}</div>', unsafe_allow_html=True)
            c2.markdown(f'<div style="color:#1e293b;font-weight:500;padding-top:6px;">{e["name"]}</div>', unsafe_allow_html=True)
            c3.markdown(f'<div style="color:#0d9488;font-size:0.78rem;padding-top:6px;">{e["category"]}</div>', unsafe_allow_html=True)
            c4.markdown(f'<div style="color:#0f766e;font-weight:700;text-align:right;padding-top:6px;">{e["amount"]}</div>', unsafe_allow_html=True)
            upd = e.get("updatedate", "—")
            c5.markdown(f'<div style="color:#94a3b8;font-size:0.78rem;padding-top:6px;">{e["datetime"]}{f" (upd {upd})" if upd != "—" else ""}</div>', unsafe_allow_html=True)
            st.markdown('<hr style="margin:4px 0;">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ADD EXPENSE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "➕ Add Expense":
    st.markdown('<div class="page-title">Add Expense</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Record a new spending entry.</div>', unsafe_allow_html=True)

    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("Expense name", placeholder="e.g. Lunch at café")
        amount = col2.number_input("Amount ($)", min_value=0.0, step=0.5, format="%.2f")
        cat_options = ["Food", "Transport", "Shopping", "Health", "Entertainment", "Bills", "Other"]
        category = col1.selectbox("Category", cat_options)
        custom_cat = col2.text_input("Custom category (optional)", placeholder="Leave blank to use above")

        submitted = st.form_submit_button("Save Expense")
        if submitted:
            if not name.strip():
                st.error("Expense name is required.")
            elif amount <= 0:
                st.error("Amount must be greater than $0.")
            else:
                final_cat = custom_cat.strip() if custom_cat.strip() else category
                entry = {
                    "id": next_id(data()),
                    "name": name.strip(),
                    "amount": f"${amount:.2f}",
                    "category": final_cat,
                    "datetime": str(datetime.now().date()),
                    "date": "No Update"
                }
                data()["expenses"].append(entry)
                save_data(data())
                st.session_state.toast = f'"{name}" added successfully.'
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: UPDATE EXPENSE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "✏️ Update Expense":
    st.markdown('<div class="page-title">Update Expense</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Edit an existing entry by its ID.</div>', unsafe_allow_html=True)

    expenses = data()["expenses"]
    if not expenses:
        st.info("No expenses to update yet.")
    else:
        ids = [e["id"] for e in expenses]
        sel_id = st.selectbox("Select expense to edit", ids,
                              format_func=lambda i: f"#{i} — {next(e['name'] for e in expenses if e['id']==i)}")

        current = next(e for e in expenses if e["id"] == sel_id)

        with st.form("update_form"):
            col1, col2 = st.columns(2)
            new_name = col1.text_input("Name", value=current["name"])
            cur_amt = float(current["amount"].replace("$",""))
            new_amount = col2.number_input("Amount ($)", value=cur_amt, min_value=0.0, step=0.5, format="%.2f")
            cat_options = ["Food", "Transport", "Shopping", "Health", "Entertainment", "Bills", "Other"]
            def_cat = current["category"] if current["category"] in cat_options else "Other"
            new_cat = col1.selectbox("Category", cat_options, index=cat_options.index(def_cat))
            custom_cat = col2.text_input("Custom category", value="" if current["category"] in cat_options else current["category"])

            submitted = st.form_submit_button("Update Expense")
            if submitted:
                if not new_name.strip():
                    st.error("Name cannot be empty.")
                else:
                    final_cat = custom_cat.strip() if custom_cat.strip() else new_cat
                    for e in data()["expenses"]:
                        if e["id"] == sel_id:
                            e["name"] = new_name.strip()
                            e["amount"] = f"${new_amount:.2f}"
                            e["category"] = final_cat
                            e["updatedate"] = str(datetime.now().date())
                    save_data(data())
                    st.session_state.toast = f'Expense #{sel_id} updated.'
                    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DELETE EXPENSE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗑️ Delete Expense":
    st.markdown('<div class="page-title">Delete Expense</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Permanently remove an entry from your log.</div>', unsafe_allow_html=True)

    expenses = data()["expenses"]
    if not expenses:
        st.info("Nothing to delete.")
    else:
        for e in expenses:
            c1, c2, c3, c4, c5 = st.columns([0.5, 3, 2, 1.5, 1.2])
            c1.markdown(f'<div style="color:#cbd5e1;font-size:0.78rem;padding-top:8px;">#{e["id"]}</div>', unsafe_allow_html=True)
            c2.markdown(f'<div style="color:#1e293b;padding-top:8px;">{e["name"]}</div>', unsafe_allow_html=True)
            c3.markdown(f'<div style="color:#0d9488;font-size:0.82rem;padding-top:8px;">{e["category"]}</div>', unsafe_allow_html=True)
            c4.markdown(f'<div style="color:#0d9488;font-weight:700;padding-top:8px;">{e["amount"]}</div>', unsafe_allow_html=True)
            if c5.button("Delete", key=f"del_{e['id']}"):
                name_del = e["name"]
                data()["expenses"] = [x for x in data()["expenses"] if x["id"] != e["id"]]
                save_data(data())
                st.session_state.toast = f'"{name_del}" deleted.'
                st.rerun()
            st.markdown('<hr style="margin:4px 0;">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Summary":
    st.markdown('<div class="page-title">Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">A breakdown of your spending patterns.</div>', unsafe_allow_html=True)

    expenses = data()["expenses"]
    if not expenses:
        st.markdown('<div class="empty-state"><div class="empty-icon">📊</div><div>No data yet.</div></div>', unsafe_allow_html=True)
    else:
        amounts = [float(e["amount"].replace("$","")) for e in expenses]
        total = sum(amounts)
        avg = total / len(amounts)
        top = max(expenses, key=lambda e: float(e["amount"].replace("$","")))

        st.markdown(f"""
        <div class="stat-row">
          <div class="stat-card"><div class="stat-label">Total spent</div><div class="stat-value stat-accent">${total:,.2f}</div></div>
          <div class="stat-card"><div class="stat-label">Average per entry</div><div class="stat-value">${avg:,.2f}</div></div>
          <div class="stat-card"><div class="stat-label">Entries</div><div class="stat-value">{len(expenses)}</div></div>
          <div class="stat-card"><div class="stat-label">Biggest spend</div><div class="stat-value" style="font-size:1.1rem;">{top["name"]} ({top["amount"]})</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">By Category</div>', unsafe_allow_html=True)
        cat_totals = {}
        for e in expenses:
            cat_totals[e["category"]] = cat_totals.get(e["category"], 0) + float(e["amount"].replace("$",""))

        for cat, amt in sorted(cat_totals.items(), key=lambda x: -x[1]):
            pct = amt / total * 100
            c1, c2, c3 = st.columns([2, 5, 1])
            c1.markdown(f'<div style="color:#0d9488;font-size:0.88rem;padding-top:6px;">{cat}</div>', unsafe_allow_html=True)
            c2.progress(int(pct))
            c3.markdown(f'<div style="color:#0d9488;font-size:0.88rem;padding-top:6px;text-align:right;">${amt:,.2f}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:1.5rem;">Recent Entries</div>', unsafe_allow_html=True)
        for e in sorted(expenses, key=lambda x: x["datetime"], reverse=True)[:5]:
            col1, col2, col3 = st.columns([3, 2, 1.5])
            col1.markdown(f'<div style="color:#1e293b;font-size:0.9rem;">{e["name"]}</div>', unsafe_allow_html=True)
            col2.markdown(f'<div style="color:#94a3b8;font-size:0.78rem;">{e["datetime"]} · {e["category"]}</div>', unsafe_allow_html=True)
            col3.markdown(f'<div style="color:#0d9488;font-weight:700;text-align:right;">{e["amount"]}</div>', unsafe_allow_html=True)
            st.markdown('<hr style="margin:4px 0;">', unsafe_allow_html=True)