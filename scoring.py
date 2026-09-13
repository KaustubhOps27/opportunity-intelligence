WEIGHTS = {
    "weak_website_positioning": 25,
    "major_product_website_change": 20,
    "category_repositioning": 20,
    "recent_funding": 15,
    "senior_marketing_brand_hire": 10,
    "active_design_brand_growth_hiring": 10
}


def calculate_score(signals):
    score = 0

    for signal_name, signal_data in signals.items():

        if signal_data.get("detected") is True:
            score += WEIGHTS.get(signal_name, 0)

    return score


def get_priority(score):

    if score >= 60:
        return "HIGH"

    elif score >= 35:
        return "MEDIUM"

    else:
        return "LOW"