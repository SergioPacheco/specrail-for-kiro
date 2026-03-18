# Testing Steering

## Test strategy
- Unit tests: service layer with mocked dependencies (Mockito)
- Sliced tests: `@WebMvcTest` for controllers, `@DataJpaTest` for repositories
- Integration tests: `@SpringBootTest` with Testcontainers for full stack
- Contract tests: if other services consume your API, use Spring Cloud Contract or Pact

## Coverage expectations
- New service methods: 80%+ branch coverage
- Bug fixes: regression test that fails without the fix
- Refactoring: existing tests pass without modification
- New endpoints: at least one happy path + one error case via `@WebMvcTest`

## Test naming
```java
@Test
void should_return_user_when_id_exists() { }

@Test
void should_return_404_when_user_not_found() { }

@Test
void should_reject_request_when_email_invalid() { }
```

## Test structure (Arrange-Act-Assert)
```java
@Test
void should_create_user_and_return_201() {
    var request = new CreateUserRequest("<email>", "<name>");

    mockMvc.perform(post("/api/v1/users")
            .contentType(APPLICATION_JSON)
            .content(objectMapper.writeValueAsString(request)))
        .andExpect(status().isCreated())
        .andExpect(header().exists("Location"))
        .andExpect(jsonPath("$.email").value("<email>"));
}
```

## Sliced tests
- `@WebMvcTest(UserController.class)` — tests controller + validation, mocks service
- `@DataJpaTest` — tests repository queries against real DB (Testcontainers)
- `@SpringBootTest(webEnvironment = RANDOM_PORT)` — full integration test

## Database tests
- Use Testcontainers with same PostgreSQL version as production
- Flyway runs automatically in `@DataJpaTest` — validates migration scripts
- Never use H2 for tests — it hides PostgreSQL-specific behavior

## What NOT to test
- Spring auto-configuration wiring
- JPA entity getters/setters
- Framework internals (security filter chain, Hibernate cascade behavior)
