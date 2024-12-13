from wbcore.contrib.icons import WBIcon
from wbcore.enums import RequestType
from wbcore.metadata.configs import buttons as bt
from wbcore.metadata.configs.buttons.view_config import ButtonViewConfig


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
