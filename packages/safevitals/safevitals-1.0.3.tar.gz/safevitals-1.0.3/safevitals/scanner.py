import argparse
import shutil
import sys
import zipfile
import os
import subprocess
from importlib.resources import files
import json
from datetime import datetime
from reportlab.lib import colors
from reportlab.platypus import Image, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import matplotlib.pyplot as plt
from io import BytesIO
import argparse
# Constants for paths
DECOMPILE_PATH = "./export/decompile/"
PDF_PATH = "./export/pdf/"
JSON_PATH = "./export/json/"


# Ensure directories exist
os.makedirs(DECOMPILE_PATH, exist_ok=True)
os.makedirs(PDF_PATH, exist_ok=True)
os.makedirs(JSON_PATH, exist_ok=True)
def check_dependencies():
    dependencies = ["apktool", "d2j-dex2jar"]
    for tool in dependencies:
        if not shutil.which(tool):
            print(f"[-] Error: {tool} is not installed or not found in PATH.")
            print("    Please install it and ensure it's accessible via the command line.")
            sys.exit(1)

# Call this function early in the main script
def get_jar_path():
    # Locate the jd.jar file in the package
    jar_path = files("resources").joinpath("jd-cli.jar")
    return str(jar_path)  # Convert to string if you need a file path

def decompile_apk(apk_path, output_folder):
    apk_name = os.path.splitext(os.path.basename(apk_path))[0]

    if os.path.exists("temp"):
        print("[~] Removing old temp directory")
        shutil.rmtree("temp")

    print("[+] Creating temp directory")
    os.makedirs("temp")
    apk_zip = "temp/" + apk_name + ".zip"
    shutil.copy2(apk_path, apk_zip)

    apk_unziped_dir = "temp/" + apk_name + "_unziped"
    os.makedirs(apk_unziped_dir)

    zip_ref = zipfile.ZipFile(apk_zip, 'r')
    zip_ref.extractall(apk_unziped_dir)
    zip_ref.close()

    apk_classes = apk_unziped_dir + "/classes.dex"
    if not os.path.exists(apk_classes):
        print("[-] Error: the APK doesn't have the classes.dex")
        return False

    print("[+] Getting the jar")
    apk_jar = "temp/" + apk_name + ".jar"
    subprocess.run(["d2j-dex2jar", apk_path, "-o", apk_jar],
                   capture_output=True, text=True)
    print("[+] Decompiling the jar")
    apk_java = "temp/" + apk_name + "_java/src"
    subprocess.run(
        ["java", "-jar", get_jar_path(), apk_jar, "-od", apk_java],
        capture_output=True, text=True
    )
    print("[+] Reverse engineering the APK")
    apk_re = "temp/" + apk_name + "_re"
    subprocess.run(
        ['apktool', 'd', apk_path, '-o', apk_re, '-f'],
        capture_output=True, text=True
    )

    print("[+] Organizing everything")
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    shutil.move(apk_java, output_folder)
    re_list = os.listdir(apk_re)
    for re_files in re_list:
        shutil.move(os.path.join(apk_re, re_files), output_folder)

    if os.path.exists("temp"):
        shutil.rmtree("temp")

    print("[+] Done decompiling the APK")
    return True

def run_mobsf_scan(output_folder, output_file):
    result = subprocess.run(
        ['mobsfscan', 'path', output_folder, '-o', output_file, '--json'],
        capture_output=True, text=True, encoding='utf-8'
    )
    return True

def create_pdf(data, output_filename):

    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    title_style = styles['Title']
    title = "Vulnerability Report by Safe Vitals"
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.2 * inch))

    active_vulnerabilities_title = "Active Vulnerabilities"
    elements.append(Paragraph(active_vulnerabilities_title, styles['Heading2']))
    elements.append(Spacer(1, 0.1 * inch))

    severity_count = {
        "INFO": 0,
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0,
        "CRITICAL": 0,
        "WARNING": 0
    }

    print("lets find result")

    for key, vulnerability in data['results'].items():
        cwe = vulnerability['metadata']['cwe']
        description = vulnerability['metadata']['description']
        severity = vulnerability['metadata']['severity']

        if severity in severity_count:
            severity_count[severity] += 1

        vulnerability_paragraph = f"<b>CWE-{cwe}</b>: {description}"
        elements.append(Paragraph(vulnerability_paragraph, styles['Normal']))
        elements.append(Spacer(1, 0.1 * inch))

        table_data = []
        try:
            for file_info in vulnerability['files']:
                file_path = file_info['file_path']
                match_lines = ', '.join(map(str, file_info['match_lines']))
                match_positions = ', '.join(map(str, file_info['match_position']))

                file_name = os.path.basename(file_path).split('/')[-1]
                match_code = truncate_text(file_info['match_string'], max_length=100)
                table_data.append([file_name, match_lines, match_positions, match_code])

            table_data.insert(0, ["File Path", "Match Lines", "Match Position", "Match Code"])
            table = Table(table_data)

            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOX', (0, 0), (-1, -1), 2, colors.black)
            ]))

            elements.append(table)
            elements.append(Spacer(1, 0.2 * inch))
        except:
            pass
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("<b>Severity Breakdown</b>", styles['Heading2']))
    elements.append(Spacer(1, 0.2 * inch))

    chart_image = create_severity_chart(severity_count)
    elements.append(Image(chart_image, width=5 * inch, height=3 * inch))

    doc.build(elements)

def truncate_text(text, max_length=50):
    """Truncates text to a maximum length and adds ellipses if needed."""
    return text if len(text) <= max_length else text[:max_length - 3] + '...'

def create_severity_chart(severity_count):
    categories = list(severity_count.keys())
    counts = list(severity_count.values())

    fig, ax = plt.subplots()
    ax.barh(categories, counts, color='skyblue')
    ax.set_xlabel('Count')
    ax.set_title('Vulnerability Severity Breakdown')

    image_stream = BytesIO()
    plt.tight_layout()
    plt.savefig(image_stream, format='png')
    plt.close(fig)
    image_stream.seek(0)
    return image_stream
def main():
    print_banner()  # Print the banner when the tool starts
    check_dependencies()
    parser = argparse.ArgumentParser(description="APK Vulnerability Scanner")
    parser.add_argument('-a', '--apk', required=True, help="Path to the APK file")
    args = parser.parse_args()



    apk_path = args.apk
    if not os.path.exists(apk_path):
        print("[-] APK file not found!")
        return

    # Process APK file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    apk_name = os.path.splitext(os.path.basename(apk_path))[0]
    output_folder = os.path.join(DECOMPILE_PATH, f"{apk_name}_{timestamp}")
    json_file = os.path.join(JSON_PATH, f"{apk_name}_{timestamp}.json")
    pdf_file = os.path.join(PDF_PATH, f"{apk_name}_{timestamp}_report.pdf")

    if not decompile_apk(apk_path, output_folder):
        print("[-] Failed to decompile APK")
        return

    print("\n[+] Start vulnerability scanning")
    if not run_mobsf_scan(output_folder, json_file):
        print("[-] Failed to scan APK")
        return

    print("[+] Generating Report..")
    with open(json_file, 'r') as f:
        data = json.load(f)

    create_pdf(data, pdf_file)
    print(f"[+] Report generated: {pdf_file}")
def print_banner():
    banner = r"""
       _____        __      __      ___ _        _     
  / ____|      / _|     \ \    / (_) |      | |    
 | (___   __ _| |_ ___   \ \  / / _| |_ __ _| |___ 
  \___ \ / _` |  _/ _ \   \ \/ / | | __/ _` | / __|
  ____) | (_| | ||  __/    \  /  | | || (_| | \__ \
 |_____/ \__,_|_| \___|     \/   |_|\__\__,_|_|___/
                                                   
                                                   
       Vulnerability Scanner by Safe Vitals
    """
    print(banner)

if __name__ == "__main__":

    main()
