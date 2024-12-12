import json
import os
from functools import lru_cache
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from pocketbase import PocketBase
from supabase import create_client


class DatabaseManager:
    """A class to manage student data across Supabase and PocketBase databases."""

    def __init__(self):
        """Initialize the database connections and load environment variables."""
        # Load environment variables
        load_dotenv()

        # Initialize Supabase
        self.SUPABASE_URL = os.environ["SUPABASE_URL"]
        self.SUPABASE_KEY = os.environ["SUPABASE_KEY"]
        self.supabase = create_client(self.SUPABASE_URL, self.SUPABASE_KEY)

        # Initialize PocketBase
        self.POCKETBASE_URL = os.environ["POCKETBASE_URL"]
        self.POCKETBASE_USERNAME = os.environ["POCKETBASE_USERNAME"]
        self.POCKETBASE_PASSWORD = os.environ["POCKETBASE_PASSWORD"]
        self.pb = PocketBase(self.POCKETBASE_URL)

        # Initialize cache
        self.grade_cache: Dict[str, List[Dict[str, str]]] = {}

        # Authenticate with PocketBase
        self._auth()

    def _auth(self) -> None:
        """Authenticate with PocketBase using admin credentials."""
        try:
            self.pb.admins.auth_with_password(
                self.POCKETBASE_USERNAME, self.POCKETBASE_PASSWORD
            )
        except Exception as e:
            print(f"PocketBase authentication error: {e}")

    def fetch_all_students(self, grade: str) -> List[str]:
        """
        Fetch all student names for a specific grade from Supabase.

        Args:
            grade (str): The grade (table name) to fetch data from.

        Returns:
            List[str]: List of student names.
        """
        try:
            response = self.supabase.table(grade).select("Name").execute()
            if response.data:
                return [student["Name"] for student in response.data]
            print(f"No data found for grade {grade}")
            return []
        except Exception as e:
            print(f"Error fetching all students from {grade}: {e}")
            return []

    def teachers_auth(self, teacher_name: str, db_name: str = "Teacher's Names"):
        """
        Fetch all student names for a specific grade from Supabase.

        Args:
            grade (str): The grade (table name) to fetch data from.

        Returns:
            List[str]: List of student names.
        """
        try:
            response = (
                self.supabase.table(db_name)
                .select("Name")
                .eq("Name", teacher_name)
                .execute()
            )

            if len(response.data) > 0:
                return True
            else:
                return False
                print("No data found for teachers")
        except Exception as e:
            print(f"Error fetching all teachers from {db_name}: {e}")

    @lru_cache()
    def fetch_grade_data(self, grade: str) -> List[Dict[str, Any]]:
        """
        Fetch and cache complete student data for a specific grade.

        Args:
            grade (str): The grade to fetch data for.

        Returns:
            List[Dict[str, Any]]: List of student data dictionaries.
        """
        response = self.supabase.table(grade).select("Name, Currency").execute()
        return response.data

    def check_existence(self, student_name: str, grade: str) -> bool:
        """
        Check if a student exists in the specified grade.

        Args:
            student_name (str): Student name to check.
            grade (str): Grade to search in.

        Returns:
            bool: True if student exists, False otherwise.
        """
        try:
            grade_data = self.fetch_grade_data(grade)
            if grade_data:
                return any(item["Name"] == student_name for item in grade_data)
            print("No data found")
            return False
        except Exception as e:
            print(f"Error checking existence: {e}")
            return False

    def fetch_currency(self, student_name: str, grade: str) -> Optional[int]:
        """
        Fetch the currency value for a student.

        Args:
            student_name (str): Student name.
            grade (str): Grade to search in.

        Returns:
            Optional[int]: Currency value or None if not found.
        """
        try:
            grade_data = self.fetch_grade_data(grade)
            if grade_data:
                for student in grade_data:
                    if student["Name"] == student_name:
                        return int(student["Currency"])
            print("Name Does Not Exist")
            return None
        except Exception as e:
            print(f"Error fetching currency: {e}")
            return None

    def update_score(self, student_name: str, grade: str, new_score: int) -> None:
        """
        Update a student's score.

        Args:
            student_name (str): Student name.
            grade (str): Student's grade.
            new_score (int): New score value.
        """
        try:
            response = (
                self.supabase.table(grade)
                .update({"Currency": new_score})
                .eq("Name", student_name)
                .execute()
            )

            if response.data:
                print(f"Successfully updated score for {student_name} to {new_score}")
                self.clear_grade_cache()  # Clear cache after update
            else:
                print(f"Failed to update score: {response.error} - {response.message}")
        except Exception as e:
            print(f"Error updating score: {e}")

    def upload_comment(
        self,
        student_name: str,
        teacher_name: str,
        points_changed: int,
        comment: str,
        grade: str,
        db_name: str,
    ) -> None:
        """
        Upload a comment to PocketBase.

        Args:
            student_name (str): Student name.
            teacher_name (str): Teacher name.
            points_changed (int): Points changed.
            comment (str): Comment text.
            grade (str): Student's grade.
        """
        try:
            self._auth()  # Ensure authentication is current
            data = {
                "student_name": student_name,
                "teacher_name": teacher_name,
                "points_changed": points_changed,
                "comment": str(comment),
                "grade": grade,
            }
            self.pb.collection(db_name).create(data)
            print("Uploaded comment successfully")
        except Exception as e:
            print(f"Error uploading comment: {e}")

    def fetch_comments(self, grade: str, student_name: str, limit: int = 20) -> str:
        """
        Fetch comments for a student.

        Args:
            student_name (str): Student name.
            limit (int): Maximum number of comments to fetch.

        Returns:
            str: JSON string containing comments data.
        """
        try:
            self._auth()
            result = self.pb.collection(grade).get_full_list(
                batch=limit,
                query_params={
                    "filter": f'student_name = "{student_name}"',
                },
            )

            comments_data = {
                "student_name": student_name,
                "grade": result[0].grade if result else None,
                "comments": [],
            }

            for record in result:
                comment = {
                    "teacher_name": record.teacher_name,
                    "points_changed": record.points_changed,
                    "comment_given": record.comment,
                    "created_at": record.created,
                }
                comments_data["comments"].append(comment)

            return json.dumps(comments_data, default=str, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Error fetching comments: {str(e)}"})

    def fetch_comments_count(self, student_name: str, db_name: str) -> int:
        """
        Fetch the count of comments for a student.

        Args:
            student_name (str): Student name.

        Returns:
            int: Number of comments.
        """
        try:
            self._auth()
            result = self.pb.collection(db_name).get_list(
                1,
                1,
                query_params={
                    "filter": f'student_name = "{student_name}"',
                    "$autoCancel": "false",
                },
            )
            return int(result.total_items)
        except Exception as e:
            print(f"Error fetching comments count: {e}")
            return 0

    def clear_grade_cache(self) -> None:
        """Clear the grade data cache."""
        self.fetch_grade_data.cache_clear()
