from collections import Counter
from nltk.corpus import stopwords
import nltk
import re

# Download the stopwords dataset (run this once)
nltk.download('stopwords')

def keyword_analysis(resume, job_description):
    # Load English stopwords
    stop_words = set(stopwords.words('english'))

    # Simple keyword analysis logic with stopwords removal
    resume_words = [word.lower() for word in re.findall(r'\b\w+\b', resume) if word.lower() not in stop_words]
    job_words = [word.lower() for word in re.findall(r'\b\w+\b', job_description) if word.lower() not in stop_words]

    common_words = set(resume_words).intersection(job_words)

    # Count occurrences of each word in the job description
    missing_words_count = Counter(job_words)

    # Subtract occurrences in the resume from the job description
    for word in common_words:
        missing_words_count[word] -= resume_words.count(word)

    # Filter out words with zero or negative occurrences
    missing_words_count = {word: count for word, count in missing_words_count.items() if count > 0}

    # Get the top missing keywords ordered by occurrence
    top_missing_keywords = [(keyword, count) for keyword, count in sorted(missing_words_count.items(), key=lambda x: x[1], reverse=True)[:10]]

    percentage_score = round((len(common_words) / len(job_words)) * 100, 2)

    return percentage_score, top_missing_keywords