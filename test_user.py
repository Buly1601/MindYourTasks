from app import User
from app import Task


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


def test_new_task():
    task = Task("this is my tast", "patkennedy79@gmail.com")
    assert task.content == "this is my tast"
    assert task.done == False
    assert task.owner == "patkennedy79@gmail.com"
