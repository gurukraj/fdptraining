package com.workshop.taskmanager.controller;

import com.workshop.taskmanager.config.SecurityConfig;
import com.workshop.taskmanager.dto.PageResponse;
import com.workshop.taskmanager.dto.TaskRequest;
import com.workshop.taskmanager.dto.TaskResponse;
import com.workshop.taskmanager.entity.TaskPriority;
import com.workshop.taskmanager.entity.TaskStatus;
import com.workshop.taskmanager.service.TaskService;
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
@RequestMapping("/api/tasks")
public class TaskController {

    private final TaskService taskService;

    public TaskController(TaskService taskService) {
        this.taskService = taskService;
    }

    @PostMapping
    public ResponseEntity<TaskResponse> createTask(
            @Valid @RequestBody TaskRequest request,
            HttpServletRequest httpRequest) {
        String userId = SecurityConfig.getUserId(httpRequest);
        TaskResponse response = taskService.createTask(request, userId);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping
    public ResponseEntity<PageResponse<TaskResponse>> getTasks(
            @RequestParam(required = false) TaskStatus status,
            @RequestParam(required = false) TaskPriority priority,
            @RequestParam(required = false) Long categoryId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(defaultValue = "createdAt,desc") String sort) {

        // Enforce max page size
        if (size > 100) {
            size = 100;
        }

        // Parse sort parameter
        String[] sortParts = sort.split(",");
        String sortField = sortParts[0];
        Sort.Direction direction = sortParts.length > 1 && "asc".equalsIgnoreCase(sortParts[1])
                ? Sort.Direction.ASC : Sort.Direction.DESC;

        Pageable pageable = PageRequest.of(page, size, Sort.by(direction, sortField));
        Page<TaskResponse> tasks = taskService.getTasks(status, priority, categoryId, pageable);

        return ResponseEntity.ok(PageResponse.from(tasks));
    }

    @GetMapping("/{id}")
    public ResponseEntity<TaskResponse> getTaskById(@PathVariable Long id) {
        TaskResponse response = taskService.getTaskById(id);
        return ResponseEntity.ok(response);
    }

    @PutMapping("/{id}")
    public ResponseEntity<TaskResponse> updateTask(
            @PathVariable Long id,
            @RequestBody TaskRequest request,
            HttpServletRequest httpRequest) {
        String userId = SecurityConfig.getUserId(httpRequest);
        TaskResponse response = taskService.updateTask(id, request, userId);
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTask(
            @PathVariable Long id,
            HttpServletRequest httpRequest) {
        String userId = SecurityConfig.getUserId(httpRequest);
        taskService.deleteTask(id, userId);
        return ResponseEntity.noContent().build();
    }
}
