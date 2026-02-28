from backend.models.audit_log import AuditLog


def log_event(db, contract_id, action, status, message):
    log = AuditLog(
        contract_id=contract_id,
        action=action,
        status=status,
        message=message
    )
    db.add(log)
    db.commit()