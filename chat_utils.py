import json
import os
from rag_pipeline import get_relevant_docs
import google.generativeai as genai
from logger_utils import create_log_entry
from web_search_utils import get_web_context

def get_chat_file(agent_key):
    if "quiz" in agent_key:
        return "chat_history_quiz.json"
    else:
        return "chat_history_tutor.json"


def load_chat_history(agent_key):
    chat_file = get_chat_file(agent_key)
    if os.path.exists(chat_file):
        with open(chat_file, "r") as f:
            return json.load(f)
    return []

def save_chat_history(chat_history, agent_key):
    chat_file = get_chat_file(agent_key)
    with open(chat_file, "w") as f:
        json.dump(chat_history, f, indent=2)

def delete_chat(index, chat_history, agent_key=None):
    if 0 <= index < len(chat_history):
        del chat_history[index]
        if agent_key:
            save_chat_history(chat_history, agent_key)
    return chat_history


# Configure the Gemini API - set your API key as environment variable GOOGLE_API_KEY
api_key = os.environ.get("GOOGLE_API_KEY", "API_KEY_HERE")
genai.configure(api_key=api_key)

def local_llm_generate(prompt: str) -> str:
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text


def classify_query(query):
    classification_prompt = f"""
Is the following question related to network security, cybersecurity, cryptography, or computer security topics?
Answer with only "YES" or "NO".

Question: {query}

Answer:"""
    
    try:
        response = local_llm_generate(classification_prompt).strip().upper()
        return "YES" in response
    except Exception as e:
        print(f"Classification error: {e}")
        return False


def get_bot_response(user_query, current_chat):
    is_network_security_query = classify_query(user_query)
    
    use_web_search = False
    web_references = []
    docs = []
    context = ""
    
    if is_network_security_query:
        docs = get_relevant_docs(user_query)
        # docs can be None if DB error
        if docs:
            context = "\n".join([d.page_content for d in docs])
        
        if not docs or len(context.strip()) < 100:
            use_web_search = True
            web_context, web_references = get_web_context(user_query)
            context = web_context if web_context else "No relevant information found."
    else:
        use_web_search = True
        web_context, web_references = get_web_context(user_query)
        context = web_context if web_context else "No relevant information found."

    conversation_context = ""
    for msg in current_chat["messages"][:-1]:
        conversation_context += f"User: {msg['user']}\nBot: {msg['bot']}\n"

    if use_web_search:
        prompt = (
            f"{conversation_context}\nContext from web search:\n{context}\n\n"
            f"You are a helpful AI assistant. Answer the user's question based on the context provided.\n"
            f"User Question: {user_query}\nAnswer below:\n"
        )
    else:
        prompt = (
            f"{conversation_context}\nContext:\n{context}\n\n"
            f"You are a networksecurity tutor. Explain clearly and concisely.\n"
            f"User Question: {user_query}\nAnswer below:\n"
        )

    try:
        bot_response = local_llm_generate(prompt)
    except Exception as e:
        return f"I encountered an error generating a response: {str(e)}"

    if use_web_search and web_references:
        bot_response += "\n\n**Web References:**\n"
        for ref in web_references:
            bot_response += f"- [{ref['title']}]({ref['url']})\n"
    else:
        sources = []
        if docs:
            for d in docs:
                src = d.metadata.get("source", "Unknown Source")
                sources.append(src)
        if sources:
            bot_response += "\n\n**Sources:** " + ", ".join(set(sources))

    create_log_entry(user_query, docs if docs else [], bot_response, agent_type="tutor")

    return bot_response
