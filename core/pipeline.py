import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

class DocumentAuditorEngine:
    """
    Core data-processing engine. Handles explicit document file ingestion, 
    vector transformations, and context-bound database retrieval mapping.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        self.llm = ChatOpenAI(
            model="gpt-4o-mini", 
            openai_api_key=api_key, 
            temperature=0  # Guarantees rigid compliance answers with zero creative drift
        )

    def process_document(self, file_path: str) -> FAISS:
        """
        Extracts raw textual strings by dynamically matching file extensions 
        to specific low-level system parser engines.
        """
        _, file_extension = os.path.splitext(file_path.lower())
        
        # Explicit parser routing architecture
        loader_routing_map = {
            ".pdf": PyPDFLoader,
            ".docx": Docx2txtLoader,
            ".txt": TextLoader,
            ".csv": CSVLoader
        }
        
        if file_extension not in loader_routing_map:
            raise ValueError(f"System exception: Stream extension '{file_extension}' rejected by core loader.")
            
        SelectedLoader = loader_routing_map[file_extension]
        loader = SelectedLoader(file_path)
        raw_docs = loader.load()
        
        # Consistent document text fragmentation standard
        splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
        chunks = splitter.split_documents(raw_docs)
        
        vector_store = FAISS.from_documents(chunks, self.embeddings)
        return vector_store

    def execute_audit_query(self, vector_store: FAISS, query: str) -> Dict[str, Any]:
        """Runs custom deterministic context matrix bindings matching user intent."""
        retriever = vector_store.as_retriever(search_kwargs={"k": 4})
        
        system_instructions = (
            "You are operating as an automated enterprise compliance auditing engine.\n"
            "Analyze the verified context sub-segments with high strictness.\n"
            "Synthesize an objective analysis answering the execution query using ONLY the verified context text below. "
            "If the empirical data cannot explicitly substantiate the answer, respond with: "
            "'CRITICAL: Compliance dataset insufficient to verify query target.'\n\n"
            "Verified Context Data:\n{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_instructions),
            ("human", "{input}"),
        ])
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        retrieved_docs = retriever.invoke(query)
        formatted_prompt = prompt.invoke({
            "context": format_docs(retrieved_docs),
            "input": query
        })
        
        model_output = self.llm.invoke(formatted_prompt)
        
        return {
            "answer": model_output.content,
            "context": retrieved_docs
        }
    