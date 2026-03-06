import os
import json
import datetime
from extractor import extract_memo_from_transcript
from prompter import generate_agent_spec
from patcher import generate_differential_changelog, apply_patch

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
DEMO_DIR = os.path.join(DATASET_DIR, "demo")
ONBOARDING_DIR = os.path.join(DATASET_DIR, "onboarding")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs", "accounts")
TASKS_DIR = os.path.join(BASE_DIR, "outputs", "tasks")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_mock_asana_task(account_id: str, company_name: str):
    """Simulates creating an Asana task tracking item."""
    ensure_dir(TASKS_DIR)
    task_data = {
        "id": f"task_{account_id}",
        "name": f"Onboard new client: {company_name}",
        "status": "TODO",
        "created_at": datetime.datetime.now().isoformat(),
        "notes": "Generated v1 agent. Awaiting onboarding updates."
    }
    with open(os.path.join(TASKS_DIR, f"{account_id}_task.json"), 'w') as f:
        json.dump(task_data, f, indent=2)
    print(f"=> Created tracking item for {account_id}.")

def process_pipeline():
    ensure_dir(OUTPUTS_DIR)
    ensure_dir(TASKS_DIR)
    
    # 1. Find all demo files to determine accounts
    demo_files = [f for f in os.listdir(DEMO_DIR) if f.endswith('.txt')]
    
    print(f"Found {len(demo_files)} accounts to process.")
    
    for demo_file in demo_files:
        # e.g. account1_demo.txt -> account1
        account_id = demo_file.split('_')[0]
        
        print(f"\n--- Processing {account_id} ---")
        
        # Setup output directories for this account
        acc_dir = os.path.join(OUTPUTS_DIR, account_id)
        v1_dir = os.path.join(acc_dir, "v1")
        v2_dir = os.path.join(acc_dir, "v2")
        ensure_dir(v1_dir)
        ensure_dir(v2_dir)
        
        # ---------------------------------------------------------
        # PIPELINE A: Demo -> Preliminary Agent (v1)
        # ---------------------------------------------------------
        print("Running Pipeline A (Demo)...")
        with open(os.path.join(DEMO_DIR, demo_file), 'r') as f:
            demo_transcript = f.read()
            
        v1_memo = extract_memo_from_transcript(demo_transcript, account_id)
        v1_spec = generate_agent_spec(v1_memo, version="v1")
        
        # Save v1 artifacts
        with open(os.path.join(v1_dir, "memo.json"), 'w') as f:
            json.dump(v1_memo, f, indent=2)
            
        with open(os.path.join(v1_dir, "agent_spec.json"), 'w') as f:
            json.dump(v1_spec, f, indent=2)
            
        print("=> Saved v1 artifacts.")
        
        # Create Task tracker item
        create_mock_asana_task(account_id, v1_memo.get("company_name", "Unknown Company"))
            
        # ---------------------------------------------------------
        # PIPELINE B: Onboarding -> Agent Modification (v2)
        # ---------------------------------------------------------
        onboarding_file = f"{account_id}_onboarding.txt"
        onboarding_path = os.path.join(ONBOARDING_DIR, onboarding_file)
        
        if os.path.exists(onboarding_path):
            print("Running Pipeline B (Onboarding updates)...")
            with open(onboarding_path, 'r') as f:
                onboarding_transcript = f.read()
                
            # Extract updates from the onboarding transcript
            updates = extract_memo_from_transcript(onboarding_transcript, account_id)
            
            # Apply patch to create v2 memo
            v2_memo = apply_patch(v1_memo, updates)
            
            # Generate differential changelog
            changelog_content = generate_differential_changelog(v1_memo, v2_memo)
            
            # Generate v2 spec
            v2_spec = generate_agent_spec(v2_memo, version="v2")
            
            # Save v2 artifacts
            with open(os.path.join(v2_dir, "memo.json"), 'w') as f:
                json.dump(v2_memo, f, indent=2)
                
            with open(os.path.join(v2_dir, "agent_spec.json"), 'w') as f:
                json.dump(v2_spec, f, indent=2)
                
            with open(os.path.join(v2_dir, "changelog.md"), 'w') as f:
                f.write(changelog_content)
                
            print("=> Saved v2 artifacts and changelog.")
        else:
             print(f"No onboarding data found for {account_id}, skipping Pipeline B.")

    print("\n--- Pipeline Execution Complete ---")

if __name__ == "__main__":
    process_pipeline()
