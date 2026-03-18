# Example: Java Legacy Project

A real walkthrough of using SpecRail on a brownfield Java enterprise system.

## The project

An internal order management system:
- Java 17, JSF 2.3, JPA/Hibernate, PostgreSQL 15
- Maven build, deployed as WAR on Tomcat
- ~200k lines of code, 8 years old, 3 developers
- Some modules have tests, many don't

## Setup

```bash
cd order-management
python path/to/specrail-for-kiro/scripts/bootstrap.py --pack java-legacy
```

Result:
```
.kiro/
├── steering/     ← 7 files with Java legacy standards
├── agents/       ← 5 agents ready to use
├── hooks/        ← 4 hooks
├── state/        ← STATE, DECISIONS, RISKS, CHANGELOG_AI
└── specs/        ← templates for features and bugfixes
```

## Step 1: Map the codebase

> "Map this codebase"

The codebase-mapper agent produces `.kiro/state/CODEBASE.md`:

```markdown
# Codebase Map

## Stack
- Language: Java 17 (OpenJDK Temurin)
- Framework: JSF 2.3 + CDI, JAX-RS for newer endpoints
- Persistence: JPA 2.2 / Hibernate 5.6
- Database: PostgreSQL 15, migrations via Flyway
- Build: Maven 3.9.4
- Tests: JUnit 5 + Mockito (partial coverage)

## Structure
src/main/java/com/acme/orders/
├── web/           ← JSF backing beans (legacy, tightly coupled)
├── rest/          ← JAX-RS endpoints (newer, better structured)
├── service/       ← Business logic (mixed quality)
├── repository/    ← JPA repositories
├── model/         ← JPA entities
├── dto/           ← DTOs (only for REST endpoints)
└── config/        ← CDI producers, Flyway config

## Patterns in use
- JSF beans use @ViewScoped and @SessionScoped
- Services are @ApplicationScoped CDI beans
- Repositories use EntityManager directly (no Spring Data)
- Error handling: inconsistent — some services throw custom exceptions,
  others return null, some use Optional
- Logging: SLF4J + Logback, but some classes still use System.out

## Concerns
- OrderService.java: 1,200 lines, handles pricing, validation, and notifications
- CustomerBean.java: JSF bean with SQL queries inside (bypasses service layer)
- No tests for: web/ package, half of service/ package
- Flyway migrations: V001 to V089, some missing rollback scripts
- Deprecated: javax.* imports (not yet migrated to jakarta.*)
```

This map is now available to the planner for every future feature.

---

## Example A: New Feature — "Add email notification on order status change"

### Step 2: Plan the feature

> "Plan a feature: send email notification when order status changes"

The planner reads CODEBASE.md and steering files, then starts the clarify phase:

**Planner asks:**
1. Which status transitions trigger email? (all, or specific ones like CONFIRMED → SHIPPED?)
2. Should the email be sent synchronously or async?
3. Is there an existing email service or do we need to create one?
4. What should the email contain? Just status, or order details too?

**You answer:**
1. Only CONFIRMED → SHIPPED and SHIPPED → DELIVERED
2. Async — don't block the status update
3. No existing email service. Use JavaMail with SMTP.
4. Order number, new status, estimated delivery date.

The planner saves this to `.kiro/specs/order-email-notification/CONTEXT.md` and produces:

**requirements.md:**
```markdown
# Requirements — Order Email Notification

## Summary
Send email notification to customer when order status changes to SHIPPED or DELIVERED.

## Acceptance criteria
- [ ] Email sent when status changes from CONFIRMED to SHIPPED
- [ ] Email sent when status changes from SHIPPED to DELIVERED
- [ ] Email contains: order number, new status, estimated delivery date
- [ ] Email is sent asynchronously (status update does not wait for email)
- [ ] Failed email does not rollback the status change
- [ ] Failed email is logged with order ID for retry
```

**design.md:**
```markdown
# Design — Order Email Notification

## Approach
Create a new EmailNotificationService that listens to order status changes
via CDI events. Async execution via @Asynchronous.

## Components affected
| Component | Change type | Risk |
|-----------|------------|------|
| OrderService | Modified — fire CDI event on status change | Low |
| EmailNotificationService | New | Low |
| EmailTemplate | New — Thymeleaf or plain text template | Low |
| application.properties | Modified — SMTP config | Low |

## Risks
| Risk | Impact | Mitigation |
|------|--------|-----------|
| SMTP server down | Emails not sent | Log failures, add retry queue later |
| OrderService is 1,200 lines | Merge conflicts | Minimal change — add 3 lines to fire event |

## Rollback strategy
Remove the CDI event observer. Status changes continue to work without notification.
```

**tasks.md:**
```markdown
# Tasks — Order Email Notification

### Task 1: Create EmailNotificationService
- Files: src/main/java/com/acme/orders/service/EmailNotificationService.java
- Done criteria:
  - [ ] Service compiles and is injectable via CDI
  - [ ] Unit test verifies email content generation
- Commit: feat(notification): add EmailNotificationService
- Parallel: yes

### Task 2: Add SMTP configuration
- Files: src/main/resources/application.properties
- Done criteria:
  - [ ] SMTP host, port, from-address configurable via properties
  - [ ] No credentials hardcoded (use env vars)
- Commit: feat(notification): add SMTP configuration
- Parallel: yes

### Task 3: Fire CDI event on status change
- Files: src/main/java/com/acme/orders/service/OrderService.java
- Done criteria:
  - [ ] CDI event fired when status changes to SHIPPED or DELIVERED
  - [ ] Existing tests still pass
  - [ ] No other behavior changed in OrderService
- Commit: feat(notification): fire event on order status change
- Dependencies: Task 1

### Task 4: Add integration test
- Files: src/test/java/com/acme/orders/service/EmailNotificationServiceTest.java
- Done criteria:
  - [ ] Test verifies email is sent on CONFIRMED→SHIPPED
  - [ ] Test verifies email is NOT sent on other transitions
  - [ ] Test verifies async execution (status update returns before email)
- Commit: test(notification): add email notification integration test
- Dependencies: Task 1, Task 3
```

### Step 3: Execute and verify

Each task is executed, hooks validate, one commit per task. After all 4 tasks:

> "Verify the order-email-notification feature"

The verifier checks all criteria and produces:

```
## Verification Report

**Spec:** order-email-notification
**Verdict:** PASS WITH NOTES

### Criteria check
- [x] Email sent on CONFIRMED → SHIPPED
- [x] Email sent on SHIPPED → DELIVERED
- [x] Email contains order number, status, delivery date
- [x] Async execution confirmed
- [x] Failed email logged, does not rollback status

### Notes
- Consider adding a retry mechanism for failed emails (logged as risk)
- OrderService is now 1,215 lines — consider extracting status management
```

### Step 4: Archive

```
.kiro/specs/order-email-notification/ → .kiro/specs/archive/2026-03-17-order-email-notification/
```

---

## Example B: Bugfix — "Discount calculation returns wrong total for orders with 10+ items"

### Step 1: Investigate

> "Bug: orders with 10+ items show wrong discount total"

The bugfix-investigator starts:

**Reproduce:**
```
1. Create order with 12 items, each $10.00
2. Apply 15% discount
3. Expected total: $102.00
4. Actual total: $103.80
```

**Root cause:**
```java
// OrderService.java line 847
BigDecimal discount = total.multiply(discountRate)
    .setScale(2, RoundingMode.HALF_UP);
// BUG: discount is calculated on the pre-tax total,
// but applied after tax is added. The tax calculation
// on line 842 uses a different rounding mode (FLOOR).
// With 10+ items, the rounding errors accumulate.
```

**Impact:**
- Affects all orders with discount + 10 or more items
- Financial impact: customers are overcharged by $0.01-$2.00 per order
- No data corruption — recalculation will fix historical orders

**bugfix.md:**
```markdown
# Bugfix — Discount Rounding Error

## Reproduction steps
1. Create order with 12 items at $10.00 each
2. Apply 15% discount
3. Observe: total is $103.80 instead of $102.00

## Root cause
Discount calculated on pre-tax total but applied after tax.
Tax uses FLOOR rounding, discount uses HALF_UP.
With 10+ items, rounding errors accumulate to visible amounts.

## Fix approach
Calculate discount before tax, using consistent HALF_UP rounding
throughout the pricing pipeline.
```

**tasks.md:**
```markdown
### Task 1: Write regression test
- Files: src/test/java/com/acme/orders/service/PricingTest.java
- Done criteria:
  - [ ] Test with 12 items + 15% discount fails with current code
  - [ ] Test asserts exact expected total: $102.00
- Commit: test(pricing): add regression test for discount rounding #456

### Task 2: Fix rounding in OrderService
- Files: src/main/java/com/acme/orders/service/OrderService.java
- Done criteria:
  - [ ] Regression test passes
  - [ ] All existing pricing tests pass
  - [ ] Rounding mode is HALF_UP consistently
- Commit: fix(pricing): use consistent rounding in discount calculation #456

### Task 3: Update state
- Commit: docs(state): record discount rounding fix
```

After execution, the verifier confirms PASS, and the spec is archived.

---

## Key takeaways

1. **Map first** — the codebase-mapper gives the planner context about the 1,200-line OrderService, the inconsistent error handling, and the missing tests. Without this, the planner would suggest changes blindly.

2. **Clarify before planning** — the planner asked 4 questions that prevented wrong assumptions (sync vs async, which transitions, existing email service).

3. **Bugfix discipline** — the investigator found the real root cause (rounding mode mismatch) instead of just patching the symptom. The regression test proves the fix works.

4. **Atomic commits** — each task is one commit. If the email notification causes issues, you can revert task 3 without losing task 1 and 2.

5. **State persists** — DECISIONS.md records "chose CDI events over direct call for notification". Next session, the planner knows this decision exists.
