
import os
import time
from pyngrok import ngrok


public_url = ngrok.connect(8501)
print("Public URL:", public_url)

os.system("streamlit run app.py &")


time.sleep(5)

print("Your Streamlit app is live at:", public_url)
