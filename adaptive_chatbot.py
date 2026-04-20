import gradio as gr

def update_profile(user_message, profile):
    profile["messages"] += 1
    lower = user_message.lower()

    if len(user_message.split()) > 15 or "explain" in lower or "why" in lower:
        profile["needs_simple_mode"] = True

    if "brief" in lower or "short" in lower or "quick" in lower:
        profile["preferred_style"] = "brief"
    elif "detail" in lower or "detailed" in lower:
        profile["preferred_style"] = "detailed"

    if "example" in lower or "for instance" in lower:
        profile["show_examples"] = True

    return profile


def generate_reply(message, profile):
    lower = message.lower()

    if "breakfast" in lower:
        if profile["preferred_style"] == "brief":
            answer = "A healthy breakfast can be Greek yogurt with fruit, oats, or eggs with toast."
        elif profile["preferred_style"] == "detailed":
            answer = (
                "A healthy breakfast should include protein, fiber, and enough calories to keep you full for several hours. "
                "Protein helps satiety and muscle maintenance, while fiber supports digestion and steadier energy. "
                "Good options include Greek yogurt with fruit and chia seeds, oats with milk and nuts, or eggs with whole grain toast."
            )
        else:
            answer = "A healthy breakfast should include protein and fiber, such as yogurt with fruit or eggs with toast."

    elif "protein" in lower or "vegetarian" in lower:
        if profile["preferred_style"] == "detailed":
            answer = (
                "Vegetarians can increase protein intake by including a protein source in each meal and snack. "
                "Useful foods include paneer, tofu, lentils, chickpeas, beans, Greek yogurt, milk, and eggs if included in the diet. "
                "A practical strategy is to eat protein at breakfast, lunch, and dinner instead of depending on only one meal."
            )
        elif profile["preferred_style"] == "brief":
            answer = "Vegetarians can eat more protein through paneer, tofu, dal, yogurt, beans, and eggs."
        elif profile["needs_simple_mode"]:
            answer = "Here is the simple version: add one protein food to each meal, like paneer, tofu, dal, yogurt, or eggs."
        else:
            answer = "Vegetarians can raise protein intake by adding paneer, tofu, dal, beans, yogurt, or eggs across the day."

    elif "weight" in lower or "fat loss" in lower or "lose weight" in lower:
        if profile["preferred_style"] == "detailed":
            answer = (
                "Weight loss usually improves when calorie intake is controlled, protein is adequate, and activity is consistent. "
                "A simple method is to build meals around protein and vegetables first, then add moderate portions of carbs and healthy fats. "
                "Walking, resistance training, and consistent meal timing can also help support fat loss."
            )
        elif profile["preferred_style"] == "brief":
            answer = "For weight loss, focus on a calorie deficit, enough protein, and regular walking or exercise."
        else:
            answer = "Weight loss usually improves with calorie control, adequate protein, and consistent physical activity."

    else:
        if profile["preferred_style"] == "detailed":
            answer = "Here is a more detailed explanation with practical guidance and examples."
        elif profile["needs_simple_mode"]:
            answer = "Here is the simple version: focus on one clear step at a time."
        else:
            answer = "Here is a standard explanation with moderate detail."

    if profile["show_examples"]:
        answer += " Example: breakfast could be Greek yogurt, fruit, and nuts."

    return answer

def adapt_ui(profile):
    if profile["needs_simple_mode"]:
        placeholder = "Ask in any way — I will simplify the answer automatically"
        mode_text = "## Adaptive Chatbot\n**Current mode:** Simple explanation mode"
    else:
        placeholder = "Ask your question here"
        mode_text = "## Adaptive Chatbot\n**Current mode:** Standard mode"

    style_text = f"**Response style:** {profile['preferred_style'].title()}"

    return (
        gr.Textbox(placeholder=placeholder, label="Your message"),
        gr.Markdown(value=mode_text),
        gr.Markdown(value=style_text)
    )


def chat(message, history, profile):
    profile = update_profile(message, profile)
    reply = generate_reply(message, profile)

    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply}
    ]

    textbox_update, mode_update, style_update = adapt_ui(profile)
    return history, profile, textbox_update, mode_update, style_update


def reset_app():
    profile = {
        "messages": 0,
        "needs_simple_mode": False,
        "preferred_style": "balanced",
        "show_examples": False
    }
    textbox_update, mode_update, style_update = adapt_ui(profile)
    return [], profile, textbox_update, mode_update, style_update


with gr.Blocks(title="Adaptive Chatbot") as demo:
    gr.Markdown("# AI-Based Adaptive HCI Demo")

    mode_text = gr.Markdown("## Adaptive Chatbot\n**Current mode:** Standard mode")
    style_text = gr.Markdown("**Response style:** Balanced")

    chatbot = gr.Chatbot(height=400)
    msg = gr.Textbox(label="Your message", placeholder="Ask your question here")
    send = gr.Button("Send")
    clear = gr.Button("Reset")

    gr.Markdown(
        "### Adaptive features\n"
        "- switches to simpler mode for more complex questions\n"
        "- changes style to brief or detailed based on wording\n"
        "- adds examples when requested"
    )

    profile_state = gr.State({
        "messages": 0,
        "needs_simple_mode": False,
        "preferred_style": "balanced",
        "show_examples": False
    })

    send.click(
        chat,
        inputs=[msg, chatbot, profile_state],
        outputs=[chatbot, profile_state, msg, mode_text, style_text]
    )

    msg.submit(
        chat,
        inputs=[msg, chatbot, profile_state],
        outputs=[chatbot, profile_state, msg, mode_text, style_text]
    )

    clear.click(
        reset_app,
        outputs=[chatbot, profile_state, msg, mode_text, style_text]
    )

if __name__ == "__main__":
    demo.launch()