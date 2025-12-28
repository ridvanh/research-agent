from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import textwrap
import os
import time
import http.client

SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive']
MAX_CHARS_PER_SLIDE = 800

def safe_execute(request_fn, retries=3, delay=2):
    for i in range(retries):
        try:
            return request_fn()
        except http.client.IncompleteRead as e:
            print(f"IncompleteRead: retrying ({i+1}/{retries})...")
            time.sleep(delay)
    raise RuntimeError("Failed after retries due to IncompleteRead")

def auth_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token,json', 'w') as token:
            token.write(creds.to_json())

    return creds

def create_presentation(service, title="AI Research Summary"):
    presentation = service.presentations().create(body={"title": title}).execute()
    return presentation

def split_text_into_chunks(text, max_chars=MAX_CHARS_PER_SLIDE):
    words = text.split()
    chunks = []
    chunk = ""

    for word in words:
        if len(chunk) + len(word) + 1 <= max_chars:
            chunk += (" " if chunk else "") + word
        else:
            chunks.append(chunk)
            chunk = word

    if chunk:
        chunks.append(chunk)

    return chunks

def create_slide(service, presentation_id, title, content):
    requests = [
        {
            "createSlide": {
                "slideLayoutReference": {
                    "predefinedLayout": "TITLE_AND_BODY"
                }
            }
        },
        {
            "insertText": {
                "objectId": "title",
                "text": title
            }
        },
        {
            "insertText": {
                "objectId": "body",
                "text": content
            }
        }
    ]
    safe_execute(lambda: service.presentations().batchUpdate(
        presentationId = presentation_id,
        body={"requests": requests}
    ).execute())

def generate_slides(papers):
    creds = auth_google()
    service = build('slides', 'v1', credentials=creds)

    pres_id = create_presentation(service)

    for paper in papers:
        title = paper['title']
        base_info = (f"Authors: {', '.join(paper['authors'])}\n"
                     f"Published: {paper['published']}\nPDF: {paper['pdf_url']}\n\n")
        summary = paper['summary']
        full_text = base_info + summary


        chunks = split_text_into_chunks(full_text)
        for chunk in chunks:
            create_slide(service, pres_id, title, chunk)

    print(f"Slides created: https://docs.google.com/presentation/d/{pres_id}")

# Example input
papers = [{
    'title': 'Exploring Mistral Models in Local AI Agents',
    'authors': ['Jane Doe', 'John Smith'],
    'published': '2025-07-12',
    'pdf_url': 'https://arxiv.org/pdf/1234.56789.pdf',
    'summary': 'This paper investigates the effectiveness of Mistral models deployed in local AI agents...'
}]

generate_slides(papers)


