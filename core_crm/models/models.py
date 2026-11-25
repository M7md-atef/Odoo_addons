from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class CrmTag(models.Model):
    _name = "core.crm.tag"
    _description = "CRM Lead Tag"
    _order = "name"

    name = fields.Char(
        string="Tag Name",
        required=True,
    )
    color = fields.Char(
        string="Color",
        default="#FC5130",
        help="Choose a tag color.",
    )
    _sql_constraints = [
        ("name_unique", "unique(name)", "Tag names must be unique."),
    ]


class CrmLeadStage(models.Model):
    _name = "core.crm.stage"
    _description = "CRM Lead Stage"
    _order = "sequence, id"

    name = fields.Char(
        string="Stage Name",
        required=True,
    )
    sequence = fields.Integer(
        default=10,
        index=True,
    )
    fold = fields.Boolean(
        string="Folded in Pipeline",
        default=False,
    )
    is_lost = fields.Boolean(
        string="Lost Stage",
        default=False,
        help="Leads in this stage need a lost reason.",
    )

    def unlink(self):
        if self.env["core.crm.lead"].search_count([("stage_id", "in", self.ids)]):
            raise UserError("Move all leads out of a stage before deleting it.")
        return super().unlink()


class CrmLeadLostReason(models.Model):
    _name = "core.crm.lost.reason"
    _description = "CRM Lead Lost Reason"
    _order = "sequence, name"

    name = fields.Char(
        string="Reason",
        required=True,
    )
    sequence = fields.Integer(
        default=10,
        index=True,
    )


class CrmLead(models.Model):
    # Odoo uses this model name to identify lead records throughout the addon.
    _name = "core.crm.lead"
    _description = "CRM Lead"
    _rec_name = "title"
    _order = "create_date desc"

    # A short title helps users recognize a lead in the list.
    title = fields.Char(
        string="Lead Title",
        required=True,
        index=True,
        help="A short summary that identifies this lead.",
    )
    name = fields.Char(
        string="Name",
        help="The name of the person you are contacting.",
    )
    nickname = fields.Selection(
        [
            ("mr", "Mr."),
            ("mrs", "Mrs."),
            ("ms", "Ms."),
            ("dr", "Dr."),
            ("eng", "Eng"),
            ("acc", "Acc"),
            ("prof", "Prof."),
            ("master", "Master"),
            ("madam", "Madam"),
            ("miss", "Miss"),
            ("rev", "Rev."),
            ("mx", "Mx."),
        ],
        string="Nickname",
        default="mr",
        help="Choose a nickname or title from the list.",
    )
    job = fields.Char(
        string="Job Title",
        help="The contact's role or position.",
    )
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
            ("prefer_not_to_say", "Prefer not to say"),
        ],
        string="Gender",
        default="male",
        help="The contact's gender, if they choose to provide it.",
    )
    lead_owner = fields.Many2one(
        "res.users",
        string="Lead Owner",
        default=lambda self: self.env.user,
        help="Defaults to the user who creates this lead.",
    )
    priority = fields.Selection(
        [
            ("0", "No Rating"),
            ("1", "1 Star"),
            ("2", "2 Stars"),
            ("3", "3 Stars"),
            ("4", "4 Stars"),
            ("5", "5 Stars"),
        ],
        string="Priority",
        default="1",
        help="Rate the lead from one to five stars.",
    )
    tag_ids = fields.Many2many(
        "core.crm.tag",
        "core_crm_lead_tag_rel",
        "lead_id",
        "tag_id",
        string="Tags",
        help="Add customizable tags to organize this lead.",
    )
    revenue = fields.Monetary(
        string="Revenue",
        currency_field="currency_id",
        help="Expected revenue for this lead.",
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env["res.currency"].search(
            [("name", "=", "EGP")],
            limit=1,
        ),
        domain=[("name", "=", "EGP")],
        required=True,
    )
    marital_status = fields.Selection(
        [
            ("single", "Single"),
            ("married", "Married"),
            ("divorced", "Divorced"),
            ("widowed", "Widowed"),
        ],
        string="Marital Status",
        help="The contact's marital status.",
    )

    phone = fields.Char(
        string="Phone",
        help="The contact's main phone number.",
    )
    stage_id = fields.Many2one(
        "core.crm.stage",
        string="Stage",
        default=lambda self: self.env.ref(
            "core_crm.core_crm_stage_new",
            raise_if_not_found=False,
        ),
        group_expand="_read_group_stage_ids",
        ondelete="restrict",
        index=True,
        help="The lead's current pipeline stage.",
    )
    lost_reason_id = fields.Many2one(
        "core.crm.lost.reason",
        string="Lost Reason",
        ondelete="restrict",
        index=True,
        help="Required when the lead is in the Lost stage.",
    )
    email = fields.Char(
        string="Email",
        help="The contact's email address.",
    )
    # This editable alias uses the existing email column, so stored email values remain intact.
    email_id = fields.Char(
        string="Email",
        related="email",
        readonly=False,
        help="The contact's email address.",
    )
    website = fields.Char(
        string="Website",
        help="The contact's or company's website.",
    )
    phone_country_id = fields.Many2one(
        "res.country",
        string="Phone Country",
        default=lambda self: self.env["res.country"].search(
            [("code", "=", "EG")],
            limit=1,
        ),
        help="Choose the country whose dialing code applies to this phone number.",
    )
    phone_country_code = fields.Char(
        string="Country Code",
        compute="_compute_phone_country_code",
        help="The dialing code for the selected phone country.",
    )
    whatsapp_no = fields.Char(
        string="WhatsApp",
        help="The contact's WhatsApp number.",
    )
    phone_ext = fields.Char(
        string="Phone Ext.",
        help="The extension for the main phone number, if any.",
    )

    city = fields.Char(
        string="City",
        help="The contact's city.",
    )
    street_no = fields.Char(
        string="Street No.",
        help="The street number for the contact's address.",
    )
    district = fields.Char(
        string="District",
        help="The district or neighborhood for the contact's address.",
    )
    building_no = fields.Char(
        string="Building No.",
        help="The building number for the contact's address.",
    )
    state_id = fields.Many2one(
        "res.country.state",
        string="State/Province",
        help="Choose the state or province within the selected country.",
    )
    country = fields.Many2one(
        "res.country",
        string="Country",
        default=lambda self: self.env["res.country"].search(
            [("code", "=", "EG")],
            limit=1,
        ),
        help="The contact's country.",
    )
    country_flag = fields.Char(
        string="Country Flag",
        related="country.image_url",
        help="Displays the selected country's flag.",
    )

    language = fields.Many2one(
        "res.lang",
        string="Print Language",
        domain=[("active", "=", True)],
        default=lambda self: self.env["res.lang"].search(
            [("code", "=", self.env.user.lang), ("active", "=", True)],
            limit=1,
        ),
        help="Choose an active Odoo language. Enable more languages in Settings to add choices.",
    )
    disabled = fields.Boolean(
        string="Disabled",
        default=False,
        help="Mark this lead as disabled.",
    )
    unsubscribed = fields.Boolean(
        string="Unsubscribed",
        default=False,
        help="Mark that this contact has unsubscribed from communications.",
    )
    blog_subscriber = fields.Boolean(
        string="Blog Subscriber",
        default=False,
        help="Enable if this contact subscribes to the blog.",
    )
    date_of_birth = fields.Date(
        string="Date of Birth",
        help="The contact's date of birth.",
    )
    age = fields.Integer(
        string="Age",
        compute="_compute_age",
        help="Calculated from the date of birth.",
    )
    description = fields.Text(
        string="Notes",
        help="Additional details about this lead.",
    )

    def init(self):
        egp = self.env["res.currency"].with_context(active_test=False).search(
            [("name", "=", "EGP")],
            limit=1,
        )
        if egp:
            if not egp.active:
                egp.active = True
            self.env.cr.execute(
                """
                UPDATE core_crm_lead
                SET currency_id = %s
                WHERE currency_id IS NULL
                """,
                (egp.id,),
            )

    @api.model_create_multi
    def create(self, vals_list):
        egp = self.env["res.currency"].with_context(active_test=False).search(
            [("name", "=", "EGP")],
            limit=1,
        )
        lost_stage_ids = set(
            self.env["core.crm.stage"].search([("is_lost", "=", True)]).ids
        )
        default_stage_id = self.default_get(["stage_id"]).get("stage_id")
        for vals in vals_list:
            if not vals.get("currency_id") and egp:
                vals["currency_id"] = egp.id
            stage_id = vals.get("stage_id", default_stage_id)
            if stage_id in lost_stage_ids and not vals.get("lost_reason_id"):
                raise ValidationError(
                    "Select a lost reason before creating a lead in a Lost stage."
                )
        return super().create(vals_list)

    def write(self, vals):
        if "stage_id" not in vals:
            return super().write(vals)

        target_stage = (
            self.env["core.crm.stage"].browse(vals["stage_id"])
            if vals["stage_id"]
            else self.env["core.crm.stage"]
        )
        if target_stage and target_stage.is_lost:
            return super().write(vals)

        leaving_lost = self.filtered(lambda lead: lead.stage_id.is_lost)
        if not leaving_lost:
            return super().write(vals)

        remaining = self - leaving_lost
        result = super(CrmLead, leaving_lost).write(
            {**vals, "lost_reason_id": False}
        )
        if remaining:
            result = super(CrmLead, remaining).write(vals)
        return result

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        return self.env["core.crm.stage"].search([], order="sequence, id")

    @api.depends("date_of_birth")
    def _compute_age(self):
        today = fields.Date.today()
        for lead in self:
            if not lead.date_of_birth:
                lead.age = False
                continue
            birth_date = lead.date_of_birth
            lead.age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day)
            )

    @api.constrains("date_of_birth")
    def _check_date_of_birth(self):
        today = fields.Date.today()
        if any(lead.date_of_birth and lead.date_of_birth > today for lead in self):
            raise ValidationError("Date of Birth cannot be in the future.")

    @api.constrains("stage_id", "lost_reason_id")
    def _check_lost_reason(self):
        for lead in self:
            if lead.stage_id.is_lost and not lead.lost_reason_id:
                raise ValidationError(
                    "Select a lost reason before moving a lead to a Lost stage."
                )

    @api.depends("phone_country_id.phone_code")
    def _compute_phone_country_code(self):
        for lead in self:
            phone_code = lead.phone_country_id.phone_code
            lead.phone_country_code = f"+{phone_code}" if phone_code else False


class CrmLeadLostWizard(models.TransientModel):
    _name = "core.crm.lead.lost"
    _description = "Select a Lost Reason"

    lead_ids = fields.Many2many(
        "core.crm.lead",
        string="Leads",
        required=True,
    )
    stage_id = fields.Many2one(
        "core.crm.stage",
        string="Lost Stage",
        required=True,
        readonly=True,
        ondelete="restrict",
    )
    lost_reason_id = fields.Many2one(
        "core.crm.lost.reason",
        string="Lost Reason",
        required=True,
    )

    def action_mark_lost(self):
        self.ensure_one()
        if not self.stage_id.is_lost:
            raise ValidationError("Choose a stage marked as Lost.")
        self.lead_ids.write(
            {
                "stage_id": self.stage_id.id,
                "lost_reason_id": self.lost_reason_id.id,
            }
        )
        return {"type": "ir.actions.act_window_close"}

