"""
This is using the Pollinations platform with contains an
AI image generator API and open-source model.

Source: https://pollinations.ai/
"""
from yta_general_utils.downloader import Downloader
from yta_general_utils.url import encode_url_parameter
from yta_general_utils.programming.parameter_validator import PythonValidator


def generate_image_with_pollinations(prompt: str, output_filename: str):
    """
    Generate an image with the Pollinations AI image generation model
    using the provided 'prompt' and stores it locally as 
    'output_filename'.
    """
    if not PythonValidator.is_string(prompt):
        raise Exception('Provided "prompt" parameter is not a valid prompt.')
    
    if not PythonValidator.is_string(output_filename):
        raise Exception('Provided "output_filename" parameter is not a valid output.')
    
    prompt = encode_url_parameter(prompt)

    # TODO: Make some of these customizable
    WIDTH = 1920
    HEIGHT = 1080
    # TODO: This seed should be a random value or
    # I will receive the same image with the same
    # prompt
    SEED = 43
    MODEL = 'flux'

    url = f'https://pollinations.ai/p/{prompt}?width={WIDTH}&height={HEIGHT}&seed={SEED}&model={MODEL}'

    Downloader.download_image(url, output_filename)

    return output_filename

"""
Check because there is also a model available for
download and to work with it (as they say here
https://pollinations.ai/):

    # Using the pollinations pypi package
    ## pip install pollinations

    import pollinations as ai

    model_obj = ai.Model()

    image = model_obj.generate(
        prompt=f'Awesome and hyperrealistic photography of a vietnamese woman... {ai.realistic}',
        model=ai.flux,
        width=1038,
        height=845,
        seed=43
    )
    image.save('image-output.jpg')

    print(image.url)
"""