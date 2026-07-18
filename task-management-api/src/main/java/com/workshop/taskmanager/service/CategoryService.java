package com.workshop.taskmanager.service;

import com.workshop.taskmanager.dto.CategoryRequest;
import com.workshop.taskmanager.dto.CategoryResponse;
import com.workshop.taskmanager.entity.Category;
import com.workshop.taskmanager.exception.DuplicateResourceException;
import com.workshop.taskmanager.exception.ResourceNotFoundException;
import com.workshop.taskmanager.repository.CategoryRepository;
import com.workshop.taskmanager.repository.TaskRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class CategoryService {

    private final CategoryRepository categoryRepository;
    private final TaskRepository taskRepository;
    private final AuditLogService auditLogService;

    public CategoryService(CategoryRepository categoryRepository,
                          TaskRepository taskRepository,
                          AuditLogService auditLogService) {
        this.categoryRepository = categoryRepository;
        this.taskRepository = taskRepository;
        this.auditLogService = auditLogService;
    }

    @Transactional
    public CategoryResponse createCategory(CategoryRequest request, String userId) {
        if (categoryRepository.existsByNameIgnoreCase(request.getName())) {
            throw new DuplicateResourceException("Category with name '" + request.getName() + "' already exists");
        }

        Category category = new Category(request.getName(), request.getDescription());
        category = categoryRepository.save(category);

        auditLogService.log("CATEGORY", category.getId(), "CREATE", userId,
                "Category created: " + category.getName());

        return CategoryResponse.fromEntity(category);
    }

    @Transactional(readOnly = true)
    public Page<CategoryResponse> getAllCategories(Pageable pageable) {
        return categoryRepository.findAll(pageable)
                .map(CategoryResponse::fromEntity);
    }

    @Transactional(readOnly = true)
    public CategoryResponse getCategoryById(Long id) {
        Category category = categoryRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Category", id));
        return CategoryResponse.fromEntity(category);
    }

    @Transactional
    public CategoryResponse updateCategory(Long id, CategoryRequest request, String userId) {
        Category category = categoryRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Category", id));

        // Check for duplicate name (case-insensitive), excluding current category
        categoryRepository.findByNameIgnoreCase(request.getName())
                .ifPresent(existing -> {
                    if (!existing.getId().equals(id)) {
                        throw new DuplicateResourceException(
                                "Category with name '" + request.getName() + "' already exists");
                    }
                });

        category.setName(request.getName());
        category.setDescription(request.getDescription());
        category = categoryRepository.save(category);

        auditLogService.log("CATEGORY", category.getId(), "UPDATE", userId,
                "Category updated: " + category.getName());

        return CategoryResponse.fromEntity(category);
    }

    @Transactional
    public void deleteCategory(Long id, String userId) {
        Category category = categoryRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Category", id));

        // Check if any non-deleted tasks reference this category
        if (taskRepository.existsByCategoryIdAndDeletedFalse(id)) {
            throw new DuplicateResourceException(
                    "Cannot delete category '" + category.getName() + "': tasks are still associated with it");
        }

        categoryRepository.delete(category);

        auditLogService.log("CATEGORY", id, "DELETE", userId,
                "Category deleted: " + category.getName());
    }
}
