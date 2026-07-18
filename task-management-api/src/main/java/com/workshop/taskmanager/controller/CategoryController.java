package com.workshop.taskmanager.controller;

import com.workshop.taskmanager.config.SecurityConfig;
import com.workshop.taskmanager.dto.CategoryRequest;
import com.workshop.taskmanager.dto.CategoryResponse;
import com.workshop.taskmanager.dto.PageResponse;
import com.workshop.taskmanager.exception.AccessDeniedException;
import com.workshop.taskmanager.service.CategoryService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/categories")
public class CategoryController {

    private final CategoryService categoryService;

    public CategoryController(CategoryService categoryService) {
        this.categoryService = categoryService;
    }

    @PostMapping
    public ResponseEntity<CategoryResponse> createCategory(
            @Valid @RequestBody CategoryRequest request,
            HttpServletRequest httpRequest) {
        if (!SecurityConfig.isAdmin(httpRequest)) {
            throw new AccessDeniedException("Only administrators can create categories");
        }
        String userId = SecurityConfig.getUserId(httpRequest);
        CategoryResponse response = categoryService.createCategory(request, userId);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping
    public ResponseEntity<PageResponse<CategoryResponse>> getAllCategories(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by("name").ascending());
        Page<CategoryResponse> categories = categoryService.getAllCategories(pageable);
        return ResponseEntity.ok(PageResponse.from(categories));
    }

    @GetMapping("/{id}")
    public ResponseEntity<CategoryResponse> getCategoryById(@PathVariable Long id) {
        CategoryResponse response = categoryService.getCategoryById(id);
        return ResponseEntity.ok(response);
    }

    @PutMapping("/{id}")
    public ResponseEntity<CategoryResponse> updateCategory(
            @PathVariable Long id,
            @Valid @RequestBody CategoryRequest request,
            HttpServletRequest httpRequest) {
        String userId = SecurityConfig.getUserId(httpRequest);
        CategoryResponse response = categoryService.updateCategory(id, request, userId);
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteCategory(
            @PathVariable Long id,
            HttpServletRequest httpRequest) {
        if (!SecurityConfig.isAdmin(httpRequest)) {
            throw new AccessDeniedException("Only administrators can delete categories");
        }
        String userId = SecurityConfig.getUserId(httpRequest);
        categoryService.deleteCategory(id, userId);
        return ResponseEntity.noContent().build();
    }
}
