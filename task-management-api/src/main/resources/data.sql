-- =====================================================
-- Seed Data for Task Management API
-- =====================================================

-- Categories
INSERT INTO categories (id, name, description, created_at, updated_at) VALUES (1, 'Bug', 'Bug fixes and defects', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO categories (id, name, description, created_at, updated_at) VALUES (2, 'Feature', 'New feature development', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO categories (id, name, description, created_at, updated_at) VALUES (3, 'Research', 'Research and investigation tasks', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO categories (id, name, description, created_at, updated_at) VALUES (4, 'Documentation', 'Documentation and knowledge base', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO categories (id, name, description, created_at, updated_at) VALUES (5, 'Testing', 'Testing and QA related tasks', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Tasks (20 tasks across different statuses, priorities, categories)
INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (1, 'Fix login page CSS', 'Login button misaligned on mobile devices running iOS 16+', 'OPEN', 'HIGH', 1, 'user1', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (2, 'Implement user dashboard', 'Create a dashboard showing task statistics and recent activity', 'IN_PROGRESS', 'HIGH', 2, 'user2', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (3, 'Research caching strategies', 'Evaluate Redis vs Caffeine for application-level caching', 'OPEN', 'MEDIUM', 3, 'user1', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (4, 'Write API documentation', 'Document all REST endpoints using OpenAPI/Swagger format', 'IN_PROGRESS', 'MEDIUM', 4, 'user3', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (5, 'Fix date parsing bug', 'Date fields not parsing correctly for timezone UTC+13', 'DONE', 'HIGH', 1, 'user2', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (6, 'Add email notifications', 'Send email when task status changes', 'OPEN', 'LOW', 2, 'user1', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (7, 'Setup CI/CD pipeline', 'Configure GitHub Actions for automated testing and deployment', 'DONE', 'HIGH', 2, 'user3', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (8, 'Integration test suite', 'Write comprehensive integration tests for all API endpoints', 'IN_PROGRESS', 'MEDIUM', 5, 'user2', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (9, 'Fix memory leak in reports', 'Reports generation causing memory leak when processing large datasets', 'OPEN', 'HIGH', 1, 'user1', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (10, 'Add dark mode support', 'Implement dark mode theme toggle for the frontend', 'OPEN', 'LOW', 2, 'user3', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (11, 'Evaluate database migration tools', 'Compare Flyway vs Liquibase for database schema migrations', 'DONE', 'MEDIUM', 3, 'user2', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (12, 'Update security dependencies', 'Upgrade Spring Security and related dependencies to latest version', 'OPEN', 'HIGH', 1, 'user1', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (13, 'Performance testing', 'Run load tests with JMeter to identify bottlenecks', 'IN_PROGRESS', 'MEDIUM', 5, 'user3', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (14, 'Create onboarding guide', 'Write developer onboarding documentation for new team members', 'OPEN', 'LOW', 4, 'user2', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (15, 'Implement file upload', 'Add file attachment support for tasks with S3 integration', 'OPEN', 'MEDIUM', 2, 'user1', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (16, 'Fix pagination offset bug', 'Pagination returns wrong results when offset exceeds total count', 'DONE', 'MEDIUM', 1, 'user3', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (17, 'Add rate limiting', 'Implement API rate limiting to prevent abuse', 'OPEN', 'MEDIUM', 2, 'user2', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (18, 'Research GraphQL migration', 'Evaluate feasibility of migrating from REST to GraphQL', 'OPEN', 'LOW', 3, 'user1', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (19, 'Unit test coverage report', 'Generate and review unit test coverage, aim for 80%+', 'IN_PROGRESS', 'MEDIUM', 5, 'user3', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (id, title, description, status, priority, category_id, created_by, deleted, created_at, updated_at)
VALUES (20, 'API versioning strategy', 'Document and implement API versioning using URL path strategy', 'OPEN', 'LOW', 4, 'user2', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Comments (15 comments across various tasks)
INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (1, 1, 'I can reproduce this on iPhone 13 with Safari browser', 'user2', false, CURRENT_TIMESTAMP);

INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (2, 1, 'Also happening on iPad Pro. Seems to be a flexbox issue.', 'user3', false, CURRENT_TIMESTAMP);

INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (3, 2, 'Dashboard wireframes are approved. Starting implementation.', 'user2', false, CURRENT_TIMESTAMP);

INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (4, 2, 'Should we include a chart library? Considering Chart.js vs D3.', 'user1', false, CURRENT_TIMESTAMP);

INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (5, 3, 'Redis would be better for distributed caching scenarios.', 'user3', false, CURRENT_TIMESTAMP);

INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (6, 4, 'Using springdoc-openapi for auto-generation. Works great!', 'user3', false, CURRENT_TIMESTAMP);

INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (7, 5, 'Fixed by using ZonedDateTime instead of LocalDateTime.', 'user2', false, CURRENT_TIMESTAMP);

INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (8, 8, 'Added tests for task CRUD. Working on category tests next.', 'user2', false, CURRENT_TIMESTAMP);

INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (9, 9, 'Profiling shows the issue is in the PDF generation library.', 'user1', false, CURRENT_TIMESTAMP);

INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (10, 9, 'Consider using async processing for large reports.', 'user3', false, CURRENT_TIMESTAMP);

INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (11, 12, 'CVE-2024-xxxx affects our current version. Priority upgrade needed.', 'user1', false, CURRENT_TIMESTAMP);

INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (12, 13, 'Initial load test shows 500ms p99 latency at 100 concurrent users.', 'user3', false, CURRENT_TIMESTAMP);

INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (13, 15, 'Max file size should be 10MB. Need to configure multipart settings.', 'user1', false, CURRENT_TIMESTAMP);

INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (14, 7, 'Pipeline is live! Builds trigger on push to main and PRs.', 'user3', false, CURRENT_TIMESTAMP);

INSERT INTO comments (id, task_id, text, author, deleted, created_at)
VALUES (15, 11, 'Flyway wins for simplicity. Liquibase is more powerful but complex.', 'user2', false, CURRENT_TIMESTAMP);

-- Audit Logs
INSERT INTO audit_logs (id, entity_type, entity_id, action, performed_by, details, created_at)
VALUES (1, 'TASK', 1, 'CREATE', 'user1', 'Task created: Fix login page CSS', CURRENT_TIMESTAMP);

INSERT INTO audit_logs (id, entity_type, entity_id, action, performed_by, details, created_at)
VALUES (2, 'TASK', 2, 'CREATE', 'user2', 'Task created: Implement user dashboard', CURRENT_TIMESTAMP);

INSERT INTO audit_logs (id, entity_type, entity_id, action, performed_by, details, created_at)
VALUES (3, 'TASK', 2, 'UPDATE', 'user2', 'Status changed: OPEN -> IN_PROGRESS', CURRENT_TIMESTAMP);

INSERT INTO audit_logs (id, entity_type, entity_id, action, performed_by, details, created_at)
VALUES (4, 'TASK', 5, 'CREATE', 'user2', 'Task created: Fix date parsing bug', CURRENT_TIMESTAMP);

INSERT INTO audit_logs (id, entity_type, entity_id, action, performed_by, details, created_at)
VALUES (5, 'TASK', 5, 'UPDATE', 'user2', 'Status changed: OPEN -> IN_PROGRESS -> DONE', CURRENT_TIMESTAMP);

INSERT INTO audit_logs (id, entity_type, entity_id, action, performed_by, details, created_at)
VALUES (6, 'CATEGORY', 1, 'CREATE', 'admin', 'Category created: Bug', CURRENT_TIMESTAMP);

INSERT INTO audit_logs (id, entity_type, entity_id, action, performed_by, details, created_at)
VALUES (7, 'CATEGORY', 2, 'CREATE', 'admin', 'Category created: Feature', CURRENT_TIMESTAMP);

INSERT INTO audit_logs (id, entity_type, entity_id, action, performed_by, details, created_at)
VALUES (8, 'COMMENT', 1, 'CREATE', 'user2', 'Comment added to task 1', CURRENT_TIMESTAMP);

INSERT INTO audit_logs (id, entity_type, entity_id, action, performed_by, details, created_at)
VALUES (9, 'TASK', 7, 'UPDATE', 'user3', 'Status changed: IN_PROGRESS -> DONE', CURRENT_TIMESTAMP);

INSERT INTO audit_logs (id, entity_type, entity_id, action, performed_by, details, created_at)
VALUES (10, 'TASK', 16, 'UPDATE', 'user3', 'Status changed: IN_PROGRESS -> DONE', CURRENT_TIMESTAMP);

-- Reset identity sequences to avoid conflicts with auto-generated IDs
ALTER TABLE categories ALTER COLUMN id RESTART WITH 100;
ALTER TABLE tasks ALTER COLUMN id RESTART WITH 100;
ALTER TABLE comments ALTER COLUMN id RESTART WITH 100;
ALTER TABLE audit_logs ALTER COLUMN id RESTART WITH 100;
