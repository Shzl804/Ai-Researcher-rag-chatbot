from app.text_cleaner import clean_data


sample_text = """
Contact researcher@gmail.com.
Visit https://example.com.
This paper uses AI!!! @#$% and reports 95% accuracy.
"""


cleaned_text = clean_data(sample_text)

print("Original text:")
print(sample_text)

print("\nCleaned text:")
print(cleaned_text)