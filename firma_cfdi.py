import os
from lxml import etree
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_der_private_key

# Mostrar información de diagnóstico sobre los archivos requeridos
print(f"Directorio actual: {os.getcwd()}")
print(f"XML existe: {os.path.exists('cfdi.xml')}")
print(f"XSLT existe: {os.path.exists('cadenaoriginal_4_0.xslt')}")

# Leer y mostrar información de los archivos XML y XSLT
try:
    with open("cfdi.xml", "r", encoding="utf-8") as f:
        contenido_xml = f.read()
        print(f"Tamaño XML: {len(contenido_xml)} bytes")
        print(f"Inicio XML: {contenido_xml[:100]}...")

    with open("cadenaoriginal_4_0.xslt", "r", encoding="utf-8") as f:
        contenido_xslt = f.read()
        print(f"Tamaño XSLT: {len(contenido_xslt)} bytes")
        print(f"Inicio XSLT: {contenido_xslt[:100]}...")
except Exception as e:
    print(f"Error al leer archivos: {e}")

# Intentar parsear los archivos XML y XSLT para validar su estructura
print("\nProbando parseo XML directo:")
try:
    tree = etree.parse("cfdi.xml")
    root = tree.getroot()
    print(f"✓ Parseo XML exitoso. Raíz: {root.tag}")
except Exception as e:
    print(f"✗ Error al parsear XML: {e}")

print("\nProbando parseo XSLT directo:")
try:
    xslt_tree = etree.parse("cadenaoriginal_4_0.xslt")
    xslt_root = xslt_tree.getroot()
    print(f"✓ Parseo XSLT exitoso. Raíz: {xslt_root.tag}")
except Exception as e:
    print(f"✗ Error al parsear XSLT: {e}")

def generar_cadena_original(xml_path, xslt_path):
    """Genera la cadena original a partir del XML y la transforma usando XSLT."""
    try:
        xml_doc = etree.parse(xml_path)  # Cargar el documento XML
        xslt_doc = etree.parse(xslt_path)  # Cargar el archivo XSLT
        transform = etree.XSLT(xslt_doc)  # Crear la transformación XSLT
        cadena = transform(xml_doc)  # Aplicar la transformación
        resultado = str(cadena)
        print(f"Resultado de transformación: {resultado[:100]}...")
        return resultado
    except etree.XMLSyntaxError as e:
        print(f"❌ Error: El XML no es válido: {e}")
    except FileNotFoundError as e:
        print(f"❌ Error: No se encontró el archivo: {e}")
    except Exception as e:
        print(f"❌ Error al generar la cadena original: {e}")
    return None

def cargar_llave_privada(ruta_key, password):
    """Carga la llave privada desde un archivo en formato DER."""
    try:
        with open(ruta_key, 'rb') as key_file:
            llave = load_der_private_key(key_file.read(), password=password)
        return llave
    except Exception as e:
        print(f"❌ Error al cargar la llave privada: {e}")
        return None

def firmar_cadena(cadena_original, llave_privada):
    """Firma la cadena original usando SHA256 y la clave privada."""
    try:
        firma = llave_privada.sign(
            cadena_original.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        sello = base64.b64encode(firma).decode('utf-8')  # Convertir firma a Base64
        return sello
    except Exception as e:
        print(f"❌ Error al firmar la cadena original: {e}")
        return None

def insertar_sello_en_xml(xml_path, sello, output_path):
    """Inserta el sello digital en el XML y lo guarda en un nuevo archivo."""
    try:
        xml_doc = etree.parse(xml_path)
        root = xml_doc.getroot()
        root.set("Sello", sello)  # Insertar el sello en el atributo correspondiente
        xml_doc.write(output_path, xml_declaration=True, encoding='UTF-8', pretty_print=True)
        print(f"✅ XML firmado correctamente: {output_path}")
    except Exception as e:
        print(f"❌ Error al insertar el sello en el XML: {e}")

if __name__ == "__main__":
    # Definición de archivos
    xml_file = "cfdi.xml"
    xslt_file = "cadenaoriginal_4_0.xslt"
    key_file = "mi_llave.key"
    key_password = b"12345678a"  # Contraseña de la clave privada (cambiar por seguridad)

    # Paso 1: Generar la cadena original
    cadena_original = generar_cadena_original(xml_file, xslt_file)
    if not cadena_original:
        exit(1)
    print("✅ Cadena Original generada:\n", cadena_original)

    # Paso 2: Cargar la clave privada
    llave_privada = cargar_llave_privada(key_file, key_password)
    if not llave_privada:
        exit(1)

    # Paso 3: Firmar la cadena original
    sello = firmar_cadena(cadena_original, llave_privada)
    if not sello:
        exit(1)
    print("✅ Sello digital generado:\n", sello[:50] + "...")

    # Paso 4: Insertar el sello en el XML
    insertar_sello_en_xml(xml_file, sello, "cfdi_firmado.xml")