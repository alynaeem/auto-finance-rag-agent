# Synthetic Training Document
# Auto Finance Eligibility Policy

Important: This is a synthetic policy document created for a portfolio project. It is not legal, financial, or credit advice.

## 1. Minimum applicant requirements

Applicants must be at least 18 years old.

Applicants must provide valid identity verification before the application can move to financing review.

The applicant must provide accurate contact information, employment information, and income information.

## 2. Income verification

Applicants must provide at least one acceptable proof of income.

Acceptable income proof may include:

- Recent salary slip
- Bank statement
- Employment letter
- Tax document
- Business income record

If income proof is missing, the application should not receive an automated approval recommendation.

## 3. Debt-to-income review

The system should calculate a basic debt-to-income signal using:

existing monthly debt / monthly income

A high debt-to-income ratio should trigger manual review.

The model output should only support decision-making. It should not be treated as the final credit decision.

## 4. Manual review triggers

Applications should be routed to manual review if any of the following are true:

- Missing identity document
- Missing income proof
- High debt-to-income ratio
- Prior serious delinquency reported by the applicant
- Conflicting applicant information
- Customer disputes credit-reporting information
- Requested loan term is outside supported policy range
- Down payment is unusually low compared with requested amount

## 5. Decision explanation

The system must explain that any risk score or eligibility result is a support signal only.

Final approval, rejection, pricing, and exceptions require human review by the finance team.
