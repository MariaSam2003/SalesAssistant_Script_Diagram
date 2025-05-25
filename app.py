
import streamlit as st
import asyncio
# Import agent and create_graph_from_script from Negotiation_Closing
# Note: create_graph_from_script will no longer be used for diagram generation in app.py,
# but the import might remain if other parts of Negotiation_Closing are still needed.
from Negotiation_Closing import agent
from Pdf_generator import generate_branded_pdf
from diagram_generator import generate_flowchart_image

# --------------------- UI Setup ---------------------
st.set_page_config("Sales Assistant", "centered")
st.title("📞 Sales Assistant")

framework_options = {
    "🔁 Auto (Recommended)": "auto",
    "🧠 Insight-Driven (Challenger)": "challenger",
    "💬 Conversation-Led (NEPQ)": "nepq",
    "❓ Problem-Focused (SPIN)": "spin",
    "💼 Qualification First (BANT)": "bant",
    "📈 ROI & Metrics-Driven (MEDDIC)": "meddic",
    "📋 Checklist-Based (Lite)": "lite"
}

# --------------------- Sidebar Inputs ---------------------
with st.sidebar:
    st.header("Context Inputs")
    industry = st.text_input("Industry")
    buyer_persona = st.text_input("Buyer Persona")
    offer = st.text_input("Offer")
    call_type = st.selectbox("Call Type", ["Cold", "Warm", "Referral"])
    # Added a default value for 'Sales Objective' for better initial display and to ensure it's not empty
    objective = st.text_input("Sales Objective", value="Negotiate and finalize product purchase")
    region = st.text_input("Region (Optional)")
    framework_label = st.selectbox("🎛️ Choose your script style:", list(framework_options.keys()))
    selected_framework = framework_options[framework_label]

    generate_button = st.button("📄 Generate Script & Diagram PDF")


# --------------------- Main Action ---------------------
if generate_button:
    with st.spinner("⏳ Generating your PDF..."):
        # Basic validation for essential inputs
        if not industry or not buyer_persona or not offer or not objective:
            st.error("Please fill in Industry, Buyer Persona, Offer, and Sales Objective.")
            st.stop() # Stop execution if essential fields are empty

        # Auto Framework logic
        if selected_framework == "auto":
            if "complex" in objective.lower() or "disrupt" in industry.lower():
                selected_framework = "challenger"
            elif "qualify" in objective.lower():
                selected_framework = "bant"
            elif "roi" in objective.lower() or "metrics" in objective.lower():
                selected_framework = "meddic"
            else:
                selected_framework = "spin"

        # Prompt creation for the AI agent
        # The prompt now explicitly tells the agent the product name to use
        prompt = f"""
Industry: {industry}
Persona: {buyer_persona}
Offer: {offer}
Call Type: {call_type}
Sales Objective: {objective}
Region: {region if region else "Not specified"}
Framework: {selected_framework}

The product being discussed is: {offer}. Ensure the agent uses the name "{offer}" explicitly when referring to the product in its dialogue, especially when highlighting features, value, or addressing objections.
"""

        # Run the negotiation agent to get the full multi-turn conversation
        response = asyncio.run(agent.run(prompt))
        final_script_content = response.output.reply

        # --- IMPORTANT CHANGE: Removed st.write(final_script_content) ---
        # This prevents the script from showing in the Streamlit UI.

        # Define a structured DOT code for a typical negotiation/closing flowchart.
        # This provides a more robust and predictable diagram structure, aligning with the desired schema.
        # This hardcoded structure replaces the dynamic parsing of the conversation for the diagram.
        structured_closing_dot_code = """
digraph G {
    rankdir=TB; // Top to Bottom flow
    node [shape=box, style="filled", fontname="Helvetica"]; // Default node style

    // Main Closing Path Nodes
    start_interest [label="Client Expresses Interest/Hesitation", shape=oval, fillcolor="lightgreen"];
    agent_acknowledge [label="Agent: Acknowledge & Propose Next Steps", fillcolor="lightblue"];
    client_objection [label="Client: Raises Objection", fillcolor="orange"];
    agent_handle_obj [label="Agent: Handle Objection", fillcolor="lightblue"];
    client_needs_info [label="Client: Needs More Info/Time", fillcolor="orange"];
    agent_propose_followup [label="Agent: Propose Follow-up/Next Action", fillcolor="lightblue"];
    client_ready_to_buy [label="Client: Ready to Proceed", fillcolor="lightgreen"];
    agent_finalize [label="Agent: Send Contract/Schedule Onboarding", fillcolor="lightblue"];

    // Specific Objection Branches (Examples)
    client_price_high [label="Client: Price Too High", fillcolor="red"];
    agent_handle_price [label="Agent: Discuss ROI/Payment Options/Discount", fillcolor="lightblue"];

    client_need_team_review [label="Client: Need to Consult Team", fillcolor="red"];
    agent_offer_team_meet [label="Agent: Offer to Join Meeting/Provide Info", fillcolor="lightblue"];

    client_considering_others [label="Client: Considering Other Options", fillcolor="red"];
    agent_provide_insights [label="Agent: Provide Competitive Insights", fillcolor="lightblue"];

    client_feature_uncertainty [label="Client: Uncertain About Feature", fillcolor="red"];
    agent_offer_demo [label="Agent: Offer Demo/Details", fillcolor="lightblue"];

    // Edges (Flow)
    start_interest -> agent_acknowledge [label="Initiates Closing"];
    agent_acknowledge -> client_objection [label="Client Responds"];

    // Main flow from objection handling
    client_objection -> agent_handle_obj [label="Agent Addresses"];
    agent_handle_obj -> client_ready_to_buy [label="Concern Resolved"];
    agent_handle_obj -> client_needs_info [label="Needs More Convincing"];

    client_needs_info -> agent_propose_followup [label="Agent Follow-up"];
    agent_propose_followup -> client_ready_to_buy [label="Proceeds After Follow-up"];
    agent_propose_followup -> start_interest [label="Re-engage Cycle"]; // Loop back for another attempt

    client_ready_to_buy -> agent_finalize [label="Commits to Purchase"];

    // Specific objection branches and their handling
    client_objection -> client_price_high [label="Pricing"];
    client_price_high -> agent_handle_price [label="Agent Handles Price"];
    agent_handle_price -> client_ready_to_buy [label="Price Resolved"];
    agent_handle_price -> client_needs_info [label="Still Hesitant on Price"];

    client_objection -> client_need_team_review [label="Team Review"];
    client_need_team_review -> agent_offer_team_meet [label="Agent Handles Team"];
    agent_offer_team_meet -> client_ready_to_buy [label="Team Buy-in"];
    agent_offer_team_meet -> client_needs_info [label="Team Needs More Time"];

    client_objection -> client_considering_others [label="Competition"];
    client_considering_others -> agent_provide_insights [label="Agent Handles Comparison"];
    agent_provide_insights -> client_ready_to_buy [label="Comparison Resolved"];
    agent_provide_insights -> client_needs_info [label="Still Comparing"];

    client_objection -> client_feature_uncertainty [label="Feature Concern"];
    client_feature_uncertainty -> agent_offer_demo [label="Agent Handles Feature"];
    agent_offer_demo -> client_ready_to_buy [label="Feature Understood"];
    agent_offer_demo -> client_needs_info [label="Still Unsure on Feature"];

    // End Node
    agent_finalize -> end_success [label="Deal Closed", shape=doublecircle, fillcolor="gold"];
    end_success [label="Success!"];
}
"""

        # Generate the flowchart image bytes using the pre-defined structured DOT code
        flowchart_image_bytes = generate_flowchart_image(structured_closing_dot_code)

        # Generate the branded PDF
        pdf_bytes = generate_branded_pdf(
            customer_logo_path="cust_logo.jfif",
            customer_name="ACME Inc.", # Placeholder, consider making this dynamic
            silni_logo_path="silni_logo.jfif",
            title="Enterprise Demo Call", # Placeholder, consider making this dynamic
            # Pass dynamic metadata from sidebar inputs
            metadata={"objective": objective, "framework": selected_framework},
            call_script_text=final_script_content, # Pass the actual generated script here
            flowchart_img=flowchart_image_bytes,   # Pass the generated flowchart image bytes
        )

        # Provide a download button for the generated PDF
        st.download_button(
            label="📄 Download Strategy PDF",
            data=pdf_bytes,
            file_name="deal_closing_strategy.pdf",
            mime="application/pdf"
        )