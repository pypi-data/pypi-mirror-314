from typing import Generator

import pandas as pd
from wbcompliance.models import RiskIncidentType
from wbcompliance.models.risk_management import backend
from wbcompliance.models.risk_management.dispatch import register
from wbcore import serializers as wb_serializers
from wbcore.serializers.fields.number import percent_decorator
from wbfdm.models import Instrument
from wbportfolio.pms.typing import Portfolio as PortfolioDTO

from .mixins import ActivePortfolioRelationshipMixin


@register("UCITS 5|10|40 Portfolio Rule Backend", rule_group_key="portfolio")
class RuleBackend(ActivePortfolioRelationshipMixin, backend.AbstractRuleBackend):
    DEFAULT_THRESHOLD_1: float = 0.05
    DEFAULT_THRESHOLD_2: float = 0.10
    DEFAULT_THRESHOLD_3: float = 0.40

    @classmethod
    def get_serializer_class(cls) -> wb_serializers.Serializer:
        class RuleBackendSerializer(wb_serializers.Serializer):
            threshold_1 = wb_serializers.FloatField(
                default=cls.DEFAULT_THRESHOLD_1, label="Threshold 1", percent=True, decorators=[percent_decorator]
            )
            threshold_2 = wb_serializers.FloatField(
                default=cls.DEFAULT_THRESHOLD_2, label="Threshold 2", percent=True, decorators=[percent_decorator]
            )
            threshold_3 = wb_serializers.FloatField(
                default=cls.DEFAULT_THRESHOLD_3, label="Threshold 3", percent=True, decorators=[percent_decorator]
            )

            @classmethod
            def get_parameter_fields(cls):
                return ["threshold_1", "threshold_2", "threshold_3"]

        return RuleBackendSerializer

    def _filter_df(self, df):
        if df.empty:
            return df
        return df[(df["weighting"] >= self.threshold_1) & (~df["is_cash"])]

    def _process_dto(self, portfolio: PortfolioDTO, **kwargs) -> Generator[backend.IncidentResult, None, None]:
        if not (df := self._filter_df(pd.DataFrame(portfolio.to_df()).astype({"weighting": float}))).empty:
            df = df[["underlying_instrument", "weighting"]].groupby("underlying_instrument").sum()
            total_weight_threshold_1_2 = df.loc[df["weighting"] < self.threshold_2, "weighting"].sum()
            highest_incident_type = RiskIncidentType.objects.order_by("-severity_order").first()
            for id, row in df.to_dict("index").items():
                if (row["weighting"] > self.threshold_2) or (total_weight_threshold_1_2 > self.threshold_3):
                    instrument = Instrument.objects.get(id=id)
                    yield backend.IncidentResult(
                        breached_object=instrument,
                        breached_object_repr=str(instrument),
                        breached_value=f'∑[0%, {self.threshold_2:.2%}]:  {row["weighting"]:+.2%} | ∑[{self.threshold_1:.2%}, {self.threshold_2:.2%}]: {total_weight_threshold_1_2:+.2%}',
                        report_details={
                            "Breach Thresholds": f"{self.threshold_1}|{self.threshold_2}|{self.threshold_3}",
                            "Weighting": f"{row['weighting']:.3f}",
                            f"Sum of positions whose weight are between {self.threshold_1:.2%} and {self.threshold_2:.2%}": f"{total_weight_threshold_1_2:.3f}",
                        },
                        severity=highest_incident_type,
                    )
