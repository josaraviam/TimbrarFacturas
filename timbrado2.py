import requests

def obtener_token(user, password):
    """
    Realiza la autenticación para obtener un token de acceso.
    Se envían las credenciales en el cuerpo de la solicitud.
    """
    url_auth = "https://services.test.sw.com.mx/security/authenticate"
    try:
        response = requests.post(url_auth, json={"user": user, "password": password})
        response.raise_for_status()  # Lanza excepción si la respuesta no es exitosa (código 2xx)

        data = response.json()
        token = data.get("token")
        if not token:
            raise Exception("No se encontró el token en la respuesta: " + response.text)
        return token
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error en la petición de autenticación: {e}")

def timbrar_xml(token, xml_path):
    """
    Envía un XML firmado a la API de timbrado utilizando multipart/form-data.
    """
    url_timbrado = "http://services.test.sw.com.mx/cfdi40/issue/v4"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        with open(xml_path, "rb") as xml_file:
            files = {
                "xml": (xml_path.split("/")[-1], xml_file, "application/xml")
            }
            response = requests.post(url_timbrado, headers=headers, files=files)
            return response
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error en la petición de timbrado: {e}")
    except IOError as e:
        raise Exception(f"Error al abrir el archivo XML: {e}")

if __name__ == "__main__":
    # Credenciales de usuario para autenticación (reemplazar con datos reales)
    user = "user"
    password = "password"

    try:
        # Obtener token de autenticación
        token = obtener_token(user, password)
        print("Token obtenido:", token)
    except Exception as e:
        print("Error en autenticación:", e)
        exit(1)

    # Ruta al archivo XML firmado a timbrar
    xml_path = "cfdi_firmado.xml"

    try:
        # Enviar XML para timbrado
        response = timbrar_xml(token, xml_path)

        if response.status_code == 200:
            print("Timbrado exitoso. Respuesta:")
            print(response.text)

            # Guardar el XML timbrado si está en la respuesta
            data = response.json()
            if "data" in data and "cfdi" in data["data"]:
                with open("cfdi_timbrado.xml", "w", encoding="utf-8") as f:
                    f.write(data["data"]["cfdi"])
                print("✅ XML timbrado guardado como cfdi_timbrado.xml")
        else:
            print(f"Error en timbrado: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")
