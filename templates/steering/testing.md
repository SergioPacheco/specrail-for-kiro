# Testing Steering

## Test strategy
- Unit tests for all service-layer business logic
- Integration tests for repository queries using Testcontainers (real PostgreSQL)
- Integration tests for REST endpoints using MockMvc or RestAssured
- No end-to-end browser tests unless explicitly requested (JSF pages are hard to test — focus on API layer)

## Coverage expectations
- New service methods: 80%+ branch coverage
- Bug fixes: must include a regression test that fails without the fix
- Refactoring: all existing tests must pass without modification — if a test breaks, the refactoring changed behavior
- Legacy code with no tests: add tests before modifying (at minimum, a characterization test that captures current behavior)

## Test naming
```java
// Pattern: should_expectedResult_when_condition
@Test
void should_return_user_when_email_exists() { }

@Test
void should_throw_not_found_when_user_deleted() { }

@Test
void should_rollback_when_payment_fails() { }
```

## Test structure
```java
@Test
void should_calculate_total_with_discount() {
    // Arrange
    var order = OrderBuilder.anOrder().withItems(3).withDiscount(10).build();

    // Act
    var total = pricingService.calculateTotal(order);

    // Assert
    assertThat(total).isEqualByComparingTo(new BigDecimal("27.00"));
}
```

## Test data
- Use builder pattern for test entities (`UserBuilder.aUser().withEmail("x").build()`)
- Never share mutable state between tests
- Integration tests: use `@Transactional` with rollback, or Testcontainers with fresh DB per class
- Never depend on data from other tests or from a shared seed script

## Database tests
- Use Testcontainers with the same PostgreSQL version as production
- Run Flyway migrations in test setup to validate migration scripts
- Test repository methods against real SQL, not H2 (H2 hides PostgreSQL-specific issues)

## What NOT to test
- JPA entity getters/setters
- Spring/CDI wiring (if it starts, it works)
- Framework behavior (Hibernate cascade, Spring Security filter chain internals)
- Private methods directly — test through the public API

## Legacy code testing rules
- Before modifying untested code: write a characterization test that captures current behavior
- If you can't test a class because it has too many dependencies: that's a design smell — extract and test the logic separately
- Prefer testing at the service boundary, not deep inside legacy spaghetti
