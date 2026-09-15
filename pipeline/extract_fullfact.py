from pipeline.extract_functions import extract, get_claims_from_user, compare_claims_with_article, InputAnalysis, VerdictResult, Claim


def fullfact():
    for claim in analysis["claims"]:
        if not claim["checkable"]:
            continue
        article_text = extract(claim["text"], "fullfact.org")
        result = compare_claims_with_article(claim["text"], article_text)
        print(result)


if __name__ == "__main__":
    fullfact()
