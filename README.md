Ever wish you could just talk to your Excel files and get answers? Well, now you can!

This project is like having a super-smart assistant for your spreadsheets. You can upload an Excel file, ask questions in plain English, and it'll give you neat insights and even create charts for you.

Here's what it can do:

Upload your Excel file: Just drag and drop! (One sheet, up to 500 rows for now).
It understands your data: No need to tell it what's what – it figures out your column names and what kind of data they hold (numbers, text, etc.).
Ask anything: Want to know the average sales? How many customers are in a certain region? Just ask!
Smart analysis: It can filter your data, group things together, and even do calculations like totals and averages.
See your data: It can create cool charts for you, like bar charts, histograms, and line charts, to help you visualize your information.
It's powered by Google: It uses the amazing Gemini AI (and guess what? The API is free!).
Ready to try it out? Here's how to get started:

Get your secret key: You'll need a "GEMINI_API_KEY" from Google. Once you have it, open your computer's terminal (or command prompt) and type this, replacing your_key_here with your actual key: export GEMINI_API_KEY=your_key_here
Install the necessary tools: In your terminal, go to the project's folder and type: pip install -r requirements.txt
Launch the assistant! Still in your terminal, type: streamlit run app.py
Just a couple of important notes:

Don't forget to replace your_key_here with your real Gemini API key.
Make sure your Excel sheet has headers (like "Name," "Age," "Sales") and a consistent layout.
Give it a try and make your Excel data talk! 😊


⚠️ Important Note
This app is an experimental conversational assistant and may occasionally produce errors or unexpected results due to limitations in data parsing or response interpretation.

For best results, try using simple, structured prompts like:

What is the average quantity sold per order?

Show a histogram of discount distribution.

Create a histogram of profit.

We’re continuously improving accuracy and flexibility. Thank you for trying it out!
