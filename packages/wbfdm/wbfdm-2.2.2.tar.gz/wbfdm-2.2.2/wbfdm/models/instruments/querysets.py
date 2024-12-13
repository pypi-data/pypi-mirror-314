from django.db.models import (
    AutoField,
    Exists,
    ExpressionWrapper,
    F,
    OuterRef,
    QuerySet,
    Subquery,
)
from django.db.models.functions import Coalesce


class InstrumentQuerySet(QuerySet):
    def annotate_classification_for_group(
        self, classification_group, classification_height: int = 0, **kwargs
    ) -> QuerySet:
        return classification_group.annotate_queryset(
            self, classification_height, "", annotation_label="ancestor_classifications", **kwargs
        )

    def annotate_base_data(self):
        base_qs = InstrumentQuerySet(self.model, using=self._db)
        return self.annotate(
            is_investable=~Exists(base_qs.filter(parent=OuterRef("pk"))),
            root=Subquery(base_qs.filter(tree_id=OuterRef("tree_id"), level=0).values("id")[:1]),
            primary_security=ExpressionWrapper(
                Coalesce(
                    Subquery(
                        base_qs.filter(
                            parent=OuterRef("pk"),
                            is_primary=True,
                            is_security=True,
                        ).values(
                            "id"
                        )[:1]
                    ),
                    F("id"),
                ),
                output_field=AutoField(),
            ),
            primary_quote=ExpressionWrapper(
                Coalesce(
                    Subquery(
                        base_qs.filter(
                            parent=OuterRef("primary_security"),
                            is_primary=True,
                        ).values(
                            "id"
                        )[:1]
                    ),
                    F("primary_security"),
                ),
                output_field=AutoField(),
            ),
        )

    def annotate_all(self):
        return self.annotate_base_data()

    @property
    def dl(self):
        """Provides access to the dataloader proxy for the entities in the QuerySet.

        This method allows for easy retrieval of the DataloaderProxy instance
        associated with the QuerySet. It enables the utilization of dataloader
        functionalities directly from the QuerySet, facilitating data fetching and
        processing tasks.

        Returns:
            DataloaderProxy: An instance of DataloaderProxy associated with the
                entities in the QuerySet.
        """
        return self.model.dl_proxy(self)
