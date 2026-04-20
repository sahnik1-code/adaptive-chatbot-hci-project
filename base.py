import gradio as gr

def respond(message, history):
    return f"You said: {message}"

demo = gr.ChatInterface(
    fn=respond,
    title="Base Chatbot Demo",
    description="A simple chatbot built from an official Gradio-style starter pattern."
)

if __name__ == "__main__":
    demo.launch()