from pathlib import Path
from typing import Dict
import xml.etree.ElementTree as ET

from consilio.utils import load_prompt_template, render_prompt, query_claude
from consilio.utils import save_interaction


@save_interaction("assemble")
def assemble(doc: Path, context: Dict[str, str]) -> str:
    print("[👀] Preparing an assembly of different perspectives ...")

    statement = doc.read_text()
    prompts = load_prompt_template("Assemble")
    system_prompt = render_prompt(prompts.system, context)
    user_context = {"DECISION": statement}
    user_context.update(context)
    user_prompt = render_prompt(prompts.user, user_context)

    # Query Claude
    response = query_claude(
        user_prompt=user_prompt,
        system_prompt=system_prompt,
        assistant="<perspectives>",
        temperature=0.8,
    )
    return "<perspectives>" + response.content


def xml_to_markdown(xml_string: str) -> str:
    """Convert XML document to markdown format."""
    # Parse XML
    root = ET.fromstring(xml_string)

    # Initialize markdown output
    markdown = []

    # Process each perspective
    for perspective in root.findall("perspective"):
        # Add title as h2
        title_element = perspective.find("title")
        title = title_element.text if title_element is not None else "No Title"
        markdown.append(f"## {title}\n")

        # Add relevance as italicized text
        relevance_element = perspective.find("relevance")
        relevance = (
            relevance_element.text if relevance_element is not None else "No Relevance"
        )
        markdown.append(f"*{relevance}*\n")

        # Process questions
        questions = perspective.find("questions")
        if questions is not None:
            markdown.append("\n**Key Questions:**\n")
            for question in questions.findall("question"):
                markdown.append(f"- {question.text}\n")

        # Add spacing between perspectives
        markdown.append("\n")

    # Join all lines and return
    return "".join(markdown)


# if __name__ == "__main__":
#     context = {
#         "domain": "NZ-based B2C iOS app startup that are pre-product-market-fit",
#         "user_role": "Solo Founder",
#         "perspective": "bootstrapped founder, who successfully navigated pre-PMF phase with limited capital with a successful exit",
#     }
#     doc_path = Path(__file__).parent.parent / "Decisions/BankLoan.md"
#     response = assemble(doc=doc_path, context=context)
#     print(response)
#     print(xml_to_markdown(escape_xml_string(response)))

#     response = escape_xml_string(
#         """
# <perspectives>
#   <perspective>
#     <title>Exit-Experienced M&A Advisor specializing in small business sales</title>
#     <relevance>Critical for validating the feasibility and timeline of the traditional business unit sale, which directly impacts the need for and risk of the loan</relevance>
#     <questions>
#       <question>Based on current market conditions, how realistic are the broker valuations, and what factors could extend the sale timeline beyond 6 months?</question>
#       <question>What specific preparation steps could accelerate the sale process while maintaining optimal valuation?</question>
#       <question>How might using the business as loan collateral impact potential buyers' interest or the sale process?</question>
#     </questions>
#   </perspective>

#   <perspective>
#     <title>Pre-PMF Startup CFO with experience in dual business model transitions</title>
#     <relevance>Can provide insights on managing cash flow during the critical period of transitioning from traditional to new business model while optimizing runway</relevance>
#     <questions>
#       <question>What alternative financial instruments or strategies could provide similar runway extension with less risk than a traditional bank loan?</question>
#       <question>How might the monthly loan payments impact your ability to pivot or respond to product-market fit discoveries?</question>
#       <question>What specific financial metrics should be tracked to ensure the loan doesn't become a burden if the sale process extends beyond expected timeline?</question>
#     </questions>
#   </perspective>

#   <perspective>
#     <title>Product-Market Fit Achievement Expert who bootstrapped to exit</title>
#     <relevance>Essential for evaluating whether additional runway from loan will meaningfully contribute to achieving product-market fit</relevance>
#     <questions>
#       <question>Based on current metrics and iteration velocity, is $25k sufficient to achieve significant PMF progress given your monthly burn rate?</question>
#       <question>What specific PMF milestones could be achieved in the extended runway period that would justify taking on debt?</question>
#       <question>How might loan repayment obligations affect your ability to make necessary product pivots or experiments?</question>
#     </questions>
#   </perspective>
# </perspectives>
# """
#     )
#     # print(response)
#     print(xml_to_markdown(response))
