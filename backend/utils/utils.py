from requests import post
from requests.exceptions import RequestException
# pip install googletrans==3.1.0a0
from googletrans import Translator
from g4f.client import Client



def translate_sentence(text: str, destination_lang: str = 'en'): # destination_lang - 'en'|'uk'
    translator = Translator()
    translation = translator.translate(text, destination_lang).text
    return translation


def ask_llm(prompt: str, lang: str = 'en') -> str:
    """
    Generate a LLM completion based on the provided prompt
    Args:
        prompt: str
        lang: str -> en|uk        
    """
    try:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            # Add any other necessary parameters
        )
        resp_text = response.choices[0].message.content

        if lang == 'en':
            return resp_text
        # AI can talk only in english, so we should translate en to uk
        elif lang == 'uk':
            return translate_sentence(resp_text, lang)
            
    except RequestException as exc:
        # raise RequestException("Unable to fetch the response.") from exc
        return ''
    except Exception as e:
        return ''
