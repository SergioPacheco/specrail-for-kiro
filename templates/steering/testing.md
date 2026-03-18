# Testing Steering

## Test strategy
- Unit tests for business logic (services, utilities)
- Integration tests for database operations and external APIs
- End-to-end tests for critical user flows only

## Coverage expectations
- New code: aim for 80%+ line coverage on business logic
- Bug fixes: must include a regression test that reproduces the bug
- Refactoring: existing tests must pass without modification

## Test naming
- Pattern: `should_<expected>_when_<condition>`
- Example: `should_return_404_when_user_not_found`

## Test structure
- Arrange / Act / Assert (AAA pattern)
- One assertion per test when possible
- No logic in tests (no if/else, no loops)

## Test data
- Use builders or factories for test data
- Never depend on shared mutable test state
- Database tests use isolated transactions or test containers

## What NOT to test
- Framework internals (Spring wiring, JPA generated queries)
- Trivial getters/setters
- Third-party library behavior
