from app.tools import get_database_schema, execute_sql

def test_database_schema():
    schema=get_database_schema()

    assert "students" in schema
    assert "id" in [column["name"] for column in schema["students"]]
    assert "marks" in [column["name"] for column in schema["students"]]

def test_execute_sql_success():
    result=execute_sql("SELECT * FROM students")

    assert result["success"] is True
    assert len(result["results"]) > 0

def test_execute_sql_failure():
    result=execute_sql(
        "SELECT * FROM students WHERE score > 80"
    )

    assert result["success"] is False
    assert "error" in result