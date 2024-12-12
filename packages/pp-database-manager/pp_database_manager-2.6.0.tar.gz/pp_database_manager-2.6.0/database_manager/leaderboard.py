import os
import sys
from operator import itemgetter
from typing import Dict, List, Optional

from dotenv import load_dotenv
from supabase import create_client


class StudentRankings:
    """
    A class to handle student rankings across different databases and grades.
    """

    def __init__(self):
        """Initialize the database connections and load environment variables."""
        # Load environment variables
        load_dotenv()

        # Initialize Supabase
        self.SUPABASE_URL = os.environ["SUPABASE_URL"]
        self.SUPABASE_KEY = os.environ["SUPABASE_KEY"]
        self.supabase = create_client(self.SUPABASE_URL, self.SUPABASE_KEY)

    def fetch_student_rankings(self, grade: str) -> Dict[str, float]:
        """
        Fetch student rankings sorted by scores in descending order from a specific grade.

        Args:
            grade (str): Grade/table name to query

        Returns:
            dict: Dictionary with student names as keys and their scores as values
        """
        try:

            # Fetch data selecting both columns and sort by Currency descending
            response = self.supabase.table(grade)\
                .select("Name,Currency")\
                .order("Currency", desc=True)\
                .execute()

            # Convert the response data to a dictionary
            result_dict = {entry['Name']: entry['Currency'] for entry in response.data}

            return result_dict

        except Exception as e:
            print(f"Error fetching data for grade {grade}: {str(e)}")
            return {}

    def get_specific_student_rank(self, grade: str, student_name: str) -> Optional[Dict[str, any]]:
        """
        Get a specific student's ranking and details within their grade.

        Args:
            table_name (str): Name of the table to query
            grade (str): Grade of the student
            student_name (str): Name of the student to look up

        Returns:
            Optional[Dict]: Dictionary containing student's rank and details, or None if not found
        """
        try:
            # Fetch all students in the grade
            all_students = self.fetch_student_rankings(grade)

            if not all_students:
                print(f"No data found for table: {grade}")
                return None

            # Convert to sorted list of tuples (name, currency)
            sorted_students = sorted(
                all_students.items(),
                key=lambda x: x[1],
                reverse=True
            )

            # Find the student's position
            for rank, (name, currency) in enumerate(sorted_students, 1):
                if name.lower() == student_name.lower():

                    # Get total number of students
                    total_students = len(sorted_students)

                    return {
                        "name": name,
                        "grade": grade,
                        "rank": rank,
                        "total_students": total_students,
                        "currency_balance": currency,
                    }

            print(f"Student {student_name} not found in {grade}")
            return None

        except Exception as e:
            print(f"Error getting rank for student {student_name}: {str(e)}")
            return None

    def get_top_students_across_grades(
        self,
        grades: List[str],
        top_n_per_grade: int = 3,
        final_top_n: int = 10
    ) -> List[Dict[str, any]]:
        """
        Get top students across multiple grades.

        Args:
            grades (List[str]): List of grades to query
            top_n_per_grade (int): Number of top students to get from each grade
            final_top_n (int): Final number of top students to return overall

        Returns:
            List[Dict]: List of dictionaries containing student info sorted by currency
        """
        # List to store top students from all grades
        all_top_students = []

        # Get top students from each grade
        for grade in grades:
            # Get data from current grade
            grade_data = self.fetch_student_rankings(grade)

            # Convert to list of dictionaries and sort by currency
            grade_students = [
                {
                    "name": name,
                    "currency": currency,
                    "grade": grade
                }
                for name, currency in grade_data.items()
            ]
            grade_students.sort(key=itemgetter('currency'), reverse=True)

            # Add top N students from this grade
            all_top_students.extend(grade_students[:top_n_per_grade])

        # Sort all students by currency and get top N overall
        final_top_students = sorted(
            all_top_students,
            key=itemgetter('currency'),
            reverse=True
        )[:final_top_n]

        return final_top_students
