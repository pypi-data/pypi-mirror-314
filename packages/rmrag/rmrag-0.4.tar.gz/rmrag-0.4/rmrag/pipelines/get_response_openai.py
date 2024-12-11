from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, HumanMessage

class Chatbot_OpenAI:
    def __init__(self, 
                 vectorstore, 
                 k=10, 
                 score_threshold=0.7, 
                 temperature=0.1, 
                 chat_history=[AIMessage(content="Hej. Jeg er en AI-bot. Hvordan kan jeg hjælpe dig?")],
                 system_prompt=ChatPromptTemplate.from_messages([
        """
        "system", "Du er en chatbot, hjælper med at svare på spørgsmål om den kontekst, du er givet. Besvar brugerens spørgsmål baseret på nedenstående kontekst. 
        
        Du oplyser altid, alle de steder i konteksten, du har fundet svaret med "Kilde: ", indsætter den på en linje nedenfor.  

        {context}

        Du giver altid det svar i konteksten, der bedst kan besvare spørgsmålet, men er du ikke sikker på svaret, siger du altid, at du ikke er sikker.
        """,
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
                                                                ])
    ):      
        self.vectorstore = vectorstore
        self.k = k
        self.score_threshold = score_threshold
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=temperature)
        self.chat_history= chat_history
        self.system_prompt = system_prompt

    def get_context_retriever_chain(self):
        try:
            llm = self.llm

            retriever = self.vectorstore.as_retriever(
                search_type="similarity_score_threshold", 
                search_kwargs={"k": self.k, "score_threshold": self.score_threshold}
            )

            prompt = ChatPromptTemplate.from_messages([
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                ("user", "På baggrund af ovenstående samtale, generer en søgeforespørgsel til at slå op i, for at få oplysninger der er relevante for samtalen")
            ])

            retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
            
            return retriever_chain
    
        except Exception as e:
            print("An error occurred while creating the context retriever chain:", e)
            return None

    def get_conversational_rag_chain(self, retriever_chain): 
        try:
            llm = self.llm
            
            prompt = self.system_prompt
            
            stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
            
            return create_retrieval_chain(retriever_chain, stuff_documents_chain)
        
        except Exception as e:
            print("An error occurred while creating the conversational RAG chain:", e)
            return None
        
    def get_response(self, user_input):
        try:
            retriever_chain = self.get_context_retriever_chain()
            conversation_rag_chain = self.get_conversational_rag_chain(retriever_chain)
            response = conversation_rag_chain.invoke({
                "chat_history": self.chat_history,
                "input": user_input
            })
            
            # Extract source documents and chunks from response["context"]
            source_info = []
            for doc in response["context"]:
                source_info.append({
                    'metadata': doc.metadata,
                    'page_content': doc.page_content
                })
            
            # Update chat history with the new interaction - gives chatbot memory
            self.chat_history.extend([
                HumanMessage(content=user_input),
                AIMessage(content=response['answer'])
            ])
            
            # Return both the answer and source information
            return {
                'answer': response['answer'],
                'sources': source_info
            }

        except Exception as e:
            print("An error occurred during response generation:", e)
            return {
                'answer': "An error occurred, and we couldn't process your request.",
                'sources': []
            }