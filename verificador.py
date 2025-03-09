import re

def validar_sello(xml_path):
    with open(xml_path, "r", encoding="utf-8") as file:
        xml_content = file.read()

    # Buscar el Sello en el XML
    match = re.search(r'<cfdi:Comprobante[^>]* Sello="([^"]+)"', xml_content)

    if match:
        sello = match.group(1)
        print("✅ Sello encontrado en el XML:\n", sello[:50] + "...")
    else:
        print("❌ ERROR: No se encontró el Sello en el XML.")

# Ruta del CFDI firmado
validar_sello("cfdi_firmado.xml")
