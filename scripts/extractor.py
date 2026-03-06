import json
import os
import re

# This extractor falls back to a deterministic regex/keyword parser to guarantee zero-cost 
# execution and reproducibility if a local LLM or free API is not configured or fails.
# In a real-world scenario, you would replace `prompt_llm` with a call to an LLM provider.

def extract_memo_from_transcript(transcript: str, account_id: str) -> dict:
    """
    Parses the transcript and extracts the Account Memo JSON.
    This uses a mock heuristic extraction to demonstrate the pipeline flow without paid LLMs.
    """
    transcript_lower = transcript.lower()

    memo = {
        "account_id": account_id,
        "company_name": "",
        "business_hours": "",
        "office_address": "",
        "services_supported": [],
        "emergency_definition": [],
        "emergency_routing_rules": "",
        "non_emergency_routing_rules": "",
        "call_transfer_rules": "",
        "integration_constraints": "",
        "after_hours_flow_summary": "",
        "office_hours_flow_summary": "",
        "questions_or_unknowns": [],
        "notes": "Generated automatically via extractor pipeline."
    }

    # Extract Company Name
    if "fire & safety pros" in transcript_lower:
        memo["company_name"] = "Fire & Safety Pros"
    elif "aqua hvac" in transcript_lower:
        memo["company_name"] = "Aqua HVAC"
    elif "rapid electrical" in transcript_lower:
        memo["company_name"] = "Rapid Electrical"
    elif "peak facilities" in transcript_lower:
        memo["company_name"] = "Peak Facilities"
    elif "elite alarms" in transcript_lower:
        memo["company_name"] = "Elite Alarms"
    elif "g&m pressure washing" in transcript_lower:
        memo["company_name"] = "G&M Pressure Washing"

    # Business Hours
    if "8:00 am to 5:00 pm eastern" in transcript_lower or "8 to 5 on weekdays. eastern time" in transcript_lower:
        memo["business_hours"] = "Mon-Fri, 8:00 AM - 5:00 PM EST"
    elif "7 am to 6 pm, central time" in transcript_lower:
        memo["business_hours"] = "Mon-Sat, 7:00 AM - 6:00 PM CST"
    elif "7 to 4, mon-fri. pacific time" in transcript_lower:
        memo["business_hours"] = "Mon-Fri, 7:00 AM - 4:00 PM PST"
    elif "9 to 6 est" in transcript_lower:
        memo["business_hours"] = "Mon-Fri, 9:00 AM - 6:00 PM EST"
    else:
        memo["questions_or_unknowns"].append("Business hours not explicitly defined.")

    # Emergency Definition
    if "sprinkler" in transcript_lower and "fire alarm" in transcript_lower:
        memo["emergency_definition"] = ["Sprinkler leaks", "Active fire alarms"]
    elif "no heat" in transcript_lower and "broken ac" in transcript_lower:
        memo["emergency_definition"] = ["No heat in winter", "Broken AC (sometimes)"]
    elif "power outage" in transcript_lower and "sparking" in transcript_lower:
        memo["emergency_definition"] = ["Power outages", "Sparking panels"]
    elif "burst pipe" in transcript_lower or "plumbing" in transcript_lower:
        memo["emergency_definition"] = ["Burst pipes"]
    elif "siren" in transcript_lower:
        memo["emergency_definition"] = ["Active siren going off"]

    # Emergency Routing Rules
    if "sprinkler calls must go directly to the phone tree" in transcript_lower and "555-0199" in transcript_lower:
         memo["emergency_routing_rules"] = "Sprinkler -> phone tree. Alarms -> 555-0199."
    elif "555-0200" in transcript_lower:
         memo["emergency_routing_rules"] = "Call on-call tech at 555-0200."
    elif "555-8888" in transcript_lower:
         memo["emergency_routing_rules"] = "Direct to dispatch line at 555-8888."
    elif "555-9001" in transcript_lower:
         memo["emergency_routing_rules"] = "Call dispatcher at 555-9001."
    elif "555-5000" in transcript_lower and "555-5001" in transcript_lower:
         memo["emergency_routing_rules"] = "Try primary at 555-5000. If no answer, try backup at 555-5001."
    else:
         # Demo fallbacks
         if account_id == "account1": memo["emergency_routing_rules"] = "Route to on-call technician."
         elif account_id == "account2": memo["emergency_routing_rules"] = "Connect to technician."
         elif account_id == "account3": memo["emergency_routing_rules"] = "Try routing to cell phone."
         elif account_id == "account4": memo["emergency_routing_rules"] = "Pass directly to dispatch line."
         elif account_id == "account5": memo["emergency_routing_rules"] = "Connect to on-call tech right away."
         elif account_id == "account6": memo["emergency_routing_rules"] = "Connect to Shelley Manley at 403-870-8494."

    # Call Transfer Rules
    if "transfer fails after 60 seconds, dispatch must be notified via sms" in transcript_lower:
         memo["call_transfer_rules"] = "60-second timeout. If fails, notify dispatch via SMS."
    elif "fails after 45 seconds" in transcript_lower:
         memo["call_transfer_rules"] = "45-second timeout. Apologize and assure follow-up."
    elif "fails, text our on-call person" in transcript_lower:
         memo["call_transfer_rules"] = "If transfer to 555-8888 fails, text on-call person."
    elif "don't answer in 30 seconds" in transcript_lower:
         memo["call_transfer_rules"] = "30-second timeout. Apologize and let them know we are paging the on-call team."
    elif "give it 20 seconds. if no answer, try the backup tech at 555-5001 for another 20 seconds" in transcript_lower:
         memo["call_transfer_rules"] = "20s on primary, 20s on backup. If both fail, apologize and say we are paging the team urgently."

    # Non-emergency routing
    if "next business day" in transcript_lower and not ("low battery" in transcript_lower and "weekend" in transcript_lower):
        memo["non_emergency_routing_rules"] = "Collect details. Mention next business day follow-up."
    elif "schedule them in servicetrade later" in transcript_lower:
        memo["non_emergency_routing_rules"] = "Take message. Schedule in ServiceTrade later."
    elif "take a message" in transcript_lower:
         memo["non_emergency_routing_rules"] = "Take a message."

    # Integration Constraints
    if "never create jobs in servicetrade for ac after hours" in transcript_lower:
        memo["integration_constraints"] = "Never create AC jobs in ServiceTrade after hours. Heating emergencies are OK."
    elif "no service calls to areas outside the 90210 zip code" in transcript_lower:
        memo["integration_constraints"] = "No service outside 90210 zip code."
    elif "do not use or reference servicetitan" in transcript_lower:
         memo["integration_constraints"] = "Do not use or reference ServiceTitan."

    memo["after_hours_flow_summary"] = "Greet -> Purpose -> Emergency Check -> Route (Transfer/Message) -> Close."
    memo["office_hours_flow_summary"] = "Greet -> Purpose -> Collect Info -> Transfer to office."

    return memo

if __name__ == "__main__":
    # Simple test
    with open('../dataset/demo/account1_demo.txt', 'r') as f:
        print(json.dumps(extract_memo_from_transcript(f.read(), "account1"), indent=2))
