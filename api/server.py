from flask import Flask, render_template, request, redirect, url_for, flash
import openai
import markdown
import os
from serverless_wsgi import handle_request

app = Flask(__name__)

# Configuration
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key_here")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mylocaldb.sqlite') 
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve form data
        date = request.form.get('date')
        location = request.form.get('location')
        description = request.form.get('description')
        objective = request.form.get('objective')
        entities = request.form.get('entities')
        details = request.form.get('details')
        opinions = request.form.get('opinions')
        context = request.form.get('context')
        actions = request.form.get('actions')
        contact = request.form.get('contact')

        # Create a prompt for the news article
        prompt_text = f"escribe un artículo para una web usando la siguiente información: {location} {description} {objective} {entities} {details} {opinions} {context} {actions} {contact}. Remember to use paragraphs and separate them with a line break. After the article, make a section called social media and write 3 proposals for instagram posts with emoticons and hashtags"

        # Use OpenAI API to generate the news content
        try:
            # Setting up the messages for chat-like interaction
            messages = [
                {"role": "system", "content": "You are a helpful assistant who specializes in writing articles for websites. Generate a news article for a website based on the following information. Remember to make it SEO friendly:"},
                {"role": "user", "content": prompt_text}
            ]
            
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Assuming GPT-4 is available and the correct model name
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            # Extracting the content of the assistant's message
            news_content = response.choices[0].message['content'].strip()
            
            # Convert markdown to HTML
            news_content_html = markdown.markdown(news_content)
    
            flash(news_content_html, 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(str(e), 'danger')
            return redirect(url_for('index'))

    return render_template('form.html')

# Handle serverless invocation
def lambda_handler(event, context):
    return handle_request(app, event, context)
