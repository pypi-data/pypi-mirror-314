from openupgradelib import openupgrade
import logging

_logger = logging.getLogger(__name__)

_xml_ids_renames = [
    (
        "somconnexio.SwitchBoard",
        "switchboard_somconnexio.Switchboard",
    ),
    (
        "somconnexio.SwitchBoardApplication",
        "switchboard_somconnexio.SwitchboardApplication",
    ),
    (
        "somconnexio.SwitchBoardDesktop",
        "switchboard_somconnexio.SwitchboardDesktop",
    ),
    (
        "somconnexio.switchboard_category",
        "switchboard_somconnexio.switchboard_category",
    ),
    (
        "somconnexio.switchboard_enreach_contact_relation",
        "switchboard_somconnexio.switchboard_enreach_contact_relation",
    ),
    (
        "somconnexio.AgentCentraletaVirtualApp500",
        "switchboard_somconnexio.AgentCentraletaVirtualApp500",
    ),
    (
        "somconnexio.AgentCentraletaVirtualDesktop500",
        "switchboard_somconnexio.AgentCentraletaVirtualDesktop500",
    ),
    (
        "somconnexio.AgentCentraletaVirtualAppUNL",
        "switchboard_somconnexio.AgentCentraletaVirtualAppUNL",
    ),
    (
        "somconnexio.AgentCentraletaVirtualDesktopUNL",
        "switchboard_somconnexio.AgentCentraletaVirtualDesktopUNL",
    ),
    (
        "somconnexio.AgentCentraletaVirtual_product_template_min_attribute_line",
        "switchboard_somconnexio.AgentCentraletaVirtual_product_template_min_attribute_line",  # noqa
    ),
    (
        "somconnexio.AgentCentraletaVirtual_product_template_company_attribute_line",
        "switchboard_somconnexio.AgentCentraletaVirtual_product_template_company_attribute_line",  # noqa
    ),
    (
        "somconnexio.AgentCentraletaVirtual_product_template_switchboard_attribute_line",  # noqa
        "switchboard_somconnexio.AgentCentraletaVirtual_product_template_switchboard_attribute_line",  # noqa
    ),
    (
        "somconnexio.AgentCentraletaVirtualApp500_product_template",
        "switchboard_somconnexio.AgentCentraletaVirtualApp500_product_template",
    ),
    (
        "somconnexio.service_supplier_enreach",
        "switchboard_somconnexio.service_supplier_enreach",
    ),
    (
        "somconnexio.service_technology_switchboard",
        "switchboard_somconnexio.service_technology_switchboard",
    ),
    (
        "somconnexio.service_switchboard_technology_service_supplier_enreach",
        "switchboard_somconnexio.service_switchboard_technology_service_supplier_enreach",  # noqa
    ),
    (
        "somconnexio.service_supplier_enreach",
        "switchboard_somconnexio.service_supplier_enreach",
    ),
    (
        "somconnexio.AgentCentraletaVirtualApp500",
        "switchboard_somconnexio.AgentCentraletaVirtualApp500",
    ),
    (
        "somconnexio.AgentCentraletaVirtualDesktop500",
        "switchboard_somconnexio.AgentCentraletaVirtualDesktop500",
    ),
    (
        "somconnexio.AgentCentraletaVirtualAppUNL",
        "switchboard_somconnexio.AgentCentraletaVirtualAppUNL",
    ),
    (
        "somconnexio.CentraletaVirtualBasic",
        "switchboard_somconnexio.CentraletaVirtualBasic",
    ),
    (
        "somconnexio.CentraletaVirtualUNL10GB",
        "switchboard_somconnexio.CentraletaVirtualUNL10GB",
    ),
    (
        "somconnexio.CentraletaVirtualUNL20GB",
        "switchboard_somconnexio.CentraletaVirtualUNL20GB",
    ),
    (
        "somconnexio.CentraletaVirtualUNLUNL",
        "switchboard_somconnexio.CentraletaVirtualUNLUNL",
    ),
    (
        "somconnexio.contract_info_contract_switchboard",
        "switchboard_somconnexio.contract_info_contract_switchboard",
    ),
    (
        "somconnexio.contract_switchboard_app_500",
        "switchboard_somconnexio.contract_switchboard_app_500",
    ),
    (
        "somconnexio.contract_line_switchboard_app_500",
        "switchboard_somconnexio.contract_line_switchboard_app_500",
    ),
    (
        "somconnexio.model_switchboard_service_contract_info",
        "switchboard_somconnexio.model_switchboard_service_contract_info",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, _xml_ids_renames)

    _logger.info("Renamed XML IDs")
