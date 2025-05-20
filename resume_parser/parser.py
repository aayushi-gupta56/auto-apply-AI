import pdfplumber
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
import operator

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_keywords(text, max_keywords=20):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    kw_model = KeyBERT()
    known_skills = [ "SpringBoot", "AWS cloud platform", "Rest API", "DS/Algo", "Java", "C++",
        "Splunk", "React", "SQL", "Swagger", "Postman", "Sonar", "OS", "AWS AI services",
        "TensorFlow", "Flask", "Nextjs", "DBMS", "Computer Networks", "Leadership",
        "Teamwork", "Communication", "Problem solving", "Public Speaking", "Python", "AWS"
    ]
    known_skills = [word.lower() for word in known_skills]
    free_keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words='english', 
                        use_mmr=True, diversity=0.7, top_n=20)
    guided_keywords = kw_model.extract_keywords(text, candidates=known_skills, top_n=15)
    merged = {kw: score for kw, score in free_keywords}
    for kw, score in guided_keywords:
        if kw not in merged or score > merged[kw]:
            merged[kw] = score
    final_keywords = sorted(merged.items(), key=operator.itemgetter(1), reverse=True)
    return [kw for kw,_ in final_keywords]

def parse_resume(file_path):
    if not file_path.endswith('.pdf'):
        raise ValueError("Unsupported file type. Please upload PDF only.")
    text = extract_text_from_pdf(file_path)
    keywords = extract_keywords(text)
    return text, keywords

# if __name__ == "__main__":
#     text = 'Developed and implemented batch user provisioning process using SpringBoot, AWS ECS and EventBridge to deliver user files to a vendor via a secure FTP on a daily basis. The solution transformed manual provisioning process to automated system improving efficiency and compliance with HR hierarchy information'
#     key = extract_keywords(text)
#     print(key)
