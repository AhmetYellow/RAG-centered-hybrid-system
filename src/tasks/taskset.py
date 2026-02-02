TASKS = [
    # Data Collection
    {"task_id": "COLLECTS_PERSONAL_DATA", "category": "collection",
     "question": "Does the policy say it collects personal data?"},
    {"task_id": "COLLECTS_LOCATION", "category": "collection",
     "question": "Does the policy say it collects location data (precise or approximate)?"},
    {"task_id": "COLLECTS_DEVICE_USAGE", "category": "collection",
     "question": "Does the policy say it collects device identifiers or usage data?"},

    # Data Sharing / Disclosure
    {"task_id": "THIRD_PARTY_SHARING", "category": "sharing",
     "question": "Does the policy share personal data with third parties?"},
    {"task_id": "SHARES_WITH_ADVERTISERS", "category": "sharing",
     "question": "Does the policy share personal data with advertisers or for advertising purposes?"},
    {"task_id": "DATA_SALE", "category": "sharing",
     "question": "Does the policy sell personal data?"},

    # Purpose & Use
    {"task_id": "TARGETED_ADS", "category": "purpose",
     "question": "Does the policy use personal data for targeted advertising?"},
    {"task_id": "ANALYTICS_PROFILING", "category": "purpose",
     "question": "Does the policy use personal data for analytics, profiling, or personalization?"},
    {"task_id": "AI_TRAINING", "category": "purpose",
     "question": "Does the policy state personal data may be used to train or improve AI/ML models?"},

    # User Rights / Controls
    {"task_id": "DELETE_RIGHT", "category": "rights",
     "question": "Does the policy describe a right to delete personal data?"},
    {"task_id": "OPT_OUT_SHARING", "category": "rights",
     "question": "Does the policy provide an opt-out from sharing/sale/targeted advertising?"},

    # Retention & Security
    {"task_id": "RETENTION_PERIOD", "category": "retention",
     "question": "Does the policy specify how long personal data is kept (a retention period or criteria)?"},
    {"task_id": "SECURITY_MEASURES", "category": "security",
     "question": "Does the policy describe security measures used to protect personal data?"},
]
