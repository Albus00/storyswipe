from better_profanity import profanity

SHORTENINGS = {"AITA": "Am I the asshole?",}

def filter_swear_words(text):
  profanity.load_censor_words()
  return profanity.censor(text)

def filer_shortening(text):
  for shortening, full_form in SHORTENINGS.items():
    text = text.replace(shortening, full_form)
  return text

# # Example usage
# text = "This is a sentence with fuck and shit and bullshit for AITA."
# filtered_text = filter_swear_words(text)
# filtered_text = filer_shortening(filtered_text)
# print(filtered_text)