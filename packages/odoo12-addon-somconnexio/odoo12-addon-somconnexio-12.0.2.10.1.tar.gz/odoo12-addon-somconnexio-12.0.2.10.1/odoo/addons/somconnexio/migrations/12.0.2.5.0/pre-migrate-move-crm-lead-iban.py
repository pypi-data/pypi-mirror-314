import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    # Add temporary iban column
    cr.execute("ALTER TABLE crm_lead ADD temporary_iban varchar(50)")
    _logger.info("New column temporary_iban created in table CRMLead.")

    # Copy crm_lead.iban to crm_lead.temporary_iban
    cr.execute("SELECT id,iban from crm_lead")
    crm_leads = cr.fetchall()
    for lead in crm_leads:
        lead_id = lead[0]
        iban = lead[1] or False
        cr.execute(
            ("UPDATE crm_lead SET temporary_iban='{}' WHERE id={}").format(
                iban, lead_id
            )
        )
    _logger.info("crm_lead.iban copied to crm_lead.temporary_iban")
