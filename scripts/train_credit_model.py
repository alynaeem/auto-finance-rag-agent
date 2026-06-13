from auto_finance_rag_agent.ml.credit_training import train_credit_risk_model


def main() -> None:
    result = train_credit_risk_model()

    print(f"Accuracy: {result['accuracy']:.4f}")
    print(f"ROC AUC: {result['roc_auc']:.4f}")
    print()
    print(f"Model saved to: {result['model_file']}")
    print(f"Metadata saved to: {result['metadata_file']}")


if __name__ == "__main__":
    main()