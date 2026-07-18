package com.workshop.taskmanager.repository;

import com.workshop.taskmanager.entity.Comment;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CommentRepository extends JpaRepository<Comment, Long> {

    Page<Comment> findByTaskIdAndDeletedFalse(Long taskId, Pageable pageable);

    @Modifying
    @Query("UPDATE Comment c SET c.deleted = true WHERE c.task.id = :taskId")
    void softDeleteByTaskId(@Param("taskId") Long taskId);

    List<Comment> findByTaskIdAndDeletedFalse(Long taskId);
}
