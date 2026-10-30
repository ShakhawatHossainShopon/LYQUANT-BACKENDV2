import MetaTrader5 as mt5
from services.mt5_service import get_account


def get_account_details():
    account = get_account()

    if not mt5.initialize():
        raise RuntimeError(f"MT5 initialization failed: {mt5.last_error()}")

    try:
        positions = mt5.positions_get()

        if positions is None:
            raise RuntimeError(f"Failed to fetch positions: {mt5.last_error()}")

        total_volume_usd = 0.0

        for position in positions:
            symbol_info = mt5.symbol_info(position.symbol)
            tick = mt5.symbol_info_tick(position.symbol)

            if symbol_info is None or tick is None:
                continue

            price = tick.bid if position.type == mt5.POSITION_TYPE_BUY else tick.ask

            position_value = (
                position.volume
                * symbol_info.trade_contract_size
                * price
            )

            total_volume_usd += position_value

        account["trading_volume"] = round(total_volume_usd, 2)
        account["total_positions"] = len(positions)
        

        return account

    finally:
        mt5.shutdown()