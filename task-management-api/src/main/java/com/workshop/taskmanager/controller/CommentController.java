package com.workshop.taskmanager.controller;

import com.workshop.taskmanager.config.SecurityConfig;
import com.workshop.taskmanager.dto.CommentRequest;
import com.workshop.taskmanager.dto.CommentResponse;
import com.workshop.taskmanager.dto.PageResponse;
import com.workshop.taskmanager.exception.AccessDeniedException;
import com.workshop.taskmanager.service.CommentService;
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
@RequestMapping("/api/tasks/{taskId}/comments")
public class CommentController {

    private final CommentService commentService;

    public CommentController(CommentService commentService) {
        this.commentService = commentService;
    }

    @PostMapping
    public ResponseEntity<CommentResponse> addComment(
            @PathVariable Long taskId,
            @Valid @RequestBody CommentRequest request,
            HttpServletRequest httpRequest) {
        String userId = SecurityConfig.getUserId(httpRequest);
        CommentResponse response = commentService.addComment(taskId, request, userId);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping
    public ResponseEntity<PageResponse<CommentResponse>> getComments(
            @PathVariable Long taskId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
        Page<CommentResponse> comments = commentService.getComments(taskId, pageable);
        return ResponseEntity.ok(PageResponse.from(comments));
    }

    @DeleteMapping("/{commentId}")
    public ResponseEntity<Void> deleteComment(
            @PathVariable Long taskId,
            @PathVariable Long commentId,
            HttpServletRequest httpRequest) {
        if (!SecurityConfig.isAdmin(httpRequest)) {
            throw new AccessDeniedException("Only administrators can delete comments");
        }
        String userId = SecurityConfig.getUserId(httpRequest);
        commentService.deleteComment(taskId, commentId, userId);
        return ResponseEntity.noContent().build();
    }
}
