from rest_framework.reverse import reverse
from wbcore.contrib.icons import WBIcon
from wbcore.enums import RequestType
from wbcore.metadata.configs import buttons as bt
from wbcore.metadata.configs.buttons.view_config import ButtonViewConfig
from wbfdm.models import Instrument
from wbportfolio.models import TradeProposal


class TradeButtonConfig(ButtonViewConfig):
    def get_custom_list_instance_buttons(self):
        return {bt.WidgetButton(key="claims", label="Claims", icon=WBIcon.TRADE.icon)}

    def get_custom_instance_buttons(self):
        btn = self.get_custom_list_instance_buttons()
        btn.add(
            bt.HyperlinkButton(
                key="import_source",
                label="Import Source",
                icon=WBIcon.SAVE.icon,
            )
        )
        return btn


class TradeInstrumentButtonConfig(TradeButtonConfig):
    def get_custom_buttons(self):
        res = set()
        if instrument_id := self.view.kwargs.get("instrument_id", None):
            instrument = Instrument.objects.get(id=instrument_id)
            res = {
                bt.WidgetButton(
                    endpoint=reverse(
                        "wbportfolio:instrument-custodiandistribution-list", args=[instrument_id], request=self.request
                    ),
                    label="Custodian Distribution",
                ),
                bt.WidgetButton(
                    endpoint=reverse(
                        "wbportfolio:instrument-customerdistribution-list", args=[instrument_id], request=self.request
                    ),
                    label="Customer Distribution",
                ),
            }
            if instrument.security_instrument_type.key == "product":
                res.add(
                    bt.WidgetButton(
                        endpoint=reverse(
                            "wbportfolio:product-nominalchart-list", args=[instrument_id], request=self.request
                        ),
                        label="Nominal Chart",
                    )
                )
                res.add(
                    bt.WidgetButton(
                        endpoint=reverse(
                            "wbportfolio:product-aumchart-list", args=[instrument_id], request=self.request
                        ),
                        label="AUM Chart",
                    )
                )
        return res


class TradeTradeProposalButtonConfig(ButtonViewConfig):
    def get_custom_buttons(self):
        if trade_proposal_id := self.view.kwargs.get("trade_proposal_id", None):
            trade_proposal = TradeProposal.objects.get(id=trade_proposal_id)
            if trade_proposal.status == TradeProposal.Status.DRAFT:
                return {
                    bt.DropDownButton(
                        label="Tools",
                        buttons=(
                            bt.ActionButton(
                                method=RequestType.PATCH,
                                identifiers=("wbportfolio:tradeproposal",),
                                endpoint=reverse(
                                    "wbportfolio:tradeproposal-reset", args=[trade_proposal_id], request=self.request
                                ),
                                icon=WBIcon.REGENERATE.icon,
                                label="Reset Trade",
                                description_fields="""
                                        <p>Delete and recreate initial trades to from its associated model portfolio</p>
                                        """,
                                action_label="Reset Trade",
                                title="Reset Trade",
                            ),
                            bt.ActionButton(
                                method=RequestType.PATCH,
                                identifiers=("wbportfolio:tradeproposal",),
                                endpoint=reverse(
                                    "wbportfolio:tradeproposal-normalize",
                                    args=[trade_proposal_id],
                                    request=self.request,
                                ),
                                icon=WBIcon.EDIT.icon,
                                label="Normalize Trades",
                                description_fields="""
                                        <p>Make sure all trades normalize to a total target weight of 100%</p>
                                        """,
                                action_label="Normalize Trades",
                                title="Normalize Trades",
                            ),
                            bt.ActionButton(
                                method=RequestType.PATCH,
                                identifiers=("wbportfolio:tradeproposal",),
                                endpoint=reverse(
                                    "wbportfolio:tradeproposal-deleteall",
                                    args=[trade_proposal_id],
                                    request=self.request,
                                ),
                                icon=WBIcon.DELETE.icon,
                                label="Delete All Trades",
                                description_fields="""
                                <p>Delete all trades from this trade proposal?</p>
                                """,
                                action_label="Delete All Trades",
                                title="Delete All Trades",
                            ),
                        ),
                    )
                }
        return {}


class TradeProposalButtonConfig(ButtonViewConfig):
    def get_custom_list_instance_buttons(self):
        return {
            bt.ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:tradeproposal",),
                key="replay",
                icon=WBIcon.SYNCHRONIZE.icon,
                label="Replay Trades",
                description_fields="""
                <p>Replay Trades. It will recompute all assets positions until next trade proposal day (or today otherwise) </p>
                """,
                action_label="Replay Trade",
                title="Replay Trade",
            )
        }

    def get_custom_instance_buttons(self):
        return self.get_custom_list_instance_buttons()
