from setuptools import setup, find_packages

setup(
    name='rmrag',
    version='0.4',
    packages=find_packages(exclude=["tests*"]),
    install_requires=[],
    author='Lasse Tranekjær Leed',
    author_email='lasseleed@gmail.com',
    description='RAG functions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9']
)

#0.2 = added tests for all function + get_response into class 
#0.3 = Fixed tests and added Chatbot_OpenSource
#0.3.1 = Updated Chatbot_OpenAI and made default model to GPT-4o mini
#0.3.2 = Fixed show_progress_bar in load_faiss_vectorstore
#0.3.3 = No longer forcing specific models
#0.3.4 = corrected to lower capital letters in name of module directory_into_faiss
#0.3.5 = updated imports that will be deprecated in langchain 1.0
#0.4 = Updated chatbots with memory and sources 