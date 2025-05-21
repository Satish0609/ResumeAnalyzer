from nlp_utils import clean_text

def load_jd(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    jd_path = "jd_input.txt"
    jd_text = load_jd(jd_path)
    print("Raw JD:\n", jd_text)

    cleaned_jd = clean_text(jd_text)
    print("\nCleaned JD:\n", cleaned_jd)
