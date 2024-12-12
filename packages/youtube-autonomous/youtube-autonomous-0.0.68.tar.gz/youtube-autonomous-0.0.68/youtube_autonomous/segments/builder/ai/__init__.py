from youtube_autonomous.segments.builder.ai.enums import ImageEngine, VoiceEngine
from yta_multimedia.image.generation.ai.prodia import generate_image_with_prodia
from yta_multimedia.experimental.image.generation.ai.flux import generate_dev as generate_image_with_flux
from yta_multimedia.image.generation.ai.pollinations import generate_image_with_pollinations
from yta_multimedia.audio.voice.generation.tts.google import narrate as narrate_google
from yta_multimedia.audio.voice.generation.tts.microsoft import narrate as narrate_microsoft
from yta_general_utils.temp import create_temp_filename


def create_ai_image(prompt: str, output_filename: str = None, image_engine: ImageEngine = ImageEngine.get_default()):
    """
    Creates an AI image with the provided 'prompt' and stores it locally
    as 'output_filename' (if it is not provided it will generate a 
    temporary file) with the also provided 'image_engine'.

    This method returns the 'output_filename' of the generated image.
    """
    if not prompt:
        raise Exception('No "prompt" provided.')
    
    if not output_filename:
        output_filename = create_temp_filename('ai.png')

    if not image_engine:
        image_engine = ImageEngine.get_default()

    if image_engine == ImageEngine.PRODIA:
        generate_image_with_prodia(prompt, output_filename)
    elif image_engine == ImageEngine.FLUX:
        generate_image_with_flux(prompt, output_filename)
    elif image_engine == ImageEngine.POLLINATIONS:
        generate_image_with_pollinations(prompt, output_filename)

    return output_filename

def create_ai_narration(text: str, output_filename: str = None, voice_engine: VoiceEngine = VoiceEngine.get_default()):
    """
    Creates an audio narration with the given 'text' and stores it
    locally as the 'output_filename' provided (if not provided, it
    generates a temporary file), generated with the also given
    'voice_engine' voice generation engine.

    This method returns the 'output_filename' of the generated audio
    narration.
    """
    if not text:
        raise Exception('No "text" provided.')
    
    if not output_filename:
        output_filename = create_temp_filename('narration.wav')

    voice_engine = VoiceEngine.to_enum(voice_engine)

    # TODO: What about language and voices (?)
    if voice_engine == VoiceEngine.GOOGLE:
        narrate_google(text, output_filename = output_filename)
    elif voice_engine == VoiceEngine.MICROSOFT:
        narrate_microsoft(text, output_filename = output_filename)
    # TODO: Add more

    # TODO: What about using this ? If we do the 'to_enum'
    # here we will have a valid value so we only have to 
    # worry about being one accepted value
    # voices = {
    #     VoiceEngine.GOOGLE: narrate_google,
    #     VoiceEngine.MICROSOFT: narrate_microsoft
    # }
    # voices[voice_engine](text, output_filename = output_filename)

    return output_filename