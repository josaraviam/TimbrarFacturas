from lxml import etree
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_der_private_key


def generar_cadena_original(xml_path, xslt_path):
    xml_doc = etree.parse(xml_path)
    xslt_doc = etree.parse(xslt_path)
    transform = etree.XSLT(xslt_doc)
    cadena = transform(xml_doc)
    return str(cadena)


def cargar_llave_privada(ruta_key, password=b'12345678a'):
    with open(ruta_key, 'rb') as key_file:
        llave = load_der_private_key(key_file.read(), password=password)
    return llave


def firmar_cadena(cadena_original, llave_privada):
    firma = llave_privada.sign(
        cadena_original.encode('utf-8'),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    sello = base64.b64encode(firma).decode('utf-8')
    return sello


def insertar_sello_en_xml(xml_path, sello, output_path):
    xml_doc = etree.parse(xml_path)
    root = xml_doc.getroot()
    root.set("Sello", sello)
    xml_doc.write(output_path, xml_declaration=True, encoding='UTF-8', pretty_print=True)


if __name__ == "__main__":
    # Paso 1: Generar la cadena original
    cadena_original = generar_cadena_original("cfdi.xml", "cadenaoriginal_4_0.xslt")
    print("Cadena Original:", cadena_original)

    # Paso 2: Cargar la clave privada
    # Si tu clave está protegida con contraseña, reemplaza None por b'tu_contraseña'
    llave_privada = cargar_llave_privada("mi_llave.key", password=b'12345678a')

    # Paso 3: Firmar la cadena original
    sello = firmar_cadena(cadena_original, llave_privada)
    print("Sello digital:", sello)

    # Paso 4: Insertar el sello en el XML y guardar el resultado
    insertar_sello_en_xml("cfdi.xml", sello, "cfdi_firmado.xml")
    print("XML firmado generado: cfdi_firmado.xml")
