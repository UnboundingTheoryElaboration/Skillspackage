import os
import json
import datetime
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = "/home/user/workspace/open_method_architecture_skill"
with open(os.path.join(ROOT, "demonstration/three_demos_results.json")) as f:
    DEMOS = json.load(f)
with open("/home/user/workspace/qcma_v4_run/v4_results.json") as f:
    V4 = json.load(f)

from sys import path as sys_path
sys_path.insert(0, os.path.join(ROOT, "demonstration"))
from v4_corpus_and_coding import FIRST_ORDER, OUTCOMES, MACRO_CONDITIONS, CODEBOOK, CASES_V4, SYNTHESIS_ONLY_RECORDS

# ==============================================================================
# DOCX HELPER FUNCTIONS (Strict OOXML Schema Order)
# ==============================================================================
def new_styled_doc():
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for hlevel, pt_size, hex_col in [
        ("Heading 1", 15, (0x01, 0x69, 0x6F)),
        ("Heading 2", 12.5, (0x1B, 0x47, 0x4D)),
        ("Heading 3", 11, (0x28, 0x25, 0x1D)),
    ]:
        s = doc.styles[hlevel]
        s.font.name = "Calibri"
        s.font.size = Pt(pt_size)
        s.font.color.rgb = RGBColor(*hex_col)
    sec = doc.sections[0]
    sec.left_margin = Cm(1.8)
    sec.right_margin = Cm(1.8)
    sec.top_margin = Cm(1.8)
    sec.bottom_margin = Cm(1.8)
    return doc

def H(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(10 if level == 1 else 7)
    h.paragraph_format.space_after = Pt(4)
    return h

def P(doc, text, bold=False, italic=False, size=10, color=None, align=None, space_after=5):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(size)
    if color:
        r.font.color.rgb = RGBColor(*color)
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    return p

def B(doc, items):
    for it in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2.5)
        if isinstance(it, tuple):
            r1 = p.add_run(it[0])
            r1.bold = True
            r1.font.size = Pt(9.8)
            r2 = p.add_run(it[1])
            r2.font.size = Pt(9.8)
        else:
            r = p.add_run(it)
            r.font.size = Pt(9.8)

def shade_cell(cell, hex_str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_str)
    tcPr.append(shd)

def set_fixed_table_layout(table):
    tblPr = table._tbl.tblPr
    for old in tblPr.findall(qn("w:tblLayout")):
        tblPr.remove(old)
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    anchor = None
    for tag in ("w:shd", "w:tblBorders", "w:tblInd", "w:tblCellSpacing", "w:jc", "w:tblW", "w:tblStyle"):
        found = tblPr.find(qn(tag))
        if found is not None:
            anchor = found
            break
    if anchor is not None:
        anchor.addnext(lay)
    else:
        tblPr.insert(0, lay)

def T(doc, headers, rows, widths=None, size=8.0, header_fill="01696F", zebra=True):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    trPr0 = t.rows[0]._tr.get_or_add_trPr()
    trPr0.append(OxmlElement("w:tblHeader"))
    trPr0.append(OxmlElement("w:cantSplit"))
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = ""
        r = c.paragraphs[0].add_run(str(h))
        r.bold = True
        r.font.size = Pt(size)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        shade_cell(c, header_fill)
    for r_idx, row in enumerate(rows):
        new_row = t.add_row()
        new_row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        cells = new_row.cells
        bg = "F7F6F2" if (zebra and r_idx % 2 == 1) else None
        for i, val in enumerate(row):
            cells[i].text = ""
            r = cells[i].paragraphs[0].add_run("" if val is None else str(val))
            r.font.size = Pt(size)
            if bg:
                shade_cell(cells[i], bg)
    if widths:
        set_fixed_table_layout(t)
        for i, w in enumerate(widths):
            t.columns[i].width = Cm(w)
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    return t

def callout(doc, title, body, fill="E9F2F2"):
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = t.rows[0].cells[0]
    shade_cell(c, fill)
    c.text = ""
    r1 = c.paragraphs[0].add_run(title)
    r1.bold = True
    r1.font.size = Pt(9.8)
    r1.font.color.rgb = RGBColor(0x1B, 0x47, 0x4D)
    p2 = c.add_paragraph()
    r2 = p2.add_run(body)
    r2.font.size = Pt(9.2)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)

def FIG(doc, path, width_cm=16.8, caption=None):
    doc.add_picture(path, width=Cm(width_cm))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    if caption:
        P(doc, caption, italic=True, size=8.6, color=(0x4A, 0x49, 0x44), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)


# ==============================================================================
# 1. BUILD STARTUP MANUAL (Markdown + Word DOCX in Simple Language)
# ==============================================================================
STARTUP_MD = """# Open Method Architecture Skill — Startup & Multi-LLM User Manual

> **Work-in-Progress Statement (Please Read First)**
> This package (**Open Method Architecture Skill, v4.1**) is an active **work in progress** and research prototype developed for the *Organization Science* Special Issue (*AI-Enabled Frontiers in Organizational Science*).
> - **What works today**: The Synthesis Layer (coding constructs and relationships across qualitative papers), the Governance & Lineage Controller (`control/oma_control.py`), the Method-Fit Diagnostic (`Skill 03`), and three deterministic math engines (`control/oma_engines.py`: Fuzzy-Set QCA, 4-Stage Process-Sequence & Entropy Analysis, and 2D Four-Regime Kruskal–Wallis & OLS Failure Auditing), plus three complete empirical demonstrations (`control/run_three_demos.py`).
> - **What is still in progress**: Blinded multi-scholar panel validation, out-of-sample transfer testing in new organizational domains, and parameterized Agent-Based Modeling (ABM) simulation engines are planned for Stage 2 development (January–May 2027).
> - **Human researcher stays in charge**: AI coding and automated runs are **starting drafts**, not final scientific truth. A human researcher must review the evidence quotes, check case boundaries, and approve every checkpoint before using results in a paper.

---

## 1. What Is Inside This Skill Package?

When you unzip `Open_Method_Architecture_Skill_Package.zip`, you will see five main parts:

| Folder or File | What It Is (in Plain English) |
|---|---|
| `START_HERE.md` & `STARTUP_MANUAL.md` | Your quick overview and this plain-language user guide. |
| `AGENT_INSTRUCTIONS.md` & `PROMPTS.md` | The main instruction sheet you give to your chosen LLM, plus ready-to-copy prompts. |
| `rules/SCIENTIFIC_RULES.md` | The 7 golden rules the AI must obey (for example: never make up quotes, never treat "not mentioned" as zero, and never pick a method before checking the data structure). |
| `skills/` (`00` through `08`) | Nine short, step-by-step guides for specific jobs: case intake (`00`), coding (`01`), cross-study translation (`02`), choosing the best method (`03`), human checkpoints (`04`), running QCA (`05`), running process-sequence & regime clustering (`06`), building theory (`07`), and validation (`08`). |
| `control/` (`oma_control.py`, `oma_engines.py`, `run_oma_checks.py`, `run_three_demos.py`) | The Python scripts that do all the real math and check that nothing was skipped or faked. |
| `demonstration/` & `templates/` | Blank CSV templates for your own papers, plus the data and full results for all three demonstrations (`three_demos_results.json` and `THREE_DEMONSTRATIONS_REPORT.md`). |

---

## 2. How the Package Works in 4 Simple Steps

1. **Step 1 — Read and Map Relationships (`Skills 01 & 02`)**:
   You give the AI your articles and case list. The AI extracts short, exact quotes with page numbers, scores constructs on a `1–5` scale, marks missing information as `NULL` (unknown), and separates empirical case studies from conceptual or broad interview papers.
2. **Step 2 — Check Which Analytical Method Fits Best (`Skill 03`)**:
   Instead of forcing every literature into QCA, the AI runs a **Method-Fit Check**. It asks: *Are these static cases (good for QCA)? Do they unfold over time in stages (good for Process-Sequence Analysis)? Does the outcome have two separate dimensions (good for 2D Regime Clustering)?*
3. **Step 3 — Let Python Run the Math (`Skills 05 & 06` + `control/oma_engines.py`)**:
   Language models are bad at doing mental math. So the LLM never guesses consistency scores, truth tables, or probabilities in prose. Instead, `control/oma_engines.py` computes the exact numbers across multiple branches (for example, strict vs. flexible rules for combining conditions or handling missing data).
4. **Step 4 — Build and Stress-Test the Theory (`Skill 07`)**:
   Finally, the system connects the math back to the exact case quotes, tests simpler rival explanations (like whether a single condition or a standard linear regression could explain the data), and lists limitations and better future study designs.

---

## 3. How to Use This Package with Different LLMs

You can use this skill package with almost any modern LLM. Pick the setup that matches your tool:

### Option A: Claude (Claude Projects, Claude Desktop, or Claude Code)
- **Claude Projects (Web/Desktop)**: Create a Project, upload `AGENT_INSTRUCTIONS.md`, `rules/SCIENTIFIC_RULES.md`, and the files in `skills/` to Project Knowledge. Paste your PDFs in batches of 5–10 and use the starter prompts from `PROMPTS.md`.
- **Claude Code (Terminal)**: Open the unzipped folder in your terminal. Rename or copy `AGENT_INSTRUCTIONS.md` to `CLAUDE.md`. Claude Code can read your PDFs and run `python3 control/oma_engines.py` and `python3 control/run_oma_checks.py` directly on your computer.

### Option B: ChatGPT (Plus / Team / Enterprise / Projects)
- Create a ChatGPT Project or thread with **Code Interpreter / Data Analysis** turned on.
- Upload the entire `Open_Method_Architecture_Skill_Package.zip` file along with your article PDFs.
- Tell ChatGPT: *"Unzip the skill package, read `AGENT_INSTRUCTIONS.md` and `rules/SCIENTIFIC_RULES.md`, and use Python to run `control/oma_control.py` and `control/oma_engines.py`."* Because ChatGPT has a built-in Python sandbox, it can run the Python engines directly in the chat.

### Option C: Google Gemini (Google AI Studio or Gemini Advanced)
- Gemini has a very large context window (1M–2M tokens), which is helpful for holding many qualitative PDFs at once.
- **Important tip for Gemini**: Even though all 30 PDFs fit in one window, ask Gemini to code **5 to 8 papers per turn** rather than all 30 in a single reply. Otherwise, output-length limits will cause it to shorten quotes or skip page numbers.

### Option D: Coding Agents (Cursor, Windsurf, Cline, Roo Code, Perplexity Computer)
- Open the unzipped package folder as your workspace.
- Copy `AGENT_INSTRUCTIONS.md` into `.cursorrules` (for Cursor) or `.clinerules` (for Cline), or simply tell the agent to read `AGENT_INSTRUCTIONS.md`.
- The agent will read your PDFs, write your coding files, and run the Python scripts automatically, pausing at each Review Card (`G1` through `G6`).

### Option E: Local Open-Weight Models (Ollama, LM Studio, vLLM)
- Best when your qualitative interviews or company documents are confidential (IRB-restricted) and cannot be sent to cloud APIs.
- Use a strong 70B+ model (such as `Qwen-2.5-72B-Instruct`, `Llama-3.3-70B-Instruct`, or `DeepSeek-R1`) with `temperature = 0.0`.
- Feed one paper and one skill file at a time, save the coded CSVs locally, and run `python3 control/run_three_demos.py` in your local terminal.

### Best Practice: Using Two Different LLMs as Independent Coders
To avoid single-model bias:
1. Run **LLM #1** (for example, Claude) in a clean session to score your cases and save `coder1.csv`.
2. Run **LLM #2** (for example, ChatGPT or Gemini) in a separate session with the exact same codebook to save `coder2.csv`.
3. Use Python to compare where the two models disagree (especially where one model guessed a score while the other marked `NULL`), and let a **human researcher** make the final call at Checkpoint `G2B`.

---

## 4. Things to Be Aware Of (Important Watch-Outs)

1. **"Not Mentioned" Is Never "Zero" (`NULL` != `0`)**: If a paper does not talk about client pressure or managerial mandates, the score must be `NULL` (unknown), **not** `1 (Low)` or `0.0`. Treating silence as absence can completely change your QCA results (as shown in Demonstration 1, where 26 of 53 cases do not report client pressure).
2. **How You Combine Conditions Matters as Much as the Data**: Combining first-order codes using a strict "weakest-link" rule (`min`) versus an "average" rule (`mean`) can cut your solution coverage in half or change how many models exist. Always run multiple branches and compare them side by side.
3. **Don't Force Every Paper into a Case Row**: Literature reviews, pre-deployment interview studies, and conceptual papers do not have a post-deployment outcome to score. Keep them in the **Synthesis-Only Register** (`Skill 01`) so they enrich your theory without polluting your truth table.
4. **Watch Out for Discretionary Case Splits**: When one qualitative paper compares two departments or two worker groups inside the same company, splitting them into separate cases increases your sample size but can create artificial clusters. Always flag splits (`is_discretionary_split = True`) and test what happens when you drop or merge them.
5. **Avoid Circular Coding ("Halo Effect")**: Never code a condition (like "mandated use" or "worker trust") using the same sentences that describe the outcome. And remember that authors of qualitative success stories often describe alignment more positively in hindsight.
6. **Know When QCA Alone Is Not Enough**: If your cases change over time (for example, an AI tool fails in month 3 and workers redesign it in month 6), a single static QCA table will mash those stages together. Use **Pathway B (Process-Sequence Analysis)** and **Pathway C (2D Regime Clustering)** alongside QCA.
7. **Always Check If a Simpler Explanation Works**: Before claiming a complex 5-variable configurational recipe, check whether a **single condition** (like Knowledge Congruence or Active Auditing alone) explains nearly as many cases, and check why a standard linear regression (OLS) fails or succeeds on the same cases.
8. **Scripted Demos Are Not Human Approvals**: Our demonstration runner (`control/run_three_demos.py`) runs in `scripted_demo` mode so you can inspect all three examples immediately. In a real research project, switch `execution_mode="researcher_operated"` so every gate waits for your real sign-off.
"""

with open(os.path.join(ROOT, "STARTUP_MANUAL.md"), "w") as f:
    f.write(STARTUP_MD)

doc_man = new_styled_doc()
P(doc_man, "Open Method Architecture Skill (v4.1)", bold=True, size=18, color=(0x01, 0x69, 0x6F), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
P(doc_man, "Plain-Language Startup & Multi-LLM User Manual", bold=True, size=13, color=(0x1B, 0x47, 0x4D), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)

callout(
    doc_man,
    "Work-in-Progress Statement (Please Read First)",
    "This skill package (Open Method Architecture Skill, v4.1) is an active work in progress and research prototype developed for the Organization Science Special Issue (AI-Enabled Frontiers in Organizational Science).\n"
    "• What is working today: The Synthesis Layer (coding constructs and relationships across qualitative papers), the Governance & Lineage Controller (control/oma_control.py), the Method-Fit Diagnostic (Skill 03), and three deterministic math engines (control/oma_engines.py: Fuzzy-Set QCA, 4-Stage Process-Sequence & Entropy Analysis, and 2D Four-Regime Kruskal–Wallis & OLS Failure Auditing), plus three complete empirical demonstrations (control/run_three_demos.py).\n"
    "• What is still in progress: Blinded multi-scholar human panel benchmarking, out-of-sample transfer testing in new organizational domains, and parameterized Agent-Based Modeling (ABM) simulation engines are Stage 2 development items (January–May 2027).\n"
    "• Human researcher stays in charge: AI coding and automated runs are starting drafts, not final scientific truth. A human researcher must review the evidence quotes, check case boundaries, and approve every checkpoint before using results in a publication."
)

H(doc_man, "1. What Is Inside This Skill Package?")
P(doc_man, "Traditional QCMA tools assume from the beginning that Fuzzy-Set QCA (fsQCA) is the only analysis you will run. The Open Method Architecture Skill is built differently: it first helps you map constructs and relationships across your papers, and then checks which analytical method (or combination of methods) actually fits your evidence best.")
T(doc_man, ["Folder or File", "What It Does (in Plain English)"], [
    ["START_HERE.md & STARTUP_MANUAL.md", "Quick orientation and this plain-language startup manual."],
    ["AGENT_INSTRUCTIONS.md & PROMPTS.md", "The master instruction sheet you give to your LLM, plus copy-paste prompts for every stage."],
    ["rules/SCIENTIFIC_RULES.md", "The 7 core scientific rules the AI must follow (e.g., never make up quotes, never treat 'not mentioned' as zero, separate empirical cases from conceptual papers, and check method fit before running math)."],
    ["skills/00_optional_case_intake_adapter.md", "Optional helper for drafting or auditing a Case Registry from raw PDFs (disabled by default when you already have approved cases)."],
    ["skills/01_construct_and_relational_coding.md", "Synthesis Layer: extracts verbatim quotes with page numbers, codes 1–5 ratings, records NULL for missing info, and logs method-neutral relationships (who did what to whom, in what sequence)."],
    ["skills/02_cross_study_translation.md", "Synthesis Layer: computes Fuzzy Jaccard similarity across constructs and separates theoretical aggregation rules (min, mean, max) from missing-data rules."],
    ["skills/03_method_fit_and_routing.md", "Analytical Gate: scores whether your data are best analyzed by static QCA, Process-Sequence modeling, 2D Regime Clustering, a Hybrid combination, or Qualitative Synthesis only."],
    ["skills/04_human_judgment_and_governance.md", "Manages human review checkpoints (G1–G6), tracks SHA-256 production lineage (produced_from), and keeps parallel branches separate."],
    ["skills/05_qca_pathway.md", "Pathway A: runs exact Quine–McCluskey fsQCA, Enhanced Standard Analysis (ESA) remainder checks, and multi-branch sensitivity."],
    ["skills/06_process_and_regime_pathway.md", "Pathways B & C: runs 4-stage Markov Process-Sequence & Shannon/Mutual-Information analysis, 2D Regime Kruskal–Wallis (eta^2) tests, and OLS linear regression failure audits."],
    ["skills/07_theory_elaboration_and_critique.md", "Builds the Theory Elaboration Register, traces propositions back to exact quotes and page numbers, tests simpler rival explanations, and ranks future study designs."],
    ["skills/08_expansion_and_validation.md", "Stage 2 literature search protocol and 7-scenario method-open validation tests."],
    ["control/ (oma_control.py, oma_engines.py, run_oma_checks.py, run_three_demos.py)", "Executable Python scripts that enforce governance rules, run all deterministic math, verify 17/17 core invariants, and recompute all three empirical demonstrations in under 3 seconds."],
    ["demonstration/ & templates/", "Blank CSV templates for your own study plus the raw inputs and full outputs for all three demonstrations."],
], widths=[5.2, 11.6], size=8.2)

H(doc_man, "2. How the Workflow Works in 4 Simple Steps")
B(doc_man, [
    ("Step 1 — Read & Map Relationships (Skills 01 & 02): ", "You supply your articles and case list. The AI extracts short verbatim quotes (8–45 words) with PDF page numbers, scores constructs on a 1–5 scale, marks unreported items as NULL (unknown), and keeps conceptual/field papers in a separate register so they do not distort case counts."),
    ("Step 2 — Check Which Method Fits Best (Skill 03): ", "Before running any QCA minimization, the system evaluates your corpus structure: how many cases you have, whether outcomes are skewed, how many papers track multi-stage processes over time, and whether the outcome has multiple dimensions. It then recommends the best analytical pathway."),
    ("Step 3 — Let Python Run the Math (Skills 05 & 06 + control/oma_engines.py): ", "The LLM never guesses consistency scores, truth tables, or probabilities in prose. All calculations are executed by control/oma_engines.py across parallel branches."),
    ("Step 4 — Build & Stress-Test the Theory (Skill 07): ", "The system links every proposition back to its supporting and deviant cases, tests rival explanations (such as a single condition or standard OLS regression), and lists concrete limitations and next-step research designs."),
])

H(doc_man, "3. How to Use This Package with Different LLMs")
T(doc_man, ["LLM Platform", "How to Set It Up", "Practical Tip for Best Results"], [
    ["Claude\n(Projects, Desktop, or Claude Code)", "• In Claude Projects: upload AGENT_INSTRUCTIONS.md, rules/SCIENTIFIC_RULES.md, and the skills/ files to Project Knowledge.\n• In Claude Code: open the folder in terminal and copy AGENT_INSTRUCTIONS.md to CLAUDE.md.", "Claude Code can run python3 control/run_three_demos.py and python3 control/oma_engines.py directly on your machine."],
    ["ChatGPT\n(Plus, Team, Enterprise, Projects)", "• Turn on Code Interpreter / Data Analysis.\n• Upload Open_Method_Architecture_Skill_Package.zip and your PDFs.\n• Ask ChatGPT to unzip the package and execute the Python scripts in control/.", "ChatGPT's built-in Python sandbox can run oma_control.py and oma_engines.py directly inside the conversation."],
    ["Google Gemini\n(AI Studio or Gemini Advanced)", "• Upload the skill files and PDFs into Gemini's 1M–2M token context window.", "Even though all 30 PDFs fit at once, ask Gemini to code 5–8 papers per message so it never shortens quotes or skips page numbers."],
    ["Coding Agents\n(Cursor, Windsurf, Cline, Perplexity Computer)", "• Open the unzipped folder as your workspace.\n• Point the agent to AGENT_INSTRUCTIONS.md.", "The agent will read PDFs, populate templates, run the Python engines, and pause at each Review Card."],
    ["Local Open-Weight LLMs\n(Ollama, LM Studio, vLLM)", "• Use a 70B+ model (Qwen-2.5-72B, Llama-3.3-70B, or DeepSeek-R1) with temperature = 0.0 for IRB-restricted data.", "Feed one paper and one skill file at a time, save CSVs locally, and run the Python scripts in your terminal."],
], widths=[3.6, 7.2, 6.0], size=8.2)

H(doc_man, "4. Copy-Paste Starter Prompts")
B(doc_man, [
    ("To run the Best-Fit Method-Open Analysis (Recommended): ", "\"Read AGENT_INSTRUCTIONS.md and rules/SCIENTIFIC_RULES.md. Reconcile my supplied articles into empirical cases and synthesis-only records, propose a construct and relational codebook, run the Method-Fit Diagnostic (Skill 03), and execute the best-fit multi-method analysis using control/oma_engines.py. Stop at each Review Card for my decision.\""),
    ("To replicate an existing QCA model (Demo 1 mode): ", "\"Read AGENT_INSTRUCTIONS.md and skills/05_qca_pathway.md. Recompute the supplied QCA model using control/oma_engines.py, separating theoretical aggregation (min vs. mean) from missing-data rules (complete-component vs. available-component vs. NULL->0.0), and audit remainder exclusions and single-condition rivals.\""),
    ("To run a new QCA-only study without replicating prior work (Demo 2 mode): ", "\"Read AGENT_INSTRUCTIONS.md, skills/01_construct_and_relational_coding.md, and skills/05_qca_pathway.md. Derive an independent outcome and conditions from these articles, run deterministic fsQCA across branches, and report both what QCA explains and what QCA alone misses.\""),
])

H(doc_man, "5. Important Things to Be Aware Of (Watch-Outs)")
B(doc_man, [
    ("1. 'Not Mentioned' Is Never 'Zero' (NULL != 0): ", "If a paper is silent on a construct, record NULL—never 1 (Low) or 0.0. In our 30-article corpus, Client Evaluation Pressure is unreported in 26 of 53 cases; treating silence as zero drastically alters truth tables."),
    ("2. Combining Rules vs. Missingness Rules Are Separate Choices: ", "Weakest-link (min) vs. average (mean) is a theoretical choice; requiring all components to be present (N=7 in Demo 1B) vs. using available components (N=49) vs. filling remaining macro NaNs with zero (N=53) is an evidence-handling choice. Keep them separate."),
    ("3. Do Not Force Conceptual or Field Papers into Case Rows: ", "Papers that interview 40 managers across 40 unnamed firms or study pre-deployment expectations belong in the Conceptual & Field-Level Synthesis Register, not as fake rows in a QCA matrix."),
    ("4. Flag Within-Paper Case Splits: ", "Splitting one article into multiple subgroup cases can drive model ambiguity. Always flag splits (is_discretionary_split = True) and test dropping them."),
    ("5. Watch Out for Retrospective Halo Bias: ", "Authors of qualitative case studies often describe knowledge alignment more positively when AI integration succeeded. Separating Decision Authority (DEC_AUTH) from Epistemic Generativity (EPI_GEN) and coding temporal stages (T0 -> T1 -> T2 -> T3) helps catch this."),
    ("6. Know When Static QCA Is Not Enough: ", "When cases experience mid-project breakdowns and redesigns, static end-state QCA compresses time. Combining QCA with 4-Stage Process-Sequence modeling and 2D Regime Clustering resolves contradictions that static QCA cannot explain."),
    ("7. Always Test Simple Rivals (Single Conditions & OLS): ", "Check whether a single condition explains nearly as much as a complex 5-variable recipe, and check where linear regression (OLS) makes sign errors."),
    ("8. Scripted Demo Approvals != Real Human Ratification: ", "The included demo runner uses execution_mode='scripted_demo' to generate complete outputs automatically. For real research, use execution_mode='researcher_operated' and review every checkpoint."),
])

man_docx_path = os.path.join(ROOT, "Open_Method_Architecture_Startup_Manual.docx")
doc_man.save(man_docx_path)
print("Saved Startup Manual DOCX:", man_docx_path)

# ==============================================================================
# 2. BUILD THREE DEMONSTRATIONS REPORT (Markdown + Comprehensive Word DOCX)
# ==============================================================================
doc_rep = new_styled_doc()
P(doc_rep, "Open Method Architecture Skill (v4.1)", bold=True, size=18, color=(0x01, 0x69, 0x6F), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
P(doc_rep, "Refined Method-Open Skill Architecture & Three Executed Empirical Demonstrations:\n(1) UTD24 Journal Submission Replication, (2) Independent (Non-UTD24 Submission) QCA-Only, and (3) Best-Fit Multi-Method Analysis", bold=True, size=12, color=(0x1B, 0x47, 0x4D), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
P(doc_rep, f"Date: {datetime.date.today().isoformat()}  |  Package: Open_Method_Architecture_Skill_Package.zip  |  Verification: 17/17 Core Invariants Passed  |  Status: Work in Progress (Provisional Research Prototype)", size=8.8, color=(0x55, 0x55, 0x55), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)

callout(
    doc_rep,
    "Work-in-Progress & Epistemic Governance Statement",
    "The Open Method Architecture Skill (v4.1) refines QCMA Skill v4.0 to align fully with the method-open architecture in the Organization Science Stage 1 proposal (Unbounding Theory Elaboration) and incorporates all methodological and software audit improvements identified during review:\n"
    "1. Method Selection as an Explicit Outcome of Synthesis: Construct and relational coding (Skills 01–02) remain method-neutral until Skill 03 (evaluate_method_fit) diagnoses the corpus structure and routes to QCA, Process-Sequence modeling, Multi-Dimensional Regime Clustering, Hybrid Triangulation, or Qualitative Synthesis.\n"
    "2. Production-Time Artifact Lineage (produced_from) & Mandatory Prerequisites: Every derived matrix, truth table, and sequence model records the SHA-256 hashes of the exact upstream artifacts used when it was computed. Issuing a new approval packet after an upstream change cannot launder an un-recomputed artifact.\n"
    "3. Orthogonal Aggregation vs. Missingness Rules: Theoretical operators (min, mean, max) are strictly separated from incomplete-evidence policies (complete_component_required, boolean_absorption_available, available_component_fallback, null_to_zero_imputation, null_to_one_stress).\n"
    "4. Genuine Raw-to-Solution Re-Execution: All three demonstrations in this report are recomputed from raw/source matrices by control/run_three_demos.py using control/oma_engines.py (never replayed from static strings)."
)

# ---------------- SECTION 1: OVERVIEW ----------------
H(doc_rep, "1. Overview of the Open Method Architecture & Three Demonstrations")
FIG(doc_rep, os.path.join(ROOT, "figs/fig0_three_demos_comparison.png"), 16.8,
    "Figure 1. Side-by-side comparison of the three empirical demonstrations executed by control/run_three_demos.py.")
FIG(doc_rep, os.path.join(ROOT, "figs/fig1_v4_architecture.png"), 16.8,
    "Figure 2. Architecture of the Open Method Architecture Skill showing the Synthesis Layer, Method-Fit Diagnostic Gate, and Three Analytical Pathways.")

T(doc_rep, ["Audit Issue Identified in Review", "Refinement Implemented in Open Method Architecture Skill (v4.1)", "Verified in Code & Tests"], [
    ["Defaulting to QCA as the only analytical destination", "Added Skill 03 (03_method_fit_and_routing.md) & oma_engines.evaluate_method_fit(), plus Skill 06 (Markov Process-Sequence & 2D Regime Kruskal–Wallis / OLS Audit). Theory synthesis (Skill 07) accepts verified outputs from any pathway.", "Test 10 & 17 in run_oma_checks.py; Demo 3"],
    ["Case intake Component 0 included inside core loop", "Converted into 00_optional_case_intake_adapter.md, disabled by default (intake_adapter_enabled=False). Researcher-approved cases and locatable excerpts are the standard entry contract.", "Tests 1 & 2 in run_oma_checks.py"],
    ["Ambiguous NULL representation ('None / 0') and bundled Branch C", "Raw coding strictly uses None/NaN for NULL (never 0). Translation rules require separate aggregation_operator and missingness_policy fields.", "Test 5 in run_oma_checks.py; Demo 1B C0 vs. A1 vs. A0 vs. C1"],
    ["Packet hashes could approve an old un-recomputed derived artifact after upstream edits", "Added production-time lineage (produced_from: {parent: sha256}) to every artifact and recursive artifact_lineage_is_fresh() verification.", "Tests 6, 7 & 13 in run_oma_checks.py"],
    ["Caller-selected required_artifacts & simulated human actor", "Enforced built-in MANDATORY_PREREQS per task and separated execution_mode ('researcher_operated', 'scripted_demo', 'computational_replay').", "Tests 3, 4 & 8 in run_oma_checks.py"],
    ["Demo runner replayed stored JSON strings; silent maxk=10 cover cap", "Rewrote control/run_three_demos.py to recompute all three demos from raw cell scores and Table A1 rows; removed silent maxk cap in cover_solutions().", "Executed in control/run_three_demos.py"],
], widths=[4.2, 8.2, 4.4], size=7.6)

# ---------------- SECTION 2: DEMONSTRATION 1 (UTD24 JOURNAL SUBMISSION REPLICATION) ----------------
H(doc_rep, "2. Demonstration 1: Replication & Sensitivity Audit of the UTD24 Journal Submission Analysis")
P(doc_rep, "In Demonstration 1, the Open Method Architecture Skill is instructed to replicate and stress-test the UTD24 Journal submission AI-integration fsQCA (Outcome: Engaged & Extensive AI Integration INT = min(ENG, EXT); 6 macro-conditions: External Receptivity ER, Knowledge Congruence KC, Mandated Automation MA, Inexperienced Augmentation IA, Transitional Ease TE, and Epistemic Uncertainty EU). We execute both Part 1A (the 55-case, 64-row aggregate truth table from Appendix Table A1) and Part 1B (raw cell-by-cell recomputation of the 53-case 30-article dual-coder dataset).")

H(doc_rep, "2.1 Part 1A: Exact 55-Case / 64-Row Table A1 Reproduction & Remainder Audit", 2)
d1a = DEMOS["demo1_utd24_replication"]["part1A_tableA1_55cases"]
B(doc_rep, [
    ("Verified Truth-Table Properties: ", "64 rows total; 26 observed rows (55 cases) and 38 empty logical remainders (59.4% limited diversity). Exactly 18 observed rows (32 cases) pass incl >= 0.80 and PRI >= 0.60 for INT; 3 observed rows (rows 5, 6, 38; 13 cases) pass for ~INT; and 5 observed rows (rows 3, 7, 19, 46, 62; 10 cases, 18.2% of N) pass neither outcome because their PRI falls between 0.452 and 0.598."),
    ("Standard vs. ESA Remainder-Excluded Intermediate Solution: ", f"Under directional expectation KC = 1 with all easy counterfactuals permitted, standard Quine–McCluskey minimization yields: {d1a['std_intermediate_without_exclusion'][0]} (where Path 2 is MA*IA*TE*EU and Path 3 is ER*IA*TE). Blocking empty remainder rows 32 (0,1,1,1,1,1) and 64 (1,1,1,1,1,1) under Enhanced Standard Analysis (ESA) reproduces the exact 5 pathways reported in the UTD24 Journal submission: {d1a['esa_intermediate_blocking_32_64'][0]}."),
    ("Reproduced Non-Integration (~INT) Solution: ", f"Conservative minimization of rows 5, 6, and 38 reproduces the exact 2 reported non-integration pathways: {d1a['reproduced_2_non_integration_paths'][0]}."),
])

T(doc_rep, ["UTD24 Path", "Assemblage Name in UTD24 Submission", "Reproduced Boolean Term", "Truth-Table Rows Covered", "Reproduced Raw Cases (n)", "Reported Fit (incl / PRI / cov / ucov)"], [
    ["Path 1a", "Decreed Acquiescence", "ER*MA*~EU", "41, 43, 45, 47, 59, 61, 63", "11", "0.849 / 0.673 / 0.381 / 0.025"],
    ["Path 1b", "Decreed Acquiescence", "MA*~TE*~EU", "9, 13, 41, 45, 61", "9", "0.829 / 0.625 / 0.362 / 0.027"],
    ["Path 2", "Decreed Reconstitution", "~KC*MA*IA*TE*EU", "16, 48 (requires blocking rem. 32 & 64)", "4", "0.949 / 0.822 / 0.181 / 0.032"],
    ["Path 3", "Selective Consultation", "ER*~MA*IA*TE", "39, 40, 55, 56 (requires blocking rem. 64)", "6", "0.919 / 0.788 / 0.337 / 0.058"],
    ["Path 4", "Cooperative Reinforcement", "KC*~MA*IA*~EU", "21, 23, 53, 55", "9", "0.974 / 0.941 / 0.366 / 0.102"],
    ["~INT 5a", "Non-Integration 5a", "~ER*~KC*~MA*IA*~TE", "5, 6", "7", "0.883 / 0.728 / 0.492 / 0.154"],
    ["~INT 5b", "Non-Integration 5b", "~KC*~MA*IA*~TE*EU", "6, 38", "11", "0.814 / 0.663 / 0.361 / 0.023"],
], widths=[1.6, 3.2, 3.3, 3.6, 1.9, 3.2], size=7.5)

P(doc_rep, "Table A1 Threshold Sensitivity Audit (Why incl = 0.70–0.85 Cannot Fail):", bold=True, size=9.5)
s_rows = [[x["spec"], str(x["n_pos_rows"]), str(x["n_models"]), x["formula"]] for x in d1a["threshold_sensitivity_grid"]]
T(doc_rep, ["Threshold Specification", "Pos. Rows", "Models", "Resulting Intermediate Solution Formula"], s_rows, widths=[4.5, 1.4, 1.2, 9.7], size=7.4)

H(doc_rep, "2.2 Part 1B: Raw-to-Solution Re-Execution of the 53-Case / 30-Article Dual-Coder Dataset", 2)
P(doc_rep, "When we recompute the 53-case 30-article dataset directly from the 954 raw cell scores in demonstration/utd24_53_attached_raw.json (rather than replaying stored result strings), separating Theoretical Aggregation from Incomplete-Evidence Handling exposes a major methodological finding:")
d1b = DEMOS["demo1_utd24_replication"]["part1B_recomputed_53cases_30articles"]
b1_labels = {
    "Branch_A0_Proposal_Available_MacroZero_N53": "A0: Proposal Macro-Zero (N=53)",
    "Branch_A1_Pure_Available_NoImpute_N49": "A1: Pure Available (N=49)",
    "Branch_B_Compensatory_Mean_N53": "B: Compensatory Mean (N=49)",
    "Branch_C0_Complete_Component_Required": "C0: Complete-Component (N=7)",
    "Branch_C1_Null_To_Zero_Imputed_N53": "C1: NULL->0.0 Imputed (N=53)",
    "Branch_D_No_Discretionary_Splits_N45": "D: No Splits (N=41)",
    "Coder1_Claude_Opus_Only_N53": "Coder 1: Claude Opus 4.6 (N=53)",
    "Coder2_GPT41_Only_N53": "Coder 2: GPT-4.1 (N=33)",
}
b1_rows = []
for bname, bobj in d1b.items():
    f_int = bobj["int_fit"]
    f_neg = bobj["neg_fit"]
    rk = bobj["kc_alone_rival"]
    b1_rows.append([
        b1_labels.get(bname, bname), str(bobj["n_complete"]), str(bobj["pos_rows"]), str(bobj["n_inter_models"]),
        f"{f_int['incl']:.3f} / {f_int['pri']:.3f} / {f_int['cov']:.3f}",
        f"{f_neg['incl']:.3f} / {f_neg['pri']:.3f} / {f_neg['cov']:.3f}",
        f"{rk['incl']:.3f} / {rk['pri']:.3f} / {rk['cov']:.3f}",
        bobj["inter_formulas"][0] if bobj["inter_formulas"] else "None"
    ])
T(doc_rep, ["Branch & Missingness Policy", "N", "Pos. Rows", "Models", "INT Fit\n(incl / PRI / cov)", "~INT Fit\n(incl / PRI / cov)", "KC-Alone Rival\n(incl / PRI / cov)", "First Intermediate Model Formula"],
  b1_rows, widths=[3.1, 0.8, 1.1, 1.1, 2.2, 2.2, 2.2, 4.1], size=6.9)

P(doc_rep, "Three critical insights from Table 2.2: (1) Complete-Component Attrition (N=7): Because Client Evaluation Pressure (CEP) is NULL in 26/53 cases and Know-What Congruence (KWC) is NULL in 25/53 cases, requiring every constituent of all 6 macro-conditions to be non-null leaves only 7 complete cases! (2) Available-Component without Macro Zero-Fill (N=49) vs. Macro Zero-Fill (N=53): Using available constituents without zero-filling leaves 4 cases with an all-NULL macro-condition (N=49, incl=0.919, PRI=0.733, cov=0.643); filling those 4 remaining macro-level NaNs with 0.0 reproduces the exact proposal baseline (N=53, incl=0.923, PRI=0.748, cov=0.641). (3) Single-Condition Rival: Across every branch, Knowledge Congruence (KC) alone achieves incl = 0.946–0.949 and cov = 0.625–0.630, matching the full 6-condition model's coverage.")

# ---------------- SECTION 3: DEMONSTRATION 2 (INDEPENDENT QCA-ONLY) ----------------
H(doc_rep, "3. Demonstration 2: Independent (Non-UTD24 Submission) QCA-Only Analysis (DEC_AUTH)")
P(doc_rep, "In Demonstration 2, we analyze the 30 supplied articles without replicating the UTD24 Journal submission, restricting the tool to a pure QCA pathway (Skill 05). We ask an independent research question: Under which combinations of sociotechnical conditions do domain experts retain or reconstruct Substantive Decision Authority over AI-mediated judgments (DEC_AUTH), and under which combinations is that decision authority displaced (~DEC_AUTH)?")
B(doc_rep, [
    ("Corpus Reconciliation (30 Articles → 20 Empirical Case Articles [27 Cases] + 10 Synthesis-Only Records): ", "Ten articles lack a bounded post-deployment case (Cruz 2024; Dutta & Naveen 2025; Ergün et al. 2026; Goto 2021, 2022, 2023; Hopf et al. 2025; Kellogg et al. 2025; Pemer & Werr 2025; Vuori et al. 2025) and are held in the Conceptual & Field-Level Register. Eight within-paper subgroup splits (EIN-D/T, FAU-A/L, PIE-S/N, VDB-HR/LM) are flagged and tested by exclusion in Branch D."),
    ("Bottom-Up First-Order Constructs & Fuzzy Jaccard Translation: ", "Ten first-order constructs (ALG_SUB, MGT_CTRL, PROF_JUR, CLI_EMB, DEV_BRG, MED_BRK, GTG_AUD, SYS_MAL, EPI_OPA, VIS_FAIL) were coded on the 1–5 rubric (with LI's unreported MGT_CTRL preserved as NULL) and translated via Fuzzy Jaccard similarity (Figure 3) into four macro-conditions: Coercive Algorithmic Closure (COERC), Institutional & Relational Standing (INST_SHD), Boundary & Malleable Infrastructure (BND_INF), and Active Epistemic Interrogation (EPI_VAL)."),
])
FIG(doc_rep, os.path.join(ROOT, "figs/fig2_jaccard_translation.png"), 14.8,
    "Figure 3. Pairwise Fuzzy Jaccard similarity J(A, B) across the 10 independent first-order constructs and 2 outcome dimensions.")

d2 = DEMOS["demo2_independent_qca_only"]
T(doc_rep, ["Branch Specification", "N", "DEC_AUTH Intermediate Formula", "DEC_AUTH Fit\n(incl / PRI / cov)", "~DEC_AUTH Intermediate Formula", "~DEC_AUTH Fit\n(incl / PRI / cov)"], [
    [k, str(V4["qca_branches"][k]["DEC_AUTH"]["n_cases"]),
     v["DEC_AUTH_formula"], f"{v['DEC_AUTH_fit'][0]:.3f} / {v['DEC_AUTH_fit'][1]:.3f} / {v['DEC_AUTH_fit'][2]:.3f}",
     v["neg_DEC_AUTH_formula"], f"{v['neg_DEC_AUTH_fit'][0]:.3f} / {v['neg_DEC_AUTH_fit'][1]:.3f} / {v['neg_DEC_AUTH_fit'][2]:.3f}"]
    for k, v in d2["branch_sensitivity_DEC_AUTH"].items()
], widths=[3.0, 0.9, 4.2, 2.7, 3.3, 2.7], size=7.4)

callout(
    doc_rep,
    "What Demonstration 2 (QCA-Only) Finds—and the 3 Structural Blind Spots It Cannot Resolve",
    "• What QCA-Only Finds: Across 8 of 9 branches (and all 19 Leave-One-Study-Out drops), Substantive Decision Authority (DEC_AUTH) is explained by ~COERC*INST_SHD + EPI_VAL (incl = 0.909–0.935, PRI = 0.891–0.921, cov = 0.936–0.964), while displacement (~DEC_AUTH) is explained by COERC*~EPI_VAL (incl = 0.907–0.935, cov = 0.636–0.701) or ~INST_SHD*~EPI_VAL (in Pure-Licensure Branch E, cov = 0.799).\n"
    "• Blind Spot 1 (Conflated High-Authority Regimes): Truth-table Row 0100 (~COERC*INST_SHD*~BND_INF*~EPI_VAL) has incl = 0.910 and OUT = 1 on DEC_AUTH, lumping unengaged radiologists who ignored AI claims (LEB-BREAST, LEB-BONE) and police brokers who monopolized an opaque algorithm (WAA) into the same 'success' set as engaged co-designers!\n"
    "• Blind Spot 2 (Unresolved Coercive-Entry Bifurcation): Eight cases enter under high coercive substitution (ALG_SUB >= 4, MGT_CTRL >= 4, PROF_JUR <= 2), yet split across GIA-DSL (retained/co-evolved), EIN-T & GIA-RM (supervisory override), MAY-BIO & MAY-REC (client-facing reconstruction), and STR-BANK, MON, VDB-LM (displaced). Static QCA cannot see the temporal sequence of operational breakdowns (VIS_FAIL) and client mobilization (CLI_EMB) that separates them.\n"
    "• Blind Spot 3 (Exclusion of 10 Conceptual/Field Studies): Static QCA has no formal way to integrate the 10 non-case studies without inventing case rows."
)

# ---------------- SECTION 4: DEMONSTRATION 3 (BEST-FIT HYBRID ANALYSIS) ----------------
H(doc_rep, "4. Demonstration 3: Method-Open Best-Fit Hybrid Analysis (Recommended by Skill 03)")
P(doc_rep, "In Demonstration 3, the Open Method Architecture Skill activates Skill 03 (oma_engines.evaluate_method_fit) before choosing an analytical engine. Because 16 of 27 empirical cases are longitudinal/ethnographic studies (59.3%), DEC_AUTH has an 81.5% positive skew, and authority exhibits two distinct dimensions (decision control vs. epistemic practice renewal), Skill 03 scores Static QCA Alone at 0.68 ('Defensible but Incomplete'), rejects Additive Linear OLS (0.25) and unparameterized ABM (0.20), and selects the Hybrid Multi-Method Triangulation Strategy (fit score = 0.94).")

H(doc_rep, "4.1 Engine 3A: 2D Outcome Disaggregation (DEC_AUTH × EPI_GEN) & Multi-Outcome GEN_AUTH fsQCA", 2)
FIG(doc_rep, os.path.join(ROOT, "figs/fig3_four_regimes_space.png"), 16.2,
    "Figure 4. Disaggregating Substantive Decision Authority (DEC_AUTH) and Epistemic Generativity (EPI_GEN) into Four Regimes across the 27 cases.")
FIG(doc_rep, os.path.join(ROOT, "figs/fig4_qca_branch_sensitivity.png"), 16.5,
    "Figure 5. Multi-outcome and multi-branch fsQCA comparison showing how tightening the outcome from DEC_AUTH (Panel A) to GEN_AUTH (Panel B) eliminates passive jurisdictional shielding.")

d3a = DEMOS["demo3_best_fit_hybrid"]["pathway_3A_multi_outcome_qca"]
T(doc_rep, ["Branch Specification", "ESA CSAs Excluded", "GEN_AUTH Intermediate Formula", "GEN_AUTH Fit\n(incl / PRI / cov)", "~GEN_AUTH Intermediate Formula", "~GEN_AUTH Fit\n(incl / PRI / cov)"], [
    [k, ", ".join(v["esa_csas_excluded"]) if v["esa_csas_excluded"] else "None",
     v["GEN_AUTH_formula"], f"{v['GEN_AUTH_fit'][0]:.3f} / {v['GEN_AUTH_fit'][1]:.3f} / {v['GEN_AUTH_fit'][2]:.3f}",
     v["neg_GEN_AUTH_formula"], f"{v['neg_GEN_AUTH_fit'][0]:.3f} / {v['neg_GEN_AUTH_fit'][1]:.3f} / {v['neg_GEN_AUTH_fit'][2]:.3f}"]
    for k, v in d3a["branch_sensitivity_GEN_AUTH"].items()
], widths=[3.0, 1.6, 4.3, 2.5, 2.9, 2.5], size=7.3)

P(doc_rep, "Why Engine 3A Solves Blind Spot 1: When the outcome requires both decision authority and epistemic renewal (GEN_AUTH = min(DEC_AUTH, EPI_GEN)), truth-table Row 0100 (~COERC*INST_SHD*~BND_INF*~EPI_VAL: LEB-BREAST, LEB-BONE, WAA) drops from incl = 0.910, PRI = 0.862 (OUT = 1) on DEC_AUTH to incl = 0.576, PRI = 0.000 (OUT = 0) on GEN_AUTH! Passive institutional standing without boundary bridging or active interrogation protects formal veto power (Regime II), but never produces generative human–AI co-evolution (Regime I). Across all branches, ~BND_INF*~EPI_VAL is sufficient for ~GEN_AUTH (incl = 0.925–0.974, PRI = 0.890–0.960).")

H(doc_rep, "4.2 Engine 3B: Four-Stage Markov Process-Sequence & Shannon/NMI Information-Gain Analysis", 2)
FIG(doc_rep, os.path.join(ROOT, "figs/fig5_temporal_alluvial.png"), 16.8,
    "Figure 6. Left: All 17 observed 4-stage process trajectories (T0 → T1 → T2 → T3). Right: Cumulative percentage of final regime entropy H(T3)=1.714 bits explained at each temporal stage.")

P(doc_rep, "Why Engine 3B Solves Blind Spot 2 (The 8-Case Coercive-Substitutive Bifurcation): Initial deployment structure T0 explains only 27.9% of final regime entropy (MI = 0.477 bits out of H(T3) = 1.714 bits). Adding the T1 epistemic trigger (operational_breakdown, epistemic_divergence, jurisdictional_threat, smooth_complementarity) doubles explained information to 64.6% (MI = 1.108 bits), and T2 mobilization practices lock in 100.0% (MI = 1.714 bits). Among the 8 cases entering at T0 = coercive_substitutive, visible operational failure (VIS_FAIL = 5) with reachable internal developers triggers hypothesis-testing co-design (GIA-DSL → Regime I); failure with unreachable developers triggers supervisory override without co-design (EIN-T, GIA-RM → Regime II); high client embeddedness (CLI_EMB = 5) shifts authority reconstruction to client explanations (MAY-BIO, MAY-REC → Regime III); and locked systems with transactional client contact lock in displacement (STR-BANK, MON, VDB-LM → Regime IV).")

H(doc_rep, "4.3 Engine 3C: Four-Regime Kruskal–Wallis Discriminant Analysis & Additive OLS Failure Audit", 2)
FIG(doc_rep, os.path.join(ROOT, "figs/fig6_regime_profiles_and_ols.png"), 16.8,
    "Figure 7. Panel A: Non-parametric Kruskal–Wallis effect sizes (η²) across the four regimes. Panel B: Additive OLS predicted vs. actual DEC_AUTH showing crossover sign errors.")

P(doc_rep, "Why Engine 3C Outperforms Variance Regression: Non-parametric Kruskal–Wallis tests across the four regimes prove that active socio-technical practices—Ground-Truth Auditing (GTG_AUD, H=18.97, η²=0.694), Technical Malleability (SYS_MAL, H=17.38, η²=0.625), Developer Co-Design (DEV_BRG, H=16.06, η²=0.568), Brokerage (MED_BRK, η²=0.432), and Client Embeddedness (CLI_EMB, η²=0.406)—discriminate regimes far more powerfully than Algorithmic Substitution (ALG_SUB, η²=0.256), Professional Jurisdiction (PROF_JUR, η²=0.193), or Managerial Control (MGT_CTRL, η²=0.130), while Experienced Opacity (EPI_OPA, η²=0.019) is a near-constant scope condition. By contrast, an additive OLS regression estimates the net effect of Boundary Infrastructure (BND_INF) on DEC_AUTH as β = +0.012 (t = 0.09, p = 0.93) and commits crossover sign errors on PIE-N (predicting 0.527 vs. actual 0.263, missing cognitive dependency drift), EIN-T (predicting 0.432 vs. actual 0.762, missing breakdown recovery), GIA-RM (predicting 0.499 vs. actual 0.524), and EIN-D on GEN_AUTH (predicting 0.631 vs. actual 0.263).")

# ---------------- SECTION 5: THEORY ELABORATION & LIMITATIONS ----------------
H(doc_rep, "5. Synthesis Across All Three Demonstrations: Theory Elaboration Register & Next Steps")
T(doc_rep, ["Prop. ID", "Elaboration Type", "Core Theoretical Proposition", "Multi-Method Empirical Signature (Demo 2 vs. Demo 3)", "Synthesis-Only Field Corroboration (10 Studies)", "Survival Status"], [
    ["P1", "Outcome Disaggregation & Boundary Specification", "Institutional jurisdiction under low coercion (~COERC*INST_SHD) preserves formal decision veto (DEC_AUTH), but without boundary infrastructure or active interrogation (~BND_INF*~EPI_VAL) it yields Defensive Shielding (Regime II) rather than Generative Co-Evolution (Regime I).", "Row 0100 flips from OUT=1 (incl=0.910) on DEC_AUTH to OUT=0 (incl=0.576, PRI=0.000) on GEN_AUTH; ~BND_INF*~EPI_VAL -> ~GEN_AUTH (incl=0.949).", "Goto (2021, 2022) & Pemer & Werr (2025) on protective professional jurisdiction.", "Invariant across all 9 branches & 19 LOSO drops."],
    ["P2", "Mechanism Refinement", "Generative human–AI co-evolution (GEN_AUTH, Regime I) requires coupling active ground-truth interrogation (EPI_VAL) with socio-technical boundary infrastructure (BND_INF: co-design, brokerage, malleability; Jaccard J=0.81–0.86) or non-coercive institutional standing.", "Branch E GEN_AUTH: ~COERC*INST_SHD*EPI_VAL + BND_INF*EPI_VAL (incl=0.981, PRI=0.974); Kruskal η²: GTG_AUD=0.694, SYS_MAL=0.625, DEV_BRG=0.568.", "Hopf et al. (2025) (hybrid group mind) & Ergün et al. (2026) (leader coaching).", "Core invariant across all branches."],
    ["P3", "Temporal Relationship Revision", "Coercive, substitutive deployment (T0 = coercive_substitutive) is not sufficient for displacement: visible operational breakdowns (T1 = VIS_FAIL) act as epistemic shocks that trigger generative re-looping when internal developers are reachable (GIA-DSL → R1) or supervisory override when they are not (EIN-T, GIA-RM → R2).", "Process NMI: T0 explains 27.9% of H(T3); T0+T1 explains 64.6%; T0+T1+T2 explains 100.0%.", "Fernandez Cruz (2024) on error-triggered intervention.", "Invisible to static QCA; 100% resolved by Pathway B."],
    ["P4", "Lateral Locus Shift", "When algorithmic selection is locked (ALG_SUB=5, DEC_AUTH=2) and no technical breakdown forces redesign, high client relational embeddedness (CLI_EMB=5) enables experts to reconstruct authority laterally toward clients (MAY-BIO, MAY-REC → Regime III).", "Kruskal CLI_EMB mean = 5.00 in R3 vs. 2.25 in R4; separating CLI_EMB in Branch E raises GEN_AUTH incl from 0.865 to 0.981.", "Dutta & Naveen (2025) on consultative HR repositioning.", "Explicitly isolated by Branch E & Pathway C."],
    ["P5", "Asymmetric Dual Failure Routes", "Epistemic displacement/erosion (Regime IV) occurs via two opposite dynamic trajectories: (a) Coercive Replacement under locked workflows and surveillance (STR-BANK, MON, VDB-LM), and (b) Smooth-Complementarity Dependency Drift under accurate-looking advisory AI outside core specialty jurisdiction (PIE-N).", "~DEC_AUTH: COERC*~EPI_VAL (incl=0.907) + PIE-N smooth-complementarity trajectory in Pathway B; OLS misses PIE-N (pred=0.527 vs act=0.263).", "Vuori et al. (2025) (covert hiding under surveillance) & Kellogg et al. (2025) (novice risk work blocking junior brokerage).", "Coercive route robust in QCA; Drift route captured by Process & Regime engines."],
    ["P6", "Scope Simplification", "Experienced algorithmic opacity (EPI_OPA) is high across all four regimes (Kruskal η²=0.019; >0.50 in 23/27 cases) and does not differentiate authority retention from displacement.", "Kruskal H=3.36, η²=0.019 (lowest of all 10 constructs).", "Challenges explainable-AI determinism across the corpus.", "Invariant across all analyses."],
], widths=[1.1, 2.5, 3.8, 3.4, 3.0, 3.0], size=7.0)

rep_docx_path = os.path.join(ROOT, "Open_Method_Architecture_Three_Demonstrations_Report.docx")
doc_rep.save(rep_docx_path)
print("Saved Three Demonstrations Report DOCX:", rep_docx_path)

# Also write demonstration/THREE_DEMONSTRATIONS_REPORT.md
with open(os.path.join(ROOT, "demonstration/THREE_DEMONSTRATIONS_REPORT.md"), "w") as f:
    f.write("""# Open Method Architecture Skill — Three Executed Empirical Demonstrations

This report summarizes the three demonstrations recomputed from source matrices by `python3 control/run_three_demos.py`:

1. **Demonstration 1 — UTD24 Journal Submission AI-Integration QCA Replication & Reconstruction (`Forced QCA Mode`)**:
   - **Part 1A (55-Case / 64-Row Table A1)**: Verifies all 26 observed rows, proves that reproducing Paths 2 (`~KC*MA*IA*TE*EU`) and 3 (`ER*~MA*IA*TE`) requires blocking empty remainder rows `32` and `64` under Enhanced Standard Analysis (ESA), and shows that threshold invariance across `incl = 0.70–0.85` is an artifact of `PRI >= 0.60` being binding.
   - **Part 1B (53-Case / 30-Article Raw Dual-Coder Re-Execution)**: Separates theoretical aggregation (`min` vs. `mean`) from incomplete-evidence policies (`A0 Proposal Macro-Zero Fallback N=53: incl=0.923, PRI=0.748, cov=0.641`; `A1 Pure Available No-Impute N=49: incl=0.919, PRI=0.733, cov=0.643`; `C0 Strict Complete-Component Required N=7` due to 26 `NULL`s in `CEP` and 25 `NULL`s in `KWC`; `B Compensatory Mean N=49`; `C1 NULL->0.0 Imputed N=53`; `D No Discretionary Splits N=41`).

2. **Demonstration 2 — Independent (Non-UTD24 Journal Submission) QCA-Only Analysis (`Substantive Decision Authority DEC_AUTH`)**:
   - Derives 10 first-order constructs and 4 macro-conditions (`COERC, INST_SHD, BND_INF, EPI_VAL`) across 27 empirical cases (keeping 10 conceptual/field studies in a separate register).
   - Finds `~COERC*INST_SHD + EPI_VAL -> DEC_AUTH` (`incl = 0.912, PRI = 0.893, cov = 0.949`) and `COERC*~EPI_VAL -> ~DEC_AUTH` (`incl = 0.907, PRI = 0.860, cov = 0.636`), and diagnoses three blind spots of stopping at static QCA alone.

3. **Demonstration 3 — Method-Open Best-Fit Hybrid Analysis (`Recommended by Skill 03, Fit Score = 0.94`)**:
   - **Engine 3A (2D Outcome Disaggregation & Multi-Outcome `GEN_AUTH` fsQCA)**: Separates `Regime I (Generative Co-Evolution, n=13)`, `Regime II (Defensive/Curatorial Shielding, n=8)`, `Regime III (Relational Reconstruction, n=2)`, and `Regime IV (Displacement/Drift, n=4)`. Tightening the outcome from `DEC_AUTH` to `GEN_AUTH = min(DEC_AUTH, EPI_GEN)` flips Row `0100` (`LEB-BREAST, LEB-BONE, WAA`) from `OUT=1` (`incl=0.910`) to `OUT=0` (`incl=0.576, PRI=0.000`), while `~BND_INF*~EPI_VAL -> ~GEN_AUTH` holds across all branches (`incl = 0.925–0.974`).
   - **Engine 3B (4-Stage Markov Process-Sequence & Shannon/NMI Information-Gain Analysis)**: Shows that initial deployment `T0` explains only `27.9%` of final regime entropy `H(T3) = 1.714 bits`, `T0+T1` explains `64.6%`, and `T0+T1+T2` explains `100.0%`, resolving all 8 `T0 = coercive_substitutive` cases.
   - **Engine 3C (Kruskal–Wallis `eta^2` & Additive OLS Failure Audit)**: Shows that `GTG_AUD` (`eta^2=0.694`), `SYS_MAL` (`0.625`), and `DEV_BRG` (`0.568`) drive regime separation while `EPI_OPA` (`0.019`) is a scope constant, and demonstrates why additive OLS (`BND_INF beta = +0.012, p = 0.93`) commits crossover sign errors on `PIE-N`, `EIN-T`, `GIA-RM`, and `EIN-D`.
""")
