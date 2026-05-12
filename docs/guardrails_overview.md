# LLM Guardrails and Safety

Guardrails are safety layers that sit between the user and the LLM (Input Guardrails) or between the LLM and the user (Output Guardrails). They ensure that the system remains safe, accurate, and on-topic.

Types of Guardrails:
1. **PII Detection**: Identifying and redacting personal information like names, emails, and phone numbers.
2. **Topic Validation**: Ensuring the conversation stays within the intended scope (e.g., technical support only).
3. **Adversarial Detection**: Blocking prompt injection attacks and malicious jailbreaks.
4. **Safety Classifiers**: Using models like Llama Guard to detect toxic or harmful content.

Implementation:
Guardrails can be implemented using rule-based regex, specialized NLP models (like Presidio), or by querying smaller LLMs as safety judges.
