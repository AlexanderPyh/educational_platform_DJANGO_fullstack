# Educational Platform

This Django-based educational platform enables course creation, lesson management, and user engagement. Users purchase lessons with tokens, track progress, and submit answers for quizzes and tasks. Admins manage content and grades, with Google Sheets integration for analytics.

## Features

### User Features
- **Course Browsing**: View available courses and their topics (`course_detail_user`).
- **Lesson Access**: Purchase lessons using tokens and access content (`purchase_lesson`, `lesson_content`).
- **Progress Tracking**: Submit answers for quizzes and tasks, with progress updates (`save_answer`, `save_quiz_answer`, `save_task_answer`).
- **Token Management**: Purchase tokens and view transaction history (`purchase_token`, `get_purchase_history`).
- **Personal Dashboard**: Access purchased lessons and track progress (`personal_page`).

### Admin/Editor Features
- **Course Creation**: Create and manage courses with topics and lessons (`create_course`, `save_course_structure`).
- **Content Management**: Add and edit lesson content (text, PDFs, videos, quizzes, tasks) (`save_lesson_content`).
- **Grading**: Evaluate open-ended answers with customizable criteria (`save_grades`).
- **Analytics**: Export data to Google Sheets for analysis (requires configuration).
- **Access Control**: Role-based permissions for editors and superusers (`editor_required`, `user_passes_test`).

## Architecture
- **Framework**: Django with Python 3.8+.
- **Database**: SQLite (default) for storing courses, lessons, user progress, and token transactions.
- **Models**: `Course`, `CourseTopic`, `Lesson`, `LessonContent`, `UserToken`, `PurchasedLesson`, `UserAnswer`, etc.
- **API Endpoints**: RESTful views for saving answers, grades, and managing tokens (`api.py`, `clear_token_history.py`).
- **Frontend**: HTML templates with CSRF protection for secure interactions.
- **Authentication**: Custom user registration and login with email support (`auth.py`).

## Setup Instructions

### Prerequisites
- Python 3.8+
- Django 4.x
- SQLite (default) or other supported database
- Google Cloud Service Account credentials for Sheets API (optional)

### Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd educational-platform
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Example `requirements.txt`:
   ```
   django==4.2
   python-dotenv==1.0.0
   google-auth==2.23.0
   google-auth-oauthlib==1.0.0
   google-api-python-client==2.100.0
   ```

3. **Configure Environment**:
   Create a `.env` file in the project root:
   ```
   SECRET_KEY=<your-django-secret-key>
   GOOGLE_CREDENTIALS_JSON=<path-to-google-credentials.json>
   GSHEET_ANALYTICS_ID=<google-sheets-id>
   ```

4. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Set Up Google Sheets** (Optional):
   - Create a Google Sheet and share it with the service account email from your Google Cloud credentials.
   - Update `GSHEET_ANALYTICS_ID` in `.env`.

6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

## Usage
- **Users**: Register (`register_view`), purchase tokens (`purchase_token`), buy lessons (`purchase_lesson`), and submit answers (`save_quiz_answer`, `save_task_answer`).
- **Editors**: Create courses (`create_course`) and manage content (`save_lesson_content`).
- **Admins**: Approve/delete courses (`delete_course`) and grade answers (`save_grades`).

## Database Schema
- **Course**: Stores course details.
- **CourseTopic**: Organizes lessons under topics.
- **Lesson**: Contains lesson metadata and pricing.
- **LessonContent**: Stores content blocks (text, PDFs, videos, quizzes, tasks).
- **UserToken**: Tracks user token balances.
- **PurchasedLesson**: Records purchased lessons.
- **UserAnswer**: Stores user responses and quiz results.
- **OpenQuestionAnswer**: Stores open-ended answers and grades.

## Security
- CSRF protection on all POST requests (`csrf_exempt` where needed).
- Role-based access with `@login_required`, `@editor_required`, and `@user_passes_test`.
- Secure file uploads for PDFs and images (`upload_pdf`, `upload_task_image`).

## Notes
- Ensure Google Sheets credentials have the `https://www.googleapis.com/auth/spreadsheets` scope.
- The platform assumes a single currency for tokens; extend models for multi-currency if needed.
- Templates (`accounts/*.html`) require customization for styling and branding.

## License
Proprietary. Unauthorized distribution or modification is prohibited.