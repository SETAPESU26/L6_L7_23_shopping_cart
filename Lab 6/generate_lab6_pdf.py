import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

pdf_filename = 'Lab6_Coverage_Deliverable.pdf'
doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    leftMargin=0.5*inch,
    rightMargin=0.5*inch,
    topMargin=0.5*inch,
    bottomMargin=0.5*inch
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=colors.HexColor('#1a365d'),
    alignment=1,
    spaceAfter=6
)
subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=15,
    textColor=colors.HexColor('#2b6cb0'),
    alignment=1,
    spaceAfter=10
)
section_style = ParagraphStyle(
    'SectionHeading',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=15,
    textColor=colors.HexColor('#2c5282'),
    spaceBefore=8,
    spaceAfter=4
)
body_style = ParagraphStyle(
    'BodyTextCustom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=13,
    textColor=colors.HexColor('#2d3748'),
    spaceAfter=6
)

story = []

story.append(Paragraph('PES University — Department of Computer Science &amp; Engineering', subtitle_style))
story.append(Paragraph('LAB 6: Code and Branch Coverage Analysis — Deliverable Report', title_style))
story.append(Paragraph('<b>Course:</b> Software Engineering Lab (SELab) &nbsp;|&nbsp; <b>Topic:</b> Code &amp; Branch Coverage Analysis with Pytest &amp; Coverage.py', body_style))
story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#2b6cb0'), spaceBefore=4, spaceAfter=8))

# Objective
story.append(Paragraph('1. Objective &amp; Learning Outcomes', section_style))
story.append(Paragraph(
    'The objective of this lab is to measure, analyze, and systematically improve test coverage using Python\'s '
    '<code>coverage</code> tool and <code>pytest</code> framework. Targeted test cases were written to achieve 100% statement '
    'coverage and 100% branch coverage on the <code>shopping_cart.py</code> module, covering all decision branches and edge cases.',
    body_style
))

# Code Coverage
story.append(Paragraph('2. Code Coverage Analysis (>90% Requirement Met: 100% Achieved)', section_style))
story.append(Paragraph(
    'Test suite <code>CodeCoverageTest_shopping_cart.py</code> was designed to execute all statements across '
    '<code>item_total</code>, <code>cart_discount</code>, and <code>shipping_fee</code>. Running '
    '<code>coverage run -m pytest CodeCoverageTest_shopping_cart.py</code> and <code>coverage report -m</code> achieved 100% statement coverage:',
    body_style
))
if os.path.exists('screenshots/code_coverage_analysis.png'):
    img = RLImage('screenshots/code_coverage_analysis.png', width=7.0*inch, height=2.4*inch)
    story.append(img)
story.append(Spacer(1, 8))

# Branch Coverage
story.append(Paragraph('3. Branch Coverage Analysis (>90% Requirement Met: 100% Achieved)', section_style))
story.append(Paragraph(
    'Decision structures (including <code>if-elif-else</code> chains, compound boolean conditions like '
    '<code>coupon == \"FLAT10\" and cart_value &gt;= 1000</code>, and nested conditionals) require every branch to evaluate to both '
    '<code>True</code> and <code>False</code>. The test suite <code>BranchCoverageTest_shopping_cart.py</code> was executed with '
    '<code>coverage run --branch -m pytest BranchCoverageTest_shopping_cart.py</code>, achieving 100% branch coverage (22/22 branches):',
    body_style
))
if os.path.exists('screenshots/branch_coverage_analysis.png'):
    img = RLImage('screenshots/branch_coverage_analysis.png', width=7.0*inch, height=2.4*inch)
    story.append(img)
story.append(Spacer(1, 8))

# Summary Table
story.append(Paragraph('4. Coverage Metrics Summary Table', section_style))
table_data = [
    ['Metric', 'Target Requirement', 'Achieved Coverage', 'Missing Statements / Branches'],
    ['Line Coverage', '>= 90%', '100% (32 / 32 Statements)', '0 missing'],
    ['Branch Coverage', '>= 90%', '100% (22 / 22 Branches)', '0 missing partial branches'],
    ['Overall Total', '>= 90%', '100% Total Coverage', 'Fully Covered']
]
t = Table(table_data, colWidths=[1.8*inch, 1.8*inch, 2.0*inch, 1.4*inch])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c5282')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 8.5),
    ('BOTTOMPADDING', (0,0), (-1,0), 4),
    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f7fafc')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t)

doc.build(story)
print('PDF generated successfully:', pdf_filename)
