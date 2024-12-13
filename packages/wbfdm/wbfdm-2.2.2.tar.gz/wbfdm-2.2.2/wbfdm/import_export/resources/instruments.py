import magic
from django.apps import apps
from django.db.models import Q
from import_export import fields
from import_export.formats.base_formats import CSV
from import_export.results import RowResult
from import_export.signals import post_import
from import_export.widgets import CharWidget, ForeignKeyWidget, ManyToManyWidget
from rest_framework.reverse import reverse
from wbcore.contrib.currency.models import Currency
from wbcore.contrib.geography.import_export.resources.geography import (
    CountryForeignKeyWidget,
)
from wbcore.contrib.io.resources import FilterModelResource
from wbcore.contrib.notifications.dispatch import send_notification
from wbfdm.models import Exchange, Instrument, InstrumentClassificationThroughModel

from .classification import ClassificationManyToManyWidget


class TypeWidget(CharWidget):
    def clean(self, value, row=None, **kwargs):
        return super().clean(value.lower().name(), row=row, **kwargs)


class InstrumentResource(FilterModelResource):
    """
    The resource to download AssetPositions
    """

    instrument_type = fields.Field(column_name="instrument_type", attribute="instrument_type", widget=TypeWidget())

    country = fields.Field(
        column_name="country",
        attribute="country",
        widget=CountryForeignKeyWidget(),
    )

    exchanges = fields.Field(
        column_name="exchanges",
        attribute="exchanges",
        m2m_add=True,
        widget=ManyToManyWidget(Exchange, field="mic_code"),
    )

    currency = fields.Field(
        column_name="currency",
        attribute="currency",
        widget=ForeignKeyWidget(Currency, field="key__iexact"),
    )

    primary_classifications = fields.Field(
        column_name="primary_classifications",
        attribute="classifications",
        m2m_add=True,
        widget=ClassificationManyToManyWidget(primary_classification_group=True),
    )
    default_classifications = fields.Field(
        column_name="default_classifications",
        attribute="classifications",
        m2m_add=True,
        widget=ClassificationManyToManyWidget(primary_classification_group=False),
    )

    def save_m2m(self, obj, data, using_transactions, dry_run):
        """
        override save m2m to define what to to with the nested classification instrument through model values
        """
        if (not using_transactions and dry_run) or self._meta.use_bulk:
            # we don't have transactions and we want to do a dry_run
            # OR use_bulk is enabled (m2m operations are not supported for bulk operations)
            pass
        else:
            for field in self.get_import_fields():
                if isinstance(field.widget, ClassificationManyToManyWidget):
                    defaults = {
                        "is_favorite": str(data.get(f"{field.column_name}__is_favorite", "")).lower()
                        in ["1", "true", "yes"],
                        "reason": data.get(f"{field.column_name}__reason", None),
                        "pure_player": data.get(f"{field.column_name}__pure_player", None),
                        "top_player": data.get(f"{field.column_name}__top_player", None),
                        "percent_of_revenue": data.get(f"{field.column_name}__percent_of_revenue", None),
                    }
                    defaults = {k: v for k, v in defaults.items() if v is not None}
                    for classification in field.clean(data):
                        InstrumentClassificationThroughModel.objects.update_or_create(
                            instrument=obj, classification=classification, defaults=defaults
                        )
                elif isinstance(field.widget, ManyToManyWidget):
                    self.import_field(field, obj, data, True)

    def get_instance(self, instance_loader, row):
        try:
            return Instrument.objects.get(
                Q(isin=row["isin"]) | Q(refinitiv_identifier_code=row["refinitiv_identifier_code"])
            )
        except Instrument.DoesNotExist:
            return None

    class Meta:
        import_id_fields = ("isin",)
        fields = (
            "id",
            "founded_year",
            "inception_date",
            "delisted_date",
            "identifier",
            "name",
            "name_repr",
            "description",
            "isin",
            "ticker",
            "refinitiv_ticker",
            "refinitiv_identifier_code",
            "refinitiv_mnemonic_code",
            "sedol",
            "valoren",
            "headquarter_address",
            "primary_url",
            "is_cash",
            "instrument_type",
            "country",
            "exchanges",
            "currency",
            "primary_classifications",
            "default_classifications",
        )
        export_order = fields
        model = Instrument


# This parser satisfy the import source framework interface. The generic logic will probably need to move the io module to avoid repetition
def parse(import_source):
    input_format = CSV(encoding="utf-8-sig")

    file_stream = import_source.file.read()
    if input_format.CONTENT_TYPE == magic.from_buffer(file_stream, mime=True):
        dataset = input_format.create_dataset(file_stream)

        model = apps.get_model(import_source.parser_handler.handler)
        result = InstrumentResource().import_data(
            dataset,
            dry_run=False,
            file_name=import_source.file.name,
            user=import_source.creator,
            rollback_on_validation_errors=True,
        )
        import_source.file.close()
        post_import.send(sender=None, model=model)
        success_message = """
        {} import finished:
        * new {}
        * updated {}
        * skipped {}
        * failed {}
        * deleted {}
        * invalid {}
        """.format(
            model._meta.verbose_name_plural,
            result.totals[RowResult.IMPORT_TYPE_NEW],
            result.totals[RowResult.IMPORT_TYPE_UPDATE],
            result.totals[RowResult.IMPORT_TYPE_SKIP],
            result.totals[RowResult.IMPORT_TYPE_ERROR],
            result.totals[RowResult.IMPORT_TYPE_DELETE],
            result.totals[RowResult.IMPORT_TYPE_INVALID],
        )
        import_source.log = success_message
        import_source.save()
        if import_source.creator:
            send_notification(
                code="io.import_done",
                name="Your import is done",
                body=success_message,
                user=import_source.creator,
                endpoint=reverse(f"{model.get_base_endpoint()}-list") if hasattr(model, "get_base_endpoint") else None,
            )
