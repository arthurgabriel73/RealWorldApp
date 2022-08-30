import pytest as pytest

from tests.acceptance.dsl.article_dsl import ArticleDSL
from tests.acceptance.dsl.auth_dsl import AuthDSL

auth_dsl = AuthDSL()
article_dsl = ArticleDSL()


@pytest.fixture(autouse=True)
def run_around_tests():
    # Before
    yield
    # After
    article_dsl.reset_data_cache()


async def test_should_create_article() -> None:
    # Arrange
    await auth_dsl.login_authorized()
    # Act
    await article_dsl.create_article()

    # Assert
    await article_dsl.assert_response_is_article_data()


async def test_should_get_article() -> None:
    # Arrange
    await auth_dsl.login_authorized()

    # Arrange
    await article_dsl.get_article()

    # Assert
    await article_dsl.assert_response_is_article_data()


async def test_should_return_not_found_if_article_doesnt_exists():
    # Arrange
    await auth_dsl.login_authorized()

    # Act
    await article_dsl.get_non_existent_article()

    # Assert
    await article_dsl.assert_response_is_not_found()
