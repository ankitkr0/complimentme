from flask import Flask, request, render_template, flash
import groq  # Ensure this import is correct based on how you've installed the Groq client library
from dotenv import load_dotenv
import os 
import secrets

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a random secret key
app.secret_key = os.getenv('SECRET_KEY')  # Ensure you have SECRET_KEY defined in your .env file

def generate_compliment(name, feeling, rant):
  client = groq.Groq()  # Assuming Groq() is the correct way to instantiate your client
  completion = client.chat.completions.create(
      model="llama3-70b-8192",
      messages=[
          {"role": "system", "content": "You are a compassionate friend who provides thoughtful and uplifting compliments. Your goal is to make the user feel valued and understood. Use one emoji at the end to add warmth. \n\nBe a nice person and comfort this person. Compliment them genuinely, as if you are a close friend. Keep your response under 150 words, ensuring it sounds heartfelt. Consider the user's name, their feelings, and any context they provide in their rant. Offer actionable advice or encouragement that resonates with their situation."},
          {"role": "user", "content": name},
          {"role": "user", "content": feeling},
          {"role": "user", "content": rant}
      ],
      temperature=1,
      max_tokens=1024,
      top_p=1,
      stream=True,
      stop=None
  )
  compliment = ""
  for chunk in completion:
      compliment += chunk.choices[0].delta.content or ""
  return compliment

@app.route('/', methods=['GET', 'POST'])
def index():
  # Initialize variables to None or default values
  name = None
  feeling = None
  rant = None

  if request.method == 'POST':
      name = request.form.get('name')
      feeling = request.form.get('feeling')
      rant = request.form.get('rant')

      # Check if all fields are provided
      if not (name and feeling and rant):
          flash("All fields are required.")
          return render_template('form.html')

      # Generate compliment if all fields are present
      compliment = generate_compliment(name, feeling, rant)
      return render_template('result.html', compliment=compliment)

  # This will execute if the method is 'GET' or if the POST check fails
  return render_template('form.html')
  
if __name__ == '__main__':
  app.run(debug=True)
