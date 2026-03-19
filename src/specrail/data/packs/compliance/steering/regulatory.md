---
description: Regulatory awareness — SOX, HIPAA, PCI-DSS, GDPR constraints
inclusion: manual
---

# Compliance Steering — Regulatory Awareness

This file helps AI agents understand regulatory constraints. It does NOT replace legal counsel — it ensures the AI doesn't accidentally violate common regulatory requirements.

## General rules

- Never log, store, or expose PII (personally identifiable information) without explicit business justification
- Never store credentials, tokens, or secrets in code or configuration files committed to git
- All data at rest must be encrypted (database, backups, file storage)
- All data in transit must use TLS 1.2+
- Retain audit logs for the period required by your regulatory framework

## SOX (Sarbanes-Oxley) awareness

Applies to: financial reporting systems, accounting software, internal controls

- All changes to financial calculation logic require dual review
- Audit trail must be immutable — append-only logs, no deletion
- Access to production financial data must be logged
- Separation of duties: developer ≠ deployer ≠ approver

## HIPAA awareness

Applies to: healthcare data, patient records, medical systems

- PHI (Protected Health Information) must be encrypted at rest and in transit
- Access to PHI must be logged with user identity and timestamp
- Minimum necessary principle: only access the data you need
- Never include real PHI in test data, logs, error messages, or AI prompts
- Data retention and deletion policies must be enforced programmatically

## PCI-DSS awareness

Applies to: payment processing, credit card data, transaction systems

- Never store full credit card numbers — use tokenization
- Never log credit card numbers, CVVs, or full track data
- Encrypt cardholder data at rest with strong cryptography
- Restrict access to cardholder data on a need-to-know basis
- Regularly test security systems and processes

## GDPR awareness

Applies to: systems processing data of EU residents

- Implement right to deletion (data erasure) — soft-delete is not enough for GDPR
- Implement data export (portability) in machine-readable format
- Record consent with timestamp and scope
- Data processing must have a legal basis (consent, contract, legitimate interest)
- Data breach notification within 72 hours — have a process ready

## How this affects SpecRail workflows

- Planner: flag tasks that touch regulated data as high-risk
- Verifier: check that audit logging is present for regulated operations
- Bugfix investigator: never include real PII in bug reproduction steps
- Report generator: never include PII in delivery reports
- Ralph loop: AI-generated code touching regulated data must be human-reviewed (HITL, not AFK)
