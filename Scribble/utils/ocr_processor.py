import easyocr

reader = None


def get_reader():

    global reader

    if reader is None:
        reader = easyocr.Reader(['en'], gpu=False)

    return reader


def extract_text_from_image(image):

    reader = get_reader()

    results = reader.readtext(image)

    text = "\n".join([result[1] for result in results])

    return text