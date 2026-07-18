package com.workshop.taskmanager.dto;

import com.workshop.taskmanager.entity.Comment;

import java.time.LocalDateTime;

public class CommentResponse {

    private Long id;
    private Long taskId;
    private String text;
    private String author;
    private LocalDateTime createdAt;

    // Constructors
    public CommentResponse() {}

    public static CommentResponse fromEntity(Comment comment) {
        CommentResponse response = new CommentResponse();
        response.setId(comment.getId());
        response.setTaskId(comment.getTask().getId());
        response.setText(comment.getText());
        response.setAuthor(comment.getAuthor());
        response.setCreatedAt(comment.getCreatedAt());
        return response;
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getTaskId() { return taskId; }
    public void setTaskId(Long taskId) { this.taskId = taskId; }

    public String getText() { return text; }
    public void setText(String text) { this.text = text; }

    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
