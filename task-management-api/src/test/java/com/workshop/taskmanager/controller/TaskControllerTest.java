package com.workshop.taskmanager.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.workshop.taskmanager.dto.TaskRequest;
import com.workshop.taskmanager.entity.TaskPriority;
import com.workshop.taskmanager.entity.TaskStatus;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class TaskControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void shouldCreateTask() throws Exception {
        TaskRequest request = new TaskRequest("Test task creation", "A test description", TaskPriority.HIGH, 1L);

        mockMvc.perform(post("/api/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "testuser")
                        .header("X-User-Role", "USER")
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.title").value("Test task creation"))
                .andExpect(jsonPath("$.status").value("OPEN"))
                .andExpect(jsonPath("$.priority").value("HIGH"))
                .andExpect(jsonPath("$.createdBy").value("testuser"));
    }

    @Test
    void shouldGetAllTasks() throws Exception {
        mockMvc.perform(get("/api/tasks")
                        .header("X-User-Id", "testuser"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray())
                .andExpect(jsonPath("$.totalElements").isNumber())
                .andExpect(jsonPath("$.page").value(0));
    }

    @Test
    void shouldFilterTasksByStatus() throws Exception {
        mockMvc.perform(get("/api/tasks")
                        .param("status", "OPEN")
                        .header("X-User-Id", "testuser"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray())
                .andExpect(jsonPath("$.content[*].status", everyItem(is("OPEN"))));
    }

    @Test
    void shouldFilterTasksByPriority() throws Exception {
        mockMvc.perform(get("/api/tasks")
                        .param("priority", "HIGH")
                        .header("X-User-Id", "testuser"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content[*].priority", everyItem(is("HIGH"))));
    }

    @Test
    void shouldFilterTasksByCategoryId() throws Exception {
        mockMvc.perform(get("/api/tasks")
                        .param("categoryId", "1")
                        .header("X-User-Id", "testuser"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content[*].categoryId", everyItem(is(1))));
    }

    @Test
    void shouldGetTaskById() throws Exception {
        mockMvc.perform(get("/api/tasks/1")
                        .header("X-User-Id", "testuser"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.title").value("Fix login page CSS"));
    }

    @Test
    void shouldReturn404ForNonExistentTask() throws Exception {
        mockMvc.perform(get("/api/tasks/9999")
                        .header("X-User-Id", "testuser"))
                .andExpect(status().isNotFound());
    }

    @Test
    void shouldUpdateTask() throws Exception {
        // Create a fresh task for this test
        TaskRequest createReq = new TaskRequest("Task to update", "Original description", TaskPriority.LOW, null);
        String createResponse = mockMvc.perform(post("/api/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "user1")
                        .content(objectMapper.writeValueAsString(createReq)))
                .andExpect(status().isCreated())
                .andReturn().getResponse().getContentAsString();
        Long taskId = objectMapper.readTree(createResponse).get("id").asLong();

        TaskRequest updateRequest = new TaskRequest();
        updateRequest.setTitle("Updated task title");

        mockMvc.perform(put("/api/tasks/" + taskId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "user1")
                        .content(objectMapper.writeValueAsString(updateRequest)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Updated task title"));
    }

    @Test
    void shouldValidateStatusTransition() throws Exception {
        // Create a fresh task for this test
        TaskRequest createReq = new TaskRequest("Transition test task", "Test transitions", TaskPriority.MEDIUM, null);
        String createResponse = mockMvc.perform(post("/api/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "testuser")
                        .content(objectMapper.writeValueAsString(createReq)))
                .andExpect(status().isCreated())
                .andReturn().getResponse().getContentAsString();
        Long taskId = objectMapper.readTree(createResponse).get("id").asLong();

        // OPEN -> IN_PROGRESS is valid
        TaskRequest request = new TaskRequest();
        request.setStatus(TaskStatus.IN_PROGRESS);

        mockMvc.perform(put("/api/tasks/" + taskId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "testuser")
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("IN_PROGRESS"));
    }

    @Test
    void shouldRejectInvalidStatusTransition() throws Exception {
        // OPEN -> DONE is invalid (must go through IN_PROGRESS)
        TaskRequest request = new TaskRequest();
        request.setStatus(TaskStatus.DONE);

        mockMvc.perform(put("/api/tasks/6")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "user1")
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest());
    }

    @Test
    void shouldSoftDeleteTask() throws Exception {
        // First create a task to delete
        TaskRequest request = new TaskRequest("Task to delete", "Will be deleted", TaskPriority.LOW, null);

        String response = mockMvc.perform(post("/api/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "testuser")
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andReturn().getResponse().getContentAsString();

        Long taskId = objectMapper.readTree(response).get("id").asLong();

        // Delete the task
        mockMvc.perform(delete("/api/tasks/" + taskId)
                        .header("X-User-Id", "testuser"))
                .andExpect(status().isNoContent());

        // Verify it's no longer retrievable
        mockMvc.perform(get("/api/tasks/" + taskId)
                        .header("X-User-Id", "testuser"))
                .andExpect(status().isNotFound());
    }

    @Test
    void shouldPaginateTasks() throws Exception {
        mockMvc.perform(get("/api/tasks")
                        .param("page", "0")
                        .param("size", "5")
                        .header("X-User-Id", "testuser"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.size").value(5))
                .andExpect(jsonPath("$.page").value(0))
                .andExpect(jsonPath("$.content", hasSize(lessThanOrEqualTo(5))));
    }

    @Test
    void shouldRejectTaskWithShortTitle() throws Exception {
        TaskRequest request = new TaskRequest("ab", "Description", TaskPriority.LOW, null);

        mockMvc.perform(post("/api/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "testuser")
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest());
    }
}
