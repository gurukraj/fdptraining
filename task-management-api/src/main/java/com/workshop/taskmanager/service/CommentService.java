package com.workshop.taskmanager.service;

import com.workshop.taskmanager.dto.CommentRequest;
import com.workshop.taskmanager.dto.CommentResponse;
import com.workshop.taskmanager.entity.Comment;
import com.workshop.taskmanager.entity.Task;
import com.workshop.taskmanager.exception.ResourceNotFoundException;
import com.workshop.taskmanager.repository.CommentRepository;
import com.workshop.taskmanager.repository.TaskRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class CommentService {

    private final CommentRepository commentRepository;
    private final TaskRepository taskRepository;
    private final AuditLogService auditLogService;

    public CommentService(CommentRepository commentRepository,
                         TaskRepository taskRepository,
                         AuditLogService auditLogService) {
        this.commentRepository = commentRepository;
        this.taskRepository = taskRepository;
        this.auditLogService = auditLogService;
    }

    @Transactional
    public CommentResponse addComment(Long taskId, CommentRequest request, String userId) {
        Task task = taskRepository.findByIdAndDeletedFalse(taskId)
                .orElseThrow(() -> new ResourceNotFoundException("Task", taskId));

        Comment comment = new Comment(task, request.getText(), userId);
        comment = commentRepository.save(comment);

        auditLogService.log("COMMENT", comment.getId(), "CREATE", userId,
                "Comment added to task " + taskId);

        return CommentResponse.fromEntity(comment);
    }

    @Transactional(readOnly = true)
    public Page<CommentResponse> getComments(Long taskId, Pageable pageable) {
        // Verify task exists
        taskRepository.findByIdAndDeletedFalse(taskId)
                .orElseThrow(() -> new ResourceNotFoundException("Task", taskId));

        return commentRepository.findByTaskIdAndDeletedFalse(taskId, pageable)
                .map(CommentResponse::fromEntity);
    }

    @Transactional
    public void deleteComment(Long taskId, Long commentId, String userId) {
        // Verify task exists
        taskRepository.findByIdAndDeletedFalse(taskId)
                .orElseThrow(() -> new ResourceNotFoundException("Task", taskId));

        Comment comment = commentRepository.findById(commentId)
                .orElseThrow(() -> new ResourceNotFoundException("Comment", commentId));

        if (!comment.getTask().getId().equals(taskId)) {
            throw new ResourceNotFoundException("Comment " + commentId + " does not belong to task " + taskId);
        }

        comment.setDeleted(true);
        commentRepository.save(comment);

        auditLogService.log("COMMENT", commentId, "DELETE", userId,
                "Comment deleted from task " + taskId);
    }
}
