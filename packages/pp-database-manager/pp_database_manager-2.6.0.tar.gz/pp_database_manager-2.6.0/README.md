# This is an package for an Private Project For an School

---

## Database Manager Package (`pp-database-manager`)

The `database_manager` package is a custom Python library designed to streamline database interactions for the Pristine Pathway project. It provides a unified interface for working with both Supabase and Pocketbase, the two database systems used across the Teacher's Panel, Student's Panel, and Leaderboard applications.

**Key Features:**

*   **Abstraction:** Simplifies database operations by providing easy-to-use methods for common tasks like fetching, updating, and inserting data.
*   **Centralized Logic:** Encapsulates all database-related code in a single package, promoting consistency and maintainability.
*   **Dual Database Support:** Seamlessly handles interactions with both Supabase (for core data and real-time features) and Pocketbase (for handling potentially larger datasets).
*   **Authentication:** Manages authentication with both Supabase and Pocketbase.
*   **Caching:** Implements caching for frequently accessed data (like grade data) to improve performance.
*   **Error Handling:** Includes robust error handling to gracefully manage database connection issues and other potential problems.
*   **Published on PyPI:** Available as a reusable package on the Python Package Index (PyPI) named `pp-database-manager`, making it easy to install and use across different projects.
