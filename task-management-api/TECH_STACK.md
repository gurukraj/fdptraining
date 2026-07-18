# Technology Stack

## Java 21

Java 21 is a Long-Term Support (LTS) release with several modern language features:

- **Records**: Immutable data carriers with auto-generated `equals()`, `hashCode()`, and `toString()`
- **Pattern Matching**: Enhanced `instanceof` and `switch` expressions for cleaner type checks
- **Sealed Classes**: Restricted class hierarchies for better domain modeling
- **Virtual Threads (Project Loom)**: Lightweight threads for high-throughput concurrent applications
- **Text Blocks**: Multi-line string literals for cleaner SQL queries and JSON templates
- **Enhanced Switch Expressions**: More concise and expressive switch statements

### Why Java 21?
- Latest LTS release with long-term vendor support
- Performance improvements over Java 17 (previous LTS)
- Modern language features reduce boilerplate code
- Full compatibility with Spring Boot 3.x

---

## Spring Boot 3.4.x

Spring Boot provides an opinionated, production-ready framework for building Spring applications:

- **Auto-Configuration**: Automatically configures beans based on classpath dependencies
- **Embedded Server**: Runs Tomcat embedded (no external server deployment needed)
- **Starter Dependencies**: Curated dependency sets (e.g., `spring-boot-starter-web`)
- **Actuator**: Production-ready monitoring and management endpoints
- **DevTools**: Hot reload and development-time optimizations

### Key Starters Used
| Starter | Purpose |
|---------|---------|
| `spring-boot-starter-web` | REST API with embedded Tomcat |
| `spring-boot-starter-data-jpa` | JPA/Hibernate ORM |
| `spring-boot-starter-validation` | Bean Validation (Jakarta) |
| `spring-boot-starter-test` | Testing framework (JUnit 5, MockMvc) |

---

## Spring Data JPA

Spring Data JPA simplifies database access with the Repository pattern:

- **Repository Pattern**: Declare interfaces, Spring generates implementations
- **Query Derivation**: Method names become queries (`findByStatusAndDeletedFalse`)
- **Custom Queries**: JPQL with `@Query` annotation for complex queries
- **Pagination**: Built-in `Pageable` and `Page` support
- **Auditing**: Automatic `createdAt`/`updatedAt` timestamps

### Example
```java
// Spring generates the SQL automatically from the method name
Page<Task> findAllByStatusAndDeletedFalse(TaskStatus status, Pageable pageable);
```

---

## H2 Database

H2 is an in-memory relational database ideal for development and testing:

- **Zero Configuration**: No installation, no Docker required
- **In-Memory Mode**: Data resets on restart (perfect for workshops)
- **Web Console**: Built-in browser-based SQL console at `/h2-console`
- **SQL Compatible**: Supports standard SQL, easy to switch to PostgreSQL
- **Fast**: Extremely fast for development and testing cycles

### Switching to PostgreSQL
The project includes a `postgres` Spring profile for production use:
```bash
# Start PostgreSQL
docker-compose up -d

# Run with PostgreSQL
mvn spring-boot:run -Dspring-boot.run.profiles=postgres
```

---

## Bean Validation (Jakarta Validation)

Declarative validation using annotations on DTOs and entities:

- **`@NotBlank`**: Ensures non-null, non-empty strings
- **`@Size`**: Validates string length (`min`, `max`)
- **`@Valid`**: Triggers validation in controller methods
- **Custom Messages**: User-friendly error messages per constraint

### Example
```java
public class TaskRequest {
    @Size(min = 3, max = 200, message = "Title must be between 3 and 200 characters")
    private String title;
}
```

---

## Maven

Apache Maven handles project build, dependency management, and lifecycle:

- **POM (Project Object Model)**: Declarative project configuration in `pom.xml`
- **Dependency Management**: Transitive dependency resolution with version management
- **Build Lifecycle**: Standard phases (`compile`, `test`, `package`, `install`)
- **Spring Boot Plugin**: Creates executable JARs with embedded server

### Common Commands
```bash
mvn clean compile       # Compile the project
mvn test                # Run tests
mvn clean package       # Build executable JAR
mvn spring-boot:run     # Run the application
```

---

## Architecture Overview

```
Client (HTTP)
    |
    v
[Controller Layer]  <-- REST endpoints, validation, request/response mapping
    |
    v
[Service Layer]     <-- Business logic, status transitions, audit logging
    |
    v
[Repository Layer]  <-- Data access, JPA queries, pagination
    |
    v
[Database (H2/PostgreSQL)]
```

This layered architecture ensures:
- **Separation of Concerns**: Each layer has a clear responsibility
- **Testability**: Layers can be tested independently
- **Maintainability**: Changes are isolated to specific layers
- **Flexibility**: Database or presentation can change without affecting business logic
