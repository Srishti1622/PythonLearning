# # Testing
# -- it is a way for us to make sure that our application is working as intended
# -- part of the software development lifecycle (SDLC) that aims to identify:
#     -- bugs, error, defects
# -- three different ways to do testing:
#     -- manual : which we do ourselves by just running the application
#     -- unit : involves testing individual components or units of software in isolation from the rest of the application, validates that each unit of the software performs as designed, developers write unit tests during the development phase, these tests are automated and executed by a testing framework (Pytest)
#     -- integration : instead of testing a single unit like unit testing, integration testing focuses on testing the iteractions between different unites or components of the piece of software, helps identify problems for the entire solution, ex- call an api endpoint and make sure the correct solution is returned


# Pytest
# -- popular testing framework for python
# -- known for simplicity, scalability and ability to handle both unit and integration tests
# -- top reasons to use Pytest:
#     -> simple and flexible : native assertions
#     -> fictures : feature setup and teardown
#     -> parameterized testing : run same tests with different data

# NOTES: Pytest will run all tests automatically that sit within files that have the name 'test' in them
# Ex- 'todos.py' will be tested by 'test_todos.py'

# Setup 
# -- create a folder named test inside the project directory
# -- create a file named "__init__.py"
# -- create a file named "test_example.py"

# IMPORTANT: to run all the tests present, we need to run the command - pytest

# Assertion = statement that checks if a condition is true
# if condition is true, test passes
# if condition is false, test fails

# Validate Integers
def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1
    assert 3 >= 2
    assert 3 != 2

# Validate Instances
def test_is_instance():
    assert isinstance('this is a string', str)
    assert not isinstance('10', int)

# Validate Booleans
def test_boolean():
    validated=True
    assert validated is True
    assert ('hello'=='world') is False

# Validate Types
def test_type():
    assert type('this is a string') is str
    assert type('world') is not int

# Validate Greater than and less than
def test_greater_and_less_than():
    assert 7>3
    assert 4<10

# Validate Lists
def test_list():
    num_list=[1,2,3,4,5]
    any_list=[False,False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)