from app import User
from app import Task
import pytest

def test_new_user():
    user = User("patkennedy79@gmail.com", "FlaskIsAwesome")
    assert user.username == "patkennedy79@gmail.com"
    assert user.password == "FlaskIsAwesome"
    assert user.level == 0
    assert user.name == "Pretzel"
    assert user.type == "cat"
    assert user.hunger == 100
    assert user.health == 100
    assert user.point == 0
    
if __name__ == "__main__":
    pytest.new_user()
