#!/usr/bin/env python3
"""Render the Apart AI x Epistemics Sprint report PDF (template structure)."""
from fpdf import FPDF

FONT_DIR = "/usr/share/fonts/truetype/liberation/"

class Report(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("serif", "", 9)
        self.set_text_color(90, 90, 90)
        self.cell(0, 10, str(self.page_no()), align="C")

pdf = Report(orientation="P", unit="mm", format="Letter")
pdf.add_font("serif", "", FONT_DIR + "LiberationSerif-Regular.ttf")
pdf.add_font("serif", "B", FONT_DIR + "LiberationSerif-Bold.ttf")
pdf.add_font("serif", "I", FONT_DIR + "LiberationSerif-Italic.ttf")
pdf.add_font("serif", "BI", FONT_DIR + "LiberationSerif-BoldItalic.ttf")
pdf.add_font("mono", "", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
pdf.set_margins(25.4, 22, 25.4)
pdf.set_auto_page_break(True, 22)
pdf.add_page()
W = pdf.w - 50.8  # text width

def conv(s):
    s = s.replace("<b>", "**").replace("</b>", "**")
    s = s.replace("<i>", "__").replace("</i>", "__")
    s = s.replace("&nbsp;", " ").replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    return s

def para(html, size=11, lh=5.9, align="J", space_after=2.6, indent=0.0):
    pdf.set_font("serif", "", size)
    pdf.set_x(pdf.l_margin + indent)
    pdf.multi_cell(W - indent, lh, conv(html), align=align, markdown=True)
    pdf.ln(space_after)

def heading(text, size=13, space_before=5.0, space_after=2.2):
    pdf.ln(space_before)
    pdf.set_font("serif", "B", size)
    pdf.multi_cell(W, 6.2, text, align="L")
    pdf.ln(space_after)

def centered(text, style="", size=11, lh=6.0, space_after=1.0):
    pdf.set_font("serif", style, size)
    pdf.multi_cell(W, lh, text, align="C")
    pdf.ln(space_after)

# ---------------------------------------------------------------- title block
pdf.ln(2)
pdf.set_font("serif", "B", 16.5)
pdf.multi_cell(W, 8.0,
    "Auditing Epistemic Guardrails From Their Own Artifacts: "
    "Independent Verification of Subjective-Logic Uncertainty Claims "
    "for LLM-Driven Actuation", align="C")
pdf.ln(3.5)
centered("Muntaser Syed", "", 11.5, space_after=0.2)
centered("Florida Institute of Technology", "", 11, space_after=0.2)
centered("msyed2011@my.fit.edu", "", 10.5, space_after=2.0)
centered("With Apart Research", "I", 10.5, space_after=0.5)
pdf.set_font("serif", "I", 8.8)
pdf.multi_cell(W, 4.6, "Research conducted at the AI x Epistemics Research Sprint, November 2026.", align="C")
pdf.ln(4)

# ---------------------------------------------------------------- abstract
pdf.set_left_margin(25.4 + 5)
pdf.set_right_margin(25.4 + 5)
pdf.set_x(pdf.l_margin)
pdf.set_font("serif", "", 10.5)
abstract = ("<b>Abstract.</b> Claims about epistemic guardrails are becoming load-bearing: if an uncertainty "
    "layer is said to be what stands between a language model and a physical actuator, other researchers and "
    "practitioners will build on that claim. Yet such claims are rarely re-derived from the artifacts released "
    "with them. This report is an artifact audit of one published system, <i>Epistemic Edge</i> (Syed and Silaghi, "
    "IEEE IRI 2026), which places subjective-logic uncertainty quantification between IoT sensors and an LLM that "
    "can actuate. I recomputed the paper's three headline claims directly from its released ground-truth result "
    "files, without re-running any model: all 17 released ablation runs (6,800 trials, including runs outside the "
    "published seven-model subset), and the BATADAL benchmark summaries, configuration heatmap, and per-timestamp "
    "scores (422 configurations). The central claim reproduces exactly: threshold-guardrail accuracy is 1.00 with "
    "the full pipeline and exactly 0.40 without the epistemic layer, in 17 of 17 runs. The BATADAL AUROC of 0.9004 "
    "re-derives exactly, and the audit localizes the failure mode precisely: accuracy collapses only when the fused "
    "opinion is vacuous or absent, not when fusion is bypassed by passthrough. Per-event analysis confirms that no "
    "single subjective-logic signal detects all five attacks best. Artifact-complete releases make claims "
    "checkable; this audit shows what checking them adds.")
pdf.set_x(pdf.l_margin)
pdf.multi_cell(W - 10, 5.6, conv(abstract), align="J", markdown=True)
pdf.set_left_margin(25.4)
pdf.set_right_margin(25.4)
pdf.ln(5)

# ---------------------------------------------------------------- 1 intro
heading("1. Introduction")
para("AI systems are increasingly asked not only to describe the world but to act on it, and to say how sure "
     "they are. The sprint's first two tracks ask the same question from opposite ends: does a model know how "
     "solid its claims are, and what trust infrastructure makes checking claims cheap and hard to manipulate? "
     "A precondition for both is that published epistemic claims are themselves checkable. In practice they "
     "usually are not: papers report aggregate numbers, and the result files behind them, if released at all, "
     "are seldom re-examined.")
para("This project takes one published epistemic-guardrail system and audits its claims against its own "
     "released artifacts. The system is <i>Epistemic Edge</i> [1], a four-tier neuro-symbolic pipeline that "
     "annotates sensor streams with subjective-logic (SL) opinions (belief, disbelief, uncertainty) [2], fuses "
     "them, decays them over time, and lets an LLM actuate only when the fused opinion passes an epistemic "
     "threshold guardrail in addition to a behavioral whitelist. The paper reports three findings: (1) removing "
     "the epistemic layer collapses threshold-guardrail accuracy from 1.00 to exactly 0.40 across seven locally "
     "deployed LLMs (2,800 controlled trials); (2) on the BATADAL water-distribution attack benchmark [3], "
     "calibrated SL opinions reach AUROC 0.9004 with no trained weights; (3) the SL dimensions are decomposable: "
     "different attack events are optimally detected by different SL-derived signals, and no single signal wins "
     "on all five events.")
para("<b>Disclosure and scope.</b> The audited paper is my own prior published work with Marius Silaghi, and "
     "the audited artifacts are its public release. This is therefore a self-audit, and Section 5 states what "
     "that does and does not establish. The sprint-period work reported here is the audit itself: the "
     "recomputation of every headline number from the released files, two analyses the paper does not contain "
     "(a paired fusion analysis over the full configuration grid, and a per-event signal analysis under a "
     "stated protocol), and this report. The system, the paper, and the underlying experiment data are "
     "preexisting and are marked as such throughout.")
para("Our main contributions are:")
for i, c in enumerate([
    "A complete artifact audit of a published epistemic-guardrail claim set: all 17 released ablation runs "
    "(6,800 trials) and all 422 BATADAL configurations, recomputed with a single released script, rather than "
    "the published subsets alone.",
    "An exact verification of the two quantitative headline claims (1.00 vs. 0.40; AUROC 0.9004), plus a "
    "sharper localization of the failure mode: the collapse occurs exactly when the fused opinion is vacuous "
    "or absent, and not under passthrough fusion.",
    "A per-event re-analysis showing the decomposability claim holds in substance (three different signals win "
    "the five events; belief-family signals are anti-predictive in the positive direction), and an audit "
    "observation about phase-dependent configuration selection that headline reading alone would miss.",
], 1):
    para(f"<b>{i}.</b>&nbsp;&nbsp;{c}", indent=4.0, space_after=1.2)
pdf.ln(1.5)

# ---------------------------------------------------------------- 2 related
heading("2. Related Work")
para("Subjective logic [2] represents an opinion as a triple of belief, disbelief, and uncertainty summing to "
     "one, with operators for fusion and discounting; it is one of several formalisms for carrying explicit "
     "uncertainty alongside a decision. The broader calibration literature shows that modern neural networks "
     "are typically miscalibrated out of the box [4], and recent work argues that common benchmarks reward "
     "confident guessing over honest abstention [5], while benchmarks such as MASK measure whether models "
     "contradict their own stated beliefs under pressure [6]. Epistemic Edge sits downstream of these "
     "questions: it does not ask the LLM to be calibrated, but wraps it in an external epistemic layer whose "
     "opinions are computed from sensor evidence, and blocks actuation when uncertainty is high.")
para("BATADAL [3] is a standard benchmark for cyber-attack detection in water distribution systems, with "
     "labeled attack events in real telemetry. Artifact and reproducibility evaluation has a long history in "
     "systems venues, but remains rare for safety-relevant ML claims, where the cost of an unchecked number is "
     "highest. This audit is a small instance of a general practice the field needs: claims shipped with "
     "complete, immutable result files, and independent recomputation treated as normal scientific work.")

# ---------------------------------------------------------------- 3 methods
heading("3. Methods")
para("<b>Artifacts audited.</b> The public repository (github.com/jemsbhai/epistemic-edge, also on PyPI as "
     "epistemic-edge) declares its experiments/results/ JSON and CSV files to be the immutable ground truth "
     "for every reported number. The audit covers: 17 ablation result files for the controlled-trial "
     "experiment; 3 BATADAL summary files; the primary run's 422-row configuration heatmap; the primary run's "
     "per-timestamp score series (4,177 evaluation rows, 43 sensors); and the run's reproducibility record.")
para("<b>Audit protocol.</b> For each headline claim I extracted the corresponding quantity from every "
     "released file that records it, not only from the files behind the published tables, and compared values "
     "exactly. No LLM was re-run and the BATADAL pipeline was not re-executed: the audit verifies that the "
     "released record supports the published numbers, and says so where verification of a different kind (for "
     "example, re-running the trials) would be needed. The audit script is released with this report "
     "(github.com/jemsbhai/epistemic-edge-audit) and uses only the Python standard library.")
para("<b>Conditions.</b> The controlled-trial experiment runs eight conditions per model over five IoT "
     "actuation scenarios, 400 trials per run. Threshold-guardrail accuracy is defined for the five conditions "
     "in which the threshold guardrail is active: C (full pipeline), D (no temporal decay), E1 (no fusion, "
     "vacuous opinion), E2 (no fusion, passthrough opinion), and G (no epistemic layer).")
para("<b>Audit-side analyses.</b> Two analyses are new. (i) A paired fusion analysis: across the "
     "422-configuration BATADAL grid, I matched configurations differing only in whether SL fusion is enabled "
     "(150 matched pairs) and compared headline AUROC. (ii) A per-event analysis: using the released "
     "per-timestamp scores of the primary run, I computed, for each of the five attack events, the rank-based "
     "AUROC of each SL-derived signal with event-window samples as positives and all non-attack samples as "
     "negatives. The paper's own per-event analysis used its authors' protocol; mine is stated here so the "
     "comparison is honest.")

def table(headers, rows, widths, aligns=None, caption=None, note=None):
    aligns = aligns or ["L"] * len(headers)
    pdf.set_font("serif", "B", 9.8)
    y0 = pdf.get_y()
    pdf.line(pdf.l_margin, y0, pdf.l_margin + sum(widths), y0)
    pdf.ln(1.0)
    x = pdf.l_margin
    for h, w, a in zip(headers, widths, aligns):
        pdf.set_xy(x, pdf.get_y())
        pdf.cell(w, 5.2, h, align=a)
        x += w
    pdf.ln(5.6)
    y1 = pdf.get_y()
    pdf.line(pdf.l_margin, y1, pdf.l_margin + sum(widths), y1)
    pdf.set_font("serif", "", 9.8)
    for row in rows:
        x = pdf.l_margin
        y = pdf.get_y()
        for v, w, a in zip(row, widths, aligns):
            pdf.set_xy(x, y)
            pdf.cell(w, 5.2, v, align=a)
            x += w
        pdf.ln(5.6)
    y2 = pdf.get_y()
    pdf.line(pdf.l_margin, y2, pdf.l_margin + sum(widths), y2)
    pdf.ln(1.6)
    if note:
        pdf.set_font("serif", "I", 8.8)
        pdf.multi_cell(W, 4.4, note, align="L")
    if caption:
        pdf.set_font("serif", "", 9.6)
        pdf.multi_cell(W, 4.8, caption, align="L")
    pdf.ln(3.2)

# ---------------------------------------------------------------- 4 results
heading("4. Results")
heading("4.1 Claim 1: the epistemic layer is necessary (verified exactly, and beyond the published subset)", size=11.5, space_before=2.0)
para("Table 1 summarizes the audit of all 17 released ablation runs. In every run, the full pipeline scores "
     "threshold-guardrail accuracy 1.00 and the no-epistemic condition scores exactly 0.40, matching the "
     "paper's claim for its published seven-model subset (2,800 trials) and extending it to the full released "
     "record (6,800 trials, including repeat and variant runs the paper does not tabulate).")
para("The condition structure also sharpens the claim. The 0.40 floor appears in exactly two conditions: G "
     "(no epistemic layer) and E1 (fusion replaced by the vacuous opinion). Condition E2, which keeps "
     "per-source opinions but passes them through without fusion, retains 1.00, as does D (no decay). The "
     "collapse is therefore not caused by the absence of fusion machinery as such; it occurs when the opinion "
     "the guardrail sees is vacuous or missing, which is precisely the state in which a threshold on "
     "uncertainty cannot discriminate. The active ingredient, on this benchmark, is a non-vacuous calibrated "
     "opinion at the guardrail.")
table(
    ["Condition", "Description", "Threshold accuracy", "Runs"],
    [["C", "Full pipeline", "1.00", "17/17"],
     ["D", "No temporal decay", "1.00", "17/17"],
     ["E2", "No fusion, passthrough", "1.00", "17/17"],
     ["E1", "No fusion, vacuous opinion", "0.40", "17/17"],
     ["G", "No epistemic layer", "0.40", "17/17"]],
    [24, 62, 42, 20],
    caption="Table 1: Artifact audit of Claim 1. Values recomputed from every released ablation result file "
            "(17 runs, 400 trials each, 6,800 total). Conditions A (bare LLM), B (raw payloads), and F (no "
            "guardrails) do not define threshold accuracy.")

heading("4.2 Claim 2: BATADAL AUROC 0.9004 (verified exactly)", size=11.5, space_before=2.0)
para("The final BATADAL summary records a best AUROC of 0.9004, attained by the configuration: historical "
     "calibration strategy, window k=24, decay λ=0.25, fusion and decay enabled, domain physics bounds, "
     "fused-disbelief anomaly score, smoothing 5. The run's reproducibility record (seed 42) reports original "
     "and verification metrics identical on every field (AUROC 0.9004, AUPRC 0.6379, best F1 0.6481), and my "
     "recomputation from the summary agrees. Two earlier summary files record 0.8447, which the audit traces "
     "to an earlier selection stage: 0.8447 is exactly the grid maximum of the fused-uncertainty signal "
     "(Section 4.3). The headline number is the final configuration's, not the largest number anywhere in "
     "the record.")
para("The paired fusion analysis supports the paper's reported fusion effect in direction: across 150 "
     "matched configuration pairs differing only in fusion, AUROC improves by a mean of +0.065 (median "
     "+0.054); 65.3% of pairs improve and 33.3% are exactly unchanged (fusion is a no-op where a timestamp "
     "carries effectively one opinion stream). I did not re-derive the paper's Wilcoxon statistic "
     "(p &lt; 0.0001, Cohen's d = 1.01) on its original subset; the paired analysis here is an independent "
     "check on the full grid, and it agrees in direction and rough magnitude.")
para("One audit observation: the full grid contains a fused-disbelief AUROC of 0.9356, higher than the "
     "selected configuration's 0.9004. It occurs in a decay-ablation-phase row (decay off, λ=0.1, smoothing "
     "1) whose selected anomaly score was a different signal; within the signal-sweep phase in which selection "
     "was performed, the selected row is the best row. The published number is thus phase-consistent, but the "
     "record shows why artifact access matters: a reader of only the heatmap could reasonably ask why 0.9356 "
     "was not the headline, and only the phase structure answers it.")

heading("4.3 Claim 3: signals are decomposable (verified in substance)", size=11.5, space_before=2.0)
para("Across the 422-configuration grid, the per-signal AUROC maxima differ widely: fused disbelief 0.9356, "
     "composite uncertainty-disbelief 0.9322, max disbelief 0.8764, fused uncertainty 0.8447, mean uncertainty "
     "0.8151, max uncertainty 0.7347. No signal's maximum is attained by the same configuration as another's, "
     "and the ranking of signals changes across the grid.")
para("The per-event re-analysis (Table 2) is more direct. Three different signals win the five events: fused "
     "uncertainty wins events 1, 4, and 5 (0.995, 0.887, 0.996), fused disbelief wins event 2 (0.805), and max "
     "disbelief wins event 3 (0.666). Event 3 is the hardest for every signal. Belief-family signals are "
     "strongly anti-predictive as positive-direction scores (fused belief: 0.008 and 0.004 on events 1 and "
     "5), which is the expected signature of belief collapsing during an attack: read in the negative "
     "direction they are among the most informative signals on those events. The paper's claim, that no single "
     "signal wins on all five events and that the SL dimensions detect structurally different attack classes, "
     "holds under this independent protocol; the stronger phrasing that every event has a distinct optimal "
     "signal does not (fused uncertainty wins three of five).")
table(
    ["Event", "Rows", "Best signal", "AUROC", "Runner-up"],
    [["1", "1731-1772", "fused uncertainty", "0.995", "fused disbelief 0.992"],
     ["2", "2337-2396", "fused disbelief", "0.805", "fused uncertainty 0.750"],
     ["3", "2851-2887", "max disbelief", "0.666", "fused disbelief 0.616"],
     ["4", "3508-3514", "fused uncertainty", "0.887", "fused disbelief 0.854"],
     ["5", "3741-3813", "fused uncertainty", "0.996", "fused disbelief 0.996"]],
    [16, 28, 38, 20, 46],
    caption="Table 2: Per-event re-analysis from the released primary-run score series, under the audit "
            "protocol of Section 3. Event windows match the released summary's attack records exactly.")

# ---------------------------------------------------------------- 5 discussion
heading("5. Discussion and Limitations")
para("The audit's positive result is narrow and worth stating narrowly: the published numbers of Epistemic "
     "Edge are exactly the numbers its released artifacts contain, across a record roughly 2.4 times larger "
     "than the published tables, and the one apparent anomaly in the record (a grid AUROC above the headline) "
     "has a documented structural explanation. That is the outcome trust infrastructure is supposed to "
     "produce, and it was cheap: one script, no compute of consequence, because the release was "
     "artifact-complete.")
para("<b>Limitations.</b> First, this is a self-audit: I am the first author of the audited paper. The "
     "mitigation is procedural, not personal: every step is recomputation from public immutable files with a "
     "released script, so any reader can repeat it exactly; but an auditor with no stake in the outcome would "
     "be stronger evidence, and this report should be read as an invitation to replicate rather than as "
     "independent certification. Second, the audit verifies the record, not the original runs: a result file "
     "fabricated at the source would pass. Provenance of the files themselves (for example, signed or "
     "timestamped result logs) is outside what the release provides, and is a concrete improvement future "
     "releases should make. Third, the controlled-trial benchmark is small and synthetic (five scenarios); "
     "the 1.00/0.40 separation is exact on it, and says little about effect sizes on messier actuation tasks. "
     "Fourth, my per-event protocol differs from the paper's, so Claim 3 is verified in substance rather than "
     "to the digit.")
para("<b>Future work.</b> Three extensions follow naturally: third-party replication of the ablation on "
     "independently run trials; provenance-signed result artifacts in the epistemic-edge release, so future "
     "audits can check origin as well as content; and applying the same audit treatment to the system's "
     "calibration claims under distribution shift, where the guardrail matters most and the current record is "
     "thinnest.")

# ---------------------------------------------------------------- 6 conclusion
heading("6. Conclusion")
para("Epistemic claims deserve the same skepticism they are built to operationalize. Auditing one published "
     "guardrail system against its own artifacts, I found its headline claims exact, its failure mode more "
     "precisely located than the paper states (vacuous or absent opinions, not missing fusion), and its "
     "decomposability claim supported in substance. The larger point is procedural: none of this required new "
     "experiments, only a complete release and the habit of checking. Benchmarks and guardrails will be "
     "trusted in proportion to how checkable they are.")

# ---------------------------------------------------------------- code & data
heading("Code and Data", size=12.5)
for line in [
    "<b>Audited system and artifacts:</b> github.com/jemsbhai/epistemic-edge (PyPI: epistemic-edge). Preexisting work, published at IEEE IRI 2026.",
    "<b>This audit</b> (script, full output, report source): github.com/jemsbhai/epistemic-edge-audit. Sprint-period work.",
    "<b>Dataset:</b> BATADAL (datasets 03/04), distributed by the BATADAL organizers; the released summaries, heatmap, and score series used here are in the audited repository.",
]:
    para(line, space_after=1.4)

heading("Author Contributions", size=12.5)
para("Muntaser Syed designed and executed the audit, wrote the audit script and analyses, and wrote this "
     "report. The audited system and paper are prior joint work with Marius Silaghi (Florida Institute of "
     "Technology), who is not an author of this sprint report.")

# ---------------------------------------------------------------- references
heading("References", size=12.5)
refs = [
    "[1] M. Syed and M. C. Silaghi. Epistemic Edge: Subjective Logic Guardrails for LLM-Driven IoT Actuation. Proc. IEEE 27th International Conference on Information Reuse and Integration for Data Science (IRI), 2026, pp. 37-40.",
    "[2] A. Jøsang. Subjective Logic: A Formalism for Reasoning Under Uncertainty. Springer, 2016.",
    "[3] R. Taormina et al. Battle of the Attack Detection Algorithms: Disclosing Cyber Threats on Water Distribution Systems. Journal of Water Resources Planning and Management, 144(8), 2018.",
    "[4] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger. On Calibration of Modern Neural Networks. Proc. ICML, 2017.",
    "[5] A. T. Kalai, O. Nachum, S. S. Vempala, and E. Zhang. Why Language Models Hallucinate. arXiv preprint, 2025.",
    "[6] J. Ren et al. The MASK Benchmark: Disentangling Honesty From Accuracy in AI Systems. arXiv preprint, 2025.",
]
for r in refs:
    para(r, size=10, lh=5.2, indent=0.0, space_after=1.2)

# ---------------------------------------------------------------- appendices
heading("Appendix A. Limitations and Dual-Use / Ethical Considerations", size=12.5)
para("<b>What this result does and does not establish.</b> The audit establishes that one paper's published "
     "numbers match its released record. It does not establish that the underlying system is safe to deploy, "
     "that its guardrails generalize beyond the tested scenarios, or that other systems' claims would survive "
     "the same treatment. The self-audit limitation of Section 5 applies in full.")
para("<b>Dual use.</b> Localizing a guardrail's failure mode (vacuous or absent opinions at the guardrail) "
     "could in principle help an attacker craft sensor inputs that drive a deployed system's fused opinion "
     "toward vacuity. Three considerations bound this risk: the audited system is published and fully open, so "
     "the ablation structure was already public; the audit introduces no new attack method and tests no live "
     "system; and the defensive value of verification practice, knowing precisely which component carries the "
     "safety claim, is the precondition for hardening it. On balance the audit is a defensive contribution.")
para("<b>Data and human subjects.</b> No personal data was collected or used. BATADAL is a public benchmark "
     "of water-utility telemetry released for attack-detection research; no human subjects are involved.")

heading("Appendix B. LLM Usage Statement", size=12.5)
para("An AI assistant was used, under the author's direction, to write and run the audit scripts and to "
     "assist in drafting this report. All numbers reported here were recomputed from the released artifacts "
     "by the audit script in the project repository, and every claim was checked against the script's output "
     "before inclusion. The author is responsible for all content.")

pdf.output("/home/hatch/workspace/epistemics-sprint/report/epistemics-sprint-report.pdf")
print("pages:", pdf.page_no())

