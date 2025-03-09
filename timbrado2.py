import requests
import json

def obtener_token(user, password):
    """
    Realiza la autenticación para obtener el token.
    Se envían los datos en formato JSON a la API de autenticación.
    """
    url_auth = "https://services.test.sw.com.mx/security/authenticate"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "user": user,
        "password": password
    }

    response = requests.post(url_auth, headers=headers, json=payload)  # Se envían los datos en el cuerpo JSON
    if response.status_code == 200:
        try:
            data = response.json()
            token = data.get("token")
            if token:
                return token
            else:
                raise Exception("No se encontró el token en la respuesta: " + response.text)
        except json.JSONDecodeError:
            raise Exception("Error en la decodificación de la respuesta JSON: " + response.text)
    else:
        raise Exception(f"Error en autenticación: {response.status_code} {response.text}")


def timbrar_xml(token, xml_path):
    """
    Envía el archivo XML firmado a la API de timbrado usando multipart/form-data.
    """
    url_timbrado = "https://services.test.sw.com.mx/cfdi33/issue/v4"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        with open(xml_path, "rb") as xml_file:
            files = {"xml": (xml_path, xml_file, "application/xml")}
            response = requests.post(url_timbrado, headers=headers, files=files)
            return response
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo XML en la ruta: {xml_path}")
        return None


if __name__ == "__main__":
    user = "usuario@pruebas.com" #Todavía no nos contestaron para el usuario de pruebas
    password = "contraseña1234"

    try:
        token = obtener_token(user, password)
        print("Token obtenido:", token)
    except Exception as e:
        print("Error en autenticación:", e)
        exit(1)

    # Ruta al archivo XML firmado que deseas enviar para timbrado
    xml_path = "cfdi_firmado.xml"

    response = timbrar_xml(token, xml_path)
    if response:
        if response.status_code == 200:
            print("Timbrado exitoso. Respuesta:")
            print(response.text)  # o response.json() si la respuesta es JSON
        else:
            print("Error en timbrado:", response.status_code, response.text)
