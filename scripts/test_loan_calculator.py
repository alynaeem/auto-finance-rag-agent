from auto_finance_rag_agent.tools.loan_calculator import calculate_loan_offer


def main() -> None:
    offer_48 = calculate_loan_offer(
        amount_financed=20000,
        annual_apr=8,
        term_months=48,
    )

    offer_60 = calculate_loan_offer(
        amount_financed=20000,
        annual_apr=8,
        term_months=60,
    )

    print("48-month offer")
    print(offer_48)

    print("-" * 80)

    print("60-month offer")
    print(offer_60)


if __name__ == "__main__":
    main()