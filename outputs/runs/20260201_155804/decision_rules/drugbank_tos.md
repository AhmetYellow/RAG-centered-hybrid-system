# drugbank_tos — Risk Report

**Overall severity:** medium

## Findings
- **advertising / ad sharing** — medium: Policy indicates personal data is used and/or shared for advertising (possibly with conditions). (tasks: TARGETED_ADS)
- **third-party sharing** — medium: Policy indicates personal data is shared with third parties (e.g., service providers), possibly under conditions. (tasks: THIRD_PARTY_SHARING)
- **profiling / personalization** — medium: Policy indicates analytics/profiling/personalization using personal data. (tasks: ANALYTICS_PROFILING)
- **location collection** — medium: Policy indicates location data may be collected. (tasks: COLLECTS_LOCATION)

## Evidence (snippets)
- **advertising / ad sharing** / TARGETED_ADS — `879a67f6140537f8` (Preamble): DrugBank does not sell or rent your Personal Information to any third party for any purpose, including for advertising or marketing purposes.
- **advertising / ad sharing** / TARGETED_ADS — `0a534ccfacfdbd04` (What personal data we collect): Should you provide consent to marketing and profiling cookies... our advertising partners may also use such technologies to collect limited information about your device and interactions.
- **third-party sharing** / THIRD_PARTY_SHARING — `879a67f6140537f8` (Preamble): we do not share Personal Information with any third parties except in the limited circumstances described in this Privacy Policy.
- **third-party sharing** / THIRD_PARTY_SHARING — `a75fe009cf95a6a6` (With whom we share your information): We share your personal data with companies and individuals that provide services to us or on our behalf or help us operate the Services or our business.
- **profiling / personalization** / ANALYTICS_PROFILING — `d48d1759f2ff7166` (How we process your personal data): Analyzing trends in the use of the Services and anonymizing user interaction data to improve Service performance and safety.
- **profiling / personalization** / ANALYTICS_PROFILING — `d48d1759f2ff7166` (How we process your personal data): Providing you a personalized AI companion and allowing you to personalize your profile, interests, and AI companion interactions.
- **location collection** / COLLECTS_LOCATION — `3dfa33e3c47b9d11` (What personal data we collect): general location information such as city, state, or geographic area.
- **location collection** / COLLECTS_LOCATION — `ace32dfd4f3e78b5` (What personal data we collect): general location information such as city, state, or geographic area.

## Task outputs (summary)
- **AI_TRAINING**: `not_specified` — The policy does not specify that personal data may be used to train or improve AI/ML models.
- **ANALYTICS_PROFILING**: `supported` — Yes, the policy uses personal data for analytics and personalization.
- **COLLECTS_DEVICE_USAGE**: `supported` — Yes, the policy states it collects both device identifiers and usage data.
- **COLLECTS_LOCATION**: `supported` — Yes, it collects general location information.
- **COLLECTS_PERSONAL_DATA**: `supported` — Yes, the policy states that it collects personal data.
- **DATA_SALE**: `supported` — No, the policy states that DrugBank does not sell or rent personal information.
- **DELETE_RIGHT**: `supported` — Yes, the policy describes a right to delete personal data.
- **OPT_OUT_SHARING**: `supported` — Yes, the policy provides an opt-out option for sharing and targeted advertising.
- **RETENTION_PERIOD**: `supported` — Yes, the policy specifies retention periods for different types of personal data.
- **SECURITY_MEASURES**: `supported` — Yes, the policy describes various security measures.
- **SHARES_WITH_ADVERTISERS**: `not_specified` — The policy states that DrugBank does not sell or rent personal information for advertising purposes.
- **TARGETED_ADS**: `conflicting` — The policy states that personal information is not sold or rented for advertising, but mentions that advertising partners may collect limited information.
- **THIRD_PARTY_SHARING**: `conflicting` — Yes, the policy states that personal data may be shared with third parties under certain circumstances.
