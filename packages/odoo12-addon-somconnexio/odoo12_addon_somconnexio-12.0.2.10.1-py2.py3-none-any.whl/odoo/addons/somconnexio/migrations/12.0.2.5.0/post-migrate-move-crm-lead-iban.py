import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    # Copy crm_lead.temporary_iban to crm_lead_line.iban
    cr.execute(
        "SELECT cll.id, cl.temporary_iban FROM crm_lead_line cll INNER JOIN crm_lead cl ON cll.lead_id = cl.id"  # noqa
    )
    crm_lead_lines = cr.fetchall()
    for crm_lead_line in crm_lead_lines:
        line_id = crm_lead_line[0]
        iban = crm_lead_line[1] or False
        cr.execute(
            ("UPDATE crm_lead_line SET iban='{}' WHERE id={}").format(iban, line_id)
        )
    _logger.info("crm_lead.temporary_iban copied to crm_lead_line.iban")

    # Drop temporary iban column
    cr.execute("ALTER TABLE crm_lead DROP COLUMN temporary_iban")
    _logger.info("Drop CRMLead column temporary_iban")
