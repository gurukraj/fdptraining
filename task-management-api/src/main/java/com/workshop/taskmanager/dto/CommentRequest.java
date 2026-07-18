package com.workshop.taskmanager.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public class CommentRequest {

    @NotBlank(message = "Comment text is required")
    @Size(min = 1, max = 1000, message = "Comment must be between 1 and 1000 characters")
    private String text;

    // Constructors
    public CommentRequest() {}

    public CommentRequest(String text) {
        this.text = text;
    }

    // Getters and Setters
    public String getText() { return text; }
    public void setText(String text) { this.text = text; }
}
