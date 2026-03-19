---
description: Audit trails, change management, approval workflows, separation of duties
inclusion: manual
---

# Compliance Steering — Audit Trails

Every change to production systems must be traceable: who changed what, when, why, and who approved it.

## Change management

All production changes follow this flow:
1. Spec created with requirements and design
2. Tasks planned and risk-assessed (planner agent)
3. Implementation with feedback loops (Ralph loop)
4. Verification report generated (verifier agent)
5. Human review and approval (PR review)
6. Deployment with rollback plan
7. Post-deployment verification

## Audit trail requirements

### Code changes
- Every commit references a spec: `feat(auth): add login endpoint [spec:user-auth/task-1]`
- CHANGELOG_AI.md records what changed and why — this is your audit log
- DECISIONS.md records architectural decisions with context and alternatives
- VERIFICATION.md proves the change was tested

### Database changes
- Every migration script has a corresponding rollback script
- Migration scripts are reviewed and approved before deployment
- Data migrations (backfills) are logged with row counts and duration
- Schema changes are documented in DECISIONS.md

### Access and authorization changes
- Changes to roles, permissions, or access control require explicit approval
- Security steering rules are never bypassed without documented justification
- Secrets rotation is logged in CHANGELOG_AI.md

## Evidence collection

For each spec, the following files serve as audit evidence:
| File | Evidence of |
|------|-------------|
| `requirements.md` | What was requested and why |
| `design.md` | How it was designed, alternatives considered |
| `tasks.md` | What was planned, in what order |
| `PROGRESS.md` | What was done in each iteration |
| `VERIFICATION.md` | That it was tested and verified |
| `DECISIONS.md` | Why specific choices were made |
| Git history | Exact code changes with timestamps |

Archive completed specs — they are your audit trail.

## Approval workflows

| Change type | Required approval |
|-------------|-------------------|
| New feature | Tech lead review |
| Database migration | DBA + tech lead |
| Security-related change | Security team |
| Production deployment | Release manager |
| Rollback | On-call engineer (can be post-hoc) |
| Emergency hotfix | Any senior engineer (documented within 24h) |

## Separation of duties

- The person who writes the code should not be the only reviewer
- AI-generated code (Ralph loop) must be reviewed by a human before production
- Database migrations should be reviewed by someone familiar with the schema
- Security changes should be reviewed by someone with security expertise
