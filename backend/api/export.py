"""
export.py  –  ATS-Optimised Resume PDF Generator (Premium Formatting)

Features:
  • Bold + ALL CAPS section headers with underline rule
  • Prominent name (large, bold, centered)
  • Bold degrees, CGPA, roles, project titles, cert names
  • Inline keyword bolding inside bullet points
  • Proper word-wrap & pagination guard
"""

from fpdf import FPDF
import io
import re

# ══════════════════════════════════════════════════════════════════════════════
#  Keywords to bold inline inside bullet points
# ══════════════════════════════════════════════════════════════════════════════

INLINE_BOLD_KEYWORDS = {
    # Languages
    "python", "sql", "c++", "java", "javascript", "r", "typescript", "go",
    # ML / DL
    "scikit-learn", "tensorflow", "pytorch", "keras", "xgboost", "nltk",
    "spacy", "huggingface", "mlflow", "numpy", "pandas", "matplotlib",
    "seaborn", "scipy",
    # Tools / Infra
    "fastapi", "streamlit", "flask", "django", "docker", "kubernetes",
    "git", "github", "aws", "azure", "gcp", "power bi", "tableau",
    "mysql", "sqlite", "postgresql", "mongodb",
    # Concepts
    "natural language processing", "nlp", "machine learning", "deep learning",
    "computer vision", "ats", "ocr", "api", "rest api",
}


# ══════════════════════════════════════════════════════════════════════════════
#  Text helpers
# ══════════════════════════════════════════════════════════════════════════════

def sanitize(text: str) -> str:
    """latin-1 safe, preserves all spaces, replaces common Unicode chars."""
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        "\u2013": "-", "\u2014": "-", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"', "\u2022": "-", "\u2026": "...",
        "\u00a0": " ", "\u2010": "-", "\u2012": "-", "\u2015": "-",
        "\u00b7": "-", "\u25cf": "-", "\u25aa": "-", "\u2019": "'",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text.encode("latin-1", errors="ignore").decode("latin-1")


def _fix_spacing(text: str) -> str:
    """Insert missing spaces between concatenated words (CamelCase run-ons)."""
    if not text:
        return ""
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)
    text = re.sub(r"(?<=[a-zA-Z])(?=\d)", " ", text)
    text = re.sub(r"  +", " ", text)
    return text.strip()


def _bold_keywords_in_text(text: str) -> str:
    """
    Wrap ATS keywords in ** for markdown bolding.
    Matches multi-word keywords first, then single-word keywords.
    """
    if not text:
        return ""
    sorted_kws = sorted(INLINE_BOLD_KEYWORDS, key=lambda k: -len(k))
    patterns = []
    for kw in sorted_kws:
        escaped = re.escape(kw)
        start = r"\b" if re.match(r"^\w", kw) else r"(?<!\w)"
        end = r"\b" if re.search(r"\w$", kw) else r"(?!\w)"
        patterns.append(f"{start}{escaped}{end}")
    pattern = "|".join(patterns)
    regex = re.compile(f"({pattern})", re.IGNORECASE)
    return regex.sub(r"**\1**", text)


def _format_cert_or_achievement(text: str) -> str:
    """Bold certifications & achievements sections separated by | or -"""
    if not text:
        return ""
    if "|" in text:
        parts = text.split("|")
        return " | ".join(f"**{p.strip()}**" for p in parts)
    elif " - " in text:
        parts = text.split(" - ")
        return " - ".join(f"**{p.strip()}**" for p in parts)
    elif " -- " in text:
        parts = text.split(" -- ")
        return " -- ".join(f"**{p.strip()}**" for p in parts)
    return f"**{text.strip()}**"


# ══════════════════════════════════════════════════════════════════════════════
#  LaTeX helper (unchanged)
# ══════════════════════════════════════════════════════════════════════════════

def escape_latex(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    conv = {
        "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
        "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}", "<": r"\textless{}", ">": r"\textgreater{}",
    }
    regex = re.compile("|".join(re.escape(k) for k in sorted(conv, key=lambda x: -len(x))))
    return regex.sub(lambda m: conv[m.group()], text)


# ══════════════════════════════════════════════════════════════════════════════
#  ResumePDF class
# ══════════════════════════════════════════════════════════════════════════════

class ResumePDF(FPDF):
    # A4 geometry
    L_MARGIN = 15
    R_MARGIN = 15
    T_MARGIN = 16
    USABLE_W = 210 - 15 - 15   # 180 mm

    # Font sizes
    FS_NAME    = 20
    FS_CONTACT = 9
    FS_SECTION = 10.5
    FS_ENTRY   = 10
    FS_SUB     = 9
    FS_BODY    = 9.5
    FS_BULLET  = 9.5

    LH = 5.0   # standard line height (mm)
    BH = 4.8   # bullet line height

    C_BLACK = (0,   0,   0)
    C_GRAY  = (80,  80,  80)
    C_LGRAY = (120, 120, 120)

    def setup(self):
        self.set_margins(self.L_MARGIN, self.T_MARGIN, self.R_MARGIN)
        self.set_auto_page_break(auto=True, margin=12)
        self.add_page()

    # ── low-level helpers ────────────────────────────────────────────────────

    def _font(self, style="", size=10, color=None):
        self.set_font("Helvetica", style, size)
        self.set_text_color(*(color or self.C_BLACK))

    def _goto_lmargin(self):
        self.set_x(self.L_MARGIN)

    # ── Name ────────────────────────────────────────────────────────────────

    def write_name(self, text: str):
        """Large, bold, centered candidate name."""
        self._font("B", self.FS_NAME)
        self._goto_lmargin()
        self.cell(self.USABLE_W, 9, sanitize(text.upper()), align="C",
                  new_x="LMARGIN", new_y="NEXT")

    # ── Contact line ────────────────────────────────────────────────────────

    def write_contact(self, parts: list):
        """Single, deduplicated contact line."""
        seen, unique = set(), []
        for p in parts:
            p = p.strip()
            if p and p.lower() not in seen:
                seen.add(p.lower())
                unique.append(p)
        self._font("", self.FS_CONTACT, self.C_GRAY)
        self._goto_lmargin()
        self.multi_cell(self.USABLE_W, 4.5, sanitize("  |  ".join(unique)), align="C")

    # ── Section header ───────────────────────────────────────────────────────

    def write_section(self, title: str):
        """Bold ALL-CAPS section heading + full-width underline rule."""
        self.ln(3)
        self._font("B", self.FS_SECTION)
        self._goto_lmargin()
        self.cell(self.USABLE_W, 6, sanitize(title.upper()),
                  new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.C_BLACK)
        self.set_line_width(0.35)
        y = self.get_y()
        self.line(self.L_MARGIN, y, self.L_MARGIN + self.USABLE_W, y)
        self.ln(2)

    # ── Entry title row (bold left | gray right) ─────────────────────────────

    def write_entry_title(self, left: str, right: str = ""):
        """Bold role/project title on the left, italic date on the right."""
        self._font("B", self.FS_ENTRY)
        self._goto_lmargin()
        lw = self.USABLE_W * 0.72
        rw = self.USABLE_W * 0.28
        self.cell(lw, self.LH, sanitize(left))
        self._font("I", self.FS_SUB, self.C_GRAY)
        self.cell(rw, self.LH, sanitize(right), align="R",
                  new_x="LMARGIN", new_y="NEXT")

    # ── Subtitle (institution / location / gpa) ──────────────────────────────

    def write_subtitle(self, text: str):
        self._font("I", self.FS_SUB, self.C_GRAY)
        self._goto_lmargin()
        self.multi_cell(self.USABLE_W, 4.5, sanitize(text), markdown=True)

    # ── Body paragraph ───────────────────────────────────────────────────────

    def write_body(self, text: str):
        text = text.replace("**", "")
        text = _fix_spacing(text)
        self._font("", self.FS_BODY)
        self._goto_lmargin()
        self.multi_cell(self.USABLE_W, self.LH, sanitize(text), markdown=True)

    # ── Skills row (bold category : items) ──────────────────────────────────

    def write_skills_row(self, label: str, items: list):
        """Bold category label then regular comma-separated items on the same line."""
        label_str = sanitize(label + ": ")
        items_str = sanitize(", ".join(str(i) for i in items))

        self._font("B", self.FS_BODY)
        label_w = min(self.get_string_width(label_str) + 1.5,
                      self.USABLE_W * 0.46)
        items_w = self.USABLE_W - label_w

        self._goto_lmargin()
        self.cell(label_w, self.LH, label_str)
        self._font("", self.FS_BODY)
        self.multi_cell(items_w, self.LH, items_str)

    # ── Bullet with inline keyword bolding ──────────────────────────────────

    def write_bullet(self, text: str):
        """
        Bullet point with inline bold for ATS keywords.
        Uses FPDF2's native markdown support and temporary left margins for perfect word-wrap.
        """
        text = text.replace("**", "")
        text = _fix_spacing(text)
        
        indent = 5    # mm from left margin to bullet symbol
        sym    = "- "

        self._font("", self.FS_BULLET)
        sym_w  = self.get_string_width(sym)

        # Set left margin temporarily to align wrapped lines
        old_margin = self.l_margin
        new_margin = old_margin + indent + sym_w
        self.set_left_margin(new_margin)

        # Print bullet symbol
        self.set_x(old_margin + indent)
        self.cell(sym_w, self.BH, sanitize(sym))

        # Write text with markdown enabled
        self.multi_cell(self.USABLE_W - indent - sym_w, self.BH, sanitize(text), markdown=True)

        # Restore left margin
        self.set_left_margin(old_margin)

    # ── Plain bullet (no keyword bolding) ───────────────────────────────────

    def write_plain_bullet(self, text: str):
        text   = _fix_spacing(text)
        indent = 5
        sym    = "- "
        self._font("", self.FS_BULLET)
        sym_w  = self.get_string_width(sym)

        # Set left margin temporarily to align wrapped lines
        old_margin = self.l_margin
        new_margin = old_margin + indent + sym_w
        self.set_left_margin(new_margin)

        # Print bullet symbol
        self.set_x(old_margin + indent)
        self.cell(sym_w, self.BH, sanitize(sym))

        # Write text
        self.multi_cell(self.USABLE_W - indent - sym_w, self.BH, sanitize(text), markdown=True)

        # Restore left margin
        self.set_left_margin(old_margin)

    # ── Pagination guard ─────────────────────────────────────────────────────

    def ensure_space(self, needed_mm: float = 28):
        if self.get_y() + needed_mm > (297 - 14):
            self.add_page()


# ══════════════════════════════════════════════════════════════════════════════
#  Public PDF API
# ══════════════════════════════════════════════════════════════════════════════

def export_resume_pdf(resume_data: dict, **kwargs) -> bytes:
    """
    Generate a fully formatted, ATS-ready PDF from a structured resume dict.
    """
    if not isinstance(resume_data, dict):
        raise ValueError("resume_data must be a dict from enhance_resume()")

    pdf = ResumePDF()
    pdf.setup()

    # ── NAME / HEADER ────────────────────────────────────────────────────────
    name = _fix_spacing(resume_data.get("name", "Candidate").strip())
    
    # If the name contains JAGDAMB, print JAGDAMB as small unbolded invocation,
    # and override name to Yash Jagtap if it becomes empty or is JAGDAMB.
    if "JAGDAMB" in name.upper():
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*(80, 80, 80)) # Gray
        pdf.cell(pdf.USABLE_W, 4, "JAGDAMB", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        clean_name = name.replace("JAGDAMB", "").strip()
        name = clean_name if clean_name else "Yash Jagtap"
        
    pdf.write_name(name)

    # ── CONTACT ──────────────────────────────────────────────────────────────
    fields = ["email", "phone", "linkedin", "github", "location"]
    parts  = [resume_data.get(f, "").strip() for f in fields]
    parts  = [p for p in parts if p]
    if parts:
        pdf.write_contact(parts)

    pdf.ln(3)

    # ── PROFESSIONAL SUMMARY ─────────────────────────────────────────────────
    summary = _fix_spacing(resume_data.get("summary", "").strip())
    if summary:
        pdf.write_section("Professional Summary")
        pdf.write_body(summary)
        pdf.ln(1)

    # ── EDUCATION ────────────────────────────────────────────────────────────
    education = resume_data.get("education", [])
    if education:
        pdf.write_section("Education")
        for edu in education:
            degree   = _fix_spacing(edu.get("degree", "").strip())
            inst     = _fix_spacing(edu.get("institution", "").strip())
            dates    = edu.get("dates", "").strip()
            gpa      = edu.get("gpa", "").strip()
            location = edu.get("location", "").strip()

            # Bold degree name on left, dates on right
            pdf.write_entry_title(degree, dates)

            sub_parts = []
            if inst:     sub_parts.append(inst)
            if location: sub_parts.append(location)
            if gpa:
                # Bold CGPA to draw immediate attention
                if "cgpa" in gpa.lower() or "score" in gpa.lower() or "gpa" in gpa.lower() or "%" in gpa or "percent" in gpa.lower():
                    sub_parts.append(f"**{gpa}**")
                else:
                    sub_parts.append(f"**CGPA: {gpa}**")
            if sub_parts:
                pdf.write_subtitle("  |  ".join(sub_parts))
            pdf.ln(1.5)

    # ── TECHNICAL SKILLS ─────────────────────────────────────────────────────
    skills = resume_data.get("skills", {})
    if skills:
        pdf.write_section("Technical Skills")
        for category, items in skills.items():
            if items:
                pdf.write_skills_row(category, [str(i) for i in items])
        pdf.ln(1)

    # ── EXPERIENCE & INTERNSHIPS ─────────────────────────────────────────────
    experience = resume_data.get("experience", [])
    if experience:
        pdf.write_section("Experience & Internships")
        for exp in experience:
            pdf.ensure_space(22)
            title   = _fix_spacing(exp.get("title", "").strip())
            company = _fix_spacing(exp.get("company", "").strip())
            loc     = exp.get("location", "").strip()
            dates   = exp.get("dates", "").strip()
            bullets = exp.get("bullets", [])

            # Bold: "Role Title  –  Company"
            left  = f"{title}  -  {company}" if company else title
            right = f"{loc}  |  {dates}" if loc and dates else (loc or dates)
            pdf.write_entry_title(left, right)

            for b in bullets:
                b = b.strip()
                if b:
                    pdf.write_bullet(b)
            pdf.ln(1.5)

    # ── PROJECTS ─────────────────────────────────────────────────────────────
    projects = resume_data.get("projects", [])
    if projects:
        pdf.write_section("Projects")
        for proj in projects:
            pdf.ensure_space(24)
            p_name  = _fix_spacing(proj.get("name", "").strip())
            tech    = proj.get("technologies", "").strip()
            dates   = proj.get("dates", "").strip()
            link    = proj.get("link", "").strip()
            bullets = proj.get("bullets", [])

            # Bold project name on left
            pdf.write_entry_title(p_name, dates)

            sub_parts = []
            if tech: sub_parts.append(f"Tech: {tech}")
            if link: sub_parts.append(link)
            if sub_parts:
                pdf.write_subtitle("  |  ".join(sub_parts))

            for b in bullets:
                b = b.strip()
                if b:
                    pdf.write_bullet(b)
            pdf.ln(1.5)

    # ── ACHIEVEMENTS & CERTIFICATIONS ────────────────────────────────────────
    certs = resume_data.get("certifications", [])
    achievements = resume_data.get("achievements", [])
    if certs or achievements:
        pdf.write_section("Achievements & Certifications")
        
        # Certifications first
        for cert in certs:
            cert = str(cert).strip()
            if cert:
                formatted_cert = _format_cert_or_achievement(cert)
                pdf.write_plain_bullet(formatted_cert)
                
        # Achievements next
        for ach in achievements:
            ach = str(ach).strip()
            if ach:
                formatted_ach = _format_cert_or_achievement(ach)
                pdf.write_plain_bullet(formatted_ach)
        pdf.ln(1)

    # ── OUTPUT ───────────────────────────────────────────────────────────────
    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf.read()


# ══════════════════════════════════════════════════════════════════════════════
#  LaTeX Generator  (Jake's Resume Overleaf template)
# ══════════════════════════════════════════════════════════════════════════════

_LATEX_PREAMBLE = r"""\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{multicol}
\input{glyphtounicode}

\usepackage[sfdefault]{FiraSans}
\usepackage[T1]{fontenc}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

\pdfgentounicode=1

\newcommand{\resumeItem}[1]{\item\small{{#1 \vspace{-2pt}}}}
\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}
\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\begin{document}
"""

_LATEX_FOOTER = r"""
\end{document}
"""


def _latex_bullets(bullets: list) -> str:
    if not bullets:
        return ""
    lines = ["    \\resumeItemListStart"]
    for b in bullets:
        if b.strip():
            lines.append(f"      \\resumeItem{{{escape_latex(b.strip())}}}")
    lines.append("    \\resumeItemListEnd")
    return "\n".join(lines)


def generate_resume_latex(resume_data: dict, **kwargs) -> str:
    if not isinstance(resume_data, dict):
        return "% Error: invalid resume data."

    lines = [_LATEX_PREAMBLE]

    name     = escape_latex(resume_data.get("name", "Your Name"))
    email    = resume_data.get("email", "")
    phone    = resume_data.get("phone", "")
    linkedin = resume_data.get("linkedin", "")
    github   = resume_data.get("github", "")
    location = resume_data.get("location", "")

    contact_items = []
    if phone:    contact_items.append(escape_latex(phone))
    if email:    contact_items.append(f"\\href{{mailto:{escape_latex(email)}}}{{{escape_latex(email)}}}")
    if linkedin:
        url = linkedin if linkedin.startswith("http") else f"https://{linkedin}"
        contact_items.append(f"\\href{{{escape_latex(url)}}}{{{escape_latex(linkedin.replace('https://','').replace('http://',''))}}}")
    if github:
        url = github if github.startswith("http") else f"https://{github}"
        contact_items.append(f"\\href{{{escape_latex(url)}}}{{{escape_latex(github.replace('https://','').replace('http://',''))}}}")
    if location: contact_items.append(escape_latex(location))

    lines += [
        r"\begin{center}",
        f"    \\textbf{{\\Huge \\scshape {name}}} \\\\ \\vspace{{1pt}}",
        f"    \\small {' $|$ '.join(contact_items)}",
        r"\end{center}", ""
    ]

    summary = resume_data.get("summary", "").strip()
    if summary:
        lines += [r"\section{Professional Summary}", r"\begin{itemize}[leftmargin=0.15in, label={}]",
                  r"    \small{\item{", f"     {escape_latex(summary)}", r"    }}", r"\end{itemize}", ""]

    education = resume_data.get("education", [])
    if education:
        lines += [r"\section{Education}", r"  \resumeSubHeadingListStart"]
        for edu in education:
            d = escape_latex(edu.get("degree", ""))
            i = escape_latex(edu.get("institution", ""))
            dt = escape_latex(edu.get("dates", ""))
            g = escape_latex(edu.get("gpa", ""))
            l = escape_latex(edu.get("location", ""))
            sub = f"{l} -- {g}" if l and g else (l or g)
            lines += [f"    \\resumeSubheading", f"      {{{d}}}{{{dt}}}", f"      {{{i}}}{{{sub}}}"]
        lines += [r"  \resumeSubHeadingListEnd", ""]

    skills = resume_data.get("skills", {})
    if skills:
        lines += [r"\section{Technical Skills}", r" \begin{itemize}[leftmargin=0.15in, label={}]", r"    \small{\item{"]
        rows = []
        for cat, items in skills.items():
            if items:
                rows.append(f"     \\textbf{{{escape_latex(cat)}}}{{: {escape_latex(', '.join(items))}}}")
        lines.append(" \\\\\n".join(rows))
        lines += [r"    }}", r" \end{itemize}", ""]

    experience = resume_data.get("experience", [])
    if experience:
        lines += [r"\section{Experience \& Internships}", r"  \resumeSubHeadingListStart"]
        for exp in experience:
            lines += [f"    \\resumeSubheading",
                      f"      {{{escape_latex(exp.get('title',''))}}}{{{escape_latex(exp.get('dates',''))}}}",
                      f"      {{{escape_latex(exp.get('company',''))}}}{{{escape_latex(exp.get('location',''))}}}",
                      _latex_bullets(exp.get("bullets", []))]
        lines += [r"  \resumeSubHeadingListEnd", ""]

    projects = resume_data.get("projects", [])
    if projects:
        lines += [r"\section{Projects}", r"    \resumeSubHeadingListStart"]
        for proj in projects:
            p_name = proj.get("name", "")
            tech   = proj.get("technologies", "")
            dates  = escape_latex(proj.get("dates", ""))
            link   = proj.get("link", "")
            label  = f"\\textbf{{\\href{{{escape_latex(link)}}}{{{escape_latex(p_name)}}}}}" if link else f"\\textbf{{{escape_latex(p_name)}}}"
            if tech: label += f" $|$ \\emph{{{escape_latex(tech)}}}"
            lines += [f"      \\resumeProjectHeading", f"          {{{label}}}{{{dates}}}", _latex_bullets(proj.get("bullets", []))]
        lines += [r"    \resumeSubHeadingListEnd", ""]

    certs = resume_data.get("certifications", [])
    achievements = resume_data.get("achievements", [])
    if certs or achievements:
        lines += [r"\section{Achievements \& Certifications}", r" \begin{itemize}[leftmargin=0.15in, label={}]", r"    \small{\item{"]
        for item in certs + achievements:
            lines.append(f"     \\textbullet\\ {escape_latex(str(item))} \\\\")
        lines += [r"    }}", r" \end{itemize}"]

    lines.append(_LATEX_FOOTER)
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
#  Roadmap PDF stub
# ══════════════════════════════════════════════════════════════════════════════

def export_roadmap_pdf(job_role, roadmap_dict, username="Student"):
    """
    Generate a formatted, print-ready PDF for the academic blueprint roadmap.
    """
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(180, 10, sanitize(f"EduAI Academic Roadmap for {username}"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Subtitle
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(180, 8, sanitize(f"Field of Study: {job_role}"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Content
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.3)
    for year, data in roadmap_dict.items():
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(180, 6, sanitize(year), new_x="LMARGIN", new_y="NEXT")
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(2)
        
        if isinstance(data, dict):
            # Write summary
            summary = data.get("summary", "")
            if summary:
                pdf.set_font("Helvetica", "I", 10)
                pdf.multi_cell(180, 5, sanitize(summary))
                pdf.ln(2)
            
            # Write topics/steps
            topics = data.get("topics", [])
            if topics:
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(180, 5, sanitize("Core Topics & Steps:"), new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("Helvetica", "", 10)
                for topic in topics:
                    pdf.multi_cell(180, 5, sanitize(f"- {topic}"))
        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(180, 5, sanitize(str(data)))
            
        pdf.ln(5)
        
    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf.read()
