package com.workshop.taskmanager.service;

import com.workshop.taskmanager.entity.AuditLog;
import com.workshop.taskmanager.repository.AuditLogRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
public class AuditLogService {

    private final AuditLogRepository auditLogRepository;

    public AuditLogService(AuditLogRepository auditLogRepository) {
        this.auditLogRepository = auditLogRepository;
    }

    public void log(String entityType, Long entityId, String action, String performedBy, String details) {
        AuditLog auditLog = new AuditLog(entityType, entityId, action, performedBy, details);
        auditLogRepository.save(auditLog);
    }

    public Page<AuditLog> getAuditLogs(String entityType, Pageable pageable) {
        if (entityType != null && !entityType.isBlank()) {
            return auditLogRepository.findByEntityType(entityType, pageable);
        }
        return auditLogRepository.findAll(pageable);
    }
}
