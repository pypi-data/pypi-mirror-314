from pathlib import Path
from typing import Dict
import xml.etree.ElementTree as ET

from consilio.utils import load_prompt_template, render_prompt, query_claude
from consilio.utils import save_interaction


@save_interaction("consult")
def get_perspective_opinion(
    doc: Path,
    title: str,
    user_prompt: str,
    assistant_prefix: str,
    perspective_title: str,
) -> str:
    """Get opinion from a single perspective"""
    response = query_claude(
        user_prompt=user_prompt,
        assistant=assistant_prefix,
        temperature=0.8,
    )
    return response.content


def consult(doc: Path, assembly_output: str, context: Dict[str, str]) -> str:
    print("[👀] Starting consultation phase...")

    # Parse assembly instruction XML
    root = ET.fromstring(assembly_output)
    perspectives = root.findall(".//perspective")

    statement = doc.read_text()
    prompts = load_prompt_template("Consult")

    responses = []
    for perspective in perspectives:
        # Extract structured data from perspective XML
        title_elem = perspective.find("title")
        relevance_elem = perspective.find("relevance")
        assert title_elem is not None and title_elem.text is not None, "Missing title"
        assert (
            relevance_elem is not None and relevance_elem.text is not None
        ), "Missing relevance"

        title = title_elem.text.strip()
        relevance = relevance_elem.text.strip()
        questions = [
            q.text.strip()
            for q in perspective.findall(".//question")
            if q.text is not None
        ]

        # Build perspective context
        perspective_context = {
            "perspective_title": title,
            "perspective_relevance": relevance,
            "perspective_questions": "\n".join(f"- {q}" for q in questions),
        }
        user_context = {"DECISION": statement}
        user_context.update(context)
        user_context.update(perspective_context)
        user_prompt = render_prompt(prompts.user, user_context)

        # Get perspective opinion
        response = get_perspective_opinion(
            doc=doc,
            title=title,
            user_prompt=user_prompt,
            assistant_prefix=f"As an expert in {title}, I'll",
            perspective_title=title,
        )
        print(f"[🔍] Opinion from perspective: {title}\n{response}")
        responses.append("<opinion>" + response)

    print("[✅] Consultation complete")
    return "<opinions>" + "".join(responses) + "</opinions>"


# if __name__ == "__main__":
#     context = {
#         "domain": "NZ-based B2C iOS app startup that are pre-product-market-fit",
#         "user_role": "Solo Founder",
#         "perspective": "bootstrapped founder, who successfully navigated pre-PMF phase with limited capital with a successful exit",
#     }
#     doc_path = Path(__file__).parent / "Decisions/BankLoan.md"
#     assembly_output = escape_xml_string(
#         """
#         <perspectives>
#             <perspective>
#                 <title>Exit-Experienced M&A Advisor specializing in small business sales</title>
#                 <relevance>Critical for validating the feasibility and timeline of the traditional business unit sale, which directly impacts the need for and risk of the loan</relevance>
#                 <questions>
#                     <question>Based on current market conditions, how realistic are the broker valuations, and what factors could extend the sale timeline beyond 6 months?</question>
#                     <question>What specific preparation steps could accelerate the sale process while maintaining optimal valuation?</question>
#                     <question>How might using the business as loan collateral impact potential buyers' interest or the sale process?</question>
#                 </questions>
#             </perspective>
#         </perspectives>
#     """
#     )
#     print(f"instruction: {assembly_output}")
#     response = consult(doc=doc_path, assembly_output=assembly_output, context=context)
#     print(response)

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
