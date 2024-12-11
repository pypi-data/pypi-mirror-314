def migrate(cr, version):
    cr.execute(
        "UPDATE ir_model_data SET name="
        "'mail_activity_type_ubication_change_orange_wo_fix', "
        "module='somconnexio' "
        "WHERE name = 'mail_activity_type_75_2178b040';"
    )
