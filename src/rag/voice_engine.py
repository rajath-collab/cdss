def speak_lab_summary(lab_data):
    # Create clean summary for voice
    summary_parts = []
    for test, details in lab_data.items():
        value = details.get('value', 'N/A')
        unit = details.get('unit', '')
        status = details.get('status', '')
        summary_parts.append(f"{test} is {value} {unit}, status {status}")

    clean_summary = "Lab Report Summary: " + ". ".join(summary_parts)
    
    print(f"[VOICE] Speaking: {clean_summary}")
    print(f"[VOICE] Voice simulated successfully.")
    
    # Optional real voice - uncomment if you have pyttsx3
    # import pyttsx3
    # engine = pyttsx3.init()
    # engine.say(clean_summary)
    # engine.runAndWait()
    
    return clean_summary