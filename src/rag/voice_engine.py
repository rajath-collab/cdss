from voice.tts_engine import synthesize_clinical_audio, get_clinical_speech_text, VERNACULAR_TEMPLATES

def get_vernacular_summary(report_text: str, language: str = "kannada") -> str:
    """Convert report summary to vernacular language"""
    summaries = {
        "kannada": f"Nimma varadiya saramsa: {report_text[:200]}",
        "hindi": f"Aapki report ka saar: {report_text[:200]}",
        "english": f"Your report summary: {report_text[:200]}"
    }
    return summaries.get(language.lower(), summaries["english"])

def text_to_speech(text: str, lang: str = "en") -> str:
    """Text to speech - works without gTTS also"""
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=lang, slow=False)
        filename = f"report_{lang}.mp3"
        tts.save(filename)
        return f"Audio saved: {filename}"
    except ImportError:
        return f"[Voice Mode] {text} - (install gTTS for audio)"
    except Exception as e:
        return f"Voice Error: {e}"

__all__ = [
    "get_vernacular_summary",
    "text_to_speech",
    "synthesize_clinical_audio",
    "get_clinical_speech_text",
    "VERNACULAR_TEMPLATES"
]

if __name__ == "__main__":
    print("Voice Engine Module - OK")
    print(get_vernacular_summary("Hemoglobin Normal", "kannada"))
