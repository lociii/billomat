# -*- coding: UTF-8 -*-
from . import base
from . import fields


class Article(base.Model):
    id = fields.IntegerField(read_only=True)
    created = fields.DateTimeField(read_only=True)
    article_number = fields.StringField(read_only=True)
    number = fields.IntegerField()
    number_pre = fields.StringField()
    title = fields.StringField()
    description = fields.StringField()
    sales_price = fields.FloatField()
    sales_price2 = fields.FloatField()
    sales_price3 = fields.FloatField()
    sales_price4 = fields.FloatField()
    sales_price5 = fields.FloatField()
    currency_code = fields.StringField()
    unit_id = fields.IntegerField()
    tax_id = fields.IntegerField()

    class Meta:
        resource = 'articles'
        object_name = 'article'
        filters = (
            'id',
            'since',
            'article_number',
            'title',
            'description',
            'currency_code',
            'unit_id',
            'tags',
        )


class ArticleProperty(base.Model):
    id = fields.IntegerField(read_only=True)
    account_id = fields.IntegerField(read_only=True)
    name = fields.StringField()
    type = fields.StringField(
        choices=(
            'TEXTFIELD', 'TEXTAREA', 'CHECKBOX',
        ),
    )
    default_value = fields.StringField()
    is_nvl = fields.BooleanField()

    class Meta:
        resource = 'article-properties'
        object_name = 'article-property'
        filters = (
            'id',
            'since',
            'article_id',
        )


class ArticlePropertyValue(base.Model):
    id = fields.IntegerField(read_only=True)
    article_id = fields.IntegerField()
    article_property_id = fields.IntegerField()
    type = fields.StringField(read_only=True)
    name = fields.StringField(read_only=True)
    value = fields.StringField()

    class Meta:
        resource = 'article-property-values'
        object_name = 'article-property-value'
        filters = (
            'id',
            'since',
            'article_id',
        )


class Client(base.Model):
    id = fields.IntegerField(read_only=True)
    created = fields.DateTimeField(read_only=True)
    archived = fields.BooleanField(default=0)
    client_number = fields.StringField(read_only=True)
    number = fields.IntegerField()
    number_pre = fields.StringField()
    name = fields.StringField()
    salutation = fields.StringField()
    first_name = fields.StringField()
    last_name = fields.StringField()
    street = fields.StringField()
    zip = fields.StringField()
    city = fields.StringField()
    state = fields.StringField()
    country_code = fields.StringField()
    phone = fields.StringField()
    fax = fields.StringField()
    mobile = fields.StringField()
    email = fields.EmailField()
    www = fields.URLField()
    tax_number = fields.StringField()
    vat_number = fields.StringField()
    bank_account_owner = fields.StringField()
    bank_number = fields.StringField()
    bank_name = fields.StringField()
    bank_account_number = fields.StringField()
    bank_swift = fields.StringField()
    bank_iban = fields.StringField()
    tax_rule = fields.StringField(
        choices=(
            'TAX', 'NO_TAX', 'COUNTRY',
        ),
        default='COUNTRY',
    )
    net_gross = fields.StringField(
        choices=(
            'NET', 'GROSS', 'SETTINGS',
        ),
        default='SETTINGS',
    )
    discount_rate_type = fields.StringField(
        choices=(
            'SETTINGS', 'ABSOLUTE', 'RELATIVE',
        ),
        default='SETTINGS',
    )
    discount_rate = fields.FloatField()
    discount_days_type = fields.StringField(
        choices=(
            'SETTINGS', 'ABSOLUTE', 'RELATIVE',
        ),
        default='SETTINGS',
    )
    discount_days = fields.FloatField()
    due_days_type = fields.StringField(
        choices=(
            'SETTINGS', 'ABSOLUTE', 'RELATIVE',
        ),
        default='SETTINGS',
    )
    due_days = fields.IntegerField()
    reminder_due_days_type = fields.StringField(
        choices=(
            'SETTINGS', 'ABSOLUTE', 'RELATIVE',
        ),
        default='SETTINGS',
    )
    reminder_due_days = fields.IntegerField()
    offer_validity_days_type = fields.StringField(
        choices=(
            'SETTINGS', 'ABSOLUTE', 'RELATIVE',
        ),
        default='SETTINGS',
    )
    offer_validity_days = fields.IntegerField()
    price_group = fields.IntegerField()
    note = fields.StringField()
    revenue_gross = fields.FloatField(read_only=True)
    revenue_net = fields.FloatField(read_only=True)

    class Meta:
        resource = 'clients'
        object_name = 'client'
        filters = (
            'id',
            'since',
            'name',
            'client_number',
            'email',
            'first_name',
            'last_name',
            'country_code',
            'note',
            'invoice_id',
            'tags',
        )


class Recurring(base.Model):
    id = fields.IntegerField(read_only=True)
    created = fields.DateTimeField(read_only=True)
    client_id = fields.IntegerField()
    contact_id = fields.IntegerField()
    template_id = fields.IntegerField()
    currency_code = fields.StringField()
    name = fields.StringField()
    cycle_number = fields.IntegerField()
    cycle = fields.StringField(
        choices=(
            'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY',
        )
    )
    action = fields.StringField(
        choices=(
            'CREATE', 'COMPLETE', 'EMAIL',
        )
    )
    hour = fields.IntegerField()
    start_date = fields.DateField()
    end_date = fields.DateField()
    last_creation_date = fields.DateField(read_only=True)
    next_creation_date = fields.DateField()
    iterations = fields.IntegerField(read_only=True)
    counter = fields.IntegerField(read_only=True)
    address = fields.StringField()
    due_days = fields.IntegerField()
    discount_rate = fields.FloatField()
    discount_days = fields.IntegerField()
    intro = fields.StringField()
    note = fields.StringField()
    total_gross = fields.FloatField()
    total_net = fields.FloatField()
    net_gross = fields.StringField(
        choices=(
            'NET', 'GROSS',
        )
    )
    reduction = fields.StringField()
    total_gross_unreduced = fields.FloatField()
    total_net_unreduced = fields.FloatField()
    quote = fields.FloatField()
    ultimo = fields.IntegerField()
    label = fields.StringField()
    supply_date_type = fields.StringField(
        choices=(
            'SUPPLY_DATE', 'DELIVERY_DATE', 'SUPPLY_TEXT', 'DELIVERY_TEXT',
        )
    )
    supply_date = fields.StringField()
    email_sender = fields.StringField()
    email_subject = fields.StringField()
    email_message = fields.StringField()
    email_filename = fields.StringField()
    payment_types = fields.ListOfFloatField()
    offer_id = fields.IntegerField()
    confirmation_id = fields.IntegerField()

    class Meta:
        resource = 'recurrings'
        object_name = 'recurring'
        filters = (
            'id',
            'since',
            'client_id',
            'contact_id',
            'name',
            'payment_type',
            'cycle',
            'label',
            'intro',
            'note',
            'tags',
        )


class RecurringItem(base.Model):
    id = fields.IntegerField(read_only=True)
    article_id = fields.IntegerField()
    recurring_id = fields.IntegerField()
    position = fields.IntegerField(read_only=True)
    unit = fields.StringField()
    quantity = fields.FloatField()
    unit_price = fields.FloatField()
    tax_name = fields.StringField()
    tax_rate = fields.FloatField()
    title = fields.StringField()
    description = fields.StringField()
    total_gross = fields.FloatField()
    total_net = fields.FloatField()
    reduction = fields.IntegerField()
    total_gross_unreduced = fields.FloatField()
    total_net_unreduced = fields.FloatField()

    class Meta:
        resource = 'recurring-items'
        object_name = 'recurring-item'
        filters = (
            'id',
            'since',
            'recurring_id',
        )


class Invoice(base.Model):
    id = fields.IntegerField(read_only=True)
    client_id = fields.IntegerField()
    contact_id = fields.IntegerField()
    created = fields.DateTimeField(read_only=True)
    invoice_number = fields.StringField(read_only=True)
    number = fields.IntegerField()
    number_pre = fields.StringField()
    status = fields.StringField(
        choices=(
            'DRAFT', 'OPEN', 'OVERDUE', 'PAID', 'CANCELED',
        )
    )
    date = fields.DateField()
    supply_date = fields.StringField()
    supply_date_type = fields.StringField(
        choices=(
            'SUPPLY_DATE', 'DELIVERY_DATE', 'SUPPLY_TEXT', 'DELIVERY_TEXT',
        )
    )
    due_date = fields.DateField()
    due_days = fields.IntegerField()
    address = fields.StringField()
    discount_rate = fields.FloatField()
    discount_date = fields.DateField()
    discount_days = fields.IntegerField()
    discount_amount = fields.FloatField()
    title = fields.StringField()
    label = fields.StringField()
    intro = fields.StringField()
    note = fields.StringField()
    total_gross = fields.FloatField()
    total_net = fields.FloatField()
    net_gross = fields.StringField(
        choices=(
            'NET', 'GROSS',
        )
    )
    reduction = fields.StringField()
    total_gross_unreduced = fields.FloatField()
    total_net_unreduced = fields.FloatField()
    paid_amount = fields.FloatField()
    open_amount = fields.FloatField()
    currency_code = fields.StringField()
    quote = fields.FloatField()
    invoice_id = fields.IntegerField()
    offer_id = fields.IntegerField()
    confirmation_id = fields.IntegerField()
    recurring_id = fields.IntegerField()
    payment_types = fields.ListOfFloatField()

    class Meta:
        resource = 'invoices'
        object_name = 'invoice'
        filters = (
            'id',
            'since',
            'client_id',
            'contact_id',
            'invoice_number',
            'status',
            'payment_type',
            'from',
            'to',
            'label',
            'intro',
            'note',
            'tags',
        )


class InvoiceItem(base.Model):
    id = fields.IntegerField(read_only=True)
    article_id = fields.IntegerField()
    invoice_id = fields.IntegerField()
    position = fields.IntegerField(read_only=True)
    unit = fields.StringField()
    quantity = fields.FloatField()
    unit_price = fields.FloatField()
    tax_name = fields.StringField()
    tax_rate = fields.FloatField()
    title = fields.StringField()
    description = fields.StringField()
    total_gross = fields.FloatField()
    total_net = fields.FloatField()
    reduction = fields.IntegerField()
    total_gross_unreduced = fields.FloatField()
    total_net_unreduced = fields.FloatField()

    class Meta:
        resource = 'invoice-items'
        object_name = 'invoice-item'
        filters = (
            'id',
            'since',
            'invoice_id',
        )


class InvoiceComment(base.Model):
    id = fields.IntegerField(read_only=True)
    created = fields.DateTimeField(read_only=True)
    invoice_id = fields.IntegerField()
    user_id = fields.IntegerField()
    comment = fields.StringField()
    actionkey = fields.StringField(
        choices=(
            'COMMENT', 'CREATE', 'COPY', 'CREATE_FROM_OFFER',
            'CREATE_FROM_RECURRING', 'STATUS', 'PAYMENT', 'PAYMENT_ERROR',
            'DELETE_PAYMENT', 'MAIL', 'LETTER', 'FAX', 'SIGN', 'SIGN_MAIL',
            'CANCEL', 'ERROR_MAIL', 'CREATE_CREDIT_NOTE', 'REMINDER_CREATE',
            'REMINDER_STATUS', 'REMINDER_MAIL', 'REMINDER_ERROR_MAIL',
            'REMINDER_LETTER', 'REMINDER_FAX', 'REMINDER_SIGN',
            'REMINDER_SIGN_MAIL', 'REMINDER_CANCEL', 'REMINDER_DELETE',
        )
    )

    class Meta:
        resource = 'invoice-comments'
        object_name = 'invoice-comment'
        filters = (
            'id',
            'since',
            'invoice_id',
        )


class InvoicePayment(base.Model):
    id = fields.IntegerField(read_only=True)
    created = fields.DateTimeField(read_only=True)
    invoice_id = fields.IntegerField()
    user_id = fields.IntegerField()
    date = fields.DateField()
    amount = fields.FloatField()
    comment = fields.StringField()
    type = fields.StringField(
        choices=(
            'CREDIT_NOTE', 'BANK_CARD', 'BANK_TRANSFER',
            'DEBIT', 'CASH', 'CHECK', 'PAYPAL', 'CREDIT_CARD',
            'COUPON', 'MISC',
        )
    )

    class Meta:
        resource = 'invoice-payments'
        object_name = 'invoice-payment'
        filters = (
            'id',
            'since',
            'invoice_id',
            'from',
            'to',
            'type',
            'user_id',
        )


class CreditNote(base.Model):
    id = fields.IntegerField(read_only=True)
    client_id = fields.IntegerField()
    contact_id = fields.IntegerField()
    created = fields.DateTimeField(read_only=True)
    credit_note_number = fields.StringField(
        read_only=True,
        field_name='credit',
    )
    number = fields.IntegerField()
    number_pre = fields.StringField()
    status = fields.StringField(
        choices=(
            'DRAFT', 'OPEN', 'PAID',
        )
    )
    date = fields.DateField()
    address = fields.StringField()
    title = fields.StringField()
    label = fields.StringField()
    intro = fields.StringField()
    note = fields.StringField()
    total_gross = fields.FloatField()
    total_net = fields.FloatField()
    net_gross = fields.StringField(
        choices=(
            'NET', 'GROSS',
        )
    )
    reduction = fields.StringField()
    total_gross_unreduced = fields.FloatField()
    total_net_unreduced = fields.FloatField()
    currency_code = fields.StringField()
    quote = fields.FloatField()
    invoice_id = fields.IntegerField()

    class Meta:
        resource = 'credit-notes'
        object_name = 'credit-note'
        filters = (
            'id',
            'since',
            'client_id',
            'contact_id',
            'credit_note_number',
            'status',
            'from',
            'to',
            'label',
            'intro',
            'note',
            'tags',
        )


class CreditNoteItem(base.Model):
    id = fields.IntegerField(read_only=True)
    article_id = fields.IntegerField()
    credit_note_id = fields.IntegerField()
    position = fields.IntegerField(read_only=True)
    unit = fields.StringField()
    quantity = fields.FloatField()
    unit_price = fields.FloatField()
    tax_name = fields.StringField()
    tax_rate = fields.FloatField()
    title = fields.StringField()
    description = fields.StringField()
    total_gross = fields.FloatField()
    total_net = fields.FloatField()
    reduction = fields.IntegerField()
    total_gross_unreduced = fields.FloatField()
    total_net_unreduced = fields.FloatField()

    class Meta:
        resource = 'credit-note-items'
        object_name = 'credit-note-item'
        filters = (
            'id',
            'since',
            'credit_note_id',
        )


class CreditNoteTag(base.Model):
    id = fields.IntegerField(read_only=True)
    credit_note_id = fields.IntegerField()
    name = fields.StringField()

    class Meta:
        resource = 'credit-note-tags'
        object_name = 'credit-note-tag'
        filters = (
            'id',
            'since',
            'credit_note_id',
        )


class Reminder(base.Model):
    id = fields.IntegerField(read_only=True)
    created = fields.DateTimeField(read_only=True)
    status = fields.StringField(
        choices=(
            'DRAFT', 'OPEN', 'OVERDUE', 'PAID', 'CANCELED',
        )
    )
    invoice_id = fields.IntegerField()
    contact_id = fields.IntegerField()
    reminder_text_id = fields.IntegerField()
    reminder_level = fields.IntegerField()
    reminder_level_name = fields.StringField(read_only=True)
    date = fields.DateField()
    label = fields.StringField()
    subject = fields.StringField()
    intro = fields.StringField()
    note = fields.StringField()
    due_date = fields.DateField()
    total_gross = fields.FloatField()
    is_old = fields.IntegerField(read_only=True)

    class Meta:
        resource = 'reminders'
        object_name = 'reminder'
        filters = (
            'id',
            'since',
            'client_id',
            'contact_id',
            'invoice_number',
            'status',
            'from',
            'to',
            'subject',
            'label',
            'intro',
            'note',
            'tags',
        )
