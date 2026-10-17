from unittest.mock import AsyncMock, MagicMock, Mock

import pytest


@pytest.fixture
def mock_uow():
    uow = AsyncMock()
    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=False)

    return uow


@pytest.fixture
def mock_response():
    response = Mock()

    return response


@pytest.fixture
def mock_session(mock_response):
    session = MagicMock()

    session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
    session.get.return_value.__aexit__ = AsyncMock(return_value=False)

    return session
