import requests

from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.get('/ask')
def ask(prompt):
        res = requests.post('http://ollama:11434/api/generate', 
                            json= {"prompt": prompt,
                                   "stream": False,
                                   "model": "deepseek-r1:7b"})
        
        return Response(content=res.text, media_type="application/json")