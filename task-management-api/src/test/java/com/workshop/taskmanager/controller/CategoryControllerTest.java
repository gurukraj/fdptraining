package com.workshop.taskmanager.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.workshop.taskmanager.dto.CategoryRequest;
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
class CategoryControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void shouldCreateCategoryAsAdmin() throws Exception {
        CategoryRequest request = new CategoryRequest("DevOps", "DevOps and infrastructure tasks");

        mockMvc.perform(post("/api/categories")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "admin1")
                        .header("X-User-Role", "ADMIN")
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name").value("DevOps"))
                .andExpect(jsonPath("$.description").value("DevOps and infrastructure tasks"));
    }

    @Test
    void shouldRejectCategoryCreationForNonAdmin() throws Exception {
        CategoryRequest request = new CategoryRequest("Unauthorized Category", "Should fail");

        mockMvc.perform(post("/api/categories")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "user1")
                        .header("X-User-Role", "USER")
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isForbidden());
    }

    @Test
    void shouldGetAllCategories() throws Exception {
        mockMvc.perform(get("/api/categories")
                        .header("X-User-Id", "user1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray())
                .andExpect(jsonPath("$.content", hasSize(greaterThanOrEqualTo(5))));
    }

    @Test
    void shouldGetCategoryById() throws Exception {
        mockMvc.perform(get("/api/categories/1")
                        .header("X-User-Id", "user1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("Bug"));
    }

    @Test
    void shouldUpdateCategory() throws Exception {
        // First create a category to update
        CategoryRequest createRequest = new CategoryRequest("UpdatableCategory", "Will be updated");
        String response = mockMvc.perform(post("/api/categories")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "admin1")
                        .header("X-User-Role", "ADMIN")
                        .content(objectMapper.writeValueAsString(createRequest)))
                .andExpect(status().isCreated())
                .andReturn().getResponse().getContentAsString();

        Long categoryId = objectMapper.readTree(response).get("id").asLong();

        // Update the category
        CategoryRequest updateRequest = new CategoryRequest("UpdatedCategory", "Updated description");
        mockMvc.perform(put("/api/categories/" + categoryId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "admin1")
                        .header("X-User-Role", "ADMIN")
                        .content(objectMapper.writeValueAsString(updateRequest)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("UpdatedCategory"));
    }

    @Test
    void shouldRejectDuplicateCategoryName() throws Exception {
        CategoryRequest request = new CategoryRequest("Feature", "Duplicate name test");

        mockMvc.perform(post("/api/categories")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("X-User-Id", "admin1")
                        .header("X-User-Role", "ADMIN")
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isConflict());
    }

    @Test
    void shouldRejectDeleteCategoryWithTasks() throws Exception {
        // Category 2 (Feature) has tasks associated with it
        mockMvc.perform(delete("/api/categories/2")
                        .header("X-User-Id", "admin1")
                        .header("X-User-Role", "ADMIN"))
                .andExpect(status().isConflict());
    }

    @Test
    void shouldRejectCategoryDeletionForNonAdmin() throws Exception {
        mockMvc.perform(delete("/api/categories/1")
                        .header("X-User-Id", "user1")
                        .header("X-User-Role", "USER"))
                .andExpect(status().isForbidden());
    }

    @Test
    void shouldReturn404ForNonExistentCategory() throws Exception {
        mockMvc.perform(get("/api/categories/9999")
                        .header("X-User-Id", "user1"))
                .andExpect(status().isNotFound());
    }
}
