from .types import RegisteredGbcMessageEffect
from ..logger import log
from ..gbc_extra import (
    GlowbuzzerInboundMessage
)
from ..machine_state import MachineState, determine_machine_state
from ..client import GbcWebsocketInterface


class MachineStateLogger(RegisteredGbcMessageEffect):
    """
    Simple effect to print when the machine state changes
    """

    def select(self, msg: GlowbuzzerInboundMessage):
        if msg.status and msg.status.machine:
            return determine_machine_state(msg.status.machine.statusWord)

    async def on_change(self, new_value: MachineState, send: GbcWebsocketInterface):
        log.info("Change in CIA402 state: %s", new_value)


class OperationErrorLogger(RegisteredGbcMessageEffect):
    """
    Simple effect to print when the operation error state changes
    """

    def select(self, msg: GlowbuzzerInboundMessage):
        if msg.status:
            return msg.status.machine.operationError, msg.status.machine.operationErrorMessage

    async def on_change(self, state, send: GbcWebsocketInterface):
        log.info("Operating error state changed: %s", state)
