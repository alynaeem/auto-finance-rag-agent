#!/usr/bin/env bash
set -euo pipefail

mkdir -p data/raw/policy_docs
mkdir -p data/raw/complaints
mkdir -p data/raw/credit
mkdir -p data/processed
mkdir -p data/synthetic/company_policy_documentscl

curl -L -o data/raw/policy_docs/cfpb_auto_loan_guide.pdf \
"https://files.consumerfinance.gov/f/documents/cfpb_auto_loan_guide.pdf"

curl -L -o data/raw/policy_docs/cfpb_auto_loan_worksheet.pdf \
"https://files.consumerfinance.gov/f/documents/201606_cfpb_auto-loan-worksheet.pdf"

curl -L -o data/raw/policy_docs/cfpb_automobile_finance_examination_procedures.pdf \
"https://files.consumerfinance.gov/f/201506_cfpb_automobile-finance-examination-procedures.pdf"

curl -L -o data/raw/policy_docs/cfpb_supervisory_highlights_auto_finance_2024_10.pdf \
"https://files.consumerfinance.gov/f/documents/cfpb_supervisory-highlights-special-ed-auto-finance_2024-10.pdf"

curl -L -o data/raw/policy_docs/cfpb_consumer_voices_auto_financing.pdf \
"https://files.consumerfinance.gov/f/documents/201606_cfpb_consumer-voices-on-automobile-financing.pdf"

curl -L -o data/raw/complaints/cfpb_vehicle_loan_lease_500.json \
"https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/?field=all&format=json&no_aggs=true&size=500&date_received_min=2023-01-01&product=Vehicle%20loan%20or%20lease"

curl -L -o data/raw/credit/statlog_german_credit_data.zip \
"https://archive.ics.uci.edu/static/public/144/statlog+german+credit+data.zip"

echo "Data download complete."