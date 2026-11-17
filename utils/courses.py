
from database.db import get_connection


# ---------------- COURSE CONTENT ----------------

COURSES = {
    "Python Programming": {
        "description": "Learn Python programming from beginner to intermediate level.",
        "category": "Programming",
        "duration": "4 Weeks",
        "level": "Beginner",
        "lessons": [
            {
                "title": "Introduction to Python",
                "content": """
Python is a popular, beginner-friendly programming language.

It is used in:
- Web development
- Artificial Intelligence
- Data Science
- Automation

Example:

print("Hello, CareerSpring!")
"""
            },
            {
                "title": "Variables and Data Types",
                "content": """
Variables store information in a program.

Example:

name = "Muskan"
age = 20
percentage = 85.5
is_student = True

Common data types:
- String
- Integer
- Float
- Boolean
"""
            },
            {
                "title": "Conditional Statements and Loops",
                "content": """
Conditional statements make decisions.

Example:

marks = 80

if marks >= 40:
    print("Pass")
else:
    print("Fail")

Loops repeat instructions.

Example:

for number in range(1, 6):
    print(number)
"""
            },
            {
                "title": "Functions",
                "content": """
Functions are reusable blocks of code.

Example:

def greet(name):
    print("Hello", name)

greet("Muskan")

Functions make programs easier to organize and reuse.
"""
            }
        ],
        "quiz": [
            {
                "question": "Which function displays output in Python?",
                "options": ["input()", "print()", "display()", "show()"],
                "answer": "print()"
            },
            {
                "question": "Which symbol is used for comments in Python?",
                "options": ["//", "/*", "#", "<!--"],
                "answer": "#"
            },
            {
                "question": "Which data type stores True or False?",
                "options": ["String", "Boolean", "Float", "Integer"],
                "answer": "Boolean"
            },
            {
                "question": "Which keyword defines a function?",
                "options": ["function", "define", "def", "fun"],
                "answer": "def"
            },
            {
                "question": "What does range(5) generate?",
                "options": ["1 to 5", "0 to 4", "1 to 4", "0 to 5"],
                "answer": "0 to 4"
            }
        ]
    },

    "C Programming": {
        "description": "Understand programming fundamentals using C.",
        "category": "Programming",
        "duration": "3 Weeks",
        "level": "Beginner",
        "lessons": [
            {
                "title": "Introduction to C",
                "content": """
C is a general-purpose programming language.

It is widely used in:
- Operating systems
- Embedded systems
- System programming

Example:

#include <stdio.h>

int main() {
    printf("Hello World");
    return 0;
}
"""
            },
            {
                "title": "Variables and Data Types",
                "content": """
Variables store values.

Example:

int age = 20;
float marks = 85.5;
char grade = 'A';

Common C data types:
- int
- float
- char
- double
"""
            },
            {
                "title": "Conditions and Loops",
                "content": """
Conditions help programs make decisions.

Example:

if (age >= 18) {
    printf("Adult");
} else {
    printf("Minor");
}

Loops include:
- for
- while
- do-while
"""
            },
            {
                "title": "Arrays and Functions",
                "content": """
Arrays store multiple values of the same type.

Example:

int numbers[3] = {10, 20, 30};

Functions divide programs into reusable blocks.

Example:

int add(int a, int b) {
    return a + b;
}
"""
            }
        ],
        "quiz": [
            {
                "question": "Which header file is commonly used for printf()?",
                "options": ["stdlib.h", "stdio.h", "string.h", "math.h"],
                "answer": "stdio.h"
            },
            {
                "question": "Which symbol ends a C statement?",
                "options": [":", ".", ";", ","],
                "answer": ";"
            },
            {
                "question": "Which data type stores whole numbers?",
                "options": ["float", "char", "int", "double"],
                "answer": "int"
            },
            {
                "question": "Which loop executes while a condition is true?",
                "options": ["while", "switch", "break", "return"],
                "answer": "while"
            },
            {
                "question": "What is the first array index in C?",
                "options": ["1", "-1", "0", "2"],
                "answer": "0"
            }
        ]
    },

    "SQL Database": {
        "description": "Learn database concepts and SQL queries.",
        "category": "Database",
        "duration": "3 Weeks",
        "level": "Beginner",
        "lessons": [
            {
                "title": "Introduction to SQL",
                "content": """
SQL stands for Structured Query Language.

It is used to manage relational databases.

SQL can:
- Create tables
- Insert records
- Retrieve data
- Update records
- Delete records
"""
            },
            {
                "title": "Creating Tables",
                "content": """
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
);

This creates a table called students.
"""
            },
            {
                "title": "SQL Queries",
                "content": """
INSERT INTO students
VALUES (1, 'Muskan', 20);

SELECT * FROM students;

UPDATE students
SET age = 21
WHERE id = 1;

DELETE FROM students
WHERE id = 1;
"""
            },
            {
                "title": "Filtering and Joins",
                "content": """
WHERE filters records.

SELECT * FROM students
WHERE age > 18;

ORDER BY sorts records.

JOIN combines information from related tables.

Example:

SELECT students.name, courses.title
FROM students
JOIN courses
ON students.id = courses.id;
"""
            }
        ],
        "quiz": [
            {
                "question": "What does SQL stand for?",
                "options": [
                    "Simple Query Language",
                    "Structured Query Language",
                    "Standard Question Language",
                    "System Query Logic"
                ],
                "answer": "Structured Query Language"
            },
            {
                "question": "Which command retrieves data?",
                "options": ["INSERT", "UPDATE", "SELECT", "DELETE"],
                "answer": "SELECT"
            },
            {
                "question": "Which clause filters records?",
                "options": ["ORDER BY", "WHERE", "GROUP BY", "JOIN"],
                "answer": "WHERE"
            },
            {
                "question": "Which command adds a new record?",
                "options": ["INSERT", "SELECT", "DROP", "ALTER"],
                "answer": "INSERT"
            },
            {
                "question": "Which key uniquely identifies a table record?",
                "options": ["Foreign Key", "Primary Key", "Duplicate Key", "Sort Key"],
                "answer": "Primary Key"
            }
        ]
    },

    "Git and GitHub": {
        "description": "Learn version control and manage coding projects.",
        "category": "Development Tools",
        "duration": "2 Weeks",
        "level": "Beginner",
        "lessons": [
            {
                "title": "Introduction to Git",
                "content": """
Git is a version control system.

It helps developers:
- Track code changes
- Restore previous versions
- Work with other developers

Git is commonly used in software development.
"""
            },
            {
                "title": "Basic Git Commands",
                "content": """
Initialize a repository:

git init

Check repository status:

git status

Add files:

git add .

Save changes:

git commit -m "Initial commit"
"""
            },
            {
                "title": "Introduction to GitHub",
                "content": """
GitHub is an online platform for hosting Git repositories.

It helps developers:
- Share projects
- Collaborate
- Maintain portfolios
- Contribute to open-source software
"""
            },
            {
                "title": "Push and Pull",
                "content": """
Connect your local repository to GitHub:

git remote add origin REPOSITORY_URL

Upload changes:

git push -u origin main

Download changes:

git pull origin main
"""
            }
        ],
        "quiz": [
            {
                "question": "What is Git?",
                "options": [
                    "A programming language",
                    "A version control system",
                    "A database",
                    "A web browser"
                ],
                "answer": "A version control system"
            },
            {
                "question": "Which command initializes a Git repository?",
                "options": ["git start", "git create", "git init", "git open"],
                "answer": "git init"
            },
            {
                "question": "Which command stages files?",
                "options": ["git add", "git push", "git pull", "git clone"],
                "answer": "git add"
            },
            {
                "question": "What is GitHub?",
                "options": [
                    "An online code hosting platform",
                    "An operating system",
                    "A database language",
                    "A text editor"
                ],
                "answer": "An online code hosting platform"
            },
            {
                "question": "Which command uploads local commits?",
                "options": ["git pull", "git push", "git init", "git status"],
                "answer": "git push"
            }
        ]
    }
}


# ---------------- DATABASE FUNCTIONS ----------------

def initialize_courses():
    """Add default courses to the database."""

    connection = get_connection()

    for title, course in COURSES.items():
        connection.execute(
            """
            INSERT OR IGNORE INTO courses
            (title, description, category, duration, level)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                title,
                course["description"],
                course["category"],
                course["duration"],
                course["level"]
            )
        )

    connection.commit()
    connection.close()


def get_courses():
    """Return all available courses."""

    connection = get_connection()

    courses = connection.execute(
        "SELECT * FROM courses ORDER BY id"
    ).fetchall()

    connection.close()

    return courses


def get_course_content(course_title):
    """Return lessons and quiz for a selected course."""

    return COURSES.get(course_title)


def save_course_progress(user_id, course_id, score):
    """Save quiz score and course completion status."""

    completed = 1 if score >= 60 else 0

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO course_progress
        (user_id, course_id, completed, score)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, course_id)
        DO UPDATE SET
            completed = MAX(course_progress.completed, excluded.completed),
            score = MAX(course_progress.score, excluded.score)
        """,
        (user_id, course_id, completed, score)
    )

    connection.commit()
    connection.close()


def get_student_progress(user_id):
    """Get the student's course completion details."""

    connection = get_connection()

    progress = connection.execute(
        """
        SELECT courses.title, course_progress.completed,
               course_progress.score
        FROM course_progress
        JOIN courses ON courses.id = course_progress.course_id
        WHERE course_progress.user_id = ?
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return progress
