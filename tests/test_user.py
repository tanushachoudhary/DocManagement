from domain.user import User

def test_create_user():
    user = User("u1", "Tanusha")
    assert user.get_id() == "u1"
    assert user.get_name() == "Tanusha"
