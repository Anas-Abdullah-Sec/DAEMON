import datetime
import os
import re
import socket
import ssl
import subprocess
import sys
import time

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# Cyber Palette
G = "\033[92m"   # Neon Green
C = "\033[96m"   # Cyan
R = "\033[91m"   # Red
Y = "\033[93m"   # Yellow
M = "\033[95m"   # Magenta
W = "\033[97m"   # White
B = "\033[1m"    # Bold
RESET = "\033[0m"


def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    
    banner = f"""
{C}{B}  ██████╗  █████╗ ███████╗███╗   ███╗██████╗ ███╗   ██╗
  ██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔══██╗████╗  ██║
  ██║  ██║███████║█████╗  ██╔████╔██║██║  ██║██╔██╗ ██║
  ██║  ██║██╔══██║██╔══╝  ██║╚██╔╝██║██║  ██║██║╚██╗██║
  ██████╔╝██║  ██║███████╗██║ ╚═╝ ██║██████╔╝██║ ╚████║
  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═══╝{RESET}
"""
    print(banner)
    print(f"   {G}{B}[❖] UNVEIL THE UNSEEN. AUDIT THE INVISIBLE.{RESET}")
    print(f"   {Y}─────────────────────────────────────────────────────────────{RESET}")
    print(f"   {R}Developer : {W}Anas Abdullah")
    print(f"   {R}GitHub    : {W}https://github.com/Anas-Abdullah-Sec")
    print(f"   {R}LinkedIn  : {W}https://linkedin.com/in/anas-abdullah")
    print(f"   {Y}─────────────────────────────────────────────────────────────{RESET}\n")


def run_cmd(command):
    try:
        res = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30).stdout.strip()
        clean_res = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', res)
        return clean_res if clean_res else "No telemetry returned or service non-responsive."
    except Exception as e:
        return f"Audit Exception: {e}"


def check_ssl(target):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((target, 443), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                cert = ssock.getpeercert()
                issuer = dict(x[0] for x in cert['issuer'])
                expiry = cert['notAfter']
                return f"Certificate Authority: {issuer.get('organizationName', 'Unknown')}\nValid Until: {expiry}"
    except Exception:
        return "HTTPS/SSL Endpoint Not Accessible (Port 443 Closed or Filtered)"


def calculate_cvss(results):
    cvss = 0.0
    reasons = []
    
    nmap_res = results.get("nmap", "")
    ssl_res = results.get("ssl", "")
    
    open_ports = nmap_res.count("open")
    if open_ports > 0:
        cvss += min(open_ports * 0.8, 5.0)
        reasons.append(f"Publicly Exposed Services ({open_ports} Open Ports Detected)")
        
    if "21/tcp" in nmap_res or "23/tcp" in nmap_res:
        cvss += 2.5
        reasons.append("Unencrypted Legacy Protocol Detected (FTP/Telnet)")
        
    if "Not Accessible" in ssl_res:
        cvss += 1.5
        reasons.append("Missing HTTPS / Encrypted Transport Layer")
        
    cvss = round(min(cvss, 10.0), 1)
    
    if cvss == 0.0:
        severity, color = "LOW RISK", "#10B981"
    elif cvss <= 3.9:
        severity, color = "LOW RISK", "#06B6D4"
    elif cvss <= 6.9:
        severity, color = "MEDIUM RISK", "#F59E0B"
    elif cvss <= 8.9:
        severity, color = "HIGH RISK", "#F97316"
    else:
        severity, color = "CRITICAL RISK", "#EF4444"
        
    return cvss, severity, color, reasons


def generate_executive_pdf(target, results, cvss_info, full_pdf_path):
    cvss_score, severity, severity_color, risk_reasons = cvss_info
    
    doc = SimpleDocTemplate(
        full_pdf_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    header_style = ParagraphStyle(
        'DocHeader', fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor("#FFFFFF"), spaceAfter=4
    )
    sub_header_style = ParagraphStyle(
        'DocSubHeader', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#00E676")
    )
    section_heading = ParagraphStyle(
        'SectionHead', fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor("#0F172A"), spaceBefore=14, spaceAfter=6
    )
    body_style = ParagraphStyle(
        'DocBody', fontName='Courier', fontSize=8, textColor=colors.HexColor("#1E293B"), leading=11
    )
    cvss_text_style = ParagraphStyle(
        'CVSSText', fontName='Helvetica', fontSize=9, textColor=colors.HexColor("#0F172A"), leading=13
    )

    elements = []
    
    header_data = [[
        Paragraph("<b>DAEMON SECURITY AUDIT REPORT</b>", header_style),
        Paragraph(f"<b>TARGET:</b> {target}<br/><b>DATE:</b> {datetime.datetime.now().strftime('%Y-%m-%d')}", ParagraphStyle('HMeta', fontName='Helvetica', fontSize=8, textColor=colors.HexColor("#CBD5E1"), alignment=2))
    ], [
        Paragraph("AUTOMATED PENETRATION TESTING & RECON SUITE", sub_header_style),
        Paragraph("<b>LEAD AUDITOR:</b> Anas Abdullah", ParagraphStyle('HMeta2', fontName='Helvetica', fontSize=8, textColor=colors.HexColor("#94A3B8"), alignment=2))
    ]]
    
    header_table = Table(header_data, colWidths=[332, 200])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 10))
    
    risk_list_str = "<br/>".join([f"• {r}" for r in risk_reasons]) if risk_reasons else "• No High Severity Threats Identified"
    
    cvss_box_content = f"""
    <b>CVSS v3.1 SCORE:</b> {cvss_score} / 10.0 &nbsp;&nbsp;|&nbsp;&nbsp; <b>SEVERITY RATING:</b> <font color="{severity_color}"><b>{severity}</b></font><br/><br/>
    <b>KEY FINDINGS:</b><br/>
    {risk_list_str}
    """
    
    p_cvss = Paragraph(cvss_box_content, cvss_text_style)
    t_cvss = Table([[p_cvss]], colWidths=[532])
    t_cvss.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('LINELEFT', (0,0), (-1,-1), 4, colors.HexColor(severity_color)),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_cvss)
    elements.append(Spacer(1, 8))
    
    sections = [
        ("PHASE 1: Infrastructure & DNS Reconnaissance (Host)", results.get("dns", "N/A")),
        ("PHASE 2: Port & Service Discovery (Nmap Engine)", results.get("nmap", "N/A")),
        ("PHASE 3: Cryptographic Transport Audit (SSL/TLS)", results.get("ssl", "N/A"))
    ]
    
    for title, content in sections:
        elements.append(Paragraph(title, section_heading))
        formatted_content = content.replace("\n", "<br/>").replace(" ", "&nbsp;")
        p = Paragraph(formatted_content, body_style)
        
        t = Table([[p]], colWidths=[532])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FAFAFA")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 6))
        
    doc.build(elements)


def run_module(phase_num, module_name, cmd_func):
    print(f" {C}[*] Phase {phase_num}:{RESET} {W}{module_name:<42}{RESET} ... ", end="", flush=True)
    start_time = time.time()
    result = cmd_func()
    elapsed = round(time.time() - start_time, 1)
    print(f"{G}[ DONE ]{RESET} {M}({elapsed}s){RESET}")
    return result


def start_daemon():
    print_banner()
    target = input(f" {R}▶{RESET} {Y}{B}[?]{RESET} {W}Enter Target Domain or IP (e.g. scanme.nmap.org): {G}").strip()
    
    if not target:
        print(f"\n {R}[!] Target scope cannot be empty! Exiting...{RESET}")
        return

    # Option 1: Custom Output Directory Input
    custom_dir = input(f" {R}▶{RESET} {Y}{B}[?]{RESET} {W}Enter Save Directory (Press Enter for Current Folder): {G}").strip()
    if custom_dir:
        output_dir = os.path.expanduser(custom_dir)
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                print(f" {R}[!] Invalid path ({e}), saving to current directory.{RESET}")
                output_dir = "."
    else:
        output_dir = "."

    # Option 2: Custom File Name Input
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    default_name = f"{target.replace('.', '_')}_{timestamp}"
    
    custom_filename = input(f" {R}▶{RESET} {Y}{B}[?]{RESET} {W}Enter Custom PDF Name (Press Enter for '{default_name}'): {G}").strip()
    
    if custom_filename:
        # User specified name
        filename = custom_filename if custom_filename.endswith(".pdf") else f"{custom_filename}.pdf"
    else:
        # Default auto-generated timestamped name to prevent overwriting
        filename = f"{default_name}.pdf"

    full_pdf_path = os.path.join(output_dir, filename)

    print(f"\n {C}{B}[*] INITIALIZING AUDIT PIPELINE AGAINST:{RESET} {Y}{B}{target}{RESET}\n")

    results = {}

    results["dns"] = run_module(1, "DNS & Infrastructure Mapping (Host)", lambda: run_cmd(f"host {target}"))
    results["nmap"] = run_module(2, "Network Port & Service Discovery (Nmap)", lambda: run_cmd(f"nmap -F -sV --version-light {target}"))
    results["ssl"] = run_module(3, "Cryptographic Transport Audit (SSL/TLS)", lambda: check_ssl(target))

    print(f"\n {C}[*]{RESET} {W}Calculating Dynamic CVSS Telemetry...{RESET}")
    cvss_info = calculate_cvss(results)
    
    print(f" {C}[*]{RESET} {W}Compiling Executive PDF Report...{RESET}")
    generate_executive_pdf(target, results, cvss_info, full_pdf_path)

    print(f"\n {G}─────────────────────────────────────────────────────────────{RESET}")
    print(f" {G}{B}[✓] AUDIT COMPLETE!{RESET} {W}Report Saved At: {Y}{B}{os.path.abspath(full_pdf_path)}{RESET}")
    print(f" {G}─────────────────────────────────────────────────────────────{RESET}\n")


if __name__ == "__main__":
    start_daemon()