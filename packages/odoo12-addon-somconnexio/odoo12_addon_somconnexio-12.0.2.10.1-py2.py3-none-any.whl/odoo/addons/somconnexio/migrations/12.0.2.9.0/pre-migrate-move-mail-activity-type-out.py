from openupgradelib import openupgrade


_xml_ids_renames = [
    (
        "somconnexio.mail_activity_type_marginalized_colletive",
        "marginalized_groups_somconnexio.mail_activity_type_marginalized_groups",
    ),
    (
        "somconnexio.marginalized_group_categ",
        "marginalized_groups_somconnexio.marginalized_group_categ",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, _xml_ids_renames)
