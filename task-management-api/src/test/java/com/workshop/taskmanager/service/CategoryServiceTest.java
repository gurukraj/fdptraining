package com.workshop.taskmanager.service;

import com.workshop.taskmanager.dto.CategoryRequest;
import com.workshop.taskmanager.dto.CategoryResponse;
import com.workshop.taskmanager.exception.DuplicateResourceException;
import com.workshop.taskmanager.exception.ResourceNotFoundException;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class CategoryServiceTest {

    @Autowired
    private CategoryService categoryService;

    @Test
    void shouldCreateCategory() {
        CategoryRequest request = new CategoryRequest("Design", "UI/UX design tasks");
        CategoryResponse response = categoryService.createCategory(request, "admin");

        assertNotNull(response.getId());
        assertEquals("Design", response.getName());
        assertEquals("UI/UX design tasks", response.getDescription());
    }

    @Test
    void shouldGetAllCategories() {
        Page<CategoryResponse> categories = categoryService.getAllCategories(PageRequest.of(0, 20));

        assertFalse(categories.isEmpty());
        assertTrue(categories.getTotalElements() >= 5); // Seed data has 5 categories
    }

    @Test
    void shouldGetCategoryById() {
        CategoryResponse response = categoryService.getCategoryById(1L);

        assertNotNull(response);
        assertEquals(1L, response.getId());
    }

    @Test
    void shouldThrowExceptionForNonExistentCategory() {
        assertThrows(ResourceNotFoundException.class,
                () -> categoryService.getCategoryById(99999L));
    }

    @Test
    void shouldRejectDuplicateCategoryName() {
        // "Feature" already exists in seed data
        CategoryRequest request = new CategoryRequest("feature", "Duplicate test");
        assertThrows(DuplicateResourceException.class,
                () -> categoryService.createCategory(request, "admin"));
    }

    @Test
    void shouldRejectDeletionOfCategoryWithTasks() {
        // Category 1 (Bug) has tasks associated
        assertThrows(DuplicateResourceException.class,
                () -> categoryService.deleteCategory(1L, "admin"));
    }

    @Test
    void shouldUpdateCategory() {
        CategoryRequest createReq = new CategoryRequest("Temp Category", "Temporary");
        CategoryResponse created = categoryService.createCategory(createReq, "admin");

        CategoryRequest updateReq = new CategoryRequest("Updated Temp Category", "Updated description");
        CategoryResponse updated = categoryService.updateCategory(created.getId(), updateReq, "admin");

        assertEquals("Updated Temp Category", updated.getName());
        assertEquals("Updated description", updated.getDescription());
    }
}
