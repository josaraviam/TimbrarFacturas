from lxml import etree
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_der_private_key

def generar_cadena_original(xml_path, xslt_path):
    """Transforma el XML CFDI en la cadena original aplicando la XSLT."""
    try:
        # Verificar si los archivos existen y contienen datos
        with open(xml_path, "r", encoding="utf-8") as f:
            contenido_xml = f.read().strip()
        if not contenido_xml:
            raise ValueError("El archivo XML está vacío.")

        with open(xslt_path, "r", encoding="utf-8") as f:
            contenido_xslt = f.read().strip()
        if not contenido_xslt:
            raise ValueError("El archivo XSLT está vacío.")

        # Cargar XML y XSLT en memoria
        xml_doc = etree.fromstring(contenido_xml.encode("utf-8"))
        xslt_doc = etree.fromstring(contenido_xslt.encode("utf-8"))
        transform = etree.XSLT(xslt_doc)

        # Generar la cadena original
        cadena = transform(xml_doc)
        return cadena.xpath("string()").strip()
    except Exception as e:
        print(f"❌ Error al generar la cadena original: {e}")
        return None

def cargar_llave_privada(ruta_key, password=b'12345678a'):
    """Carga la llave privada desde un archivo .key en formato DER."""
    try:
        with open(ruta_key, 'rb') as key_file:
            llave = load_der_private_key(key_file.read(), password=password)
        return llave
    except Exception as e:
        print(f"❌ Error al cargar la llave privada: {e}")
        return None

def firmar_cadena(cadena_original, llave_privada):
    """Firma la cadena original con la llave privada usando SHA256 y PKCS1 v1.5."""
    try:
        firma = llave_privada.sign(
            cadena_original.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        # Convertir la firma a Base64 para su uso en XML
        sello = base64.b64encode(firma).decode('utf-8')
        return sello
    except Exception as e:
        print(f"❌ Error al firmar la cadena original: {e}")
        return None

def insertar_sello_en_xml(xml_path, sello, output_path):
    """Inserta el sello digital en el XML CFDI dentro del atributo 'Sello'."""
    try:
        xml_doc = etree.parse(xml_path)  # Cargar el XML CFDI
        root = xml_doc.getroot()
        root.set("Sello", sello)  # Insertar el sello digital generado
        xml_doc.write(output_path, xml_declaration=True, encoding='UTF-8', pretty_print=True)
        print(f"✅ XML firmado correctamente: {output_path}")
    except Exception as e:
        print(f"❌ Error al insertar el sello en el XML: {e}")

if __name__ == "__main__":
    # Paso 1: Generar la cadena original aplicando la transformación XSLT
    cadena_original = generar_cadena_original("cfdi.xml", "cadenaoriginal_4_0.xslt")
    if not cadena_original:
        exit(1)
    print("✅ Cadena Original generada:\n", cadena_original)

    # Paso 2: Cargar la clave privada desde un archivo .key
    llave_privada = cargar_llave_privada("mi_llave.key", password=b'12345678a')
    if not llave_privada:
        exit(1)

    # Paso 3: Firmar la cadena original generada
    sello = firmar_cadena(cadena_original, llave_privada)
    if not sello:
        exit(1)
    print("✅ Sello digital generado:\n", sello[:50] + "...")

    # Paso 4: Insertar el sello en el XML y guardar el documento firmado
    insertar_sello_en_xml("cfdi.xml", sello, "cfdi_firmado.xml")
