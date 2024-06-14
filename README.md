"# Social-Media-API"

Introduction
The Social Media API is designed to provide a RESTful interface for a social media platform. It allows users to create profiles, follow other users, create and retrieve posts, manage likes and comments, and perform other basic social media actions.

Features
User Registration and Authentication
Profile Management
Follow/Unfollow Users
Post Creation and Retrieval
Likes and Comments
Scheduled Post Creation (using Celery)
Installation
Prerequisites
Python 3.8 or higher
Virtualenv (optional but recommended)
Steps
1. Clone the repository: git clone https://github.com/stamaksim/Social-Media-API.git
cd social_media_api
2. Create and activate a virtual environment: python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install the dependencies: pip install -r requirements.txt
4. Apply the migrations: python manage.py migrate
5. Create a superuser: python manage.py createsuperuser
6. Start the development server: python manage.py runserver

Configuration
Environment Variables
Create a .env file in the root directory to configure the following settings:
1. SECRET_KEY=your_secret_key
2. DEBUG=True
3. ALLOWED_HOSTS=localhost,127.0.0.1
4. DATABASE_URL=sqlite:///db.sqlite3  # Or configure your preferred database

Celery Configuration (Optional)
If you want to use Celery for scheduled post creation, configure it in your settings.py:

# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

And start the Celery worker:
celery -A social_media_api worker --loglevel=info
On Windows, install gevent and use the following command:
celery -A social_media_api worker --loglevel=INFO -P gevent


API Endpoints
User Registration and Authentication
1. User Registration
Endpoint: /api/register/
Method: POST
Description: Register a new user with email and password.
2. User Login (Token Obtain)
Endpoint: api/users/token/
Method: POST
Description: Login with credentials to receive an authentication token.
3. Token Refresh
Endpoint: api/users/token/refresh/
Method: POST
Description: Refresh the authentication token.
4. Token Verify
Endpoint: api/users/token/verify/
Method: POST
Description: Verify the authentication token.
5. User Logout
Endpoint: api/users/logout/
Method: POST
Description: Logout and invalidate the authentication token.
User Profile
6. Create/Update Profile
Endpoint: api/users/me/
Method: POST/PUT
Description: Create or update user profile.
7. Retrieve Profile
Endpoint: api/users/users/<str:email>/
Method: GET
Description: Retrieve a user's profile by email.
8. Search Users
Endpoint: api/users/profiles/
Method: GET
Description: Search for users by email or other criteria.
Follow/Unfollow
9. Follow/Unfollow User
Endpoint: api/users/follow-unfollow/
Method: POST
Description: Follow or unfollow a user.
10. List Followers/Following
Endpoint: api/users/followers/
Method: GET
Description: View the list of users following the specified user.

Post Creation and Retrieval
1. Create Post
Endpoint: api/social-api/posts/
Method: POST
Description: Create a new post with text content and optional media attachments.
2. Retrieve Posts
Endpoint: api/social-api/posts/
Method: GET
Description: Retrieve all posts.
3. Retrieve Post by ID
Endpoint: api/social-api/posts/<int:pk>/
Method: GET
Description: Retrieve a post by its ID.
4. Likes and Comments 
Like/Unlike Post
Endpoint: api/social-api/posts/<int:pk>/like/
Method: POST
Description: Like or unlike a post.
5. List Liked Posts
Endpoint: api/social-api/liked-posts/
Method: GET
Description: View the list of posts the user has liked.
6. Add Comment
Endpoint: api/social-api/comments/
Method: POST
Description: Add a comment to a post.
7. Retrieve Comment
Endpoint: api/social-api/comments/<int:pk>/
Method: GET
Description: Retrieve a comment by its ID.
8. Schedule Post Creation using Celery 
Schedule Post
Endpoint: api/social-api/posts/schedule_post_creation/
Method: POST
Description: Schedule a post to be created at a specified time.