import pytest as pytest
from tests.acceptance.dsl.user_dsl import UserDSL


user_dsl = UserDSL()


@pytest.fixture(autouse=True)
def run_around_tests():
    # Before
    yield
    # After
    user_dsl.reset_data_cache()


async def test_should_get_user() -> None:

    # Arrange
    await user_dsl.login_authorized()

    # Act
    await user_dsl.get_user_01()

    # Assert
    await user_dsl.assert_response_is_user_01_data()


def test_should_return_not_found_if_user_dont_exists():
    # Arrange
    user_dsl.login_authorized()

    # Act
    user_dsl.get_non_existent_user()

    # Assert
    user_dsl.assert_response_is_not_found()
