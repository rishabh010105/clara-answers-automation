import json

def generate_differential_changelog(v1_memo: dict, v2_memo: dict) -> str:
    """
    Compares the v1 Account Memo and v2 Account Memo and generates a human-readable 
    changelog highlighting the specific updates made during the onboarding process.
    """
    changelog = []
    changelog.append("# Agent Configuration Changelog")
    changelog.append("## Overview\nChanges implemented from the demo (v1) to the onboarding configuration (v2).\n")

    for key, v2_value in v2_memo.items():
        v1_value = v1_memo.get(key)
        
        # We only record meaningful changes
        if v1_value != v2_value and key not in ["notes"]:
            
            val1_str = str(v1_value) if v1_value else "None"
            val2_str = str(v2_value) if v2_value else "None"
            
            # Format cleanly
            if isinstance(v1_value, list) or isinstance(v2_value, list):
                val1_str = ", ".join(v1_value) if v1_value else "None"
                val2_str = ", ".join(v2_value) if v2_value else "None"
            
            changelog.append(f"### Updated: `{key}`")
            changelog.append(f"- **Previous**: {val1_str}")
            changelog.append(f"- **New**: {val2_str}\n")
    
    if len(changelog) == 2:
         changelog.append("No material configuration changes detected during onboarding.")

    return "\n".join(changelog)

def apply_patch(v1_memo: dict, extracted_updates: dict) -> dict:
    """
    Takes the v1 memo and the raw extracted updates from the onboarding call,
    and intelligently merges them to create the v2 memo.
    """
    v2_memo = v1_memo.copy()
    
    # Overwrite v1 assumptions with v2 validated data
    for key, value in extracted_updates.items():
        # Only overwrite if the extractor found meaningful new data.
        if value and str(value).strip() != "" and value != []: 
             # If it's a list, and we have new defined items, we replace
             if isinstance(value, list) and len(value) > 0:
                  v2_memo[key] = value
             elif not isinstance(value, list):
                  v2_memo[key] = value
                  
        # Clear out unknowns if they have been addressed
        if key == "business_hours" and value and "business_hours" not in v2_memo.get("questions_or_unknowns", []):
             v2_memo["questions_or_unknowns"] = [q for q in v2_memo.get("questions_or_unknowns", []) if "business" not in q.lower()]

    v2_memo["notes"] = "Updated via onboarding pipeline (v2)."
    return v2_memo

if __name__ == "__main__":
    v1 = {"business_hours": "Unknown", "emergency_routing_rules": "Route to technician"}
    v2_extracted = {"business_hours": "Mon-Fri 9-5", "emergency_routing_rules": "Call 555-1234"}
    
    v2_final = apply_patch(v1, v2_extracted)
    print("V2:", json.dumps(v2_final, indent=2))
    print("\nChangelog:")
    print(generate_differential_changelog(v1, v2_final))
