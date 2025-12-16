from . import cursor, db

class Course:
    def __init__(
        self, 
        code: str = None,
        name: str = None,
        college: str = None
    ) -> None:
        self.code = code
        self.name = name
        self.college = college


    def get_all(self, page_num: int = None, item_per_page: int = None, paginate: bool = True) -> list:
        """Get all courses, optionally paginated."""
        if not paginate:
            return self.course_list()

        offset = (page_num - 1) * item_per_page
        query = f'''
            SELECT course.code, course.name, course.college AS collegecode, college.name
            FROM course
            JOIN college
            ON course.college = college.code
            ORDER BY course.code DESC
            LIMIT {item_per_page} OFFSET {offset}
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        courses = [list(course) for course in result]
        return courses


    @staticmethod
    def get_total() -> int:
        """Get total number of courses."""
        query = '''SELECT COUNT(*) FROM course'''
        cursor.execute(query)
        (total,) = cursor.fetchone()
        return total


    @staticmethod
    def course_list() -> list:
        """Get full course list (no pagination)."""
        query = '''
            SELECT course.code, course.name, course.college AS collegecode, college.name
            FROM course
            JOIN college
            ON course.college = college.code
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        courses = [list(course) for course in result]
        return courses


    def search(self, keyword: str = None, field: str = None) -> list:
        """Search courses by keyword and optional field."""
        keyword = keyword.upper()
        courses = self.get_all(paginate=False)
        result = []

        if field is None:
            result = self.search_by_field(courses, keyword, 'all')
        elif field == 'code':
            result = self.search_by_field(courses, keyword, 'code')
        elif field == 'name':
            result = self.search_by_field(courses, keyword, 'name')
        elif field == 'college':
            result = self.search_by_field(courses, keyword, 'college')

        return result


    @staticmethod
    def search_by_field(rows: list = None, keyword: str = None, field: str = None) -> list:
        """Helper function for search."""
        result = []
        for row in rows:
            row_allcaps = [str(cell).upper() for cell in row if cell != '']

            if field == 'all':
                if any(keyword in cell for cell in row_allcaps):
                    result.append(row)
            elif field == 'code' and keyword in row_allcaps[0]:
                result.append(row)
            elif field == 'name' and keyword in row_allcaps[1]:
                result.append(row)
            elif field == 'college' and keyword in row_allcaps[2]:
                result.append(row)

        return result


    @staticmethod
    def get_coursecodes() -> list:
        """Return list of all course codes."""
        query = 'SELECT code FROM course'
        cursor.execute(query)
        result = cursor.fetchall()
        return [code[0] for code in result]


    @staticmethod
    def get_coursecode_for(course_name: str = None) -> str:
        """Get course code for a given course name."""
        query = f'''
            SELECT code
            FROM course
            WHERE name = '{course_name}'
        '''
        cursor.execute(query)
        coursecode = cursor.fetchone()
        return coursecode[0] if coursecode else None


    def add_new(self) -> None:
        """Add a new course record."""
        query = f'''
            INSERT INTO course (code, name, college)
            VALUES ('{self.code}', '{self.name}', '{self.college}')
        '''
        cursor.execute(query)
        db.commit()
        return None


    @staticmethod
    def delete(code: str = None) -> None:
        """Delete a course by code."""
        query = f'''
            DELETE FROM course
            WHERE code = '{code}'
        '''
        cursor.execute(query)
        db.commit()
        return None


    def update(self) -> None:
        """Update an existing course record."""
        query = f'''
            UPDATE course
            SET 
                name = '{self.name}',
                college = '{self.college}'
            WHERE
                code = '{self.code}'
        '''
        cursor.execute(query)
        db.commit()
        return None


    @staticmethod
    def get_collegecode(course_name: str = None) -> str:
        """Get the college code for a given course name."""
        query = f'''
            SELECT course.name, college.code
            FROM course
            JOIN college
            ON course.college = college.code
            WHERE course.name = '{course_name}'
            LIMIT 1
        '''
        cursor.execute(query)
        row = cursor.fetchone()
        return row[1] if row else None
