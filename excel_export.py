from openpyxl import Workbook


def export_to_excel(file_path, lines):
    wb = Workbook()
    ws = wb.active
    ws.append(["Preference Adjustments", "Value (dB)"])

    # Extract filter values from lines and write to Excel
    # Assuming the structure of the lines and filter values are provided in lines
    for line in lines:
        if "Filter" in line and "Gain" in line:
            filter_name = line.split("Filter")[1].split(" ")[0].strip()
            filter_gain = float(line.split("Gain")[1].strip().split(" ")[0])
            ws.append([f"Filter {filter_name}", filter_gain])

    wb.save(file_path)
