import base64


def image_to_base64(image_path):
    """
    Converts an image file to a Base64 encoded string.

    :param image_path: Path to the image file
    :return: Base64 string representing the image
    """
    try:
        with open(image_path, "rb") as image_file:
            # Read the image file in binary mode
            image_data = image_file.read()
            # Encode the binary data to Base64
            base64_string = base64.b64encode(image_data).decode('utf-8')
            return base64_string
    except FileNotFoundError:
        print(f"File '{image_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None