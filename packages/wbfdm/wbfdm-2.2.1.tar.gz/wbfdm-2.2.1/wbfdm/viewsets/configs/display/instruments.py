from contextlib import suppress
from typing import Optional

from django.utils.translation import gettext as _
from dynamic_preferences.registries import global_preferences_registry
from rest_framework.reverse import reverse
from wbcore.metadata.configs import display as dp
from wbcore.metadata.configs.display import DisplayViewConfig
from wbcore.metadata.configs.display.instance_display import Section
from wbcore.metadata.configs.display.instance_display.layouts.inlines import Inline
from wbcore.metadata.configs.display.instance_display.layouts.layouts import Layout
from wbcore.metadata.configs.display.instance_display.pages import Page
from wbcore.metadata.configs.display.instance_display.shortcuts import (
    Display,
    create_simple_section,
    default,
)
from wbcore.metadata.configs.display.instance_display.styles import Style
from wbcore.metadata.configs.display.instance_display.utils import repeat
from wbfdm.contrib.metric.viewsets.configs.utils import (
    get_performance_fields,
    get_statistic_field,
)
from wbfdm.models import Instrument

ALL_GRIDS = [
    "swe-summary",
    "swe-income-statement",
    "swe-balance-sheet",
    "swe-cashflow-statement",
    "swe-ratios",
    "swe-margins",
    "swe-cashflow-ratios",
    "swe-asset-turnover-ratios",
    "swe-credit",
    "swe-long-term-solvency",
    "swe-short-term-liquidity",
]


def _get_hierarchy_section_title(instrument_id):
    with suppress(Instrument.DoesNotExist):
        instrument = Instrument.objects.get(id=instrument_id)
        if instrument.children.exists():
            if instrument.level == 0:
                return "Securities"
            elif instrument.level == 1:
                return "Quotes"
    return "Children"


def get_financial_summary_section_name() -> str:
    try:
        return global_preferences_registry.manager()["wbfdm__financial_summary_section_name"]
    except Exception:
        return "Financial Summary"


def remove_ref_from_list(grid_list: list, ref: str) -> list[str]:
    _l = grid_list.copy()
    _l.remove(ref)
    return _l


class InstrumentDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(
                    key=None,
                    label=_("Information"),
                    open_by_default=False,
                    children=[
                        dp.Field(key="instrument_type", label=_("Instrument Type"), show="open"),
                        dp.Field(key="exchange", label=_("Exchange"), show="open"),
                        dp.Field(key="isin", label=_("ISIN")),
                        dp.Field(key="ticker", label=_("Ticker")),
                        dp.Field(key="description", label=_("Description"), show="open"),
                        dp.Field(key="currency", label=_("Currency"), show="open"),
                        dp.Field(key="country", label=_("Country"), show="open"),
                        dp.Field(key="classifications", label="Classifications", show="open"),
                        dp.Field(key="tags", label="Tags", show="open"),
                    ],
                ),
                dp.Field(
                    key=None,
                    label=_("Extra"),
                    open_by_default=False,
                    children=[
                        dp.Field(key="is_primary", label=_("Primary")),
                        dp.Field(key="is_investable_universe", label=_("Investable Universe"), show="open"),
                        dp.Field(key="is_security", label=_("Security"), show="open"),
                        dp.Field(key="is_managed", label=_("Internally Managed"), show="open"),
                    ],
                ),
                dp.Field(key=None, label=_("Performance"), open_by_default=False, children=get_performance_fields()),
                get_statistic_field(),
            ],
            tree=True,
            tree_group_pinned="left",
            tree_group_field="name",
            tree_group_label="Name",
            tree_group_level_options=[
                dp.TreeGroupLevelOption(
                    filter_key="parent",
                    filter_depth=1,
                    # lookup="id_repr",
                    list_endpoint=reverse(
                        "wbfdm:instrument-list",
                        args=[],
                        request=self.request,
                    ),
                )
            ],
        )

    def get_instance_display(self):
        return Display(
            pages=[
                Page(
                    title="Home",
                    layouts={
                        ">1000": Layout(
                            grid_template_areas=[
                                ["name", "name_repr", "market_data", "valuation_ratios-new"],
                                ["instrument_type", "exchange", "market_data", "valuation_ratios-new"],
                                ["isin", "ticker", "market_data", "valuation_ratios-new"],
                                ["currency", "country", "market_data", "valuation_ratios-new"],
                                ["inception_date", "delisted_date", "market_data", "valuation_ratios-new"],
                                [".", ".", "market_data", "valuation_ratios-new"],
                                ["description", "description", "description", "description"],
                            ],
                            grid_template_rows=["auto"] * 6 + ["300px"],
                            grid_template_columns=["1fr", "1fr", "500px", "500px"],
                            inlines=[
                                Inline(key="market_data", endpoint="market_data"),
                                Inline(key="valuation_ratios-new", endpoint="valuation_ratios-new"),
                            ],
                        ),
                        default(): Layout(
                            grid_template_areas=[
                                ["name", "market_data", "valuation_ratios-new"],
                                ["isin", "market_data", "valuation_ratios-new"],
                                ["ticker", "market_data", "valuation_ratios-new"],
                                [".", "market_data", "valuation_ratios-new"],
                            ],
                            grid_template_rows=["auto", "auto", "auto", "300px"],
                            grid_template_columns=["1fr", "350px", "350px"],
                            inlines=[
                                Inline(key="market_data", endpoint="market_data"),
                                Inline(key="valuation_ratios-new", endpoint="valuation_ratios-new"),
                            ],
                        ),
                        "<700": Layout(
                            grid_template_areas=[
                                ["name"],
                                ["isin"],
                                ["ticker"],
                                ["market_data"],
                                ["valuation_ratios"],
                            ],
                            grid_template_rows=["auto", "auto", "auto", "auto"],
                            inlines=[
                                Inline(key="market_data", endpoint="market_data"),
                                Inline(key="valuation_ratios", endpoint="valuation_ratios"),
                            ],
                        ),
                    },
                ),
                Page(
                    title=get_financial_summary_section_name(),
                    layouts={
                        default(): Layout(
                            grid_template_areas=[
                                ["summary"],
                                ["statements"],
                                ["profitability-ratios"],
                                ["margin-ratios"],
                                ["cash-ratios"],
                                ["assets-ratios"],
                                ["liquidity-ratios"],
                                ["solvency-ratios"],
                                ["credit-ratios"],
                            ],
                            grid_template_rows=[
                                "auto",
                                "auto",
                                "auto",
                                "auto",
                                "auto",
                                "auto",
                                "auto",
                                "auto",
                                "auto",
                            ],
                            sections=[
                                Section(
                                    key="summary",
                                    title="Financial Summary",
                                    display=Display(
                                        pages=[
                                            Page(
                                                layouts={
                                                    default(): Layout(
                                                        grid_template_areas=[["swe-summary"]],
                                                        grid_template_rows=["850px"],
                                                        inlines=[
                                                            Inline(
                                                                key="swe-summary",
                                                                endpoint="swe-summary",
                                                                aligned_keys=remove_ref_from_list(
                                                                    ALL_GRIDS, "swe-summary"
                                                                ),
                                                            )
                                                        ],
                                                    )
                                                }
                                            )
                                        ]
                                    ),
                                    collapsed=False,
                                ),
                                Section(
                                    key="statements",
                                    title="Statements (IBES)",
                                    display=Display(
                                        pages=[
                                            Page(
                                                title="Income Statment (IBES)",
                                                layouts={
                                                    default(): Layout(
                                                        grid_template_areas=[["swe-income-statement"]],
                                                        grid_template_rows=["850px"],
                                                        inlines=[
                                                            Inline(
                                                                key="swe-income-statement",
                                                                endpoint="swe-income-statement",
                                                                aligned_keys=remove_ref_from_list(
                                                                    ALL_GRIDS, "swe-income-statement"
                                                                ),
                                                            )
                                                        ],
                                                    )
                                                },
                                            ),
                                            Page(
                                                title="Balance Sheet (IBES)",
                                                layouts={
                                                    default(): Layout(
                                                        grid_template_areas=[["swe-balance-sheet"]],
                                                        grid_template_rows=["850px"],
                                                        inlines=[
                                                            Inline(
                                                                key="swe-balance-sheet",
                                                                endpoint="swe-balance-sheet",
                                                                aligned_keys=remove_ref_from_list(
                                                                    ALL_GRIDS, "swe-balance-sheet"
                                                                ),
                                                            )
                                                        ],
                                                    )
                                                },
                                            ),
                                            Page(
                                                title="Cashflow Statement (IBES)",
                                                layouts={
                                                    default(): Layout(
                                                        grid_template_areas=[["swe-cashflow-statement"]],
                                                        grid_template_rows=["850px"],
                                                        inlines=[
                                                            Inline(
                                                                key="swe-cashflow-statement",
                                                                endpoint="swe-cashflow-statement",
                                                                aligned_keys=remove_ref_from_list(
                                                                    ALL_GRIDS, "swe-cashflow-statement"
                                                                ),
                                                            )
                                                        ],
                                                    )
                                                },
                                            ),
                                        ]
                                    ),
                                    collapsed=True,
                                ),
                                Section(
                                    key="profitability-ratios",
                                    title="Profitability Analysis",
                                    display=Display(
                                        pages=[
                                            Page(
                                                layouts={
                                                    default(): Layout(
                                                        grid_template_areas=[["swe-ratios"]],
                                                        grid_template_rows=["500px"],
                                                        inlines=[
                                                            Inline(
                                                                key="swe-ratios",
                                                                endpoint="swe-ratios",
                                                                aligned_keys=remove_ref_from_list(
                                                                    ALL_GRIDS, "swe-ratios"
                                                                ),
                                                            )
                                                        ],
                                                    )
                                                }
                                            )
                                        ]
                                    ),
                                    collapsed=True,
                                ),
                                Section(
                                    key="margin-ratios",
                                    title="Marginality Analysis",
                                    display=Display(
                                        pages=[
                                            Page(
                                                layouts={
                                                    default(): Layout(
                                                        grid_template_areas=[["swe-margins"]],
                                                        grid_template_rows=["500px"],
                                                        inlines=[
                                                            Inline(
                                                                key="swe-margins",
                                                                endpoint="swe-margins",
                                                                aligned_keys=remove_ref_from_list(
                                                                    ALL_GRIDS, "swe-margins"
                                                                ),
                                                            )
                                                        ],
                                                    )
                                                }
                                            )
                                        ]
                                    ),
                                    collapsed=True,
                                ),
                                Section(
                                    key="cash-ratios",
                                    title="Cashflow Ratios",
                                    display=Display(
                                        pages=[
                                            Page(
                                                layouts={
                                                    default(): Layout(
                                                        grid_template_areas=[["swe-cashflow-ratios"]],
                                                        grid_template_rows=["500px"],
                                                        inlines=[
                                                            Inline(
                                                                key="swe-cashflow-ratios",
                                                                endpoint="swe-cashflow-ratios",
                                                                aligned_keys=remove_ref_from_list(
                                                                    ALL_GRIDS, "swe-cashflow-ratios"
                                                                ),
                                                            )
                                                        ],
                                                    )
                                                }
                                            )
                                        ]
                                    ),
                                    collapsed=True,
                                ),
                                Section(
                                    key="assets-ratios",
                                    title="Asset-Turnover",
                                    display=Display(
                                        pages=[
                                            Page(
                                                layouts={
                                                    default(): Layout(
                                                        grid_template_areas=[["swe-asset-turnover-ratios"]],
                                                        grid_template_rows=["500px"],
                                                        inlines=[
                                                            Inline(
                                                                key="swe-asset-turnover-ratios",
                                                                endpoint="swe-asset-turnover-ratios",
                                                                aligned_keys=remove_ref_from_list(
                                                                    ALL_GRIDS, "swe-asset-turnover-ratios"
                                                                ),
                                                            )
                                                        ],
                                                    )
                                                }
                                            )
                                        ]
                                    ),
                                    collapsed=True,
                                ),
                                Section(
                                    key="credit-ratios",
                                    title="Credit Ratios",
                                    display=Display(
                                        pages=[
                                            Page(
                                                layouts={
                                                    default(): Layout(
                                                        grid_template_areas=[["swe-credit"]],
                                                        grid_template_rows=["500px"],
                                                        inlines=[
                                                            Inline(
                                                                key="swe-credit",
                                                                endpoint="swe-credit",
                                                                aligned_keys=remove_ref_from_list(
                                                                    ALL_GRIDS, "swe-credit"
                                                                ),
                                                            )
                                                        ],
                                                    )
                                                }
                                            )
                                        ]
                                    ),
                                    collapsed=True,
                                ),
                                Section(
                                    key="solvency-ratios",
                                    title="Long-Term Solvency Analysis",
                                    display=Display(
                                        pages=[
                                            Page(
                                                layouts={
                                                    default(): Layout(
                                                        grid_template_areas=[["swe-long-term-solvency"]],
                                                        grid_template_rows=["500px"],
                                                        inlines=[
                                                            Inline(
                                                                key="swe-long-term-solvency",
                                                                endpoint="swe-long-term-solvency",
                                                                aligned_keys=remove_ref_from_list(
                                                                    ALL_GRIDS, "swe-long-term-solvency"
                                                                ),
                                                            )
                                                        ],
                                                    )
                                                }
                                            )
                                        ]
                                    ),
                                    collapsed=True,
                                ),
                                Section(
                                    key="liquidity-ratios",
                                    title="Short-Term Liquidity Analysis",
                                    display=Display(
                                        pages=[
                                            Page(
                                                layouts={
                                                    default(): Layout(
                                                        grid_template_areas=[["swe-short-term-liquidity"]],
                                                        grid_template_rows=["500px"],
                                                        inlines=[
                                                            Inline(
                                                                key="swe-short-term-liquidity",
                                                                endpoint="swe-short-term-liquidity",
                                                                aligned_keys=remove_ref_from_list(
                                                                    ALL_GRIDS, "swe-short-term-liquidity"
                                                                ),
                                                            )
                                                        ],
                                                    )
                                                }
                                            )
                                        ]
                                    ),
                                    collapsed=True,
                                ),
                            ],
                        )
                    },
                ),
                Page(
                    title="Additional Informations",
                    layouts={
                        default(): Layout(
                            grid_template_areas=[
                                ["classifications_list", "instrument_lists"],
                            ],
                            grid_template_columns=[Style.pct(50), Style.pct(50)],
                            sections=[
                                create_simple_section(
                                    key="classifications_list",
                                    title="Classifications",
                                    grid_template_areas=[["classifications_list"]],
                                    inline_key="classifications_list",
                                    collapsible=False,
                                ),
                                create_simple_section(
                                    key="instrument_lists",
                                    title="Instrument Lists",
                                    grid_template_areas=[["instrument_lists"]],
                                    inline_key="instrument_lists",
                                    collapsible=False,
                                ),
                            ],
                        )
                    },
                ),
                # TODO Renable after adapting the code to use financial dataloader
                # Page(
                #     title="Financial Analysis",
                #     layouts={
                #         default(): Layout(
                #             grid_template_areas=[
                #                 ["sect_head_fin_summary", "sect_head_fin_summary"],
                #                 ["summary_table", "summary_table"],
                #                 ["sect_head_inc_cf_summary", "sect_head_inc_cf_summary"],
                #                 ["financials_graph", "cash_flow_analysis_chart"],
                #                 ["sect_head_profit_debt_summary", "sect_head_profit_debt_summary"],
                #                 ["profitability_ratios", "net_debt_and_ebitda_chart"],
                #                 ["sect_head_earnings", "sect_head_earnings"],
                #                 ["earnings_chart_ttm", "earnings_chart_ntm"],
                #             ],
                #             grid_template_rows=[
                #                 Style.px(40),
                #                 Style.px(800),
                #                 Style.px(40),
                #                 Style.px(500),
                #                 Style.px(40),
                #                 Style.px(500),
                #                 Style.px(40),
                #                 Style.px(500),
                #             ],
                #             inlines=[
                #                 Inline(key="summary_table", endpoint="summary_table"),
                #                 Inline(key="financials_graph", endpoint="financials_graph"),
                #                 Inline(key="profitability_ratios", endpoint="profitability_ratios"),
                #                 Inline(key="cash_flow_analysis_chart", endpoint="cash_flow_analysis_chart"),
                #                 Inline(key="net_debt_and_ebitda_chart", endpoint="net_debt_and_ebitda_chart"),
                #                 Inline(key="earnings_chart_ttm", endpoint="earnings_chart_ttm"),
                #                 Inline(key="earnings_chart_ntm", endpoint="earnings_chart_ntm"),
                #             ],
                #             sections=[
                #                 create_simple_section(key="sect_head_fin_summary", title="Financial Summary"),
                #                 create_simple_section(
                #                     key="sect_head_inc_cf_summary",
                #                     title="Income Statement and Cash Flow Summary Charts",
                #                 ),
                #                 create_simple_section(
                #                     key="sect_head_profit_debt_summary",
                #                     title="Profitability and Net Debt Summary Charts",
                #                 ),
                #                 create_simple_section(key="sect_head_earnings", title="Earnings Analysis"),
                #             ],
                #         )
                #     },
                # ),
                # Page(
                #     title="Valuation Ratios",
                #     layouts={
                #         default(): Layout(
                #             grid_template_areas=[
                #                 ["valuation_ratios_ranges", "valuation_ratios_related"],
                #             ],
                #             grid_template_columns=[Style.pct(50), Style.pct(50)],
                #             grid_template_rows=[Style.px(575), Style.fr(1)],
                #             inlines=[
                #                 Inline(key="valuation_ratios_ranges", endpoint="valuation_ratios_ranges"),
                #                 Inline(key="valuation_ratios_related", endpoint="valuation_ratios_related"),
                #             ],
                #         )
                #     },
                # ),
                Page(
                    title="Management",
                    layouts={
                        default(): Layout(
                            grid_template_areas=[
                                ["ticker", "refinitiv_identifier_code", "refinitiv_mnemonic_code", "identifier"],
                                ["base_color", "old_isins", "is_cash", "."],
                                ["tags", "tags", "related", "related"],
                            ],
                            grid_template_columns=[repeat(4, Style.fr(1))],
                            inlines=[
                                Inline(key="exchanges", endpoint="exchanges"),
                                Inline(key="related", endpoint="related_instruments"),
                            ],
                        )
                    },
                ),
                Page(
                    title="Hierarchy",
                    layouts={
                        default(): Layout(
                            grid_template_areas=[
                                ["children"],
                            ],
                            grid_template_rows=["auto"],
                            sections=[
                                Section(
                                    key="children",
                                    title="Hierarchy",
                                    display=Display(
                                        pages=[
                                            Page(
                                                layouts={
                                                    default(): Layout(
                                                        grid_template_areas=[["children"]],
                                                        grid_template_rows=["850px"],
                                                        inlines=[
                                                            Inline(
                                                                key="children",
                                                                endpoint="children",
                                                            )
                                                        ],
                                                    )
                                                }
                                            )
                                        ]
                                    ),
                                    collapsed=False,
                                )
                            ],
                        )
                    },
                ),
            ]
        )
