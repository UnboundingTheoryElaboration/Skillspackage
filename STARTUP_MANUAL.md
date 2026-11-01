# Open Method Architecture Skill — Startup & Multi-LLM User Manual

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
