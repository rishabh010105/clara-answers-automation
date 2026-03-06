import json

def generate_agent_spec(memo: dict, version: str = "v1") -> dict:
    """
    Takes the Account Memo JSON and generates a Retell Agent Spec JSON.
    Ensures strict adherence to prompt hygiene rules.
    """
    
    business_hours = memo.get("business_hours", "Not specified")
    emergencies = ", ".join(memo.get("emergency_definition", []))
    eme_routing = memo.get("emergency_routing_rules", "Not specified")
    non_eme_routing = memo.get("non_emergency_routing_rules", "Collect details and mention next business day follow-up.")
    transfer_rules = memo.get("call_transfer_rules", "If transfer fails, apologize and assure follow-up.")
    constraints = memo.get("integration_constraints", "None")
    
    system_prompt = f"""
You are Clara, the AI voice assistant for {memo.get('company_name', 'our company')}.

### Context
- Business Hours: {business_hours}
- The following are considered EMERGENCIES: {emergencies}
- Special Constraints: {constraints}

### Instructions
Follow these steps carefully based on the time of the call:

**Business Hours Flow:**
1. Greet the caller: "Hi, thanks for calling {memo.get('company_name', 'our company')}. How can I help you today?"
2. Ask for the purpose of their call.
3. Collect their name and phone number.
4. Route or transfer the call to the office.
5. If the transfer fails: {transfer_rules}
6. Confirm next steps and ask "Is there anything else I can help with?"
7. Politely close the call.

**After-Hours Flow:**
1. Greet the caller and state that the office is currently closed.
2. Ask for the purpose of their call.
3. Confirm emergency based on the emergency definitions above.
4. IF EMERGENCY: 
   - Collect their name, phone number, and address IMMEDIATELY.
   - Follow this routing protocol: {eme_routing}
   - If transfer fails: {transfer_rules}
   - Assure quick followup.
5. IF NON-EMERGENCY:
   - Follow this protocol: {non_eme_routing}
6. Ask "Is there anything else I can help with?"
7. Politely close the call.

**STRICT RULES:**
- Do not mention tools, function calls, or technical mechanics to the caller.
- Do not ask unnecessary questions; only collect what is needed for routing and dispatch.
"""

    spec = {
        "agent_name": f"{memo.get('company_name', 'Company')} Agent {version}",
        "voice": "11labs-Rachel", 
        "system_prompt": system_prompt.strip(),
        "key_variables": {
            "timezone": "Extracted from business hours",
            "business_hours": business_hours,
            "emergency_routing": eme_routing
        },
        "tool_invocation_placeholders": [
            "transfer_call",
            "end_call"
        ],
        "call_transfer_protocol": transfer_rules,
        "fallback_protocol_if_transfer_fails": transfer_rules,
        "version": version
    }
    
    return spec

if __name__ == "__main__":
    # Test
    sample_memo = {
        "company_name": "Test Co",
        "business_hours": "Mon-Fri 9-5 EST",
        "emergency_definition": ["Leaks"],
        "emergency_routing_rules": "Call 555-0000",
        "call_transfer_rules": "Timeout after 30s, apologize."
    }
    print(json.dumps(generate_agent_spec(sample_memo), indent=2))
