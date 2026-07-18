package com.workshop.taskmanager.repository;

import com.workshop.taskmanager.entity.Task;
import com.workshop.taskmanager.entity.TaskPriority;
import com.workshop.taskmanager.entity.TaskStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {

    @Query("SELECT t FROM Task t WHERE t.deleted = false " +
           "AND (:status IS NULL OR t.status = :status) " +
           "AND (:priority IS NULL OR t.priority = :priority) " +
           "AND (:categoryId IS NULL OR t.category.id = :categoryId)")
    Page<Task> findAllWithFilters(
            @Param("status") TaskStatus status,
            @Param("priority") TaskPriority priority,
            @Param("categoryId") Long categoryId,
            Pageable pageable);

    Optional<Task> findByIdAndDeletedFalse(Long id);

    boolean existsByCategoryIdAndDeletedFalse(Long categoryId);
}
