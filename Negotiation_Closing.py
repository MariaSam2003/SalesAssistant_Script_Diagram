
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
import re

# Define dependencies if needed (not required for simple example)
class Dependencies(BaseModel):
    pass
# Define the output format
class NegotiationOutput(BaseModel):
    reply: str = Field(description="A full multi-turn conversation between Client and Agent")

system_prompt = """
You are a persuasive, emotionally intelligent sales agent.
Your task is to simulate a multi-turn dialogue between a Client and an Agent.

Context: The client has already expressed interest and reached out regarding a specific product.
Your goal is to negotiate any remaining concerns, overcome objections, and successfully close the deal for the product. You are not making a cold call or conducting initial discovery; the client is already aware of the product.

Steps:
- Begin with the Agent acknowledging the client's interest and directly moving towards addressing potential barriers to purchase or proposing next steps for closing.
- Let the Client reply with emotions, questions, or objections related to the product or the deal.
- Use persuasive techniques (like Cialdini’s 6 principles, calibrated questions, tactical empathy) to address their concerns and build value.
- Respond step-by-step, not all at once.

Format the output like this:
Client: ...
Agent: ...

Also, for Client lines, insert inline tags where needed:
- [QUESTION: pricing]
- [EMOTION: hesitant]
- [OBJECTION: too expensive]
- [CUE: wants credibility]
- etc.

End with the Agent attempting to close or book next steps to finalize the purchase.

Stay conversational, natural, and helpful — avoid sounding robotic.
"""


# Create the agent
agent = Agent(
    model="openai:gpt-4o-mini",  # Or any other OpenAI model
    deps_type=Dependencies,
    output_type=NegotiationOutput,
    system_prompt= system_prompt,
)

# --- Persuasion Tools ---
@agent.tool
def authority(_: RunContext, product: str) -> str:
    """Use expert status or certifications to boost credibility."""
    return "We're certified leaders in this space, recognized by top industry reviewers."

@agent.tool
def scarcity(_: RunContext, product: str) -> str:
    """Mention limited availability or urgency to act."""
    return "We only have a few slots left for this month — just wanted to flag that for you."

@agent.tool
def liking(_: RunContext, product: str) -> str:
    """Use personal connection or compliments to build rapport."""
    return "I really appreciate how thoughtful you’ve been with your questions."

@agent.tool
def consensus(_: RunContext, product: str) -> str:
    """Show how others in similar situations made the decision."""
    return "Many others in your role found this solution really aligned with their goals."

@agent.tool
def consistency(_: RunContext, product: str) -> str:
    """Tie back to the client's earlier statements or goals."""
    return "Earlier you mentioned wanting better ROI — this fits directly with that."

@agent.tool
def emotional_persuasion(_: RunContext, emotion: str)-> str:
    """Acknowledge and respond to the client's emotions empathetically."""
    return f"I can hear the {emotion} in your voice — and it totally makes sense to feel that way."

@agent.tool
def tactical_empathy(_:RunContext,objection: str)-> str:
    """Label objections and show empathy."""
    return f"It sounds like you're concerned about {objection}. Let’s walk through that together."


def create_graph_from_script(script: str) -> str:
    """
    Parses a multi-turn script and generates a Graphviz DOT diagram.
    This version tries to include more detail on edges based on client tags.
    """

    dot_lines = [
        "digraph SalesFlow {",
        "    rankdir=TB;  // Top to Bottom flow",
        "    node [shape=box, style=filled, color=lightblue];",
        "    edge [fontsize=10];"  # Smaller font for edge labels
    ]

    lines = script.strip().split('\n')

    # Using unique IDs for nodes to handle potential identical text
    node_counter = 0
    previous_node_id = "Start"
    dot_lines.append(f'    "{previous_node_id}" [shape=circle, color=green, label="Call Start"];')

    for line in lines:
        if line.startswith("Client:"):
            node_counter += 1
            current_node_id = f"Client_{node_counter}"
            clean_line = line.replace('Client:', '').strip()

            # Extract tags for edge labels
            label_parts = []

            emotion_match = re.search(r"\[EMOTION:\s*(.+?)\]", clean_line, re.IGNORECASE)
            if emotion_match:
                label_parts.append(f"Emotion: {emotion_match.group(1)}")

            question_match = re.search(r"\[QUESTION:\s*(.+?)\]", clean_line, re.IGNORECASE)
            if question_match:
                label_parts.append(f"Q: {question_match.group(1)}")

            objection_match = re.search(r"\[OBJECTION:\s*(.+?)\]", clean_line, re.IGNORECASE)
            if objection_match:
                label_parts.append(f"Objection: {objection_match.group(1)}")

            cue_match = re.search(r"\[CUE:\s*(.+?)\]", clean_line, re.IGNORECASE)
            if cue_match:
                label_parts.append(f"Cue: {cue_match.group(1)}")

            edge_label = "Client speaks"
            if label_parts:
                edge_label = ", ".join(label_parts)

            # Remove tags from the node label
            node_label = re.sub(r'\[.*?\]', '', clean_line).strip()
            if not node_label:  # Fallback if only tags were present
                node_label = "Client Response"

            dot_lines.append(f'    "{current_node_id}" [label="Client: {node_label}", color=orange, shape=box];')
            dot_lines.append(f'    "{previous_node_id}" -> "{current_node_id}" [label="{edge_label}"];')
            previous_node_id = current_node_id

        elif line.startswith("Agent:"):
            node_counter += 1
            current_node_id = f"Agent_{node_counter}"
            clean_line = line.replace('Agent:', '').strip()

            dot_lines.append(f'    "{current_node_id}" [label="Agent: {clean_line}", color=lightblue, shape=box];')
            dot_lines.append(f'    "{previous_node_id}" -> "{current_node_id}" [label="Agent Responds"];')
            previous_node_id = current_node_id

    dot_lines.append("}")
    return "\n".join(dot_lines)
