from app.utils.openarena_authenticator import OpenArenaAuthenticator
import requests


auth = OpenArenaAuthenticator()


def generate_program(user_input):
    openarena_token = auth.authenticate_and_get_token()

    headers = {
        'Authorization': f'Bearer {openarena_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "workflow_id": "592081d1-0a6e-4b5f-93b1-a08a674bf4bc",
        "query": user_input,
        "is_persistence_allowed": True,
        "modelparams": {
            "anthropic_direct.claude-v4-sonnet": {
                "temperature": "0.7",
                "top_p": "1",
                "max_tokens": "63999",
                "top_k": "250",
                "system_prompt": ("You are Experienced python developer , "
                                  "write efficient programs."),
                "enable_reasoning": "true",
                "budget_tokens": "35425"
            }
        }
    }
    try:
        response = requests.post(
            "https://aiopenarena.gcs.int.thomsonreuters.com/v1/inference",
            headers=headers, json=payload
        )
        print(f" OpenArena API Response Status: {response.status_code}")
        if response.status_code == 200:
            ai_response = response.json()
            feedback = ai_response.get('result', {}).get(
                'answer', {}
            ).get('anthropic_direct.claude-v4-sonnet', '')
            # FIX: get cost from the correct nested location
            cost = ai_response.get('result', {}).get(
                'cost_track', {}
            ).get('total_cost', None)
            print("💬 Generated Program:", feedback)
            print("💲 Estimated Query Cost:", cost)
            # Return the generated program and cost
            return {
                "program": feedback,
                "cost": cost,
                "status": "success"
            }
        else:
            error_msg = (f"⚠️ OpenArena Error: {response.status_code}, "
                         f"{response.text}")
            print(error_msg)
            return {
                "program": "",
                "cost": None,
                "status": "error",
                "error": f"API returned status {response.status_code}"
            }
    except Exception as e:
        print(f"🚨 Failed to Generate Program: {e}")
        return {
            "program": "",
            "cost": None,
            "status": "error",
            "error": str(e)
        }
