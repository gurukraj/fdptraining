package com.workshop.taskmanager.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.workshop.taskmanager.dto.CommentRequest;
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
class CommentControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void shouldAddComment() throws Exception {
        CommentRequest request = new CommentRequest("This is a test comment for task 1");

        mockMvc.perform(post("/api/tasks/1/comments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "testuser")
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.text").value("This is a test comment for task 1"))
                .andExpect(jsonPath("$.author").value("testuser"))
                .andExpect(jsonPath("$.taskId").value(1));
    }

    @Test
    void shouldGetCommentsForTask() throws Exception {
        mockMvc.perform(get("/api/tasks/1/comments")
                        .header("X-User-Id", "testuser"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray())
                .andExpect(jsonPath("$.content", hasSize(greaterThanOrEqualTo(2))));
    }

    @Test
    void shouldDeleteCommentAsAdmin() throws Exception {
        // First add a comment
        CommentRequest request = new CommentRequest("Comment to be deleted by admin");
        String response = mockMvc.perform(post("/api/tasks/2/comments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "testuser")
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andReturn().getResponse().getContentAsString();

        Long commentId = new ObjectMapper().readTree(response).get("id").asLong();

        // Delete as admin
        mockMvc.perform(delete("/api/tasks/2/comments/" + commentId)
                        .header("X-User-Id", "admin1")
                        .header("X-User-Role", "ADMIN"))
                .andExpect(status().isNoContent());
    }

    @Test
    void shouldRejectCommentDeletionForNonAdmin() throws Exception {
        mockMvc.perform(delete("/api/tasks/1/comments/1")
                        .header("X-User-Id", "user1")
                        .header("X-User-Role", "USER"))
                .andExpect(status().isForbidden());
    }

    @Test
    void shouldReturn404ForCommentsOnNonExistentTask() throws Exception {
        mockMvc.perform(get("/api/tasks/9999/comments")
                        .header("X-User-Id", "testuser"))
                .andExpect(status().isNotFound());
    }

    @Test
    void shouldRejectEmptyComment() throws Exception {
        CommentRequest request = new CommentRequest("");

        mockMvc.perform(post("/api/tasks/1/comments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "testuser")
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest());
    }

    @Test
    void shouldPaginateComments() throws Exception {
        mockMvc.perform(get("/api/tasks/1/comments")
                        .param("page", "0")
                        .param("size", "5")
                        .header("X-User-Id", "testuser"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.size").value(5))
                .andExpect(jsonPath("$.page").value(0));
    }
}
