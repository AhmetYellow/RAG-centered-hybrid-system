# replika_tos — Risk Report

**Overall severity:** medium

## Findings
- **advertising / ad sharing** — medium: Policy indicates personal data is used and/or shared for advertising (possibly with conditions). (tasks: SHARES_WITH_ADVERTISERS, TARGETED_ADS)
- **third-party sharing** — medium: Policy indicates personal data is shared with third parties (e.g., service providers), possibly under conditions. (tasks: THIRD_PARTY_SHARING)
- **profiling / personalization** — medium: Policy indicates analytics/profiling/personalization using personal data. (tasks: ANALYTICS_PROFILING)
- **ai training / model improvement** — medium: Policy indicates data may be used to train or improve AI/ML models. (tasks: AI_TRAINING)
- **location collection** — medium: Policy indicates location data may be collected. (tasks: COLLECTS_LOCATION)

## Evidence (snippets)
- **advertising / ad sharing** / SHARES_WITH_ADVERTISERS — `879a67f6140537f8` (Preamble): DrugBank does not sell or rent your Personal Information to any third party for any purpose, including for advertising or marketing purposes.
- **advertising / ad sharing** / SHARES_WITH_ADVERTISERS — `a75fe009cf95a6a6` (With whom we share your information): We will never share your conversations with your Replika AI companion or any photos or other content you provide within the Apps with our advertising partners, or use such information for marketing or advertising purposes.
- **advertising / ad sharing** / SHARES_WITH_ADVERTISERS — `a75fe009cf95a6a6` (With whom we share your information): We share information about visitors to our Website... with advertising companies for interest-based advertising and other marketing purposes, where we have a legal basis for doing so.
- **advertising / ad sharing** / TARGETED_ADS — `879a67f6140537f8` (Preamble): DrugBank does not sell or rent your Personal Information to any third party for any purpose, including for advertising or marketing purposes.
- **advertising / ad sharing** / TARGETED_ADS — `0a534ccfacfdbd04` (What personal data we collect): Should you provide consent to marketing and profiling cookies... our advertising partners may also use such technologies to collect limited information about your device and interactions with the Services.
- **third-party sharing** / THIRD_PARTY_SHARING — `879a67f6140537f8` (Preamble): we do not share Personal Information with any third parties except in the limited circumstances described in this Privacy Policy.
- **third-party sharing** / THIRD_PARTY_SHARING — `a75fe009cf95a6a6` (With whom we share your information): We share your personal data with companies and individuals that provide services to us or on our behalf.
- **profiling / personalization** / ANALYTICS_PROFILING — `d48d1759f2ff7166` (How we process your personal data): Providing you a personalized AI companion and allowing you to personalize your profile, interests, and AI companion interactions.
- **profiling / personalization** / ANALYTICS_PROFILING — `d48d1759f2ff7166` (How we process your personal data): Analyzing trends in the use of the Services and anonymizing user interaction data to improve Service performance and safety.
- **ai training / model improvement** / AI_TRAINING — `d48d1759f2ff7166` (How we process your personal data): The anonymized data is used only internally and is not used to train third-party large language models or other AI systems.
- **ai training / model improvement** / AI_TRAINING — `430c6572510aa6d6` (How we process your personal data): This includes collecting and immediately anonymizing user feedback, and small portions of Messages and Content data to train our proprietary safety algorithms.
- **location collection** / COLLECTS_LOCATION — `3dfa33e3c47b9d11` (What personal data we collect): general location information such as city, state, or geographic area.
- **location collection** / COLLECTS_LOCATION — `ace32dfd4f3e78b5` (What personal data we collect): general location information such as city, state, or geographic area.

## Task outputs (summary)
- **AI_TRAINING**: `conflicting` — The policy states that anonymized data is used to train proprietary safety algorithms but explicitly mentions that it is not used to train third-party AI systems.
- **ANALYTICS_PROFILING**: `supported` — Yes, the policy uses personal data for analytics, profiling, and personalization.
- **COLLECTS_DEVICE_USAGE**: `supported` — Yes, the policy states it collects both device identifiers and usage data.
- **COLLECTS_LOCATION**: `supported` — Yes, it collects general location information.
- **COLLECTS_PERSONAL_DATA**: `supported` — Yes, the policy states that it collects personal data.
- **DATA_SALE**: `not_specified` — The policy does not specify whether personal data is sold.
- **DELETE_RIGHT**: `supported` — Yes, the policy describes a right to delete personal data.
- **OPT_OUT_SHARING**: `supported` — Yes, the policy provides an opt-out option for sharing and targeted advertising.
- **RETENTION_PERIOD**: `supported` — Yes, the policy specifies retention periods for different types of personal data.
- **SECURITY_MEASURES**: `supported` — Yes, the policy describes various security measures.
- **SHARES_WITH_ADVERTISERS**: `conflicting` — The policy states that personal information is not sold or rented for advertising, but it does share certain data with advertising partners.
- **TARGETED_ADS**: `conflicting` — The policy states that personal information is not sold or rented for advertising, but it allows advertising partners to collect limited information for targeted advertising.
- **THIRD_PARTY_SHARING**: `conflicting` — Yes, the policy shares personal data with third parties under certain conditions.
