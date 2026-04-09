import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io
import time
import streamlit.components.v1 as components
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import TableStyle
from zoneinfo import ZoneInfo

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="SASTRA COE CUB",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Custom CSS ----------------
st.markdown("""
<style>

/* =========================
   GLOBAL BACKGROUND
========================= */

.stApp {
    background-color: #f4f6f9;
}

/* Main container padding */
.block-container {
    padding-top: 3rem;
    padding-left: 4rem;
    padding-right: 4rem;
}

/* =========================
   HEADINGS & TEXT
========================= */

h1 {
    color: #0f172a !important;
    text-align: center;
    font-weight: 700;
    margin-bottom: 10px;
    margin-top: 0;
}

h2, h3 {
    color: #1e293b !important;
    font-weight: 600;
}

p, label, span, div {
    color: #1e293b;
}

/* =========================
   CARD STYLE
========================= */

.section-card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.05);
    margin-bottom: 30px;
}

/* =========================
   SIDEBAR
========================= */

[data-testid="stSidebar"] {
    background-color: #1e293b;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* =============================================
   SIDEBAR TOGGLE — nuclear override
   Targets every known selector Streamlit uses
   for the collapsed-sidebar re-open button
============================================= */

/* Collapsed state: the small arrow tab on the left edge */
[data-testid="collapsedControl"],
[data-testid="collapsedControl"] > button,
section[data-testid="stSidebarCollapsedControl"],
section[data-testid="stSidebarCollapsedControl"] > button {
    display:        flex !important;
    visibility:     visible !important;
    opacity:        1 !important;
    pointer-events: auto !important;
    position:       fixed !important;
    left:           0 !important;
    top:            50vh !important;
    transform:      translateY(-50%) !important;
    z-index:        999999 !important;
    width:          2rem !important;
    height:         3.5rem !important;
    background-color: #2563eb !important;
    border-radius:  0 10px 10px 0 !important;
    border:         none !important;
    box-shadow:     3px 0 10px rgba(0,0,0,0.35) !important;
    cursor:         pointer !important;
    align-items:    center !important;
    justify-content: center !important;
    color:          white !important;
}

[data-testid="collapsedControl"]:hover,
[data-testid="collapsedControl"] > button:hover,
section[data-testid="stSidebarCollapsedControl"]:hover,
section[data-testid="stSidebarCollapsedControl"] > button:hover {
    background-color: #1d4ed8 !important;
    width: 2.4rem !important;
}

/* Arrow icon inside the button */
[data-testid="collapsedControl"] svg,
[data-testid="collapsedControl"] > button svg,
section[data-testid="stSidebarCollapsedControl"] svg,
section[data-testid="stSidebarCollapsedControl"] > button svg {
    fill:       white !important;
    color:      white !important;
    display:    block !important;
    visibility: visible !important;
    opacity:    1 !important;
    width:      1rem !important;
    height:     1rem !important;
}

/* Collapse button (inside open sidebar) */
[data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"],
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {
    visibility:     visible !important;
    opacity:        1 !important;
    background-color: #2563eb !important;
    border-radius:  0 8px 8px 0 !important;
    color:          white !important;
}

[data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"] svg,
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button svg {
    fill:    white !important;
    color:   white !important;
    opacity: 1 !important;
}

/* =========================
   INPUT FIELDS
========================= */

input, textarea {
    background-color: #ffffff !important;
    color: #111827 !important;
    caret-color: #2563eb !important;
}

/* Streamlit specific inputs */
.stTextInput input,
.stTextArea textarea,
.stDateInput input,
.stNumberInput input {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    padding: 8px !important;
    caret-color: #2563eb !important;
}

/* Focus effect */
.stTextInput input:focus,
.stTextArea textarea:focus,
.stDateInput input:focus,
.stNumberInput input:focus {
    border: 2px solid #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37,99,235,0.15) !important;
}

div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* Dropdown arrow */
svg {
    fill: #000000 !important;
}

/* =========================
   BUTTONS
========================= */

.stButton button {
    background-color: #2563eb !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    border: none !important;
}

.stButton button:hover {
    background-color: #1d4ed8 !important;
}

/* Download button specific */
.stDownloadButton button {
    background-color: #2563eb !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    border: none !important;
}

.stDownloadButton button:hover {
    background-color: #1d4ed8 !important;
}

/* =========================
   DATAFRAME - force light mode + text wrapping
========================= */

[data-testid="stDataFrame"] {
    background-color: #ffffff !important;
    border-radius: 10px;
    padding: 10px;

    /* glide-data-grid CSS custom properties — read at paint time */
    --gdg-bg-cell:              #ffffff !important;
    --gdg-bg-cell-medium:       #f8fafc !important;
    --gdg-bg-header:            #f1f5f9 !important;
    --gdg-bg-header-has-focus:  #e2e8f0 !important;
    --gdg-bg-header-hovered:    #e8edf2 !important;
    --gdg-text-dark:            #1e293b !important;
    --gdg-text-medium:          #475569 !important;
    --gdg-text-light:           #64748b !important;
    --gdg-text-header:          #0f172a !important;
    --gdg-border-color:         #e2e8f0 !important;
    --gdg-accent-color:         #2563eb !important;
    --gdg-accent-light:         rgba(37,99,235,0.15) !important;
    --gdg-selection-color:      rgba(37,99,235,0.15) !important;
    --gdg-link-color:           #2563eb !important;
}

/* Wrapper divs inside the dataframe widget */
[data-testid="stDataFrame"] > div,
[data-testid="stDataFrame"] > div > div {
    background-color: #ffffff !important;
}

/* The scrollable canvas container */
.dvn-scroller { background-color: #ffffff !important; }
.dvn-underlay > * { background-color: #ffffff !important; }

/* All glide-data-grid class elements */
[class^="gdg-"], [class*=" gdg-"] {
    background-color: #ffffff !important;
    color: #1e293b !important;
}

/* Force text wrapping */
[data-testid="stDataFrame"] td {
    white-space: pre-wrap !important;
    word-break: break-word !important;
    max-width: 300px;
    color: #1e293b !important;
    background-color: #ffffff !important;
}

/* =========================
   REMOVE DARK MODE OVERRIDES
========================= */

/* Hide toolbar icons but keep sidebar toggle */
[data-testid="stToolbar"] {
    background: transparent;
}
            
/* =========================
   FINAL TIME DROPDOWN FIX
========================= */

/* Popover container */
div[data-baseweb="popover"] {
    background-color: #ffffff !important;
}

/* List container */
ul[role="listbox"] {
    background-color: #ffffff !important;
}

/* Each option container */
li[role="option"] {
    background-color: #ffffff !important;
}

/* FORCE text color inside option */
li[role="option"] * {
    color: #000000 !important;
    opacity: 1 !important;
}

/* Hover */
li[role="option"]:hover {
    background-color: #f1f5f9 !important;
}

/* Selected option */
li[aria-selected="true"] {
    background-color: #e2e8f0 !important;
}

li[aria-selected="true"] * {
    color: #000000 !important;
    opacity: 1 !important;
}

/* =========================
   INFO BOXES
========================= */

.stInfo {
    background-color: #dbeafe !important;
    border-left-color: #2563eb !important;
}

.stSuccess {
    background-color: #d1fae5 !important;
    border-left-color: #059669 !important;
}

.stError {
    background-color: #fee2e2 !important;
    border-left-color: #dc2626 !important;
}

.stWarning {
    background-color: #fef3c7 !important;
    border-left-color: #d97706 !important;
}

/* =========================
   HEADER ALIGNMENT
========================= */

.header-container {
    margin-top: 40px;
    margin-bottom: 30px;
}

.header-logo {
    margin-top: 30px;
    text-align: center;
}

/* =========================
   DATE PICKER FIX - FORCE LIGHT THEME
========================= */

/* Date input container */
.stDateInput {
    background-color: #ffffff !important;
}

/* Date picker popup calendar */
div[data-baseweb="calendar"] {
    background-color: #ffffff !important;
    color: #000000 !important;
}

div[data-baseweb="calendar"] * {
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* Calendar header */
div[data-baseweb="calendar"] header {
    background-color: #f8fafc !important;
    color: #0f172a !important;
}

/* Calendar days */
div[data-baseweb="calendar"] button {
    background-color: #ffffff !important;
    color: #0f172a !important;
}

div[data-baseweb="calendar"] button:hover {
    background-color: #e2e8f0 !important;
}

/* Selected date */
div[data-baseweb="calendar"] button[aria-selected="true"] {
    background-color: #2563eb !important;
    color: #ffffff !important;
}

/* Today's date */
div[data-baseweb="calendar"] button[aria-current="date"] {
    border: 2px solid #2563eb !important;
}

/* Calendar month/year dropdown */
div[data-baseweb="calendar"] div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* =========================
   TABS STYLING
========================= */

.stTabs [data-baseweb="tab-list"] {
    background-color: #f1f5f9;
    border-radius: 8px;
    padding: 5px;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #475569;
    border-radius: 6px;
}

.stTabs [aria-selected="true"] {
    background-color: #ffffff !important;
    color: #2563eb !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ---------------- Google Sheets URLs ----------------
# PLEASE REPLACE THESE WITH YOUR ACTUAL GOOGLE SHEETS URLs
LOG_SHEET_URL = "https://docs.google.com/spreadsheets/d/17ygWdYJSKHKLrx5_8iMBuSkTaWuC_i1X47ljcKdRo98/edit?gid=1732522338#gid=1732522338"
TIMETABLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1GZpFmP-fMhupeakDTSd7L8U6r6oFVY6l1MW0KqobIaw/edit?gid=912912585#gid=912912585"
THIRD_YEAR_SHEET_URL = "https://docs.google.com/spreadsheets/d/1hD58PSTYLe_WTa8VpkUMLXY6AsODZdvlIdFRwZcT_c8/edit?gid=2075450599#gid=2075450599"
FINAL_YEAR_SHEET_URL = "https://docs.google.com/spreadsheets/d/1p9JmHYPTBMJamtzXYLy_zOFayMbW15Wcymp4sORsKmI/edit?gid=1506650140#gid=1506650140"

from streamlit_gsheets import GSheetsConnection
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Failed to connect to Google Sheets. Please ensure .streamlit/secrets.toml is configured correctly.")
    conn = None

def safe_read(spreadsheet, worksheet=0, max_retries=3, delay=2):
    """Wrapper for conn.read with automatic retry logic for API limits."""
    if conn is None: return pd.DataFrame()
    for attempt in range(max_retries):
        try:
            return conn.read(spreadsheet=spreadsheet, worksheet=worksheet).dropna(how="all")
        except Exception as e:
            error_str = str(e).lower()
            # If it's a rate limit error (429), wait and retry
            if "exhausted" in error_str or "429" in error_str or "limit" in error_str:
                if attempt < max_retries - 1:
                    time.sleep(delay * (attempt + 1))  # Exponential backoff
                    continue
            # For other errors or final attempt, re-raise to be caught by UI
            raise e
    return pd.DataFrame()

# Problem Statements Dictionary
PROBLEM_STATEMENTS = {
    "1": "EWS",
    "2": "Customer Segmentation",
    "3": "Transaction Acquisition",
    "4": "CASA Buildup",
    "5": "AI Insight Chatbot For Staffs",
    "6": "HR Chatbot"
}


@st.cache_data(ttl=3600)
def load_students():
    """Load main student list from Sheet1."""
    return safe_read(spreadsheet=LOG_SHEET_URL, worksheet="Sheet1")

@st.cache_data(ttl=600)
def load_logs():
    """Load all student logs from Sheet2."""
    df = safe_read(spreadsheet=LOG_SHEET_URL, worksheet="Sheet2")
    if df.empty: return pd.DataFrame(columns=["reg_no","name","faculty","date","start_time","end_time","description"])
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.normalize()
    if 'reg_no' in df.columns:
        df['reg_no'] = df['reg_no'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    return df

def save_log(new_data):
    if conn is None: return
    df_logs = load_logs()
    new_entry = pd.DataFrame([new_data])
    new_entry['date'] = pd.to_datetime(new_entry['date'], errors='coerce').dt.normalize()
    new_entry['date'] = new_entry['date'].dt.strftime('%Y-%m-%d')
    if 'date' in df_logs.columns:
        df_logs['date'] = pd.to_datetime(df_logs['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df_logs = pd.concat([df_logs, new_entry], ignore_index=True)
    conn.update(spreadsheet=LOG_SHEET_URL, worksheet="Sheet2", data=df_logs)
    load_logs.clear()

@st.cache_data(ttl=3600)
def load_professors():
    """Load the list of professors/faculty."""
    return safe_read(spreadsheet=LOG_SHEET_URL, worksheet="Sheet3")

def save_professor(new_prof):
    if conn is None: return
    df_prof = load_professors()
    df_prof = pd.concat([df_prof, pd.DataFrame([new_prof])], ignore_index=True)
    conn.update(spreadsheet=LOG_SHEET_URL, worksheet="Sheet3", data=df_prof)
    load_professors.clear()

@st.cache_data(ttl=600)
def load_active_sessions():
    """Load active (logged-in) sessions."""
    df = safe_read(spreadsheet=LOG_SHEET_URL, worksheet="Active_Sessions")
    if df.empty: return pd.DataFrame(columns=["reg_no", "name", "faculty", "problem_no", "start_time"])
    
    if "reg_no" in df.columns:
        df["reg_no"] = df["reg_no"].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    return df

def save_active_session(new_session):
    if conn is None: return
    df = load_active_sessions()
    if not df.empty and "reg_no" in df.columns:
        df = df[df["reg_no"] != str(new_session["reg_no"]).strip()]
    df = pd.concat([df, pd.DataFrame([new_session])], ignore_index=True)
    conn.update(spreadsheet=LOG_SHEET_URL, worksheet="Active_Sessions", data=df)
    load_active_sessions.clear()

def remove_active_session(reg_no):
    if conn is None: return
    df = load_active_sessions()
    if not df.empty and "reg_no" in df.columns:
        df = df[df["reg_no"] != str(reg_no).strip()]
        conn.update(spreadsheet=LOG_SHEET_URL, worksheet="Active_Sessions", data=df)
        load_active_sessions.clear()

@st.cache_data(ttl=600)
def load_student_hours():
    """Load total accumulated hours per student."""
    df = safe_read(spreadsheet=LOG_SHEET_URL, worksheet="Student_Hours")
    if df.empty: return pd.DataFrame(columns=["reg_no", "name", "total_hours"])
    
    if "reg_no" in df.columns:
        df["reg_no"] = df["reg_no"].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    return df

def update_student_hours(reg_no, name, hours_worked):
    if conn is None: return
    df = load_student_hours()
    reg_no_str = str(reg_no).strip()
    
    if df.empty or reg_no_str not in df["reg_no"].values:
        new_entry = {"reg_no": reg_no_str, "name": name, "total_hours": hours_worked}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    else:
        idx = df[df["reg_no"] == reg_no_str].index[0]
        df.loc[idx, "total_hours"] += hours_worked
        
    conn.update(spreadsheet=LOG_SHEET_URL, worksheet="Student_Hours", data=df)
    load_student_hours.clear()

def parse_time_slot(time_str):
    """Parse '8:45 to 9:45' into two datetime.time objects for today."""
    if not isinstance(time_str, str) or "to" not in time_str.lower():
        return None, None
        
    parts = [p.strip() for p in time_str.lower().split("to")]
    if len(parts) != 2:
        return None, None
        
    def to_24_from_context(h, m, is_start=True, prev_h24=8):
        if h == 12: return 12, m
        if h < 8: return h + 12, m
        if h >= 8 and h < 12:
            if prev_h24 >= 12 or h < prev_h24:
                return h + 12, m
            return h, m
        return h, m

    try:
        from datetime import time
        sh, sm = map(int, parts[0].split(':'))
        eh, em = map(int, parts[1].split(':'))
        
        start_h24, start_m24 = to_24_from_context(sh, sm, True, 8)
        end_h24, end_m24 = to_24_from_context(eh, em, False, start_h24)
        
        return time(start_h24, start_m24), time(end_h24, end_m24)
    except Exception:
        return None, None

@st.cache_data(ttl=3600)
def load_timetable(day_name):
    """Load the schedule from cub (1).xlsx for a specific day."""
    df = safe_read(spreadsheet=TIMETABLE_SHEET_URL, worksheet=day_name)
    if df.empty: return [], []
    
    try:
        df = df.dropna(axis=1, how="all")
        time_headers = df.iloc[0].values
        student_col = df.columns[1] 
        
        schedule = []
        for idx in range(1, len(df)):
            name = df.iloc[idx][student_col]
            if pd.isna(name): continue
            
            row_data = {"name": str(name).strip(), "slots": {}}
            is_sys_occ = "system" in str(name).lower() and "occupied" in str(name).lower()
            
            for col_idx in range(2, len(df.columns)):
                if col_idx < len(time_headers):
                    time_str = str(time_headers[col_idx]).strip()
                    if 'to' not in time_str.lower(): continue
                    val = df.iloc[idx, col_idx]
                    
                    if pd.notna(val):
                        if is_sys_occ and float(val) > 0:
                            row_data["slots"][time_str] = int(val)
                        elif not is_sys_occ and val == 1:
                            row_data["slots"][time_str] = True
                    
            schedule.append(row_data)
        
        slots_ordered = []
        for t in time_headers[2:]:
            s = str(t).strip()
            if 'to' in s.lower() and s not in slots_ordered:
                slots_ordered.append(s)
                
        return schedule, slots_ordered
    except Exception as e:
        return [], []

@st.cache_data(ttl=3600)
def load_target_hours():
    """Load target weekly hours for each student from Sheet1."""
    df = safe_read(spreadsheet=TIMETABLE_SHEET_URL, worksheet="Sheet1")
    if df.empty: return {}
    
    try:
        name_col = df.columns[1] 
        target_col = "Total Hrs"
        if target_col not in df.columns:
            return {}
            
        targets = {}
        import re
        def norm(n): return "".join(sorted(re.findall(r'[a-zA-Z]+', str(n).lower())))
        
        for idx, row in df.iterrows():
            if pd.notna(row[name_col]) and pd.notna(row[target_col]):
                val = row[target_col]
                try:
                    targets[norm(row[name_col])] = float(val)
                except:
                    pass
        return targets
    except:
        return {}


@st.cache_data(ttl=3600)
def load_third_year_students():
    """Load 3rd year students from separate Excel file"""
    df = safe_read(spreadsheet=THIRD_YEAR_SHEET_URL, worksheet=0)
    if df.empty: return pd.DataFrame(columns=["reg_no", "name", "guide", "problem_no"])
    
    df.columns = df.columns.astype(str).str.strip().str.lower()
    if "reg no" in df.columns: df["reg_no"] = df["reg no"].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    if "student name" in df.columns: df["name"] = df["student name"]
    if "guide name" in df.columns: df["guide"] = df["guide name"]
    if "problem statement no." in df.columns: df["problem_no"] = df["problem statement no."].astype(str).str.strip()
    return df

@st.cache_data(ttl=3600)
def load_final_year_students():
    """Load final year students from separate Excel file"""
    df = safe_read(spreadsheet=FINAL_YEAR_SHEET_URL, worksheet=0)
    if df.empty: return pd.DataFrame(columns=["reg_no", "name", "guide", "problem_no"])
    
    df.columns = df.columns.astype(str).str.strip().str.lower()
    if "reg no" in df.columns: df["reg_no"] = df["reg no"].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    if "student name" in df.columns: df["name"] = df["student name"]
    if "guide name" in df.columns: df["guide"] = df["guide name"]
    if "problem statement no." in df.columns: df["problem_no"] = df["problem statement no."].astype(str).str.strip()
    return df

def get_all_students():
    """Combine all students from both year files"""
    third_year = load_third_year_students()
    final_year = load_final_year_students()
    all_students = pd.concat([third_year, final_year], ignore_index=True)
    return all_students

def get_monday_of_current_week():
    """Get the Monday of the current week as a date (midnight, no time component)"""
    today = datetime.today().date()
    monday = today - timedelta(days=today.weekday())  # weekday() 0=Monday
    return pd.Timestamp(monday)

def get_problem_statement_name(prob_no):
    """Get problem statement name from ID"""
    s = str(prob_no).strip()
    if s.endswith(".0"): 
        s = s[:-2]
    return PROBLEM_STATEMENTS.get(s, "Unknown")

def prepare_display_df(df):
    """Prepare a dataframe for display on the web - format dates nicely."""
    display = df.copy()
    if 'date' in display.columns:
        display['date'] = pd.to_datetime(display['date'], errors='coerce').dt.strftime('%d-%m-%Y')
    # Convert times to string for display
    for col in ['start_time', 'end_time']:
        if col in display.columns:
            display[col] = display[col].astype(str)
    return display

def light_table(df, column_config=None):
    """
    Render a dataframe as a fully light-mode HTML table.
    Streamlit's st.dataframe uses a canvas renderer that ignores CSS in dark-mode
    OS/browser settings. This helper always renders in light mode.
    column_config is accepted for API compatibility but ignored (labels come from df columns).
    """
    display = df.copy()
    # Convert all columns to strings for safe HTML rendering
    for col in display.columns:
        display[col] = display[col].astype(str).replace('nan', '').replace('NaT', '')

    # Build HTML
    header_cells = "".join(f"<th>{col}</th>" for col in display.columns)
    rows_html = ""
    for i, row in display.iterrows():
        bg = "#ffffff" if i % 2 == 0 else "#f8fafc"
        cells = "".join(
            f"<td style='background:{bg};'>{val}</td>"
            for val in row.values
        )
        rows_html += f"<tr>{cells}</tr>"

    html = f"""
    <div style="overflow-x:auto; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:1rem;">
    <table style="
        width:100%;
        border-collapse:collapse;
        font-family:sans-serif;
        font-size:13px;
        color:#1e293b;
        background:#ffffff;
    ">
        <thead>
            <tr style="background:#f1f5f9; color:#0f172a; text-align:left;">
                {header_cells}
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


    """Class to handle PDF generation with footer on every page"""
    def __init__(self, title="Weekly Log Report", report_type="General"):
        self.title = title
        self.report_type = report_type
        self.report_time = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d-%m-%Y %H:%M:%S")
        self.buffer = io.BytesIO()
        # FIX: Use landscape A4 for more column space
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=landscape(A4),
            rightMargin=40,
            leftMargin=40,
            topMargin=50,
            bottomMargin=60
        )
        self.elements = []
        self.style = getSampleStyleSheet()

    def header_footer(self, canvas, doc):
        """Add header and footer to every page"""
        canvas.saveState()
        footer_text = f"SASTRA COE CUB | Report generated on: {self.report_time} | Page {doc.page}"
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.HexColor('#64748b'))
        canvas.drawCentredString(landscape(A4)[0] / 2, 30, footer_text)
        canvas.restoreState()

    def build(self, data):
        """Build the PDF with properly wrapped table"""
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.style['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=6,
            alignment=1
        )
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.style['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#475569'),
            spaceAfter=4,
            alignment=1
        )
        report_info_style = ParagraphStyle(
            'ReportInfo',
            parent=self.style['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=12,
            alignment=1
        )

        # Paragraph styles for table cells (enables text wrapping in PDF)
        header_cell_style = ParagraphStyle(
            'HeaderCell',
            parent=self.style['Normal'],
            fontSize=11,
            textColor=colors.whitesmoke,
            fontName='Helvetica-Bold',
            wordWrap='LTR',
            leading=14,
        )
        body_cell_style = ParagraphStyle(
            'BodyCell',
            parent=self.style['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1e293b'),
            fontName='Helvetica',
            wordWrap='LTR',
            leading=13,
        )

        self.elements.append(Paragraph("SASTRA COE CUB", title_style))
        self.elements.append(Paragraph(self.title, subtitle_style))
        self.elements.append(Paragraph(self.report_type, report_info_style))
        self.elements.append(Spacer(1, 10))

        # Prepare table data
        display_data = data.copy()
        if 'date' in display_data.columns:
            display_data['date'] = pd.to_datetime(display_data['date'], errors='coerce').dt.strftime('%d-%m-%Y')

        # Select and reorder columns for PDF
        pdf_columns = ['reg_no', 'name', 'faculty', 'date', 'start_time', 'end_time', 'description']
        available_columns = [col for col in pdf_columns if col in display_data.columns]
        display_data = display_data[available_columns]

        column_mapping = {
            'reg_no': 'Reg No',
            'name': 'Student Name',
            'date': 'Date',
            'start_time': 'Start',
            'end_time': 'End',
            'description': 'Work Description',
            'faculty': 'Faculty Guide'
        }
        display_data.columns = [column_mapping.get(col, col) for col in display_data.columns]

        # FIX: Use landscape A4 available width
        available_width = landscape(A4)[0] - 80  # 40px margin each side

        # FIX: Explicit proportional column widths that add up correctly
        col_width_map = {
            'Reg No':         available_width * 0.11,
            'Student Name':   available_width * 0.14,
            'Faculty Guide':  available_width * 0.13,
            'Date':           available_width * 0.09,
            'Start':          available_width * 0.08,
            'End':            available_width * 0.08,
            'Work Description': available_width * 0.37,
        }
        col_widths = [col_width_map.get(col, available_width / len(display_data.columns)) for col in display_data.columns]

        # FIX: Wrap ALL cell content in Paragraph objects for proper text wrapping in PDF
        def make_cell(val, style):
            text = str(val) if val is not None else ""
            return Paragraph(text, style)

        header_row = [make_cell(col, header_cell_style) for col in display_data.columns]
        body_rows = [
            [make_cell(cell, body_cell_style) for cell in row]
            for row in display_data.values.tolist()
        ]
        table_data = [header_row] + body_rows

        table = Table(table_data, colWidths=col_widths, repeatRows=1, splitByRow=True)

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8fafc'), colors.white]),
        ])
        table.setStyle(table_style)

        self.elements.append(table)
        self.doc.build(self.elements, onFirstPage=self.header_footer, onLaterPages=self.header_footer)
        self.buffer.seek(0)
        return self.buffer

class PDFReport:
    """Class to handle PDF generation with footer on every page"""
    def __init__(self, title="Weekly Log Report", report_type="General"):
        self.title = title
        self.report_type = report_type
        self.report_time = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d-%m-%Y %H:%M:%S")
        self.buffer = io.BytesIO()
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=landscape(A4),
            rightMargin=40,
            leftMargin=40,
            topMargin=50,
            bottomMargin=60
        )
        self.elements = []
        self.style = getSampleStyleSheet()

    def header_footer(self, canvas, doc):
        """Add header and footer to every page"""
        canvas.saveState()
        footer_text = f"SASTRA COE CUB | Report generated on: {self.report_time} | Page {doc.page}"
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.HexColor('#64748b'))
        canvas.drawCentredString(landscape(A4)[0] / 2, 30, footer_text)
        canvas.restoreState()

    def build(self, data):
        """Build the PDF with properly wrapped table"""
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.style['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=6,
            alignment=1
        )
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.style['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#475569'),
            spaceAfter=4,
            alignment=1
        )
        report_info_style = ParagraphStyle(
            'ReportInfo',
            parent=self.style['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=12,
            alignment=1
        )
        header_cell_style = ParagraphStyle(
            'HeaderCell',
            parent=self.style['Normal'],
            fontSize=11,
            textColor=colors.whitesmoke,
            fontName='Helvetica-Bold',
            wordWrap='LTR',
            leading=14,
        )
        body_cell_style = ParagraphStyle(
            'BodyCell',
            parent=self.style['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1e293b'),
            fontName='Helvetica',
            wordWrap='LTR',
            leading=13,
        )

        self.elements.append(Paragraph("SASTRA COE CUB", title_style))
        self.elements.append(Paragraph(self.title, subtitle_style))
        self.elements.append(Paragraph(self.report_type, report_info_style))
        self.elements.append(Spacer(1, 10))

        display_data = data.copy()
        if 'date' in display_data.columns:
            display_data['date'] = pd.to_datetime(display_data['date'], errors='coerce').dt.strftime('%d-%m-%Y')

        pdf_columns = ['reg_no', 'name', 'faculty', 'date', 'start_time', 'end_time', 'description']
        available_columns = [col for col in pdf_columns if col in display_data.columns]
        display_data = display_data[available_columns]

        column_mapping = {
            'reg_no': 'Reg No',
            'name': 'Student Name',
            'date': 'Date',
            'start_time': 'Start',
            'end_time': 'End',
            'description': 'Work Description',
            'faculty': 'Faculty Guide'
        }
        display_data.columns = [column_mapping.get(col, col) for col in display_data.columns]

        available_width = landscape(A4)[0] - 80
        col_width_map = {
            'Reg No':           available_width * 0.11,
            'Student Name':     available_width * 0.14,
            'Faculty Guide':    available_width * 0.13,
            'Date':             available_width * 0.09,
            'Start':            available_width * 0.08,
            'End':              available_width * 0.08,
            'Work Description': available_width * 0.37,
        }
        col_widths = [col_width_map.get(col, available_width / len(display_data.columns)) for col in display_data.columns]

        def make_cell(val, style):
            text = str(val) if val is not None else ""
            return Paragraph(text, style)

        header_row = [make_cell(col, header_cell_style) for col in display_data.columns]
        body_rows = [
            [make_cell(cell, body_cell_style) for cell in row]
            for row in display_data.values.tolist()
        ]
        table_data = [header_row] + body_rows

        table = Table(table_data, colWidths=col_widths, repeatRows=1, splitByRow=True)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8fafc'), colors.white]),
        ]))

        self.elements.append(table)
        self.doc.build(self.elements, onFirstPage=self.header_footer, onLaterPages=self.header_footer)
        self.buffer.seek(0)
        return self.buffer


def generate_pdf(data, title="Weekly Log Report", report_type="General"):
    """Wrapper function to generate PDF and return bytes buffer"""
    pdf = PDFReport(title, report_type)
    return pdf.build(data)

# ---------------- Session State ----------------
if "prof_logged_in" not in st.session_state:
    st.session_state.prof_logged_in = False

if "prof_name" not in st.session_state:
    st.session_state.prof_name = ""

if "prof_faculty_id" not in st.session_state:
    st.session_state.prof_faculty_id = ""

if "student_logged_in" not in st.session_state:
    st.session_state.student_logged_in = False

if "student_reg_no" not in st.session_state:
    st.session_state.student_reg_no = ""

# ---------------- Header with Logos ----------------
def render_header():
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        st.markdown('<div class="header-logo">', unsafe_allow_html=True)
        try:
            st.image("sastra_logo-Photoroom.png", width=280)
        except:
            st.markdown("📷 **Logo**")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("<h1 style='text-align: center; color: #0f172a; margin: 0; padding-top: 20px;'>SASTRA COE CUB</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #475569; margin: 0;'>Student Log Management System</p>", unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="header-logo">', unsafe_allow_html=True)
        try:
            st.image("City_Union_Bank.svg_.png", width=120)
        except:
            st.markdown("📷 **Logo**")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- UI ----------------
render_header()

# JS: keep the sidebar toggle button permanently visible regardless of Streamlit version
components.html("""
<script>
(function() {
    function fixSidebarToggle() {
        // All known selectors across Streamlit versions
        var selectors = [
            '[data-testid="collapsedControl"]',
            'section[data-testid="stSidebarCollapsedControl"]',
            '[data-testid="stSidebarCollapsedControl"]',
        ];
        selectors.forEach(function(sel) {
            var els = window.parent.document.querySelectorAll(sel);
            els.forEach(function(el) {
                el.style.setProperty('display',         'flex',              'important');
                el.style.setProperty('visibility',      'visible',           'important');
                el.style.setProperty('opacity',         '1',                 'important');
                el.style.setProperty('pointer-events',  'auto',              'important');
                el.style.setProperty('position',        'fixed',             'important');
                el.style.setProperty('left',            '0',                 'important');
                el.style.setProperty('top',             '50vh',              'important');
                el.style.setProperty('transform',       'translateY(-50%)',  'important');
                el.style.setProperty('z-index',         '999999',            'important');
                el.style.setProperty('width',           '2rem',              'important');
                el.style.setProperty('min-width',       '2rem',              'important');
                el.style.setProperty('height',          '3.5rem',            'important');
                el.style.setProperty('background-color','#2563eb',           'important');
                el.style.setProperty('border-radius',   '0 10px 10px 0',     'important');
                el.style.setProperty('border',          'none',              'important');
                el.style.setProperty('box-shadow',      '3px 0 10px rgba(0,0,0,0.35)', 'important');
                el.style.setProperty('cursor',          'pointer',           'important');
                el.style.setProperty('align-items',     'center',            'important');
                el.style.setProperty('justify-content', 'center',            'important');
                // Fix SVG arrow colour inside
                el.querySelectorAll('svg').forEach(function(svg) {
                    svg.style.setProperty('fill',    'white', 'important');
                    svg.style.setProperty('color',   'white', 'important');
                    svg.style.setProperty('display', 'block', 'important');
                });
            });
        });
    }
    // Run immediately and on every DOM change
    fixSidebarToggle();
    var observer = new MutationObserver(fixSidebarToggle);
    observer.observe(window.parent.document.body, { childList: true, subtree: true });
})();
</script>
""", height=0)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go To", ["Student", "Professor", "TimeTable", "Live Attendance"])

# --- SIDEBAR SYSTEM TOOLS ---
st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ System Tools")
if st.sidebar.button("Clear Cache & Refresh", use_container_width=True):
    st.cache_data.clear()
    st.success("Cache Cleared!")
    st.rerun()


# ================= STUDENT PAGE =================
if page == "Student":
    # Session-level caching for student list
    if "all_students_df" not in st.session_state:
        try:
            with st.spinner("Loading database..."):
                st.session_state.all_students_df = get_all_students()
        except Exception as e:
            st.error(f"⚠️ **Database Unavailable**: {e}")
            if st.button("🔄 Retry Connection"):
                st.cache_data.clear()
                st.rerun()
            st.stop()
    
    all_students_df = st.session_state.all_students_df

    # Load logs and students locally for this page
    try:
        students_df = load_students()
        logs_df = load_logs()
    except Exception as e:
        st.error(f"⚠️ **Connection Busy**: {e}")
        if st.button("🔄 Refresh Logs"):
            st.cache_data.clear()
            st.rerun()
        st.stop()

    if not st.session_state.student_logged_in:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🎓 Student Login")

        try:
            all_students_df = get_all_students()
        except Exception as e:
            st.error(f"⚠️ **Database Temporary Unavailable**: {e}")
            st.info("The link to Google Sheets might be slow or hit a limit. Click below to try again.")
            if st.button("🔄 Reload Student Database"):
                st.cache_data.clear()
                st.rerun()
            st.stop()

        if all_students_df.empty:
            st.warning("⚠️ **Student Database seems empty.**")
            if st.button("🔄 Force Refresh Database", key="empty_db_refresh"):
                st.cache_data.clear()
                st.rerun()
            st.stop()

        reg_no = st.text_input("Enter Register Number")

        if st.button("Login"):
            valid_student = all_students_df[all_students_df["reg_no"] == reg_no.strip()]
            if not valid_student.empty:
                st.session_state.student_logged_in = True
                st.session_state.student_reg_no = reg_no.strip()
                st.success("Login Successful! Syncing with database...")
                time.sleep(3)
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("Invalid Register Number. Please check your Reg No or contact your guide.")

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("Logout"):
                st.session_state.student_logged_in = False
                st.session_state.student_reg_no = ""
                st.rerun()

        st.subheader("📝 Student Log Entry")

        all_students_df = get_all_students()
        student_matches = all_students_df[all_students_df["reg_no"] == st.session_state.student_reg_no]
        if student_matches.empty:
            st.error("Student record not found. Please re-login.")
            st.stop()

        student = student_matches.iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            st.write("**Name:**", student["name"])
            st.write("**Problem Statement:**", get_problem_statement_name(student["problem_no"]))
            st.write("**Problem Number:**", student["problem_no"])
        with col2:
            st.write("**Faculty Guide:**", student["guide"])
            st.write("**Date:**", datetime.today().strftime("%d-%m-%Y"))

        active_sessions = load_active_sessions()
        student_session = active_sessions[active_sessions["reg_no"] == student["reg_no"]]

        if student_session.empty:
            st.info("You haven't started your work for today.")
            if st.button("Log In (Start Work)", type="primary"):
                now = datetime.now(ZoneInfo("Asia/Kolkata"))
                new_session = {
                    "reg_no": student["reg_no"],
                    "name": student["name"],
                    "faculty": student["guide"],
                    "problem_no": student["problem_no"],
                    "start_time": now.strftime("%Y-%m-%d %H:%M:%S")
                }
                save_active_session(new_session)
                st.success(f"Log In saved! Work session started at {now.strftime('%I:%M %p')}. Syncing with database...")
                time.sleep(3)
                st.cache_data.clear()
                st.rerun()
        else:
            session_data = student_session.iloc[0]
            start_dt = datetime.strptime(session_data["start_time"], "%Y-%m-%d %H:%M:%S")
            start_dt = start_dt.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
            
            st.success(f"🟢 Active Work Session (Started at: {start_dt.strftime('%I:%M %p')})")
            
            description = st.text_area("Work Description")
            
            if st.button("Log Out (End Work)", type="primary"):
                if not description.strip():
                    st.error("Please enter a Work Description before logging out.")
                else:
                    end_dt = datetime.now(ZoneInfo("Asia/Kolkata"))
                    
                    if end_dt < start_dt:
                        end_dt = start_dt
                        
                    hours_worked = (end_dt - start_dt).total_seconds() / 3600.0
                    
                    new_log = {
                        "reg_no": student["reg_no"],
                        "name": student["name"],
                        "faculty": student["guide"],
                        "date": end_dt.strftime("%Y-%m-%d"), 
                        "start_time": start_dt.strftime("%H:%M:%S"),
                        "end_time": end_dt.strftime("%H:%M:%S"),
                        "description": description.strip()
                    }
                    save_log(new_log)
                    
                    update_student_hours(student["reg_no"], student["name"], hours_worked)
                    remove_active_session(student["reg_no"])
                    
                    st.success(f"✅ Log Out Successful! Duration: {hours_worked:.2f} hours. Syncing with database...")
                    time.sleep(3)
                    st.cache_data.clear()
                    st.rerun()

        # Show student's own logs
        st.markdown("---")
        st.markdown("#### 📋 My Previous Logs")
        fresh_logs_student = load_logs()
        my_logs = fresh_logs_student[fresh_logs_student["reg_no"].astype(str).str.strip() == st.session_state.student_reg_no]
        my_logs = my_logs.sort_values("date", ascending=False).reset_index(drop=True)
        if not my_logs.empty:
            light_table(prepare_display_df(my_logs))
        else:
            st.info("No logs found yet.")

        st.markdown('</div>', unsafe_allow_html=True)

# ================= PROFESSOR PAGE =================
if page == "Professor":

    if not st.session_state.prof_logged_in:

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🔐 Professor Authentication")

        auth_option = st.radio("Select Option", ["Login", "Sign Up"])

        # ---------------- SIGN UP ----------------
        if auth_option == "Sign Up":
            st.markdown("### 📝 Professor Sign Up")

            faculty_id = st.text_input("Faculty ID")
            name = st.text_input("Name")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Create Account"):
                if not faculty_id.strip() or not name.strip() or not password:
                    st.error("All fields are required.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    df_prof = load_professors()
                    if faculty_id.strip() in df_prof["faculty_id"].astype(str).str.strip().values:
                        st.error("Faculty ID already exists!")
                    else:
                        new_prof = {
                            "faculty_id": faculty_id.strip(),
                            "name": name.strip(),
                            "password": password
                        }
                        save_professor(new_prof)
                        st.success("✅ Account created successfully! Please login.")

        # ---------------- LOGIN ----------------
        elif auth_option == "Login":
            st.markdown("### 🔑 Professor Login")

            faculty_id = st.text_input("Faculty ID")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                df_prof = load_professors()
                df_prof["faculty_id"] = df_prof["faculty_id"].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
                df_prof["password"] = df_prof["password"].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
                user = df_prof[
                    (df_prof["faculty_id"] == faculty_id.strip()) &
                    (df_prof["password"] == password)
                ]

                if not user.empty:
                    st.session_state.prof_logged_in = True
                    st.session_state.prof_name = user.iloc[0]["name"]
                    st.session_state.prof_faculty_id = faculty_id.strip()
                    st.success("Login Successful! Syncing with database...")
                    time.sleep(3)
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Invalid Faculty ID or Password")

        st.markdown('</div>', unsafe_allow_html=True)

    # ================= AFTER LOGIN =================
    else:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.success(f"Welcome {st.session_state.prof_name} 👨‍🏫")

        if st.button("Logout"):
            st.session_state.prof_logged_in = False
            st.session_state.prof_name = ""
            st.session_state.prof_faculty_id = ""
            st.rerun()

        prof_option = st.sidebar.radio(
            "Professor Options",
            ["Live Dashboard", "Weekly Target Tracking", "View All Logs", "Problem Statement Overview", "Search by Student Name", "Generate Report"],
            key="prof_sidebar_options"
        )

        st.subheader(" Professor Dashboard")

        # Load data for Professor tools
        try:
            students_df = load_students()
            logs_df = load_logs()
            all_students_df = get_all_students()
        except Exception as e:
            st.error(f"⚠️ **Connection Issue**: {e}")
            if st.button("🔄 Refresh Data"):
                st.cache_data.clear()
                st.rerun()
            st.stop()

        # ---- LIVE DASHBOARD ----
        if prof_option == "Live Dashboard":
            st.markdown("### 🟢 Currently Working Students")
            active_sessions = load_active_sessions()
            if active_sessions.empty:
                st.info("No students are currently logged in.")
            else:
                display_df = active_sessions.copy()
                display_df["Start Time"] = pd.to_datetime(display_df["start_time"]).dt.strftime("%I:%M %p")
                display_df["Problem Statement"] = display_df["problem_no"].apply(get_problem_statement_name)
                
                display_df = display_df[["reg_no", "name", "faculty", "Problem Statement", "Start Time"]]
                display_df.columns = ["Reg No", "Name", "Faculty Guide", "Problem Statement", "Log In Time"]
                
                light_table(display_df)
                
            st.markdown("---")
            st.markdown("### ⏱️ Total Hours Worked")
            student_hours = load_student_hours()
            if student_hours.empty:
                st.info("No hours have been logged yet.")
            else:
                student_hours = student_hours.sort_values(by="total_hours", ascending=False)
                student_hours.columns = ["Reg No", "Name", "Total Hours"]
                student_hours["Total Hours"] = student_hours["Total Hours"].apply(lambda x: f"{x:.2f}")
                light_table(student_hours)

        # ---- WEEKLY TARGET TRACKING ----
        elif prof_option == "Weekly Target Tracking":
            st.markdown("### 🎯 Weekly Target Tracking")
            
            targets = load_target_hours()
            if not targets:
                st.warning("Could not load Target Hours from 'cub (1).xlsx' (Sheet1). Make sure the column 'Total Hrs' exists.")
            else:
                monday = get_monday_of_current_week()
                fresh_logs = load_logs()
                
                # Filter logs for current week only
                fresh_logs["_date_obj"] = pd.to_datetime(fresh_logs["date"], format="%Y-%m-%d", errors="coerce").dt.date
                week_logs = fresh_logs[fresh_logs["_date_obj"] >= monday.date()].copy()
                
                # Sum hours per normalized student name
                import re
                def norm_name(n): return "".join(sorted(re.findall(r'[a-zA-Z]+', str(n).lower())))
                
                def _calc_hrs(r):
                    try:
                        s = pd.to_datetime(str(r["start_time"])).time()
                        e = pd.to_datetime(str(r["end_time"])).time()
                        from datetime import datetime, date, timedelta
                        dt_s = datetime.combine(date.today(), s)
                        dt_e = datetime.combine(date.today(), e)
                        if dt_e < dt_s: dt_e += timedelta(days=1)
                        return (dt_e - dt_s).total_seconds() / 3600.0
                    except:
                        return 0.0
                        
                week_logs["hours_worked"] = week_logs.apply(_calc_hrs, axis=1)
                week_logs["_norm_name"] = week_logs["name"].apply(norm_name)
                weekly_hours = week_logs.groupby("_norm_name")["hours_worked"].sum().to_dict()
                
                # Fetch 3rd and Final Year students
                third_years = load_third_year_students()
                final_years = load_final_year_students()
                
                tab1, tab2 = st.tabs(["🎓 3rd Year Tracking", "🎓 Final Year Tracking"])
                
                def render_tracking_table(df_students):
                    if df_students.empty:
                        st.info("No students found in this category.")
                        return
                        
                    html = '''
                    <div style="overflow-x:auto; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:1rem;">
                    <table style="width:100%; border-collapse:collapse; font-family:sans-serif; font-size:14px; color:#1e293b; background:#ffffff;">
                        <thead>
                            <tr style="background:#f8fafc; color:#475569; text-align:left; border-bottom:2px solid #cbd5e1;">
                                <th style="padding:12px 15px;">Student Name</th>
                                <th style="padding:12px 15px; width: 160px; text-align:center;">Weekly Status</th>
                                <th style="padding:12px 15px; min-width: 250px;">Target Progress</th>
                            </tr>
                        </thead>
                        <tbody>
                    '''
                    
                    has_rows = False
                    for idx, row in df_students.iterrows():
                        raw_name = row["name"]
                        if pd.isna(raw_name): continue
                        
                        nn = norm_name(raw_name)
                        target_hr = targets.get(nn, 0)
                        if target_hr <= 0: continue 
                        
                        worked_hr = weekly_hours.get(nn, 0.0)
                        has_rows = True
                        
                        pct = min((worked_hr / target_hr) * 100, 100)
                        is_over = worked_hr > target_hr
                        
                        bar_color = "#3b82f6" # Blue default
                        if worked_hr >= target_hr:
                            bar_color = "#eab308" if is_over else "#22c55e" # Gold if exceeded
                        elif pct > 75:
                            bar_color = "#8b5cf6" # purple near completion
                            
                        bg_tr = "#ffffff" if idx % 2 == 0 else "#f8fafc"
                        
                        html += f'<tr style="background:{bg_tr}; border-bottom:1px solid #e2e8f0;">'
                        html += f'<td style="padding:12px 15px; font-weight: 500;">{raw_name}</td>'
                        html += f'<td style="padding:12px 15px; text-align:center;"><b>{worked_hr:.1f}</b> / {target_hr:.0f} hr</td>'
                        html += f'<td style="padding:12px 15px;">'
                        html += f'<div style="width: 100%; background-color: #e2e8f0; border-radius: 9999px; height: 16px; overflow: hidden; position: relative;">'
                        html += f'<div style="width: {pct}%; background-color: {bar_color}; height: 100%; border-radius: 9999px; transition: width 0.5s ease;"></div>'
                        if is_over:
                             html += f'<div style="position: absolute; width: 100%; text-align: center; top: 0; font-size: 10px; color: white; line-height: 16px; font-weight: bold;">OVERACHIEVED</div>'
                        html += f'</div>'
                        html += '</td></tr>'
                        
                    html += '</tbody></table></div>'
                    
                    if not has_rows:
                        st.info("None of the students in this category have assigned weekly targets in 'cub (1).xlsx'.")
                    else:
                        st.markdown(html, unsafe_allow_html=True)
                
                with tab1:
                    render_tracking_table(third_years)
                
                with tab2:
                    render_tracking_table(final_years)

        # ---- VIEW ALL LOGS ----
        elif prof_option == "View All Logs":
            st.markdown("### 📋 All Logs")
            fresh_logs = load_logs()
            fresh_logs = fresh_logs.sort_values("date", ascending=False).reset_index(drop=True)
            display_df = prepare_display_df(fresh_logs)
            light_table(display_df)

        # ---- PROBLEM STATEMENT OVERVIEW ----
        elif prof_option == "Problem Statement Overview":
            st.markdown("### 📌 Problem Statement Overview")

            # Build a reg_no → problem_no lookup from both year files
            all_students_df = get_all_students()

            # Build mapping with multiple normalisation forms to handle
            # Excel float conversion (e.g. "12345.0"), leading zeros, whitespace, etc.
            def norm_reg(val):
                """Normalise a reg_no to a clean string for matching."""
                s = str(val).strip()
                # Remove .0 suffix Excel sometimes adds (numeric cells read as float)
                if s.endswith(".0"):
                    s = s[:-2]
                return s.upper()

            reg_to_ps = {}
            for _, row in all_students_df.iterrows():
                rn = norm_reg(row["reg_no"])
                ps = str(row["problem_no"]).strip()
                if ps.endswith(".0"):
                    ps = ps[:-2]
                reg_to_ps[rn] = ps

            # Also pull from main Log sheet (Sheet1) as fallback
            if not students_df.empty and "problem_no" in students_df.columns:
                for _, row in students_df.iterrows():
                    rn = norm_reg(row["reg_no"])
                    if rn not in reg_to_ps:
                        ps = str(row["problem_no"]).strip()
                        if ps.endswith(".0"):
                            ps = ps[:-2]
                        reg_to_ps[rn] = ps

            # Reload fresh from file so newly added entries are included
            fresh_logs = load_logs()
            # Attach PS label to logs using normalised reg_no
            logs_with_ps = fresh_logs.copy().reset_index(drop=True)
            logs_with_ps["ps_no"] = (
                logs_with_ps["reg_no"]
                .apply(norm_reg)
                .map(reg_to_ps)
                .fillna("Unknown")
            )
            logs_with_ps["ps_name"] = logs_with_ps["ps_no"].apply(get_problem_statement_name)
            # Sort newest first
            logs_with_ps = logs_with_ps.sort_values("date", ascending=False).reset_index(drop=True)

            # Debug expander — shows unmapped reg_nos so you can spot mismatches
            unknown_count = (logs_with_ps["ps_no"] == "Unknown").sum()
            if unknown_count > 0:
                with st.expander(f"⚠️ {unknown_count} log(s) could not be mapped to a PS (click to inspect)", expanded=False):
                    unknown_regs = logs_with_ps[logs_with_ps["ps_no"] == "Unknown"]["reg_no"].unique()
                    st.write("Unmapped reg_nos in logs:", list(unknown_regs))
                    sample_keys = list(reg_to_ps.keys())[:10]
                    st.write("Sample reg_nos in student file:", sample_keys)

            # View mode selector
            st.markdown("#### 🔎 View by Problem Statement")

            monday = get_monday_of_current_week()
            today_end = pd.Timestamp(datetime.today().date()) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

            def show_ps_logs(df, label):
                if df.empty:
                    st.info(f"No logs found for {label}.")
                    return

                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Total Entries", len(df))
                col_b.metric("Students", df["reg_no"].nunique())
                col_c.metric("Faculty", df["faculty"].nunique() if "faculty" in df.columns else "-")

                light_table(prepare_display_df(df))
            ps_choice_map = {f"PS {k} — {v}": k for k, v in PROBLEM_STATEMENTS.items()}
            selected_ps_label = st.selectbox(
                "Select Problem Statement",
                list(ps_choice_map.keys()),
                key="ps_detail_select"
            )

            selected_ps_id = ps_choice_map[selected_ps_label]

            ps_logs = logs_with_ps[logs_with_ps["ps_no"] == selected_ps_id]

            st.markdown(f"#### Results for PS {selected_ps_id} — {PROBLEM_STATEMENTS[selected_ps_id]}")
            show_ps_logs(ps_logs, PROBLEM_STATEMENTS[selected_ps_id])

        # ---- SEARCH BY STUDENT NAME ----
        elif prof_option == "Search by Student Name":
            st.markdown("### 👥 Search by Student Name")

            third_year_df = load_third_year_students()
            final_year_df = load_final_year_students()

            tab1, tab2 = st.tabs(["3rd Year Students", "Final Year Students"])

            with tab1:
                st.markdown("#### Select 3rd Year Student")
                if not third_year_df.empty:
                    third_year_df["display_name"] = (
                        third_year_df["name"] + " (" +
                        third_year_df["reg_no"] + ") - " +
                        third_year_df["problem_no"].apply(get_problem_statement_name)
                    )
                    selected_3rd = st.selectbox(
                        "Choose Student",
                        options=[""] + third_year_df["display_name"].tolist(),
                        key="third_year_select"
                    )
                    if selected_3rd:
                        selected_student = third_year_df[third_year_df["display_name"] == selected_3rd].iloc[0]
                        reg_no = selected_student["reg_no"]

                        info_col1, info_col2 = st.columns(2)
                        with info_col1:
                            st.write(f"**Reg No:** {reg_no}")
                            st.write(f"**Name:** {selected_student['name']}")
                        with info_col2:
                            st.write(f"**Guide:** {selected_student['guide']}")
                            st.write(f"**Problem:** {get_problem_statement_name(selected_student['problem_no'])}")

                        st.markdown("---")
                        fresh_logs = load_logs()
                        filtered = fresh_logs[fresh_logs["reg_no"].astype(str).str.strip() == reg_no.strip()]
                        filtered = filtered.sort_values("date", ascending=False).reset_index(drop=True)
                        if not filtered.empty:
                            st.markdown("**📋 Work Logs:**")
                            light_table(prepare_display_df(filtered))
                        else:
                            st.info(f"No logs found for {selected_student['name']}")
                else:
                    st.error("3rd year students data not found. Please check if '3rd_year.xlsx' exists.")

            with tab2:
                st.markdown("#### Select Final Year Student")
                if not final_year_df.empty:
                    final_year_df["display_name"] = (
                        final_year_df["name"] + " (" +
                        final_year_df["reg_no"] + ") - " +
                        final_year_df["problem_no"].apply(get_problem_statement_name)
                    )
                    selected_final = st.selectbox(
                        "Choose Student",
                        options=[""] + final_year_df["display_name"].tolist(),
                        key="final_year_select"
                    )
                    if selected_final:
                        selected_student = final_year_df[final_year_df["display_name"] == selected_final].iloc[0]
                        reg_no = selected_student["reg_no"]

                        info_col1, info_col2 = st.columns(2)
                        with info_col1:
                            st.write(f"**Reg No:** {reg_no}")
                            st.write(f"**Name:** {selected_student['name']}")
                        with info_col2:
                            st.write(f"**Guide:** {selected_student['guide']}")
                            st.write(f"**Problem:** {get_problem_statement_name(selected_student['problem_no'])}")

                        st.markdown("---")
                        fresh_logs = load_logs()
                        filtered = fresh_logs[fresh_logs["reg_no"].astype(str).str.strip() == reg_no.strip()]
                        filtered = filtered.sort_values("date", ascending=False).reset_index(drop=True)
                        if not filtered.empty:
                            st.markdown("**📋 Work Logs:**")
                            light_table(prepare_display_df(filtered))
                        else:
                            st.info(f"No logs found for {selected_student['name']}")
                else:
                    st.error("Final year students data not found. Please check if 'final_year.xlsx' exists.")

        # ---- GENERATE REPORT ----
        elif prof_option == "Generate Report":
            st.markdown("### 📊 Generate Reports")


            report_type = st.radio(
                "Select Report Type",
                [
                    "General Report (All Students)",
                    "Report by Problem Statement",
                    "Current Week Report (Monday to Today)",
                    "Current Week Report by Problem Statement",
                ],
                key="report_type_select"
            )

            def norm_reg(val):
                s = str(val).strip()
                if s.endswith(".0"):
                    s = s[:-2]
                return s.upper()

            def get_reg_to_ps():
                """Build normalised reg_no → ps_no lookup from all student sources."""
                all_students = get_all_students()
                mapping = {}
                for _, row in all_students.iterrows():
                    rn = norm_reg(row["reg_no"])
                    ps = str(row["problem_no"]).strip().rstrip(".0") if str(row["problem_no"]).strip().endswith(".0") else str(row["problem_no"]).strip()
                    mapping[rn] = ps
                # Fallback from Sheet1
                s_df = load_students()
                if not s_df.empty and "problem_no" in s_df.columns and "reg_no" in s_df.columns:
                    for _, row in s_df.iterrows():
                        rn = norm_reg(row["reg_no"])
                        if rn not in mapping:
                            ps = str(row["problem_no"]).strip()
                            if ps.endswith(".0"):
                                ps = ps[:-2]
                            mapping[rn] = ps
                return mapping

            # ── General Report ──────────────────────────────────────────
            if report_type == "General Report (All Students)":
                st.markdown("#### General Report")
                col1, col2 = st.columns(2)
                from_date = col1.date_input("From Date", key="gen_from")
                to_date   = col2.date_input("To Date",   key="gen_to")

                if st.button("Generate General Report", key="gen_report_btn"):
                    if from_date > to_date:
                        st.error("'From Date' must be before 'To Date'.")
                    else:
                        fresh = load_logs()
                        # Compare as Python date objects — avoids all Timestamp/tz issues
                        fresh["_date_only"] = fresh["date"].dt.date
                        filtered = fresh[
                            (fresh["_date_only"] >= from_date) &
                            (fresh["_date_only"] <= to_date)
                        ].drop(columns=["_date_only"])
                        st.info(f"Total logs in file: {len(fresh)} | After date filter: {len(filtered)}")
                        if not filtered.empty:
                            buf = generate_pdf(
                                filtered,
                                "General Log Report",
                                f"Period: {from_date.strftime('%d-%m-%Y')} to {to_date.strftime('%d-%m-%Y')}"
                            )
                            filename = f"general_report_{datetime.now(ZoneInfo("Asia/Kolkata")).strftime('%Y%m%d_%H%M%S')}.pdf"
                            st.success(f"Found {len(filtered)} log entries.")
                            st.download_button("📥 Download PDF", buf, file_name=filename, mime="application/pdf")
                        else:
                            st.warning("No logs found in selected date range.")

            # ── Report by Problem Statement ─────────────────────────────
            elif report_type == "Report by Problem Statement":
                st.markdown("#### Report by Problem Statement")

                prob_options = {f"{k} - {v}": k for k, v in PROBLEM_STATEMENTS.items()}
                selected_prob_display = st.selectbox(
                    "Select Problem Statement",
                    options=list(prob_options.keys()),
                    key="prob_select"
                )
                selected_prob_id = prob_options[selected_prob_display]

                col1, col2 = st.columns(2)
                from_date = col1.date_input("From Date", key="prob_from")
                to_date   = col2.date_input("To Date",   key="prob_to")

                if st.button("Generate Problem Statement Report", key="prob_report_btn"):
                    if from_date > to_date:
                        st.error("'From Date' must be before 'To Date'.")
                    else:
                        reg_to_ps = get_reg_to_ps()
                        # All reg_nos assigned to selected PS
                        all_regs = {rn for rn, ps in reg_to_ps.items() if ps == selected_prob_id}

                        fresh = load_logs()
                        fresh["_norm_reg"]  = fresh["reg_no"].apply(norm_reg)
                        fresh["_date_only"] = fresh["date"].dt.date
                        filtered = fresh[
                            (fresh["_norm_reg"].isin(all_regs)) &
                            (fresh["_date_only"] >= from_date) &
                            (fresh["_date_only"] <= to_date)
                        ].drop(columns=["_norm_reg", "_date_only"])

                        st.info(f"Total logs in file: {len(fresh)} | Matched PS {selected_prob_id}: {len(filtered)}")
                        if not filtered.empty:
                            prob_name = PROBLEM_STATEMENTS[selected_prob_id]
                            buf = generate_pdf(
                                filtered,
                                "Problem Statement Report",
                                f"Problem: {prob_name} | Period: {from_date.strftime('%d-%m-%Y')} to {to_date.strftime('%d-%m-%Y')}"
                            )
                            filename = f"problem_{selected_prob_id}_report_{datetime.now(ZoneInfo("Asia/Kolkata")).strftime('%Y%m%d_%H%M%S')}.pdf"
                            st.success(f"Found {len(filtered)} log entries.")
                            st.download_button("📥 Download PDF", buf, file_name=filename, mime="application/pdf")
                        else:
                            st.warning(f"No logs found for Problem Statement {selected_prob_id} in the selected date range.")

            # ── Current Week Report ─────────────────────────────────────
            elif report_type == "Current Week Report (Monday to Today)":
                st.markdown("#### Current Week Report")

                monday    = get_monday_of_current_week()
                today_end = pd.Timestamp(datetime.today().date()) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

                st.info(
                    f"Generating report from **{monday.strftime('%d-%m-%Y')}** (Monday) "
                    f"to **{datetime.today().strftime('%d-%m-%Y')}** (Today)"
                )

                if st.button("Generate Current Week Report", key="week_report_btn"):
                    fresh = load_logs()
                    fresh["_date_only"] = fresh["date"].dt.date
                    today_date = datetime.today().date()
                    monday_date = monday.date()
                    filtered = fresh[
                        (fresh["_date_only"] >= monday_date) &
                        (fresh["_date_only"] <= today_date)
                    ].drop(columns=["_date_only"])
                    st.info(f"Total logs in file: {len(fresh)} | This week: {len(filtered)} | Valid dates: {fresh['date'].notna().sum()}")
                    if not filtered.empty:
                        buf = generate_pdf(
                            filtered,
                            "Current Week Report",
                            f"Week: {monday.strftime('%d-%m-%Y')} to {datetime.today().strftime('%d-%m-%Y')}"
                        )
                        filename = f"weekly_report_{datetime.now(ZoneInfo("Asia/Kolkata")).strftime('%Y%m%d_%H%M%S')}.pdf"
                        st.success(f"Found {len(filtered)} log entries for this week.")
                        st.download_button("📥 Download PDF", buf, file_name=filename, mime="application/pdf")
                    else:
                        st.warning(
                            f"No logs found for the current week "
                            f"({monday.strftime('%d-%m-%Y')} to {datetime.today().strftime('%d-%m-%Y')})."
                        )

            # ── Current Week Report by Problem Statement ────────────────
            elif report_type == "Current Week Report by Problem Statement":
                st.markdown("#### 📅 Current Week Report — by Problem Statement")

                monday    = get_monday_of_current_week()
                today_end = pd.Timestamp(datetime.today().date()) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

                st.info(
                    f"Generating report from **{monday.strftime('%d-%m-%Y')}** (Monday) "
                    f"to **{datetime.today().strftime('%d-%m-%Y')}** (Today)"
                )

                ps_scope = st.radio(
                    "Which Problem Statement?",
                    ["All Problem Statements", "Specific Problem Statement"],
                    key="week_ps_scope",
                    horizontal=True
                )

                if ps_scope == "Specific Problem Statement":
                    ps_choice_map  = {f"PS {k} — {v}": k for k, v in PROBLEM_STATEMENTS.items()}
                    selected_ps_id = ps_choice_map[st.selectbox("Select Problem Statement", list(ps_choice_map.keys()), key="week_ps_select")]
                else:
                    selected_ps_id = None

                if st.button("Generate Weekly PS Report", key="week_ps_report_btn"):
                    reg_to_ps = get_reg_to_ps()

                    fresh = load_logs()
                    fresh["_norm_reg"]  = fresh["reg_no"].apply(norm_reg)
                    fresh["ps_no"]      = fresh["_norm_reg"].map(reg_to_ps).fillna("Unknown")
                    today_date  = datetime.today().date()
                    monday_date = monday.date()
                    fresh["_date_only"] = fresh["date"].dt.date

                    week_logs = fresh[
                        (fresh["_date_only"] >= monday_date) &
                        (fresh["_date_only"] <= today_date)
                    ].drop(columns=["_date_only"]).copy()

                    if week_logs.empty:
                        st.warning(f"No logs found for the current week ({monday.strftime('%d-%m-%Y')} to {datetime.today().strftime('%d-%m-%Y')}).")
                    else:
                        if selected_ps_id:
                            ps_logs = week_logs[week_logs["ps_no"] == selected_ps_id].drop(columns=["_norm_reg", "ps_no"])
                            if ps_logs.empty:
                                st.warning(f"No logs for PS {selected_ps_id} this week.")
                            else:
                                ps_name = PROBLEM_STATEMENTS[selected_ps_id]
                                st.success(f"Found {len(ps_logs)} entries for PS {selected_ps_id} — {ps_name}.")
                                buf = generate_pdf(
                                    ps_logs,
                                    f"Weekly Report — PS {selected_ps_id}: {ps_name}",
                                    f"Week: {monday.strftime('%d-%m-%Y')} to {datetime.today().strftime('%d-%m-%Y')}"
                                )
                                filename = f"weekly_ps{selected_ps_id}_report_{datetime.now(ZoneInfo("Asia/Kolkata")).strftime('%Y%m%d_%H%M%S')}.pdf"
                                st.download_button("📥 Download PDF", buf, file_name=filename, mime="application/pdf")
                        else:
                            # Combined multi-section PDF for all PS
                            pdf_obj = PDFReport(
                                "Current Week Report — All Problem Statements",
                                f"Week: {monday.strftime('%d-%m-%Y')} to {datetime.today().strftime('%d-%m-%Y')}"
                            )
                            title_style = ParagraphStyle('CombTitle', parent=pdf_obj.style['Heading1'],
                                fontSize=16, textColor=colors.HexColor('#0f172a'), spaceAfter=6, alignment=1)
                            subtitle_style = ParagraphStyle('CombSub', parent=pdf_obj.style['Normal'],
                                fontSize=11, textColor=colors.HexColor('#475569'), spaceAfter=12, alignment=1)
                            ps_heading_style = ParagraphStyle('PSHeading', parent=pdf_obj.style['Heading2'],
                                fontSize=13, textColor=colors.HexColor('#1e3a8a'), spaceBefore=14, spaceAfter=6)
                            header_cell_style = ParagraphStyle('HdrCell', parent=pdf_obj.style['Normal'],
                                fontSize=11, textColor=colors.whitesmoke, fontName='Helvetica-Bold', wordWrap='LTR', leading=14)
                            body_cell_style = ParagraphStyle('BdyCell', parent=pdf_obj.style['Normal'],
                                fontSize=10, textColor=colors.HexColor('#1e293b'), fontName='Helvetica', wordWrap='LTR', leading=13)

                            pdf_obj.elements.append(Paragraph("SASTRA COE CUB", title_style))
                            pdf_obj.elements.append(Paragraph("Current Week Report — All Problem Statements", subtitle_style))
                            pdf_obj.elements.append(Paragraph(
                                f"Week: {monday.strftime('%d-%m-%Y')} to {datetime.today().strftime('%d-%m-%Y')}", subtitle_style))
                            pdf_obj.elements.append(Spacer(1, 12))

                            available_width = landscape(A4)[0] - 80
                            col_width_map = {
                                'Reg No': available_width * 0.11, 'Student Name': available_width * 0.14,
                                'Faculty Guide': available_width * 0.13, 'Date': available_width * 0.09,
                                'Start': available_width * 0.08, 'End': available_width * 0.08,
                                'Work Description': available_width * 0.37,
                            }
                            column_mapping = {
                                'reg_no': 'Reg No', 'name': 'Student Name', 'faculty': 'Faculty Guide',
                                'date': 'Date', 'start_time': 'Start', 'end_time': 'End', 'description': 'Work Description'
                            }
                            pdf_columns = ['reg_no', 'name', 'faculty', 'date', 'start_time', 'end_time', 'description']

                            def mc(val, sty):
                                return Paragraph(str(val) if val is not None else "", sty)

                            found_any = False
                            for ps_id, ps_name in PROBLEM_STATEMENTS.items():
                                ps_logs = week_logs[week_logs["ps_no"] == ps_id].copy()
                                if ps_logs.empty:
                                    continue
                                found_any = True
                                pdf_obj.elements.append(Paragraph(
                                    f"PS {ps_id} — {ps_name}  ({len(ps_logs)} entries)", ps_heading_style))
                                ps_logs["date"] = pd.to_datetime(ps_logs["date"], errors="coerce").dt.strftime("%d-%m-%Y")
                                avail_cols  = [c for c in pdf_columns if c in ps_logs.columns]
                                ps_display  = ps_logs[avail_cols].copy()
                                ps_display.columns = [column_mapping.get(c, c) for c in ps_display.columns]
                                col_widths  = [col_width_map.get(c, available_width / len(ps_display.columns)) for c in ps_display.columns]
                                header_row  = [mc(c, header_cell_style) for c in ps_display.columns]
                                body_rows   = [[mc(cell, body_cell_style) for cell in row] for row in ps_display.values.tolist()]
                                tbl = Table([header_row] + body_rows, colWidths=col_widths, repeatRows=1, splitByRow=True)
                                tbl.setStyle(TableStyle([
                                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
                                    ('ALIGN', (0,0), (-1,-1), 'LEFT'), ('VALIGN', (0,0), (-1,-1), 'TOP'),
                                    ('LEFTPADDING', (0,0), (-1,-1), 5), ('RIGHTPADDING', (0,0), (-1,-1), 5),
                                    ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                                    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f8fafc'), colors.white]),
                                ]))
                                pdf_obj.elements.append(tbl)
                                pdf_obj.elements.append(Spacer(1, 10))

                            if not found_any:
                                st.warning("No logs found for any Problem Statement this week.")
                            else:
                                pdf_obj.doc.build(pdf_obj.elements,
                                    onFirstPage=pdf_obj.header_footer, onLaterPages=pdf_obj.header_footer)
                                pdf_obj.buffer.seek(0)
                                total_entries = sum(len(week_logs[week_logs["ps_no"] == ps_id]) for ps_id in PROBLEM_STATEMENTS)
                                st.success(f"Generated report with {total_entries} total log entries across all problem statements.")
                                filename = f"weekly_all_ps_report_{datetime.now(ZoneInfo("Asia/Kolkata")).strftime('%Y%m%d_%H%M%S')}.pdf"
                                st.download_button("📥 Download PDF", pdf_obj.buffer, file_name=filename, mime="application/pdf")
        st.markdown('</div>', unsafe_allow_html=True)

# ================= TIMETABLE PAGE =================
if page == "TimeTable":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📅 Weekly Student TimeTable")
    
    # Load required data for this page
    try:
        all_students_df = get_all_students()
        target_hours = load_target_hours()
        student_hours_df = load_student_hours()
    except Exception as e:
        st.error(f"⚠️ **Connection Busy**: {e}")
        if st.button("🔄 Retry Connection"):
            st.cache_data.clear()
            st.rerun()
        st.stop()
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    current_day_name = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%A")
    default_idx = days.index(current_day_name) if current_day_name in days else 0
    
    selected_day = st.selectbox("Select Day", days, index=default_idx)
    
    schedule_data, time_slots = load_timetable(selected_day)
    
    if not schedule_data:
        st.error(f"Could not load timetable for {selected_day}. Please ensure the Timetable sheet is reachable.")
    else:
        # Build HTML Table
        html = '''
        <div style="overflow-x:auto; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:1rem; margin-top:1rem;">
        <table style="width:100%; border-collapse:collapse; font-family:sans-serif; font-size:13px; color:#1e293b; background:#ffffff;">
            <thead>
                <tr style="background:#f1f5f9; color:#0f172a; text-align:center;">
                    <th style="padding:10px; border-bottom:2px solid #cbd5e1; text-align:left; min-width: 150px; position: sticky; left: 0; background:#f1f5f9; z-index: 2;">Student Name</th>
        '''
        for slot in time_slots:
            html += f'<th style="padding:10px; border-bottom:2px solid #cbd5e1; min-width: 100px;">{slot}</th>'
        html += '</tr></thead><tbody>'
        
        for row_idx, student in enumerate(schedule_data):
            is_sys_occ = "system" in student["name"].lower() and "occupied" in student["name"].lower()
            bg_tr = "#f1f5f9" if is_sys_occ else ("#ffffff" if row_idx % 2 == 0 else "#f8fafc")
            
            html += f'<tr style="background:{bg_tr};">'
            html += f'<td style="padding:10px; border-bottom:1px solid #e2e8f0; font-weight: 600; position: sticky; left: 0; background:{bg_tr}; z-index: 1;">{student["name"]}</td>'
            
            for slot in time_slots:
                slot_val = student["slots"].get(slot, False)
                if not slot_val:
                    html += '<td style="padding:10px; border-bottom:1px solid #e2e8f0;"></td>'
                elif is_sys_occ:
                    html += f'<td style="padding:10px; border-bottom:1px solid #e2e8f0; text-align:center;">'
                    html += f'<div style="background:#475569; color:#ffffff; padding:6px 8px; border-radius:6px; font-weight:600; font-size:11px;">{slot_val} Total</div>'
                    html += '</td>'
                else:
                    html += f'<td style="padding:10px; border-bottom:1px solid #e2e8f0; text-align:center;">'
                    html += f'<div style="background:#eff6ff; color:#1e40af; padding:6px 8px; border-radius:6px; font-weight:600; font-size:11px;">Scheduled</div>'
                    html += '</td>'
            html += '</tr>'
            
        html += '</tbody></table></div>'
        st.markdown(html, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

# ================= LIVE ATTENDANCE PAGE =================
if page == "Live Attendance":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🔴 Live Attendance Monitor")
    
    # Load required data for this page
    try:
        active_sessions = load_active_sessions()
    except Exception as e:
        st.error(f"⚠️ **Connection Busy**: {e}")
        if st.button("🔄 Retry Connection"):
            st.cache_data.clear()
            st.rerun()
        st.stop()
    
    current_day_name = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%A")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    # Handle Saturday overrides
    if current_day_name == "Saturday":
        st.info("Today is Saturday. If it is a working day, please select the day order below to track live attendance.")
        override_day = st.selectbox("Select Day Order", days)
        tracking_day = override_day
    else:
        tracking_day = current_day_name
    
    if tracking_day not in days:
        st.info(f"Today is {current_day_name}. There is no live schedule actively tracking today.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        if current_day_name == "Saturday":
            st.markdown(f"**Tracking real-time schedule for:** {tracking_day} (Saturday Override)")
        else:
            st.markdown(f"**Tracking real-time schedule for:** {tracking_day}")
            
        schedule_data, time_slots = load_timetable(tracking_day)
        
        if not schedule_data:
            st.error(f"Could not load timetable for {current_day_name}.")
        else:
            import re
            def norm_name(n):
                return "".join(sorted(re.findall(r'[a-zA-Z]+', str(n).lower())))
                
            active_sessions = load_active_sessions()
            active_names = [norm_name(n) for n in active_sessions["name"].tolist() if pd.notna(n)]
            
            now_time = datetime.now(ZoneInfo("Asia/Kolkata")).time()
            
            # Build HTML Table
            html = '''
            <div style="overflow-x:auto; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:1rem; margin-top:1rem;">
            <table style="width:100%; border-collapse:collapse; font-family:sans-serif; font-size:13px; color:#1e293b; background:#ffffff;">
                <thead>
                    <tr style="background:#f1f5f9; color:#0f172a; text-align:center;">
                        <th style="padding:10px; border-bottom:2px solid #cbd5e1; text-align:left; min-width: 150px; position: sticky; left: 0; background:#f1f5f9; z-index: 2;">Student Name</th>
            '''
            for slot in time_slots:
                html += f'<th style="padding:10px; border-bottom:2px solid #cbd5e1; min-width: 100px;">{slot}</th>'
            html += '</tr></thead><tbody>'
            
            for row_idx, student in enumerate(schedule_data):
                is_sys_occ = "system" in student["name"].lower() and "occupied" in student["name"].lower()
                bg_tr = "#f1f5f9" if is_sys_occ else ("#ffffff" if row_idx % 2 == 0 else "#f8fafc")
                
                html += f'<tr style="background:{bg_tr};">'
                html += f'<td style="padding:10px; border-bottom:1px solid #e2e8f0; font-weight: 600; position: sticky; left: 0; background:{bg_tr}; z-index: 1;">{student["name"]}</td>'
                
                student_name_clean = norm_name(student["name"])
                is_logged_in = student_name_clean in active_names
                
                for slot in time_slots:
                    slot_val = student["slots"].get(slot, False)
                    if not slot_val:
                        html += '<td style="padding:10px; border-bottom:1px solid #e2e8f0;"></td>'
                    elif is_sys_occ:
                        html += f'<td style="padding:10px; border-bottom:1px solid #e2e8f0; text-align:center;">'
                        html += f'<div style="background:#475569; color:#ffffff; padding:6px 8px; border-radius:6px; font-weight:600; font-size:11px;">{slot_val} Total</div>'
                        html += '</td>'
                    else:
                        start_t, end_t = parse_time_slot(slot)
                        is_current_slot = False
                        
                        if start_t and end_t:
                            if start_t <= end_t:
                                is_current_slot = (start_t <= now_time <= end_t)
                            else:
                                is_current_slot = (now_time >= start_t or now_time <= end_t)
                                
                        cell_bg = "#eff6ff" 
                        cell_text = "Scheduled"
                        cell_color = "#1e40af"
                        
                        if is_current_slot:
                            if is_logged_in:
                                cell_bg = "#22c55e" # Green
                                cell_color = "#ffffff"
                                cell_text = "Logged In"
                            else:
                                cell_bg = "#ef4444" # Red
                                cell_color = "#ffffff"
                                cell_text = "Missing"
                                
                        html += f'<td style="padding:10px; border-bottom:1px solid #e2e8f0; text-align:center;">'
                        html += f'<div style="background:{cell_bg}; color:{cell_color}; padding:6px 8px; border-radius:6px; font-weight:600; font-size:11px;">{cell_text}</div>'
                        html += '</td>'
                html += '</tr>'
                
            html += '</tbody></table></div>'
            st.markdown(html, unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)
