import base64
import logging

from odoo import _, http
from odoo.addons.easy_my_coop_api.controllers.controllers import (
    UserController as BaseAPIKeyController,
)
from odoo.addons.mass_mailing.controllers import main
from odoo.addons.somconnexio.services import schemas
from odoo.addons.somconnexio.services.res_partner_service import ResPartnerService
from odoo.addons.web.controllers.main import content_disposition, serialize_exception
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.tools.pdf import merge_pdf
from pyopencell.client import Client
from pyopencell.exceptions import PyOpenCellAPIException

try:
    from cerberus import Validator
except ImportError:
    _logger = logging.getLogger(__name__)
    _logger.debug("Can not import cerberus")


class APIKeyController(BaseAPIKeyController):
    @http.route(
        BaseAPIKeyController._root_path + "partner/check_sponsor",
        auth='api_key',
        methods=['GET']
    )
    @serialize_exception
    def check_sponsor(self, vat, sponsor_code, **kw):
        data = ResPartnerService(request).check_sponsor(vat, sponsor_code)
        return request.make_json_response(data)

    @http.route(
        BaseAPIKeyController._root_path + "contract",
        auth='api_key',
        methods=['GET'],
    )
    def get_contract(self, **params):
        v = Validator()
        if not (
            v.validate(
                params,
                self.validator_search_contract(),
            )
            or v.validate(
                params,
                self.validator_search_multi_filter_contract(),
            )
        ):
            raise ValidationError(_('BadRequest {}').format(v.errors))
        response = request.env["contract.service"].search(**params)
        return request.make_json_response(response)

    @http.route(
        BaseAPIKeyController._root_path + "partner/sponsees",
        auth='api_key',
        methods=['GET'],
    )
    def get_partner_sponsorship_data(self, ref, **kw):
        data = ResPartnerService(request).get_sponship_data(ref)
        return request.make_json_response(data)

    @http.route(
        BaseAPIKeyController._root_path + "contract/available-fibers-to-link-with-mobile",  # noqa
        auth='api_key',
        methods=['GET'],
    )
    def run_contract_fiber_contracts_to_pack(self, **params):
        v = Validator()
        if not v.validate(params, self.validator_get_fiber_contracts_to_pack(),):
            raise ValidationError(_('BadRequest {}').format(v.errors))
        response = request.env["contract.service"].get_fiber_contracts_to_pack(**params)
        return request.make_json_response(response)

    @staticmethod
    def validator_search_contract():
        return schemas.S_CONTRACT_SEARCH

    @staticmethod
    def validator_search_multi_filter_contract():
        return schemas.S_CUSTOMER_CONTRACT_MULTI_FILTER_SEARCH

    @staticmethod
    def validator_get_fiber_contracts_to_pack():
        return schemas.S_CONTRACT_GET_FIBER_CONTRACTS_TO_PACK

    @http.route(
        BaseAPIKeyController._root_path + "contract/terminate",
        auth="api_key",
        methods=["POST"],
        csrf=False,
    )
    def run_terminate_contract(self, **params):
        v = Validator()
        if not v.validate(
            params,
            self.validator_terminate(),
        ):
            raise ValidationError(_("BadRequest {}").format(v.errors))
        response = request.env["contract.service"].terminate(**params)
        return request.make_json_response(response)

    @staticmethod
    def validator_terminate():
        return schemas.S_TERMINATE_CONTRACT

    @http.route(
        BaseAPIKeyController._root_path + "contract/terminate_reasons",
        auth="api_key",
        methods=["GET"],
        csrf=False,
    )
    def get_terminate_reasons(self):
        reasons = request.env["contract.service"].get_terminate_reasons()
        return request.make_json_response(reasons)


class UserController(http.Controller):
    @http.route(
        ['/web/binary/download_invoice'], auth='user',
        methods=['GET'], website=False
    )
    @serialize_exception
    def download_invoice(self, invoice_number, **kw):
        try:
            invoice_response = Client().get(
                "/invoice", invoiceNumber=invoice_number, includePdf=True
            )
        except PyOpenCellAPIException:
            return request.not_found()
        invoice_base64 = invoice_response["invoice"]["pdf"]
        filecontent = base64.b64decode(invoice_base64)
        if not filecontent:
            return request.not_found()
        else:
            filename = "{}.pdf".format(invoice_number)
            return request.make_response(filecontent, [
                ('Content-Type', 'application/octet-stream'),
                ('Content-Disposition', content_disposition(filename))
            ])

    @http.route(
        ["/web/binary/download_attachments"],
        auth="user",
        methods=["GET"],
        website=True,
    )
    @serialize_exception
    def download_attachments(self, attachment_ids, **kw):
        attachment_ids = [int(id) for id in attachment_ids.split(",")]
        attachments = request.env["ir.attachment"].sudo().browse(attachment_ids)
        attachments_datas = [
            base64.b64decode(a.datas, validate=True) for a in attachments
        ]
        merged_attachments = merge_pdf(attachments_datas)
        filename = "{}.pdf".format(_("delivery_labels"))
        return request.make_response(
            merged_attachments,
            [
                ("Content-Type", "application/octet-stream"),
                ("Content-Disposition", content_disposition(filename)),
            ],
        )


class MassMailingController(main.MassMailController):

    @http.route('/mail/mailing/unsubscribe', type='json', auth='none')
    def unsubscribe(self, mailing_id, opt_in_ids, opt_out_ids, email, res_id, token):
        partner = request.env['res.partner'].sudo().search([('email', '=', email)])
        if partner.exists():
            if not self._valid_unsubscribe_token(mailing_id, res_id, email, token):
                return 'unauthorized'
            partner.write({'only_indispensable_emails': True})
            return True
        return 'error'
