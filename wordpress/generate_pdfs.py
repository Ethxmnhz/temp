#!/usr/bin/env python3
"""
HexaDynamics Pvt Ltd — Corporate Document Generator
Generates realistic internal PDFs for the vuln lab environment.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white, gray
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os
import sys

BRAND_DARK = HexColor("#0f172a")
BRAND_ACCENT = HexColor("#3b82f6")
BRAND_LIGHT = HexColor("#e2e8f0")
BRAND_RED = HexColor("#ef4444")

styles = getSampleStyleSheet()

title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontSize=26, textColor=BRAND_DARK, spaceAfter=20, alignment=TA_CENTER)
subtitle_style = ParagraphStyle('CustomSubtitle', parent=styles['Normal'], fontSize=14, textColor=BRAND_ACCENT, spaceAfter=30, alignment=TA_CENTER)
heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading1'], fontSize=16, textColor=BRAND_DARK, spaceBefore=20, spaceAfter=10)
subheading_style = ParagraphStyle('CustomSubHeading', parent=styles['Heading2'], fontSize=13, textColor=BRAND_ACCENT, spaceBefore=14, spaceAfter=8)
body_style = ParagraphStyle('CustomBody', parent=styles['Normal'], fontSize=10, leading=14, textColor=black, alignment=TA_JUSTIFY, spaceAfter=8)
confidential_style = ParagraphStyle('Confidential', parent=styles['Normal'], fontSize=9, textColor=BRAND_RED, alignment=TA_CENTER, spaceBefore=40, spaceAfter=10)
footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=gray, alignment=TA_CENTER)


def make_cover(story, title, subtitle, classification="INTERNAL — CONFIDENTIAL"):
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(subtitle, subtitle_style))
    story.append(Spacer(1, 0.5 * inch))
    story.append(HRFlowable(width="60%", thickness=2, color=BRAND_ACCENT))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("HexaDynamics Pvt Ltd", ParagraphStyle('Company', parent=styles['Normal'], fontSize=12, textColor=BRAND_DARK, alignment=TA_CENTER)))
    story.append(Paragraph("www.hexadynamics.local", footer_style))
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph(f"Classification: {classification}", confidential_style))
    story.append(Paragraph("© 2026 HexaDynamics Pvt Ltd. All rights reserved.", footer_style))
    story.append(PageBreak())


# ============================================================
# 1. Employee Handbook
# ============================================================
def generate_employee_handbook(path):
    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
    story = []
    make_cover(story, "Employee Handbook", "Human Resources Department — FY 2025-2026")

    story.append(Paragraph("1. Welcome to HexaDynamics", heading_style))
    story.append(Paragraph(
        "Welcome to HexaDynamics Pvt Ltd. We are a leading provider of AI-driven enterprise security solutions "
        "headquartered in Bengaluru, India with satellite offices in Hyderabad, Pune, and Singapore. "
        "This handbook outlines our policies, expectations, and the benefits available to all full-time employees.", body_style))

    story.append(Paragraph("2. Company Overview", heading_style))
    story.append(Paragraph(
        "Founded in 2019, HexaDynamics has grown to over 340 employees across four offices. Our core products "
        "include HexaShield (endpoint protection), HexaScan (vulnerability assessment platform), and HexaSOC "
        "(managed SOC-as-a-Service). We serve clients in BFSI, healthcare, and government sectors.", body_style))

    story.append(Paragraph("3. Working Hours & Leave Policy", heading_style))
    story.append(Paragraph(
        "Standard working hours are 9:30 AM to 6:30 PM IST, Monday through Friday. All employees are entitled to "
        "24 days of paid leave, 12 days of casual leave, and 10 public holidays per year. Work-from-home is permitted "
        "up to 2 days per week with manager approval.", body_style))

    story.append(Paragraph("4. IT & Acceptable Use Policy", heading_style))
    story.append(Paragraph(
        "All employees must use company-issued devices for work. Personal devices may not connect to the corporate "
        "network without IT approval. The internal marketing portal is accessible at http://intranet.hexadynamics.local. "
        "VPN credentials are issued by the IT helpdesk upon onboarding.", body_style))
    story.append(Paragraph(
        "Employees must not share credentials, install unauthorized software, or attempt to access systems beyond "
        "their role-based permissions. Violations will be handled per the Incident Response Policy (see Section 8).", body_style))

    story.append(Paragraph("5. Information Security Responsibilities", heading_style))
    story.append(Paragraph(
        "All employees are responsible for safeguarding company data. Passwords must be at least 12 characters, "
        "include uppercase, lowercase, numbers, and symbols. Password rotation is enforced every 90 days. "
        "Multi-factor authentication is mandatory for all cloud services and VPN access.", body_style))

    story.append(Paragraph("6. Departments", heading_style))
    dept_data = [
        ["Department", "Head", "Headcount"],
        ["Engineering", "Arjun Mehta", "142"],
        ["Marketing", "Priya Sharma", "28"],
        ["DevOps", "Vikram Singh", "35"],
        ["Human Resources", "Neha Gupta", "18"],
        ["Finance", "Rajesh Kumar", "22"],
        ["Security Operations", "Ananya Rao", "45"],
        ["Sales & BD", "Karthik Nair", "50"],
    ]
    t = Table(dept_data, colWidths=[200, 150, 80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BRAND_LIGHT]),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    story.append(Paragraph("7. Code of Conduct", heading_style))
    story.append(Paragraph(
        "HexaDynamics maintains a zero-tolerance policy toward harassment, discrimination, and unethical behavior. "
        "All employees must complete annual compliance training. Ethical concerns can be reported anonymously via "
        "the internal whistleblower portal at https://ethics.hexadynamics.local.", body_style))

    story.append(Paragraph("8. Incident Response", heading_style))
    story.append(Paragraph(
        "Security incidents must be reported to security@hexadynamics.local within 1 hour of discovery. "
        "The SOC team will triage, investigate, and coordinate response. Critical incidents trigger the "
        "Incident Commander protocol with mandatory C-suite notification within 4 hours.", body_style))

    doc.build(story)


# ============================================================
# 2. Network Architecture Document
# ============================================================
def generate_network_architecture(path):
    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
    story = []
    make_cover(story, "Network Architecture", "Infrastructure & DevOps Team — Q4 2025", "STRICTLY CONFIDENTIAL")

    story.append(Paragraph("1. Network Overview", heading_style))
    story.append(Paragraph(
        "HexaDynamics operates a hybrid infrastructure spanning on-premise data centers in Bengaluru and AWS "
        "ap-south-1 region. The network is segmented into the following zones: DMZ, Corporate LAN, Development, "
        "Staging, Production, and Management.", body_style))

    story.append(Paragraph("2. Network Segments", heading_style))
    net_data = [
        ["Segment", "VLAN", "Subnet", "Purpose"],
        ["DMZ", "VLAN 10", "10.10.10.0/24", "Public-facing web servers"],
        ["Corporate LAN", "VLAN 20", "10.10.20.0/24", "Employee workstations"],
        ["Development", "VLAN 30", "10.10.30.0/24", "Dev/test environments"],
        ["Staging", "VLAN 40", "10.10.40.0/24", "Pre-production testing"],
        ["Production", "VLAN 50", "10.10.50.0/24", "Live application servers"],
        ["Management", "VLAN 99", "10.10.99.0/24", "Infrastructure management"],
        ["Database", "VLAN 60", "10.10.60.0/24", "MySQL, PostgreSQL, Redis"],
    ]
    t = Table(net_data, colWidths=[90, 70, 120, 170])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BRAND_LIGHT]),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    story.append(Paragraph("3. Key Servers", heading_style))
    servers = [
        ["Hostname", "IP Address", "OS", "Role"],
        ["hx-web-01", "10.10.10.5", "Ubuntu 22.04", "Corporate website (Apache)"],
        ["hx-wp-01", "10.10.10.8", "Ubuntu 22.04", "WordPress intranet portal"],
        ["hx-db-01", "10.10.60.10", "Ubuntu 20.04", "MySQL 5.7 (WordPress DB)"],
        ["hx-db-02", "10.10.60.11", "Ubuntu 20.04", "PostgreSQL 14 (HexaScan)"],
        ["hx-gitlab-01", "10.10.30.5", "Ubuntu 22.04", "GitLab CE (internal repos)"],
        ["hx-jenkins-01", "10.10.30.10", "Ubuntu 22.04", "Jenkins CI/CD"],
        ["hx-soc-01", "10.10.99.5", "Ubuntu 22.04", "Wazuh SIEM"],
        ["hx-vpn-01", "10.10.10.2", "pfSense", "OpenVPN gateway"],
        ["hx-mail-01", "10.10.20.15", "Ubuntu 22.04", "Postfix mail server"],
    ]
    t2 = Table(servers, colWidths=[90, 90, 90, 190])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BRAND_LIGHT]),
    ]))
    story.append(t2)
    story.append(Spacer(1, 15))

    story.append(Paragraph("4. Firewall Rules Summary", heading_style))
    story.append(Paragraph(
        "The perimeter firewall (pfSense) enforces strict ingress filtering. Only ports 80, 443, and 22 are "
        "exposed externally. Inter-VLAN routing is controlled via ACLs on the core switch (Cisco Catalyst 9300). "
        "Database servers are restricted to connections from application servers only.", body_style))

    story.append(Paragraph("5. Known Issues & Technical Debt", heading_style))
    story.append(Paragraph(
        "• hx-wp-01: WordPress intranet still running legacy plugins. Scheduled for audit in Q1 2026.<br/>"
        "• SSH access uses password authentication on some servers. Migration to key-based auth is 70% complete.<br/>"
        "• The .git directory on the web server may be publicly accessible. DevOps to verify and remediate.<br/>"
        "• Database backups are stored unencrypted on hx-db-01:/backups. Encryption rollout planned for March 2026.<br/>"
        "• Python3 has elevated capabilities on hx-wp-01 for legacy automation scripts. Review pending.",
        body_style))

    story.append(Paragraph("6. Contact", heading_style))
    story.append(Paragraph(
        "For infrastructure queries, contact: devops@hexadynamics.local<br/>"
        "Emergency escalation: Vikram Singh (DevOps Lead) — +91-98765-43210",
        body_style))

    doc.build(story)


# ============================================================
# 3. IT Security Policy
# ============================================================
def generate_security_policy(path):
    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
    story = []
    make_cover(story, "Information Security Policy", "Security Operations Center — Version 3.2")

    story.append(Paragraph("1. Purpose", heading_style))
    story.append(Paragraph(
        "This document establishes the information security policies for HexaDynamics Pvt Ltd. It applies to "
        "all employees, contractors, and third-party vendors with access to company systems and data.", body_style))

    story.append(Paragraph("2. Password Policy", heading_style))
    story.append(Paragraph(
        "• Minimum 12 characters with complexity requirements (upper, lower, digit, special)<br/>"
        "• Passwords must be rotated every 90 days<br/>"
        "• No password reuse for the last 12 passwords<br/>"
        "• Service accounts must use randomly generated 24-character passwords<br/>"
        "• Default credentials must be changed immediately upon deployment<br/>"
        "• <b>Note:</b> The marketing portal (WordPress) currently uses a shared admin account for content "
        "publishing. Migration to individual accounts is scheduled for Q2 2026.",
        body_style))

    story.append(Paragraph("3. Access Control", heading_style))
    story.append(Paragraph(
        "Access is granted on a least-privilege basis. Role-based access control (RBAC) is enforced across "
        "all systems. Privileged access requires approval from the department head and InfoSec team. "
        "All privileged sessions are logged and monitored via the SIEM.", body_style))

    story.append(Paragraph("4. Vulnerability Management", heading_style))
    story.append(Paragraph(
        "Monthly vulnerability scans are conducted using HexaScan. Critical vulnerabilities must be patched "
        "within 7 days. High-severity within 30 days. Medium within 90 days. Exception requests require "
        "CISO approval with a documented risk acceptance.", body_style))

    story.append(Paragraph("5. Incident Classification", heading_style))
    incident_data = [
        ["Severity", "Response Time", "Example"],
        ["P1 — Critical", "15 minutes", "Active data breach, ransomware"],
        ["P2 — High", "1 hour", "Unauthorized access, malware outbreak"],
        ["P3 — Medium", "4 hours", "Phishing campaign, suspicious login"],
        ["P4 — Low", "24 hours", "Policy violation, minor misconfiguration"],
    ]
    t = Table(incident_data, colWidths=[100, 100, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BRAND_LIGHT]),
    ]))
    story.append(t)

    story.append(Paragraph("6. Data Classification", heading_style))
    story.append(Paragraph(
        "• <b>Public:</b> Marketing materials, press releases<br/>"
        "• <b>Internal:</b> Employee communications, project updates<br/>"
        "• <b>Confidential:</b> Client data, financial reports, source code<br/>"
        "• <b>Restricted:</b> Credentials, encryption keys, PII, medical records",
        body_style))

    story.append(Paragraph("7. Approved Tools & Software", heading_style))
    story.append(Paragraph(
        "Only software from the approved catalog may be installed. The approved list includes: VS Code, "
        "Docker, Git, Postman, Slack, Zoom, LibreOffice. Browser extensions require IT approval. "
        "WordPress plugins must be reviewed by the security team before installation.", body_style))

    doc.build(story)


# ============================================================
# 4. Project Status Report
# ============================================================
def generate_project_report(path):
    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
    story = []
    make_cover(story, "Project Status Report", "Q4 2025 — Engineering & Product", "INTERNAL")

    story.append(Paragraph("1. Executive Summary", heading_style))
    story.append(Paragraph(
        "Q4 2025 was a strong quarter for HexaDynamics. We shipped HexaShield v4.2 with ML-based threat "
        "detection, onboarded 12 new enterprise clients, and completed SOC 2 Type II certification. "
        "Revenue grew 23% QoQ. Key challenges included delayed infrastructure migration and a staffing "
        "gap in the DevOps team.", body_style))

    story.append(Paragraph("2. Product Updates", heading_style))
    products = [
        ["Product", "Version", "Status", "Notes"],
        ["HexaShield", "4.2.1", "Released", "ML threat engine, 40% fewer false positives"],
        ["HexaScan", "3.1.0", "In QA", "Added WordPress plugin scanning module"],
        ["HexaSOC", "2.5.0", "Released", "Wazuh integration, custom dashboards"],
        ["Intranet Portal", "1.3.0", "Live", "WordPress 6.4 — migration from 5.x complete"],
        ["HexaVPN", "1.0.2", "Beta", "WireGuard-based, replacing OpenVPN"],
    ]
    t = Table(products, colWidths=[90, 60, 70, 230])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BRAND_LIGHT]),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    story.append(Paragraph("3. Infrastructure Migration", heading_style))
    story.append(Paragraph(
        "The migration from on-premise to AWS hybrid is 65% complete. Key milestones:<br/>"
        "• Corporate website migrated to EC2 (completed Oct 2025)<br/>"
        "• WordPress intranet containerized with Docker (completed Nov 2025)<br/>"
        "• Database migration to RDS (scheduled Q1 2026)<br/>"
        "• Legacy automation scripts still require Python3 with elevated permissions on web server<br/>"
        "• Git repository cleanup pending — some servers still expose .git directories",
        body_style))

    story.append(Paragraph("4. Security Audit Findings", heading_style))
    story.append(Paragraph(
        "The Q4 internal security audit identified the following issues:", body_style))
    audit = [
        ["Finding", "Severity", "Status"],
        ["Exposed .git directory on web server", "High", "Remediation Pending"],
        ["WordPress admin using shared credentials", "High", "Scheduled Q2 2026"],
        ["Outdated WP plugins (File Manager)", "Critical", "Under Review"],
        ["SSH password auth on 3 servers", "Medium", "70% migrated to keys"],
        ["Python3 capabilities misconfiguration", "High", "Legacy dependency — TBD"],
        ["Unencrypted DB backups", "Medium", "Encryption planned Mar 2026"],
    ]
    t2 = Table(audit, colWidths=[220, 80, 150])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BRAND_LIGHT]),
    ]))
    story.append(t2)

    story.append(Paragraph("5. Upcoming Q1 2026 Goals", heading_style))
    story.append(Paragraph(
        "• Complete AWS RDS migration for all databases<br/>"
        "• Remediate all Critical and High findings from Q4 audit<br/>"
        "• Launch HexaScan 3.1 with WordPress scanning module<br/>"
        "• Hire 5 additional DevOps engineers<br/>"
        "• Deploy HexaVPN company-wide<br/>"
        "• Migrate WordPress admin to individual SSO-based accounts",
        body_style))

    doc.build(story)


# ============================================================
# 5. Employee Directory (Internal)
# ============================================================
def generate_employee_directory(path):
    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
    story = []
    make_cover(story, "Employee Directory", "Human Resources — Updated Feb 2026", "INTERNAL — DO NOT DISTRIBUTE")

    story.append(Paragraph("Key Personnel Directory", heading_style))
    story.append(Paragraph(
        "This document contains contact information for key personnel at HexaDynamics Pvt Ltd. "
        "This document is classified as Internal and must not be shared externally.", body_style))

    story.append(Paragraph("Leadership Team", subheading_style))
    leadership = [
        ["Name", "Title", "Email", "Extension"],
        ["Suresh Patel", "CEO & Founder", "suresh.patel@hexadynamics.local", "1001"],
        ["Meera Iyer", "CTO", "meera.iyer@hexadynamics.local", "1002"],
        ["Rahul Deshmukh", "CISO", "rahul.deshmukh@hexadynamics.local", "1003"],
        ["Kavitha Menon", "CFO", "kavitha.menon@hexadynamics.local", "1004"],
        ["Amit Joshi", "VP Engineering", "amit.joshi@hexadynamics.local", "1005"],
    ]
    t = Table(leadership, colWidths=[100, 90, 200, 60])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BRAND_LIGHT]),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    story.append(Paragraph("IT & DevOps Team", subheading_style))
    devops = [
        ["Name", "Role", "Email", "SSH Username"],
        ["Vikram Singh", "DevOps Lead", "vikram.singh@hexadynamics.local", "devops"],
        ["Priya Sharma", "Marketing Lead", "priya.sharma@hexadynamics.local", "marketing"],
        ["Ravi Teja", "SysAdmin", "ravi.teja@hexadynamics.local", "ravi"],
        ["Sneha Kulkarni", "Jr. DevOps", "sneha.k@hexadynamics.local", "sneha"],
        ["Deepak Reddy", "DBA", "deepak.reddy@hexadynamics.local", "deepak"],
    ]
    t2 = Table(devops, colWidths=[110, 90, 200, 80])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BRAND_LIGHT]),
    ]))
    story.append(t2)
    story.append(Spacer(1, 15))

    story.append(Paragraph("Service Accounts", subheading_style))
    story.append(Paragraph(
        "The following service accounts are used for automated processes:<br/>"
        "• <b>wp_user</b> — WordPress database access (MySQL)<br/>"
        "• <b>deploy_bot</b> — Jenkins CI/CD deployments<br/>"
        "• <b>backup_svc</b> — Automated backup service<br/>"
        "• <b>monitor_agent</b> — Wazuh monitoring agent",
        body_style))

    story.append(Paragraph("Office Locations", subheading_style))
    offices = [
        ["Location", "Address", "Phone"],
        ["Bengaluru (HQ)", "Tower B, 14th Floor, Manyata Tech Park, Hebbal", "+91-80-4567-8900"],
        ["Hyderabad", "Unit 5, Raheja Mindspace, HITEC City", "+91-40-2345-6789"],
        ["Pune", "202, ICC Trade Tower, SB Road", "+91-20-6789-0123"],
        ["Singapore", "71 Robinson Road, #14-01", "+65-6234-5678"],
    ]
    t3 = Table(offices, colWidths=[100, 250, 120])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BRAND_LIGHT]),
    ]))
    story.append(t3)

    doc.build(story)


# ============================================================
# 6. Company Brochure (Public-facing)
# ============================================================
def generate_brochure(path):
    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
    story = []

    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("HexaDynamics Pvt Ltd", title_style))
    story.append(Paragraph("AI-Driven Enterprise Security Solutions", subtitle_style))
    story.append(HRFlowable(width="50%", thickness=2, color=BRAND_ACCENT))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Innovating the future of secure infrastructure.", ParagraphStyle('Tag', parent=styles['Normal'], fontSize=14, textColor=gray, alignment=TA_CENTER)))
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("www.hexadynamics.local | info@hexadynamics.local", footer_style))
    story.append(PageBreak())

    story.append(Paragraph("About Us", heading_style))
    story.append(Paragraph(
        "HexaDynamics is a next-generation cybersecurity company founded in 2019. We specialize in "
        "AI-powered threat detection, vulnerability management, and managed security operations. "
        "With over 340 professionals and 200+ enterprise clients, we are trusted by organizations "
        "across banking, healthcare, government, and technology sectors.", body_style))

    story.append(Paragraph("Our Solutions", heading_style))

    story.append(Paragraph("HexaShield — Endpoint Protection", subheading_style))
    story.append(Paragraph(
        "AI-powered endpoint detection and response (EDR) platform with real-time threat intelligence, "
        "behavioral analysis, and automated incident response. Reduces mean time to detect (MTTD) by 85%.", body_style))

    story.append(Paragraph("HexaScan — Vulnerability Assessment", subheading_style))
    story.append(Paragraph(
        "Comprehensive vulnerability scanning for networks, web applications, and cloud infrastructure. "
        "Supports OWASP Top 10, CIS Benchmarks, and custom compliance frameworks. Integrates with "
        "CI/CD pipelines for DevSecOps workflows.", body_style))

    story.append(Paragraph("HexaSOC — Managed SOC-as-a-Service", subheading_style))
    story.append(Paragraph(
        "24/7 security operations center staffed by certified analysts (OSCP, CEH, GCIH). "
        "Powered by Wazuh SIEM with custom correlation rules and threat hunting capabilities.", body_style))

    story.append(Paragraph("Why Choose HexaDynamics?", heading_style))
    story.append(Paragraph(
        "• 200+ enterprise clients across 8 countries<br/>"
        "• SOC 2 Type II certified<br/>"
        "• ISO 27001:2022 certified<br/>"
        "• 99.9% uptime SLA on all managed services<br/>"
        "• Dedicated customer success team<br/>"
        "• Competitive pricing with flexible licensing",
        body_style))

    story.append(Paragraph("Client Testimonials", heading_style))
    story.append(Paragraph(
        "<i>\"HexaDynamics transformed our security posture. Their SOC team detected a sophisticated "
        "APT campaign that our previous vendor missed entirely.\"</i><br/>"
        "— CISO, Leading Indian Bank", body_style))
    story.append(Paragraph(
        "<i>\"HexaScan integrates seamlessly into our Jenkins pipeline. We catch vulnerabilities before "
        "they hit production. Game changer.\"</i><br/>"
        "— VP Engineering, SaaS Startup", body_style))

    story.append(Paragraph("Contact Us", heading_style))
    story.append(Paragraph(
        "Email: info@hexadynamics.local<br/>"
        "Sales: sales@hexadynamics.local<br/>"
        "Phone: +91-80-4567-8900<br/>"
        "Web: www.hexadynamics.local",
        body_style))

    doc.build(story)


# ============================================================
# 7. Onboarding Checklist
# ============================================================
def generate_onboarding_checklist(path):
    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
    story = []
    make_cover(story, "New Employee Onboarding", "IT & HR Department — Checklist v2.1", "INTERNAL")

    story.append(Paragraph("New Employee IT Onboarding Checklist", heading_style))
    story.append(Paragraph(
        "This checklist must be completed within the first 3 business days of a new employee's start date. "
        "IT and HR share responsibility for ensuring all items are addressed.", body_style))

    story.append(Paragraph("Day 1 — Account Setup", subheading_style))
    checklist_1 = [
        ["#", "Task", "Owner", "Status"],
        ["1", "Create Active Directory account", "IT", "☐"],
        ["2", "Assign role-based email (firstname.lastname@hexadynamics.local)", "IT", "☐"],
        ["3", "Issue laptop with pre-configured image (Ubuntu 22.04 or Win 11 Pro)", "IT", "☐"],
        ["4", "Set up VPN credentials and test connectivity", "IT", "☐"],
        ["5", "Create WordPress intranet account (if Marketing/Content team)", "IT", "☐"],
        ["6", "Provide SSH key pair and add to authorized servers", "DevOps", "☐"],
        ["7", "Add to relevant Slack channels", "HR", "☐"],
    ]
    t = Table(checklist_1, colWidths=[25, 280, 60, 40])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BRAND_LIGHT]),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    story.append(Paragraph("Day 2 — Security Training", subheading_style))
    checklist_2 = [
        ["#", "Task", "Owner", "Status"],
        ["8", "Complete Security Awareness Training (online module)", "Employee", "☐"],
        ["9", "Read and acknowledge Information Security Policy", "Employee", "☐"],
        ["10", "Set up MFA on all accounts (Authenticator app)", "Employee", "☐"],
        ["11", "Change all temporary passwords", "Employee", "☐"],
        ["12", "Review incident reporting procedures", "HR/Security", "☐"],
    ]
    t2 = Table(checklist_2, colWidths=[25, 280, 80, 40])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BRAND_LIGHT]),
    ]))
    story.append(t2)
    story.append(Spacer(1, 15))

    story.append(Paragraph("Day 3 — System Access Verification", subheading_style))
    checklist_3 = [
        ["#", "Task", "Owner", "Status"],
        ["13", "Verify email access and calendar integration", "Employee", "☐"],
        ["14", "Verify VPN connectivity from remote location", "IT", "☐"],
        ["15", "Verify access to internal Git repositories", "DevOps", "☐"],
        ["16", "Verify access to WordPress intranet (if applicable)", "IT", "☐"],
        ["17", "Verify access to JIRA/project management tools", "IT", "☐"],
        ["18", "Complete and sign IT Asset Acknowledgment Form", "Employee", "☐"],
    ]
    t3 = Table(checklist_3, colWidths=[25, 280, 60, 40])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, gray),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BRAND_LIGHT]),
    ]))
    story.append(t3)

    story.append(Spacer(1, 20))
    story.append(Paragraph("Important Notes", heading_style))
    story.append(Paragraph(
        "• Temporary credentials are provided via secure channel only. Never share via email or chat.<br/>"
        "• All temporary passwords must be changed within 24 hours of issuance.<br/>"
        "• Report any access issues to helpdesk@hexadynamics.local or ext. 9999.<br/>"
        "• WordPress intranet admin credentials are managed by the Marketing team lead.",
        body_style))

    doc.build(story)


# ============================================================
# Main — Generate all PDFs
# ============================================================
if __name__ == "__main__":
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "/var/www/html"

    public_dir = os.path.join(output_dir, "assets", "docs")
    internal_dir = os.path.join(output_dir, "intranet", "wp-content", "uploads", "2026", "01")

    os.makedirs(public_dir, exist_ok=True)
    os.makedirs(internal_dir, exist_ok=True)

    # Public documents (accessible from corporate site)
    generate_brochure(os.path.join(public_dir, "HexaDynamics-Company-Brochure-2026.pdf"))
    print("[+] Generated: Company Brochure (public)")

    # Internal documents (inside WordPress uploads)
    generate_employee_handbook(os.path.join(internal_dir, "HexaDynamics-Employee-Handbook-2026.pdf"))
    print("[+] Generated: Employee Handbook (internal)")

    generate_network_architecture(os.path.join(internal_dir, "HexaDynamics-Network-Architecture-Q4-2025.pdf"))
    print("[+] Generated: Network Architecture (internal)")

    generate_security_policy(os.path.join(internal_dir, "HexaDynamics-InfoSec-Policy-v3.2.pdf"))
    print("[+] Generated: Information Security Policy (internal)")

    generate_project_report(os.path.join(internal_dir, "HexaDynamics-Project-Status-Q4-2025.pdf"))
    print("[+] Generated: Project Status Report (internal)")

    generate_employee_directory(os.path.join(internal_dir, "HexaDynamics-Employee-Directory-2026.pdf"))
    print("[+] Generated: Employee Directory (internal)")

    generate_onboarding_checklist(os.path.join(internal_dir, "HexaDynamics-Onboarding-Checklist-v2.1.pdf"))
    print("[+] Generated: Onboarding Checklist (internal)")

    # Also place some docs in marketing user's home directory (post-exploitation flavor)
    home_dir = "/home/marketing/Documents"
    os.makedirs(home_dir, exist_ok=True)
    generate_network_architecture(os.path.join(home_dir, "network-architecture-DRAFT.pdf"))
    generate_employee_directory(os.path.join(home_dir, "employee-directory.pdf"))
    print("[+] Generated: Documents in marketing home directory")

    print("\n[✓] All corporate PDFs generated successfully.")
