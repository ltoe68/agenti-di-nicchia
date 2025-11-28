import os
import base64
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage

def get_llm():
    # Force GPT-4o or GPT-4-Turbo for Vision
    model_name = os.getenv("LLM_MODEL", "gpt-4o")
    return ChatOpenAI(temperature=0, model_name=model_name, max_tokens=1000)

def encode_image(image_file):
    """Encodes a file object to base64 string."""
    return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_label(image_file):
    """
    Sends the image to GPT-4 Vision for compliance analysis.
    """
    llm = get_llm()
    base64_image = encode_image(image_file)
    
    system_prompt = """You are a Food Regulatory Compliance Expert for the EU and FDA markets.
    Your task is to analyze the provided food label image and identify potential non-compliance issues.
    
    CHECKLIST:
    1. **Allergens**: Are common allergens (Milk, Soy, Nuts, Wheat, etc.) clearly emphasized (Bold, Italic, or Uppercase) in the ingredients list?
    2. **Net Quantity**: Is the net weight/volume clearly visible and in the bottom 30% of the label?
    3. **Nutrition Facts**: Is the nutrition table present and legible?
    4. **Health Claims**: Are there any suspicious health claims (e.g. "Cures cancer", "Instant weight loss")?
    
    OUTPUT FORMAT:
    Provide a structured report in Markdown:
    - **Status**: [PASS / FAIL / WARNING]
    - **Summary**: Brief overview.
    - **Detailed Checks**:
        - [ ] Allergens: ...
        - [ ] Net Quantity: ...
        - [ ] Nutrition Facts: ...
        - [ ] Claims: ...
    - **Recommendations**: What to fix.
    """
    
    human_message = HumanMessage(
        content=[
            {"type": "text", "text": "Analyze this food label for regulatory compliance."},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                },
            },
        ]
    )
    
    try:
        response = llm.invoke([SystemMessage(content=system_prompt), human_message])
        return response.content
    except Exception as e:
        return f"Error analyzing image: {e}"
