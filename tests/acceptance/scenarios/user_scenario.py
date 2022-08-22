import pytest as pytest

from acceptance.dsl.auth_dsl import AuthDSL
from acceptance.dsl.user_dsl import UserDSL

user_dsl = UserDSL()
auth_dsl = AuthDSL()


@pytest.fixture(autouse=True)
def run_around_tests():
    # Before
    yield
    # After
    user_dsl.reset_data_cache()


async def test_should_get_user() -> None:
    # Arrange
    await auth_dsl.login_authorized()

    # Act
    await user_dsl.get_user_01()

    # Assert
    await user_dsl.assert_response_is_user_01_data()


async def test_should_return_not_found_if_user_doesnt_exists():
    # Arrange
    await auth_dsl.login_authorized()

    # Act
    await user_dsl.get_non_existent_user()

    # Assert
    await user_dsl.assert_response_is_not_found()


async def test_should_return_updated_user_if_valid_user_is_given():
    # Arrange
    await auth_dsl.login_authorized()

    # Act
    await user_dsl.update_valid_user()

    # Assert
    await user_dsl.assert_response_is_updated_user()
