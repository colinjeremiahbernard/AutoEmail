from groq import Groq
import os
os.environ['GROQ_API_KEY'] = '***REMOVED***'
try:
    client = Groq()
    response = client.chat.completions.create(model='llama-3.1-8b-instant', messages=[{'role':'user', 'content':'hi'}])
    print("SUCCESS")
except Exception as e:
    print(repr(e))
