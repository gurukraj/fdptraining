package com.workshop.taskmanager.service;

import com.workshop.taskmanager.dto.TaskRequest;
import com.workshop.taskmanager.dto.TaskResponse;
import com.workshop.taskmanager.entity.TaskPriority;
import com.workshop.taskmanager.entity.TaskStatus;
import com.workshop.taskmanager.exception.InvalidStatusTransitionException;
import com.workshop.taskmanager.exception.ResourceNotFoundException;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class TaskServiceTest {

    @Autowired
    private TaskService taskService;

    @Test
    void shouldCreateTaskWithDefaults() {
        TaskRequest request = new TaskRequest("Service test task", "Testing service layer", null, null);
        TaskResponse response = taskService.createTask(request, "serviceTestUser");

        assertNotNull(response.getId());
        assertEquals("Service test task", response.getTitle());
        assertEquals(TaskStatus.OPEN, response.getStatus());
        assertEquals(TaskPriority.MEDIUM, response.getPriority());
        assertEquals("serviceTestUser", response.getCreatedBy());
    }

    @Test
    void shouldCreateTaskWithSpecifiedPriority() {
        TaskRequest request = new TaskRequest("High priority task", "Urgent task", TaskPriority.HIGH, 1L);
        TaskResponse response = taskService.createTask(request, "user1");

        assertEquals(TaskPriority.HIGH, response.getPriority());
        assertNotNull(response.getCategoryId());
    }

    @Test
    void shouldGetTaskById() {
        TaskResponse response = taskService.getTaskById(1L);

        assertNotNull(response);
        assertEquals(1L, response.getId());
        assertEquals("Fix login page CSS", response.getTitle());
    }

    @Test
    void shouldThrowExceptionForNonExistentTask() {
        assertThrows(ResourceNotFoundException.class,
                () -> taskService.getTaskById(99999L));
    }

    @Test
    void shouldFilterTasksByStatus() {
        Page<TaskResponse> openTasks = taskService.getTasks(
                TaskStatus.OPEN, null, null, PageRequest.of(0, 20));

        assertFalse(openTasks.isEmpty());
        openTasks.getContent().forEach(task ->
                assertEquals(TaskStatus.OPEN, task.getStatus()));
    }

    @Test
    void shouldFilterTasksByPriority() {
        Page<TaskResponse> highPriorityTasks = taskService.getTasks(
                null, TaskPriority.HIGH, null, PageRequest.of(0, 20));

        assertFalse(highPriorityTasks.isEmpty());
        highPriorityTasks.getContent().forEach(task ->
                assertEquals(TaskPriority.HIGH, task.getPriority()));
    }

    @Test
    void shouldValidateStatusTransitionOpenToInProgress() {
        // OPEN -> IN_PROGRESS should be valid
        assertDoesNotThrow(() ->
                taskService.validateStatusTransition(TaskStatus.OPEN, TaskStatus.IN_PROGRESS));
    }

    @Test
    void shouldValidateStatusTransitionInProgressToDone() {
        // IN_PROGRESS -> DONE should be valid
        assertDoesNotThrow(() ->
                taskService.validateStatusTransition(TaskStatus.IN_PROGRESS, TaskStatus.DONE));
    }

    @Test
    void shouldValidateStatusTransitionInProgressToOpen() {
        // IN_PROGRESS -> OPEN should be valid (reopen)
        assertDoesNotThrow(() ->
                taskService.validateStatusTransition(TaskStatus.IN_PROGRESS, TaskStatus.OPEN));
    }

    @Test
    void shouldValidateStatusTransitionDoneToOpen() {
        // DONE -> OPEN should be valid (reopen)
        assertDoesNotThrow(() ->
                taskService.validateStatusTransition(TaskStatus.DONE, TaskStatus.OPEN));
    }

    @Test
    void shouldRejectInvalidTransitionOpenToDone() {
        // OPEN -> DONE should be invalid
        assertThrows(InvalidStatusTransitionException.class,
                () -> taskService.validateStatusTransition(TaskStatus.OPEN, TaskStatus.DONE));
    }

    @Test
    void shouldRejectInvalidTransitionDoneToInProgress() {
        // DONE -> IN_PROGRESS should be invalid
        assertThrows(InvalidStatusTransitionException.class,
                () -> taskService.validateStatusTransition(TaskStatus.DONE, TaskStatus.IN_PROGRESS));
    }

    @Test
    void shouldRejectTaskWithShortTitle() {
        TaskRequest request = new TaskRequest("ab", "Short title", TaskPriority.LOW, null);
        assertThrows(IllegalArgumentException.class,
                () -> taskService.createTask(request, "user1"));
    }

    @Test
    void shouldSoftDeleteTask() {
        // Create a task first
        TaskRequest request = new TaskRequest("Task to soft delete", "Will be deleted", TaskPriority.LOW, null);
        TaskResponse created = taskService.createTask(request, "user1");

        // Delete it
        taskService.deleteTask(created.getId(), "user1");

        // Verify it's gone
        assertThrows(ResourceNotFoundException.class,
                () -> taskService.getTaskById(created.getId()));
    }

    @Test
    void shouldUpdateTaskTitle() {
        // Create a task
        TaskRequest createRequest = new TaskRequest("Original title", "Description", TaskPriority.MEDIUM, null);
        TaskResponse created = taskService.createTask(createRequest, "user1");

        // Update title
        TaskRequest updateRequest = new TaskRequest();
        updateRequest.setTitle("Updated title");
        TaskResponse updated = taskService.updateTask(created.getId(), updateRequest, "user1");

        assertEquals("Updated title", updated.getTitle());
    }
}
