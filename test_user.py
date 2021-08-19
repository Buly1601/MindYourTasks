from app import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    user = User('patkennedy79@gmail.com', 'FlaskIsAwesome')
    assert user.username == 'patkennedy79@gmail.com'
    assert user.password == 'FlaskIsAwesome'
    assert user.level == 0
    assert user.name == "Pretzel"
    assert user.type == "cat"
    assert user.hunger == 100
    assert user.health == 100
    assert user.point == 0