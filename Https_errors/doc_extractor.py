#to capture the HTTP requests into a file to analyze it later run: "python3.12 doc_extractor.py | grep "HTTP Request" > http_logs.txt"

import agentic_doc.parse
from agentic_doc.parse import parse_documents
import time

#staging key - export VISION_AGENT_API_KEY=OW5iazhpMmd0NmU2Mmc0ZTk0aWhmOmdRQTlUcW9IR2w5QnVhandhT1d3WEsyRmdhekZ2MEMy
#production key - export VISION_AGENT_API_KEY=MGxjNWFzcG9naHBub3pvNDhnOGZmOkQ1dmhRWHVFV2ZHbHFHVFRTTjZydXhQOU03MDZHMFNo
agentic_doc.parse._ENDPOINT_URL = "https://api.va.staging.landing.ai/v1/tools/agentic-document-analysis"
# Parse a local file '/Users/macbookpro/Downloads/Marco Aurelio-Meditaciones.pdf'
start_time = time.time()

results = parse_documents(["Https_errors/PDF/Marco_Aurelio_Meditaciones_1000_pages.pdf"])
parsed_doc = results[0]
#print(parsed_doc.markdown)  # Get the extracted data as markdown
print(parsed_doc.chunks)  # Get the extracted data as structured chunks of content

try:
    text = parsed_doc.text  # Most common
except AttributeError:
    try:
        text = parsed_doc.get_text()  # Alternate possibility
    except AttributeError:
        text = str(parsed_doc)  # Fallback

# Save to a text file
with open("output.txt", "w", encoding="utf-8") as file:
    file.write(text)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time:.2f} seconds")