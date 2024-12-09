import pytest

from crypto_connector.base.exchange import Exchange
from crypto_connector.base.schemas import Transfer


@pytest.mark.parametrize(
    "exchange",
    argvalues=[
        ("Binance"),
        ("HTX"),
    ],
    indirect=["exchange"],
)
def test_get_transfer_history(exchange: Exchange) -> None:
    transfers = exchange.get_transfer_history()
    assert [Transfer.model_validate(tr) for tr in transfers]


if __name__ == "__main__":
    pytest.main([__file__])
