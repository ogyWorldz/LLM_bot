from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, request, jsonify
from collections import Counter
from nltk.corpus import stopwords
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import textwrap
import nltk
import re

load_dotenv(find_dotenv())
# embeddings = OpenAIEmbeddings() ##### this function appears to cause a 502 error. Could it be python version? Both appear to be 3.11


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



application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/youtubeChatAI')
def youtubeChatAI():
    return render_template('youtubeChatAI.html')

@application.route('/resume')
def resume():
    return render_template('resume.html')

@application.route('/resumeMatch')
def resumeMatch():
    return render_template('resume_match.html')

@application.route('/memegame')
def memegame():
    return render_template('memegame.html')

@application.route('/jobApplicationAnalyzer', methods=['GET', 'POST'])
def jobApplicationAnalyzer():
    if request.method == 'POST':
        resume = request.form['resume']
        job_description = request.form['job_description']

        percentage_score, missing_keywords = keyword_analysis(resume, job_description)

        return render_template('jobApplicationAnalyzer.html', score=percentage_score, missing_keywords=missing_keywords)

    return render_template('jobApplicationAnalyzer.html', score=None, missing_keywords=None)


@application.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    video_url = data['videoUrl']
    query = data['query']
    answer = 'this response is still under development.'
    return jsonify({'answer': answer})

# ########### jobApplicationAnalyzer 

# def keyword_analysis(resume, job_description):
#     # Load English stopwords
#     stop_words = set(stopwords.words('english'))

#     # Simple keyword analysis logic with stopwords removal
#     resume_words = [word.lower() for word in re.findall(r'\b\w+\b', resume) if word.lower() not in stop_words]
#     job_words = [word.lower() for word in re.findall(r'\b\w+\b', job_description) if word.lower() not in stop_words]

#     common_words = set(resume_words).intersection(job_words)

#     # Count occurrences of each word in the job description
#     missing_words_count = Counter(job_words)

#     # Subtract occurrences in the resume from the job description
#     for word in common_words:
#         missing_words_count[word] -= resume_words.count(word)

#     # Filter out words with zero or negative occurrences
#     missing_words_count = {word: count for word, count in missing_words_count.items() if count > 0}

#     # Get the top missing keywords ordered by occurrence
#     top_missing_keywords = [(keyword, count) for keyword, count in sorted(missing_words_count.items(), key=lambda x: x[1], reverse=True)[:10]]

#     percentage_score = round((len(common_words) / len(job_words)) * 100, 2)

#     return percentage_score, top_missing_keywords






# ###########



if __name__ == '__main__':
    application.run(debug=True)




############################################################################################################ -testing
############################################################################################################

# load_dotenv(find_dotenv())
# embeddings = OpenAIEmbeddings()


# application = Flask(__name__)

# @application.route('/')
# def index():
#     return render_template('index.html')




# def create_db_from_youtube_video_url(video_url):
#     loader = YoutubeLoader.from_youtube_url(video_url)
#     transcript = loader.load()

#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
#     docs = text_splitter.split_documents(transcript)

#     db = FAISS.from_documents(docs, embeddings)
#     return db


# def get_response_from_query(db, query, k=4):
#     docs = db.similarity_search(query, k=k)
#     docs_page_content = " ".join([d.page_content for d in docs])

#     chat = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0.2)

#     # Template to use for the system message prompt
#     template = """
#         You are a helpful assistant that that can answer questions about youtube videos 
#         based on the video's transcript: {docs}
        
#         Only use the factual information from the transcript to answer the question.
        
#         If you feel like you don't have enough information to answer the question, say "I don't know".
        
#         """

#     system_message_prompt = SystemMessagePromptTemplate.from_template(template)

#     # Human question prompt
#     human_template = "Answer the following question: {question}"
#     human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

#     chat_prompt = ChatPromptTemplate.from_messages(
#         [system_message_prompt, human_message_prompt]
#     )

#     chain = LLMChain(llm=chat, prompt=chat_prompt)

#     response = chain.run(question=query, docs=docs_page_content)
#     response = response.replace("\n", "")
#     return response, docs

# @application.route('/submit', methods=['POST'])
# def submit():
#     data = request.get_json()
#     video_url = data['videoUrl']
#     db = create_db_from_youtube_video_url(video_url)
#     query = data['query']
#     response, docs = get_response_from_query(db, query)
#     print(textwrap.fill(response, width=50))
#     return jsonify({'answer': response})

# if __name__ == '__main__':
#     application.run(debug=True)

