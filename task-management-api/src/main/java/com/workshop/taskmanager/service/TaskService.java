package com.workshop.taskmanager.service;

import com.workshop.taskmanager.dto.TaskRequest;
import com.workshop.taskmanager.dto.TaskResponse;
import com.workshop.taskmanager.entity.Category;
import com.workshop.taskmanager.entity.Task;
import com.workshop.taskmanager.entity.TaskPriority;
import com.workshop.taskmanager.entity.TaskStatus;
import com.workshop.taskmanager.exception.InvalidStatusTransitionException;
import com.workshop.taskmanager.exception.ResourceNotFoundException;
import com.workshop.taskmanager.repository.CategoryRepository;
import com.workshop.taskmanager.repository.CommentRepository;
import com.workshop.taskmanager.repository.TaskRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Set;

@Service
public class TaskService {

    private final TaskRepository taskRepository;
    private final CategoryRepository categoryRepository;
    private final CommentRepository commentRepository;
    private final AuditLogService auditLogService;

    // Valid status transitions: from -> allowed targets
    private static final java.util.Map<TaskStatus, Set<TaskStatus>> VALID_TRANSITIONS = java.util.Map.of(
            TaskStatus.OPEN, Set.of(TaskStatus.IN_PROGRESS),
            TaskStatus.IN_PROGRESS, Set.of(TaskStatus.DONE, TaskStatus.OPEN),
            TaskStatus.DONE, Set.of(TaskStatus.OPEN)
    );

    public TaskService(TaskRepository taskRepository,
                      CategoryRepository categoryRepository,
                      CommentRepository commentRepository,
                      AuditLogService auditLogService) {
        this.taskRepository = taskRepository;
        this.categoryRepository = categoryRepository;
        this.commentRepository = commentRepository;
        this.auditLogService = auditLogService;
    }

    @Transactional
    public TaskResponse createTask(TaskRequest request, String userId) {
        if (request.getTitle() == null || request.getTitle().length() < 3) {
            throw new IllegalArgumentException("Title must be at least 3 characters");
        }

        Category category = null;
        if (request.getCategoryId() != null) {
            category = categoryRepository.findById(request.getCategoryId())
                    .orElseThrow(() -> new ResourceNotFoundException("Category", request.getCategoryId()));
        }

        Task task = new Task(
                request.getTitle(),
                request.getDescription(),
                request.getPriority() != null ? request.getPriority() : TaskPriority.MEDIUM,
                category,
                userId
        );

        task = taskRepository.save(task);

        auditLogService.log("TASK", task.getId(), "CREATE", userId,
                "Task created: " + task.getTitle());

        return TaskResponse.fromEntity(task);
    }

    @Transactional(readOnly = true)
    public Page<TaskResponse> getTasks(TaskStatus status, TaskPriority priority,
                                       Long categoryId, Pageable pageable) {
        return taskRepository.findAllWithFilters(status, priority, categoryId, pageable)
                .map(TaskResponse::fromEntity);
    }

    @Transactional(readOnly = true)
    public TaskResponse getTaskById(Long id) {
        Task task = taskRepository.findByIdAndDeletedFalse(id)
                .orElseThrow(() -> new ResourceNotFoundException("Task", id));
        return TaskResponse.fromEntity(task);
    }

    @Transactional
    public TaskResponse updateTask(Long id, TaskRequest request, String userId) {
        Task task = taskRepository.findByIdAndDeletedFalse(id)
                .orElseThrow(() -> new ResourceNotFoundException("Task", id));

        // Update title if provided
        if (request.getTitle() != null) {
            if (request.getTitle().length() < 3 || request.getTitle().length() > 200) {
                throw new IllegalArgumentException("Title must be between 3 and 200 characters");
            }
            task.setTitle(request.getTitle());
        }

        // Update description if provided
        if (request.getDescription() != null) {
            task.setDescription(request.getDescription());
        }

        // Update priority if provided
        if (request.getPriority() != null) {
            task.setPriority(request.getPriority());
        }

        // Update category if provided
        if (request.getCategoryId() != null) {
            Category category = categoryRepository.findById(request.getCategoryId())
                    .orElseThrow(() -> new ResourceNotFoundException("Category", request.getCategoryId()));
            task.setCategory(category);
        }

        // Update status if provided (with transition validation)
        if (request.getStatus() != null && request.getStatus() != task.getStatus()) {
            validateStatusTransition(task.getStatus(), request.getStatus());
            task.setStatus(request.getStatus());
        }

        task = taskRepository.save(task);

        auditLogService.log("TASK", task.getId(), "UPDATE", userId,
                "Task updated: " + task.getTitle());

        return TaskResponse.fromEntity(task);
    }

    @Transactional
    public void deleteTask(Long id, String userId) {
        Task task = taskRepository.findByIdAndDeletedFalse(id)
                .orElseThrow(() -> new ResourceNotFoundException("Task", id));

        // Soft delete the task
        task.setDeleted(true);
        task.setDeletedAt(LocalDateTime.now());
        taskRepository.save(task);

        // Cascade soft-delete comments
        commentRepository.softDeleteByTaskId(id);

        auditLogService.log("TASK", id, "DELETE", userId,
                "Task soft-deleted: " + task.getTitle());
    }

    public void validateStatusTransition(TaskStatus from, TaskStatus to) {
        Set<TaskStatus> allowed = VALID_TRANSITIONS.get(from);
        if (allowed == null || !allowed.contains(to)) {
            throw new InvalidStatusTransitionException(from, to);
        }
    }
}
