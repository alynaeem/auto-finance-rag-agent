def calculate_loan_offer(
    amount_financed: float,
    annual_apr: float,
    term_months: int,
) -> dict:
    monthly_rate = annual_apr / 100 / 12

    if monthly_rate == 0:
        monthly_payment = amount_financed / term_months
    else:
        monthly_payment = (
            amount_financed
            * monthly_rate
            / (1 - (1 + monthly_rate) ** (-term_months))
        )

    total_payment = monthly_payment * term_months
    total_interest = total_payment - amount_financed

    return {
        "amount_financed": round(amount_financed, 2),
        "annual_apr": round(annual_apr, 2),
        "term_months": term_months,
        "monthly_payment": round(monthly_payment, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
    }


def compare_loan_offers(
    amount_financed: float,
    annual_apr: float,
    terms_months: list[int],
) -> dict:
    offers = []

    for term_months in terms_months:
        offer = calculate_loan_offer(
            amount_financed=amount_financed,
            annual_apr=annual_apr,
            term_months=term_months,
        )
        offers.append(offer)

    lowest_monthly_payment = min(
        offers,
        key=lambda offer: offer["monthly_payment"],
    )

    lowest_total_interest = min(
        offers,
        key=lambda offer: offer["total_interest"],
    )

    return {
        "amount_financed": round(amount_financed, 2),
        "annual_apr": round(annual_apr, 2),
        "offers": offers,
        "lowest_monthly_payment_term": lowest_monthly_payment["term_months"],
        "lowest_total_interest_term": lowest_total_interest["term_months"],
    }