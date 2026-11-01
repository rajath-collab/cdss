"""
Security Guardrails & Input Validation Engine
MedFuse-AI - Multimodal Clinical Decision Support System (CDSS)
Enforces:
  - Full Name Validation (alphabetical characters only, strictly no numbers or symbols)
  - Strict Indian 10-Digit Mobile Number Validation (6-9 prefix, no arbitrary strings)
  - Medical Council Registration Format (NMC Act 2019 / State Council verification)
  - Email Address & Postal Pincode Format
  - Password Strength & Confirm Password Matching
"""

import re
from typing import Tuple

# Recognized State Medical Council & National Medical Commission Prefixes
RECOGNIZED_COUNCILS = {
    "KMC": "Karnataka Medical Council",
    "MMC": "Maharashtra Medical Council",
    "DMC": "Delhi Medical Council",
    "TNMC": "Tamil Nadu Medical Council",
    "APMC": "Andhra Pradesh Medical Council",
    "TSMC": "Telangana State Medical Council",
    "WBMC": "West Bengal Medical Council",
    "GMC": "Gujarat Medical Council",
    "MCI": "Medical Council of India (Legacy)",
    "NMC": "National Medical Commission"
}

# Council registration pattern: e.g. KMC-58291, MMC-41209, NMC-2024-1234
COUNCIL_REGEX = re.compile(
    r"^(?P<council>[A-Z]{2,5})[-/ ](?P<seq>[0-9]{4,8}(?:-[0-9]{2,4})?)$",
    re.IGNORECASE
)

# Standard Email Regex
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# Indian Postal Pincode Regex (6 digits, first digit 1-9)
PINCODE_REGEX = re.compile(r"^[1-9][0-9]{5}$")


def validate_full_name(name: str, lang: str = "en") -> Tuple[bool, str]:
    """
    Validates that Full Name contains strictly letters and spaces with multi-lingual error support.
    """
    lang_code = (lang or "en").lower()
    if not name or not name.strip():
        msgs = {
            "kn": "ಪೂರ್ಣ ಹೆಸರು ಖಾಲಿಯಿರಬಾರದು. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಹೆಸರನ್ನು ನಮೂದಿಸಿ.",
            "hi": "पूरा नाम खाली नहीं हो सकता। कृपया अपना नाम दर्ज करें।",
            "ta": "முழு பெயர் காலியாக இருக்கக்கூடாது. உங்கள் பெயரை உள்ளிடவும்.",
            "te": "పూర్తి పేరు ఖాళీగా ఉండకూడదు. దయచేసి మీ పేరును నమోదు చేయండి.",
            "ml": "പൂർണ്ണമായ പേര് ശൂന്യമായിരിക്കരുത്. നിങ്ങളുടെ പേര് നൽകുക.",
            "en": "Full Name cannot be empty. Please enter your name."
        }
        return False, msgs.get(lang_code, msgs["en"])

    clean_name = name.strip()

    if re.search(r"\d", clean_name):
        msgs = {
            "kn": "ಪೂರ್ಣ ಹೆಸರಿನಲ್ಲಿ ಸಂಖ್ಯೆಗಳು ಅಥವಾ ಅಂಕಿಗಳು ಇರಬಾರದು. ಕೇವಲ ಅಕ್ಷರಗಳನ್ನು ಮಾತ್ರ ನಮೂದಿಸಿ.",
            "hi": "पूरे नाम में संख्याएँ या अंक नहीं होने चाहिए। केवल अक्षरों को दर्ज करें।",
            "ta": "முழு பெயரில் எண்கள் இருக்கக்கூடாது. எழுத்துக்களை மட்டுமே உள்ளிடவும்.",
            "te": "పూర్తి పేరులో సంఖ్యలు లేదా అంకెలు ఉండకూడదు. అక్షరాలను మాత్రమే నమోదు చేయండి.",
            "ml": "പൂർണ്ണമായ പേരിൽ അക്കങ്ങൾ ഉണ്ടാകരുത്. അക്ഷരങ്ങൾ മാത്രം നൽകുക.",
            "en": "Full Name cannot contain numbers or digits. Please enter alphabetic characters only."
        }
        return False, msgs.get(lang_code, msgs["en"])

    if not re.match(r"^[A-Za-z\s.'-]{2,60}$", clean_name):
        msgs = {
            "kn": "ಪೂರ್ಣ ಹೆಸರು ಕೇವಲ ಅಕ್ಷರಗಳು ಮತ್ತು ಸ್ಥಳಾವಕಾಶಗಳನ್ನು ಹೊಂದಿರಬೇಕು (2 ರಿಂದ 60 ಅಕ್ಷರಗಳು).",
            "hi": "पूरे नाम में केवल अक्षर और स्थान होने चाहिए (2 से 60 वर्ण)।",
            "ta": "முழு பெயரில் எழுத்துக்கள் மற்றும் இடைவெளிகள் மட்டுமே இருக்க வேண்டும் (2 முதல் 60 எழுத்துக்கள்).",
            "te": "పూర్తి పేరులో అక్షరాలు మరియు ఖాళీలు మాత్రమే ఉండాలి (2 నుండి 60 అక్షరాలు).",
            "ml": "പൂർണ്ണമായ പേരിൽ അക്ഷരങ്ങളും ഇടവേളകളും മാത്രമേ ഉണ്ടാകാവൂ (2 മുതൽ 60 അക്ഷരങ്ങൾ).",
            "en": "Full Name must contain only alphabetic letters and spaces (2 to 60 characters)."
        }
        return False, msgs.get(lang_code, msgs["en"])

    letters = re.findall(r"[A-Za-z]", clean_name)
    if len(letters) < 2:
        msgs = {
            "kn": "ಪೂರ್ಣ ಹೆಸರು ಕನಿಷ್ಠ 2 ಅಕ್ಷರಗಳನ್ನು ಹೊಂದಿರಬೇಕು.",
            "hi": "पूरे नाम में कम से कम 2 अक्षर होने चाहिए।",
            "ta": "முழு பெயரில் குறைந்தது 2 எழுத்துக்கள் இருக்க வேண்டும்.",
            "te": "పూర్తి పేరులో కనీసం 2 అక్షరాలు ఉండాలి.",
            "ml": "പൂർണ്ണമായ പേരിൽ കുറഞ്ഞത് 2 അക്ഷരങ്ങൾ ഉണ്ടായിരിക്കണം.",
            "en": "Full Name must contain at least 2 alphabetic letters."
        }
        return False, msgs.get(lang_code, msgs["en"])

    return True, ""


def validate_phone_number(phone: str, lang: str = "en") -> Tuple[bool, str, str]:
    """
    Validates a 10-digit Indian mobile number with full vernacular localization (en, kn, hi, ta, te, ml).
    Accepts raw 10 digits or numbers with +91 / 0 prefix.
    Rejects letters, random lengths, and numbers starting with 0-5.
    Returns: (is_valid, error_message, cleaned_10_digit_number)
    """
    lang_code = (lang or "en").lower()

    if not phone or not phone.strip():
        msgs = {
            "kn": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ಖಾಲಿಯಿರಬಾರದು. ದಯವಿಟ್ಟು 10-ಅಂಕಿಯ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.",
            "hi": "मोबाइल नंबर खाली नहीं हो सकता। कृपया 10 अंकों का नंबर दर्ज करें।",
            "ta": "மொபைல் எண் காலியாக இருக்கக்கூடாது. தயவுசெய்து 10 இலக்க எண்ணை உள்ளிடவும்.",
            "te": "మొబైల్ సంఖ్య ఖాళీగా ఉండకూడదు. దయచేసి 10 అంకెల సంఖ్యను నమోదు చేయండి.",
            "ml": "മൊബൈൽ നമ്പർ ശൂന്യമായിരിക്കരുത്. ദയവായി 10 അക്ക നമ്പർ നൽകുക.",
            "en": "Mobile phone number cannot be empty."
        }
        return False, msgs.get(lang_code, msgs["en"]), ""

    raw = phone.strip()

    # Normalize: strip out spaces, dashes, parentheses
    cleaned = re.sub(r"[\s\-\(\)]", "", raw)

    # Strip leading +91 or 91 if followed by 10 digits
    if cleaned.startswith("+91") and len(cleaned) == 13:
        cleaned = cleaned[3:]
    elif cleaned.startswith("91") and len(cleaned) == 12:
        cleaned = cleaned[2:]
    elif cleaned.startswith("0") and len(cleaned) == 11:
        cleaned = cleaned[1:]

    # Check for non-digit characters
    if not cleaned.isdigit():
        msgs = {
            "kn": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯಲ್ಲಿ ಕೇವಲ ಅಂಕಿಗಳು ಮಾತ್ರ ಇರಬೇಕು. ಅಕ್ಷರಗಳು ಅಥವಾ ಚಿಹ್ನೆಗಳನ್ನು ಅನುಮತಿಸಲಾಗುವುದಿಲ್ಲ.",
            "hi": "मोबाइल नंबर में केवल अंक होने चाहिए। अक्षर या विशेष वर्ण अनुमत नहीं हैं।",
            "ta": "மொபைல் எண்ணில் எண்கள் மட்டுமே இருக்க வேண்டும். எழுத்துக்கள் அனுமதிக்கப்படாது.",
            "te": "మొబైల్ సంఖ్యలో అంకెలు మాత్రమే ఉండాలి. అక్షరాలు అనుమతించబడవు.",
            "ml": "മൊബൈൽ നമ്പറിൽ അക്കങ്ങൾ മാത്രമേ ഉണ്ടാകാവൂ. അക്ഷരങ്ങൾ അനുവദനീയമല്ല.",
            "en": "Mobile number must contain digits only. Letters and special symbols are not allowed."
        }
        return False, msgs.get(lang_code, msgs["en"]), ""

    # Check exact 10 digits
    if len(cleaned) != 10:
        msgs = {
            "kn": f"ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯು ನಿಖರವಾಗಿ 10 ಅಂಕಿಗಳನ್ನು ಹೊಂದಿರಬೇಕು (ನೀವು {len(cleaned)} ಅಂಕಿಗಳನ್ನು ನಮೂದಿಸಿದ್ದೀರಿ).",
            "hi": f"मोबाइल नंबर ठीक 10 अंकों का होना चाहिए (आपने {len(cleaned)} अंक दर्ज किए हैं)।",
            "ta": f"மொபைல் எண் சரியாக 10 இலக்கங்களாக இருக்க வேண்டும் (நீங்கள் {len(cleaned)} இலக்கங்களை உள்ளிட்டுள்ளீர்கள்).",
            "te": f"మొబైల్ సంఖ్య ఖచ్చితంగా 10 అంకెలు ఉండాలి (మీరు {len(cleaned)} అంకెలు నమోదు చేశారు).",
            "ml": f"മൊബൈൽ നമ്പർ കൃത്യമായി 10 അക്കങ്ങൾ ആയിരിക്കണം (നിങ്ങൾ {len(cleaned)} അക്കങ്ങൾ നൽകി).",
            "en": f"Mobile number must be exactly 10 digits (you entered {len(cleaned)} digits)."
        }
        return False, msgs.get(lang_code, msgs["en"]), ""

    # Check valid Indian mobile starting prefix (6, 7, 8, 9)
    if cleaned[0] not in ["6", "7", "8", "9"]:
        msgs = {
            "kn": f"ಅಮಾನ್ಯ ಮೊಬೈಲ್ ಪೂರ್ವಪ್ರತ್ಯಯ '{cleaned[0]}'. ಮಾನ್ಯ ಭಾರತೀಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಗಳು 6, 7, 8, ಅಥವಾ 9 ರಿಂದ ಪ್ರಾರಂಭವಾಗಬೇಕು.",
            "hi": f"अमान्य मोबाइल उपसर्ग '{cleaned[0]}'। वैध भारतीय मोबाइल नंबर 6, 7, 8, या 9 से शुरू होने चाहिए।",
            "ta": f"தவறான முன்னொட்டு '{cleaned[0]}'. சரியான இந்திய எண்கள் 6, 7, 8 அல்லது 9 இல் தொடங்க வேண்டும்.",
            "te": f"చెల్లని ప్రిఫిక్స్ '{cleaned[0]}'. చెల్లుబాటు అయ్యే భారతీయ సంఖ్యలు 6, 7, 8 లేదా 9తో ప్రారంభం కావాలి.",
            "ml": f"അസാധുവായ പ്രിഫിക്സ് '{cleaned[0]}'. സാധുവായ ഇന്ത്യൻ നമ്പറുകൾ 6, 7, 8 അല്ലെങ്കിൽ 9 ൽ ആരംഭിക്കണം.",
            "en": f"Invalid mobile prefix '{cleaned[0]}'. Valid Indian mobile numbers must start with 6, 7, 8, or 9."
        }
        return False, msgs.get(lang_code, msgs["en"]), ""

    # Check against repetitive dummy numbers like 0000000000 or 1111111111
    if len(set(cleaned)) == 1:
        msgs = {
            "kn": "ಅಮಾನ್ಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ: ಪುನರಾವರ್ತಿತ ಅಂಕಿಗಳು ಪತ್ತೆಯಾಗಿವೆ.",
            "hi": "अमान्य मोबाइल नंबर: दोहराए गए अंक पाए गए।",
            "ta": "தவறான மொபைல் எண்: மீண்டும் மீண்டும் வரும் எண்கள் கண்டறியப்பட்டன.",
            "te": "చెల్లని మొబైల్ సంఖ్య: పునరావృత అంకెలు కనుగొనబడ్డాయి.",
            "ml": "അസാധുവായ മൊബൈൽ നമ്പർ: ആവർത്തിച്ചുള്ള അക്കങ്ങൾ കണ്ടെത്തി.",
            "en": "Invalid mobile number: repetitive digits detected."
        }
        return False, msgs.get(lang_code, msgs["en"]), ""

    return True, "", cleaned


def validate_email(email: str, allow_empty: bool = True, lang: str = "en") -> Tuple[bool, str]:
    """
    Validates standard email format and strictly enforces @gmail.com domain to prevent
    temporary/disposable spam mail accounts (e.g. tempmail, guerrillamail, 10minutemail, yopmail).
    """
    lang_code = (lang or "en").lower()
    if not email or not email.strip():
        if allow_empty:
            return True, ""
        msgs = {
            "kn": "ಇಮೇಲ್ ವಿಳಾಸ ಅಗತ್ಯವಿದೆ.",
            "hi": "ईमेल पता आवश्यक है।",
            "ta": "மின்னஞ்சல் முகவரி தேவை.",
            "te": "ఇమెయిల్ చిరునామా అవసరం.",
            "ml": "ഇമെയിൽ വിലാസം ആവശ്യമാണ്.",
            "en": "Email address is required."
        }
        return False, msgs.get(lang_code, msgs["en"])

    clean = email.strip().lower()
    if not EMAIL_REGEX.match(clean):
        msgs = {
            "kn": "ದಯವಿಟ್ಟು ಮಾನ್ಯವಾದ ಇಮೇಲ್ ವಿಳಾಸವನ್ನು ನಮೂದಿಸಿ (ಉದಾ: name@gmail.com).",
            "hi": "कृपया एक मान्य ईमेल पता दर्ज करें (उदा: name@gmail.com)।",
            "ta": "சரியான மின்னஞ்சல் முகவரியை உள்ளிடவும் (எ.கா: name@gmail.com).",
            "te": "దయచేసి చెల్లుబాటు అయ్యే ఇమెయిల్ చిరునామాను నమోదు చేయండి (ఉదా: name@gmail.com).",
            "ml": "സാധുവായ ഒരു ഇമെയിൽ വിലാസം നൽകുക (ഉദാ: name@gmail.com).",
            "en": "Please enter a valid email address (e.g., username@gmail.com)."
        }
        return False, msgs.get(lang_code, msgs["en"])

    if not clean.endswith("@gmail.com"):
        msgs = {
            "kn": "⚠️ ಭದ್ರತಾ ನೀತಿ: ಕೇವಲ ಪರಿಶೀಲಿಸಿದ @gmail.com ವಿಳಾಸಗಳನ್ನು ಮಾತ್ರ ಅನುಮತಿಸಲಾಗಿದೆ. ತಾತ್ಕಾಲಿಕ ಅಥವಾ ಅಮಾನ್ಯ ಇಮೇಲ್ ಡೊಮೇನ್‌ಗಳನ್ನು ಕಟ್ಟುನಿಟ್ಟಾಗಿ ನಿರ್ಬಂಧಿಸಲಾಗಿದೆ.",
            "hi": "⚠️ सुरक्षा नीति: केवल सत्यापित @gmail.com पते की अनुमति है। अस्थायी या डिस्पोजेबल ईमेल प्रतिबंधित हैं।",
            "ta": "⚠️ பாதுகாப்பு கொள்கை: சரிபார்க்கப்பட்ட @gmail.com முகவரிகள் மட்டுமே அனுமதிக்கப்படுகின்றன.",
            "te": "⚠️ భద్రతా విధానం: ధృవీకరించబడిన @gmail.com చిరునామాలు మాత్రమే అనుమతించబడతాయి.",
            "ml": "⚠️ സുരക്ഷാ നയം: സ്ഥിരീകരിച്ച @gmail.com വിലാസങ്ങൾ മാത്രമേ അനുവദിക്കൂ.",
            "en": "⚠️ Security Policy: Only verified @gmail.com addresses are permitted. Temporary, disposable, or unverified domains are strictly blocked."
        }
        return False, msgs.get(lang_code, msgs["en"])

    return True, ""


def validate_pincode(pincode: str, lang: str = "en") -> Tuple[bool, str]:
    """Validates Indian 6-digit postal pincode with multi-lingual error messages."""
    if not pincode or not pincode.strip():
        return True, ""
    clean = pincode.strip()
    if not PINCODE_REGEX.match(clean):
        lang_code = (lang or "en").lower()
        msgs = {
            "kn": "ಅಂಚೆ ಪಿನ್‌ಕೋಡ್ ಮಾನ್ಯವಾದ 6-ಅಂಕಿಯ ಸಂಖ್ಯೆಯಾಗಿರಬೇಕು.",
            "hi": "डाक पिनकोड एक मान्य 6-अंकीय संख्या होनी चाहिए।",
            "ta": "அஞ்சல் குறியீடு சரியான 6 இலக்க எண்ணாக இருக்க வேண்டும்.",
            "te": "పోస్టల్ పిన్‌కోడ్ చెల్లుబాటు అయ్యే 6 అంకెల సంఖ్య అయి ఉండాలి.",
            "ml": "തപാൽ പിൻകോഡ് സാധുവായ 6 അക്ക നമ്പർ ആയിരിക്കണം.",
            "en": "Postal Pincode must be a valid 6-digit number."
        }
        return False, msgs.get(lang_code, msgs["en"])
    return True, ""


def validate_doctor_reg(reg_number: str) -> Tuple[bool, str, str]:
    """
    Validates a doctor's State Medical Council or NMC registration identifier.
    Returns: (is_valid, error_message, normalized_reg)
    """
    if not reg_number or not reg_number.strip():
        return False, "Medical Council Registration number cannot be empty for Doctor registration.", ""

    clean_reg = reg_number.strip().upper()
    match = COUNCIL_REGEX.match(clean_reg)
    if not match:
        return False, (
            "Invalid council registration format. Expected format: Council-Sequence "
            "(e.g., KMC-58291, MMC-41209, or NMC-2024-1234)."
        ), ""

    council = match.group("council").upper()
    if council not in RECOGNIZED_COUNCILS:
        allowed = ", ".join(RECOGNIZED_COUNCILS.keys())
        return False, f"Unrecognized Medical Council code '{council}'. Supported codes: {allowed}.", ""

    return True, "", clean_reg


def validate_password(password: str, confirm_password: str = None, lang: str = "en") -> Tuple[bool, str]:
    """
    Validates password length, security, and checks confirm_password matching with localization.
    """
    lang_code = (lang or "en").lower()

    if not password:
        msgs = {
            "kn": "ಪಾಸ್‌ವರ್ಡ್ ಖಾಲಿಯಿರಬಾರದು.",
            "hi": "पासवर्ड खाली नहीं हो सकता।",
            "ta": "கடவுச்சொல் காலியாக இருக்கக்கூடாது.",
            "te": "పాస్‌వర్డ్ ఖాళీగా ఉండకూడదు.",
            "ml": "പാസ്‌വേഡ് ശൂന്യമായിരിക്കരുത്.",
            "en": "Password cannot be empty."
        }
        return False, msgs.get(lang_code, msgs["en"])

    if len(password) < 6:
        msgs = {
            "kn": f"ಪಾಸ್‌ವರ್ಡ್ ಕನಿಷ್ಠ 6 ಅಕ್ಷರಗಳನ್ನು ಹೊಂದಿರಬೇಕು (ಪ್ರಸ್ತುತ {len(password)} ಅಕ್ಷರಗಳು).",
            "hi": f"पासवर्ड कम से कम 6 अक्षरों का होना चाहिए (वर्तमान में {len(password)} अक्षर)।",
            "ta": f"கடவுச்சொல் குறைந்தது 6 எழுத்துக்கள் நீளமாக இருக்க வேண்டும் ({len(password)} எழுத்துக்கள் உள்ளன).",
            "te": f"పాస్‌వర్డ్ కనీసం 6 అక్షరాలు ఉండాలి (ప్రస్తుతం {len(password)} అక్షరాలు).",
            "ml": f"പാസ്‌വേഡിന് കുറഞ്ഞത് 6 അക്ഷരങ്ങൾ നീളം ഉണ്ടായിരിക്കണം ({len(password)} അക്ഷരങ്ങൾ ഉണ്ട്).",
            "en": f"Password must be at least 6 characters long (currently {len(password)} characters)."
        }
        return False, msgs.get(lang_code, msgs["en"])

    if confirm_password is not None:
        if password != confirm_password:
            msgs = {
                "kn": "ಪಾಸ್‌ವರ್ಡ್‌ಗಳು ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ. ದಯವಿಟ್ಟು ಎರಡೂ ಕ್ಷೇತ್ರಗಳಲ್ಲಿ ಒಂದೇ ರೀತಿಯ ಪಾಸ್‌ವರ್ಡ್ ನಮೂದಿಸಿ.",
                "hi": "पासवर्ड मेल नहीं खाते। कृपया दोनों फ़ील्ड में समान पासवर्ड पुनः दर्ज करें।",
                "ta": "கடவுச்சொற்கள் பொருந்தவில்லை. தயவுசெய்து இரண்டு புலங்களிலும் ஒரே கடவுச்சொல்லை உள்ளிடவும்.",
                "te": "పాస్‌వర్డ్‌లు సరిపోలడం లేదు. దయచేసి రెండు ఫీల్డ్‌లలో ఒకే పాస్‌వర్డ్‌ను నమోదు చేయండి.",
                "ml": "പാസ്‌വേഡുകൾ പൊരുത്തപ്പെടുന്നില്ല. രണ്ട് ഫീൽഡുകളിലും ഒരേ പാസ്‌വേഡ് നൽകുക.",
                "en": "Passwords do not match. Please re-enter identical passwords in both fields."
            }
            return False, msgs.get(lang_code, msgs["en"])

    return True, ""


__all__ = [
    "validate_full_name",
    "validate_phone_number",
    "validate_email",
    "validate_pincode",
    "validate_doctor_reg",
    "validate_password",
    "RECOGNIZED_COUNCILS"
]
