

class PromptService:
    def __init__(self):
        pass

    def getBasePrompt(self):
        return """
        You are a helpful assistant that can answer questions and help with tasks.
        """
    
    def getLucidPrompt(self, context: str, question: str):
        return f"""
        I'm attaching a Lucid diagrams to this message. Please analyze the diagram and answer the question.
        Context: {context}
        Question: {question}
        """
    
    def getWikiPrompt(self, context: str, question: str):
        return f"""
        Below is the context of the wiki document. Please analyze the context and answer the question.
        Context: {context}
        Question: {question}
        """
    
    def getPromptRules(self):
        return """
        # Analysis rules
        - You are an expert in the context of the document.
        - You are able to answer questions about the document.
        - You are able to provide detailed analysis of the document.
        - You are able to provide detailed analysis of the document.
        - Don't make up information.
        - Don't hallucinate.
        - If you don't know the answer, say no.
        - Only answer the question based on the context.
        - Convert the summarization into a HTML markdown format.
        - HTML markdown format rules:
            - Use <h1> for headers
            - Use <b> for bold
            - Use <i> for italic
            - Use <ul> for unordered lists
            - Use <ol> for ordered lists
            - Use <a> for links
        """
    
    