from pathlib import Path

OUT_DIR = Path("data/synthetic/company_policy_documents")
OUT_DIR.mkdir(parents=True, exist_ok=True)

docs = {
    "eligibility_policy.md": """# Synthetic Training Document
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
""",

    "required_documents_policy.md": """# Synthetic Training Document
# Required Documents Policy for Auto Finance Applications

Important: This is a synthetic policy document created for a portfolio project. It is not legal, financial, or credit advice.

## 1. Required documents for salaried applicants

A salaried applicant should provide:

- Valid identity document
- Recent salary slip
- Employment verification letter
- Recent bank statement
- Vehicle quotation or invoice
- Insurance information, if available

## 2. Required documents for self-employed applicants

A self-employed applicant should provide:

- Valid identity document
- Business registration proof, where applicable
- Recent bank statement
- Business income evidence
- Tax document, where available
- Vehicle quotation or invoice
- Insurance information, if available

## 3. Guarantor documents

If a guarantor is required, the guarantor should provide:

- Valid identity document
- Contact information
- Income proof
- Relationship to applicant
- Signed guarantor consent form

## 4. Missing document handling

If required documents are missing, the application should be marked as incomplete.

The system should clearly list missing documents and ask the applicant to submit them before further processing.

## 5. Escalation rules

Manual review is required when:

- Identity document is missing
- Income proof is missing
- Documents appear inconsistent
- Applicant information conflicts with submitted documents
- Guarantor information is incomplete
""",

    "loan_pricing_policy.md": """# Synthetic Training Document
# Auto Finance Loan Pricing Policy

Important: This is a synthetic policy document created for a portfolio project. It is not legal, financial, or credit advice.

## 1. Loan amount and down payment

The amount financed should be calculated after subtracting the down payment from the vehicle price.

A larger down payment may reduce the amount financed and total interest paid.

## 2. Loan term

Supported loan terms are typically between 12 and 84 months.

Longer loan terms may reduce monthly payment but can increase total interest paid over the life of the loan.

Shorter loan terms may increase monthly payment but usually reduce total interest paid.

## 3. Annual percentage rate

The annual percentage rate represents the yearly cost of borrowing.

The system should explain APR clearly and avoid implying that a displayed APR is guaranteed.

## 4. Monthly payment calculation

Monthly payment should be calculated using the financed amount, annual APR, and term length.

The system should use a deterministic calculator tool instead of asking the language model to calculate payment manually.

## 5. Total cost comparison

When comparing two offers, the system should show:

- Monthly payment
- Total payment
- Total interest
- Term length
- Tradeoff between lower monthly payment and higher total cost

## 6. Pricing safety rule

The system must not promise final approval, final APR, or final monthly payment.

Final pricing requires lender review, applicant verification, and policy approval.
""",

    "complaint_handling_policy.md": """# Synthetic Training Document
# Auto Finance Complaint Handling Policy

Important: This is a synthetic policy document created for a portfolio project. It is not legal, financial, or credit advice.

## 1. Complaint intake

Every complaint should be logged with:

- Customer name or reference number
- Date received
- Product type
- Complaint category
- Description of issue
- Supporting documents, if any
- Requested resolution

## 2. Complaint categories

Common auto-finance complaint categories include:

- Payment processing issue
- Add-on product cancellation
- Refund delay
- Repossession dispute
- Credit reporting dispute
- Loan servicing issue
- Incorrect balance or payoff amount

## 3. Severity levels

Low severity complaints involve general questions or minor delays.

Medium severity complaints involve missing documentation, unclear communication, or repeated follow-up.

High severity complaints involve potential legal, compliance, repossession, credit reporting, discrimination, or financial harm issues.

## 4. Escalation rules

The complaint should be escalated to human review if it involves:

- Repossession
- Credit reporting dispute
- Add-on product cancellation or refund denial
- Allegation of unfair treatment
- Legal or regulatory language
- Customer financial harm
- Repeated unresolved complaint

## 5. Response requirements

The response should be clear, professional, and grounded in policy.

The system should avoid admitting fault unless reviewed by an authorized human team.

The system should recommend next steps and required documentation.

## 6. Safety rule

The AI system should not provide legal advice.

For high-risk complaints, the system should recommend escalation to the compliance or servicing team.
""",

    "add_on_products_policy.md": """# Synthetic Training Document
# Add-On Products Policy

Important: This is a synthetic policy document created for a portfolio project. It is not legal, financial, or credit advice.

## 1. Optional product disclosure

Add-on products must be presented as optional unless a specific product is legally or contractually required.

Customers should receive clear information about product cost, coverage, cancellation rules, and refund eligibility.

## 2. Consent requirement

The customer should provide clear consent before an add-on product is included in the financing agreement.

The system should flag cases where consent is unclear or disputed.

## 3. Cancellation request

When a customer requests cancellation of an add-on product, the servicing team should verify:

- Customer identity
- Product type
- Purchase date
- Cancellation window
- Contract terms
- Refund eligibility
- Whether the product provider or finance company handles cancellation

## 4. Refund handling

If a refund may be due, the case should be reviewed by the servicing team.

The system should not promise a refund automatically.

## 5. Escalation triggers

Manual review is required if:

- Customer says the product was added without consent
- Customer says cancellation was ignored
- Customer says refund was denied
- Product cost was not clearly disclosed
- Complaint includes legal or regulatory concern

## 6. Customer response rule

The AI response should acknowledge the issue, request relevant documents, explain that the case requires review, and route the matter to the appropriate servicing or compliance team.
""",
}

for filename, content in docs.items():
    path = OUT_DIR / filename
    path.write_text(content, encoding="utf-8")
    print(f"Created {path}")

print("Synthetic company policy documents created successfully.")