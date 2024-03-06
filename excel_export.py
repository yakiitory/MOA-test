from openpyxl import Workbook

def export_to_excel(file_path, lines, tonality_value, bass_value, treble_value, intensity_value):
    wb = Workbook()
    ws = wb.active

    # Write headers
    ws.append(["Preference Adjustments", "Value (dB)"])

    # Write specific adjustments
    ws.append(["Tonality", tonality_value])
    ws.append(["Bass", bass_value])
    ws.append(["Treble", treble_value])
    ws.append(["Intensity", intensity_value])

    # Save Excel file
    wb.save(file_path)


