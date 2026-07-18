package com.workshop.taskmanager.exception;

import com.workshop.taskmanager.entity.TaskStatus;

public class InvalidStatusTransitionException extends RuntimeException {

    public InvalidStatusTransitionException(TaskStatus from, TaskStatus to) {
        super("Invalid status transition from " + from + " to " + to);
    }

    public InvalidStatusTransitionException(String message) {
        super(message);
    }
}
