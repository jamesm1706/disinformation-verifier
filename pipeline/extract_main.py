from extract_functions import get_claims_from_user, InputAnalysis, Claim
from dotenv import load_dotenv


def user_claims(input_text: str):
    analysis = get_claims_from_user(input_text)
    for claim in analysis["claims"]:
        if not claim["checkable"]:
            continue
        print(
            f"Claim: {claim['text']}\nClaim Type: {claim['claim_type']}\n Checkable: {claim['checkable']}")


if __name__ == "__main__":
    load_dotenv()
    input_text = input("Enter your claim: ")
    user_claims(input_text)
