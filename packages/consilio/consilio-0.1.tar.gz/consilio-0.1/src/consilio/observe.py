from pathlib import Path
from typing import Dict
import xml.etree.ElementTree as ET

from utils import (
    load_prompt_template,
    render_prompt,
    query_claude,
    save_interaction,
    escape_xml_string,
)


@save_interaction("observe")
def observe(doc: Path, context: Dict[str, str]) -> str:
    """Run initial observation stage"""
    print("[👀] Analyse and prepare clarification questions ...")

    statement = doc.read_text()
    prompts = load_prompt_template("Observe")
    system_prompt = render_prompt(prompts.system, context)
    user_prompt_data = {"DECISION": statement}
    user_prompt_data.update(context)
    user_prompt = render_prompt(prompts.user, user_prompt_data)

    # Query Claude
    response = query_claude(
        user_prompt=user_prompt,
        system_prompt=system_prompt,
        assistant="<observe>",
        temperature=0.9,
    )

    print("[✅] Observation complete")
    return "<observe>" + response.content


def xml_to_markdown(xml_string):
    root = ET.fromstring(escape_xml_string(xml_string))
    markdown = ""

    # Process observations
    observations = root.find("observations")
    if observations is not None:
        markdown += "## Observations\n\n"
        for i, obs in enumerate(observations.findall("observation"), 1):
            markdown += f"{i}. {obs.text}\n"

    # Process questions
    questions = root.find("questions")
    if questions is not None:
        markdown += "\n\n## Questions\n\n"
        for i, q in enumerate(questions.findall("question"), 1):
            markdown += f"{i}. {q.text}\n"

    return markdown


if __name__ == "__main__":
    context = {
        "domain": "NZ-based B2C iOS app startup that are pre-product-market-fit",
        "user_role": "Solo Founder",
        "perspective": "bootstrapped founder, who successfully navigated pre-PMF phase with limited capital with a successful exit",
    }
    doc_path = Path(__file__).parent.parent / "Decisions/BankLoan.md"
    observation = observe(doc=doc_path, context=context)
    print(xml_to_markdown(observation))

    # observation = """
    # <observe>
    #     <observations>
    #         <observation>The business has a relatively short runway of 4 months ($40k / $10k burn) without considering the $1k monthly revenue from the traditional unit</observation>
    #         <observation>The traditional business unit sale valuations show significant variance ($80k-$170k), suggesting uncertainty in the actual value and potentially challenging sale process</observation>
    #         <observation>The loan would extend runway by ~2.5 months ($25k / $10k burn) but add a fixed monthly obligation of ~$800, effectively increasing burn rate by 8%</observation>
    #         <observation>Current investors are waiting for "outstanding metrics" before further investment, indicating possible challenges in achieving desired performance levels</observation>
    #         <observation>The business is in a critical pre-PMF phase while simultaneously managing a business unit sale process, which could divide focus and resources</observation>
    #         <observation>The loan would be secured against the traditional business unit, which is planned for sale, creating potential complications in the sale process</observation>
    #         <observation>The timing mismatch between the 3-6+ month expected sale process and the 4-month runway presents a significant risk</observation>
    #     </observations>

    #     <questions>
    #         <question>What specific metrics are your current investors looking for, and what is your realistic timeline for achieving them? Understanding this helps evaluate whether taking on debt is bridging to a genuine milestone or potentially delaying inevitable harder decisions.</question>
    #         <question>Have you explored alternative approaches to extend runway without taking on debt - such as pre-selling the traditional business unit with an earnout structure, reducing burn rate, or generating immediate revenue through consulting/services? This helps assess if debt is truly the best option.</question>
    #         <question>What is your contingency plan if the traditional business unit sale takes longer than 6 months or falls through entirely? Given you're securing the loan against this asset, understanding the backup plan is crucial for risk assessment.</question>
    #         <question>Can you break down your current $10k monthly burn rate and identify any potential areas for reduction without significantly impacting progress toward PMF? This helps evaluate if the loan is truly necessary at the current burn rate.</question>
    #         <question>What specific product milestones or metrics improvements do you expect to achieve with the extended runway? Understanding the concrete objectives helps assess if the additional time will meaningfully improve your position.</question>
    #         <question>Have you had preliminary discussions with potential buyers for the traditional business unit? Understanding the level of buyer interest and likely timeline is crucial for evaluating the viability of your runway extension strategy.</question>
    #         <question>What impact would managing both the sale process and product development have on your team's bandwidth and focus? This helps assess potential hidden costs or delays in achieving your primary objectives.</question>
    #         <question>Have you considered the psychological impact of taking on debt during the pre-PMF phase? As a bootstrapped founder myself, I've seen how debt obligations can affect decision-making and risk tolerance during this critical period.</question>
    #         <question>What specific aspects of your unit economics validation give you confidence that you're on the right track toward PMF? This helps evaluate whether extending runway is likely to lead to meaningful progress.</question>
    #         <question>Have you explored partnership opportunities or strategic investors who might be interested in both the traditional business unit and your new direction? This could provide alternatives to traditional debt financing.</question>
    #     </questions>
    # </observe>"""
    # print(xml_to_markdown(observation))
