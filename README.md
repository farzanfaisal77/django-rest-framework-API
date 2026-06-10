# 🚀 Django REST Framework Blog API

A robust, production-ready RESTful Blog API built using **Django** and **Django REST Framework (DRF)**. The project features full token-based user authentication, fine-grained access control permissions, automated API documentation (Swagger & Redoc), custom user models, and CORS support.

---

## 🛠️ Tech Stack & Key Libraries

This API leverages a modern Django ecosystem to handle authentication, documentation, and security:

*   **[Django REST Framework (DRF)](https://www.django-rest-framework.org/)** (v3.17.1): Used for building the API endpoints, serializing models (`serializers.ModelSerializer`), handling request routing (`SimpleRouter`), and implementing views (`ModelViewSet`).
*   **[dj-rest-auth](https://dj-rest-auth.readthedocs.io/)** (v7.2.0): Provides REST API endpoints for user authentication lifecycle (login, logout, password reset, password change, user profile details).
*   **[django-allauth](https://docs.allauth.org/)** (v65.18.0): Powers the user registration and verification engine under the hood for `dj-rest-auth`.
*   **[drf-spectacular](https://drf-spectacular.readthedocs.io/)** (v0.29.0): Automatically generates OpenAPI 3.0 schemas and serves interactive UI documentation.
*   **[django-cors-headers](https://github.com/adamchainz/django-cors-headers)** (v4.9.0): Middleware to handle Cross-Origin Resource Sharing (CORS), allowing communication from separate frontend applications.
*   **[environs](https://github.com/sloria/environs)** (v15.0.1): Simplifies environment variable parsing and configuration management for settings.
*   **[whitenoise](https://whitenoise.readthedocs.io/)** (v6.12.0): Serves static files directly from the WSGI/ASGI application.

---

## 🔒 Authentication & CORS Configuration

### 1. Authentication Mechanisms
The API is configured in `settings.py` with two default authentication backends under the `DEFAULT_AUTHENTICATION_CLASSES` setting:
*   **`TokenAuthentication`**: Uses HTTP Header `Authorization: Token <token_key>` for stateless API access (e.g., mobile apps, SPA frontends). Tokens are generated and managed by `dj-rest-auth`.
*   **`SessionAuthentication`**: Uses Django's default session-based authentication. Excellent for testing endpoints directly in the **DRF Browsable API** interface.

By default, all endpoints (except registration/login/password reset) require authentication as defined in the global settings:
```python
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  
    ],
    ...
}
```

### 2. CORS & CSRF Configuration
To allow a separate frontend (e.g., React on port 3000) to communicate with this backend, the application integrates `django-cors-headers`:
*   **Middleware**: `corsheaders.middleware.CorsMiddleware` is loaded before standard Django common middleware.
*   **CORS Whitelist**:
    ```python
    CORS_ORIGIN_WHITELIST = (
        "http://localhost:8000",
        "http://localhost:3000",
    )
    ```
*   **CSRF Trusted Origins**: `CSRF_TRUSTED_ORIGINS = ["http://localhost/8000"]` (configured to trust local reverse proxy / server routes).

---

## 🛣️ API Endpoints & Permissions Matrix

The routing is implemented using DRF's `SimpleRouter` for the `posts` and `users` resources, combined with standard URL paths for auth and docs.

### Global Permission Definitions:
*   **Authenticated User**: A user that has successfully logged in and is presenting a valid Session Cookie or Auth Token.
*   **Superuser (Admin)**: A user with `is_superuser = True` (and typically `is_staff = True`).
*   **Anonymous**: An unauthenticated guest client.

| Route Path | HTTP Method | View / ViewSet | Description | Normal (Authenticated) User | Superuser (Admin) | Library Used |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| **`api/v1/`** | `GET` | `PostViewSet` | List all blog posts | ✅ **Allowed** | ✅ **Allowed** | DRF (`ModelViewSet`) |
| | `POST` | `PostViewSet` | Create a new blog post | ✅ **Allowed** | ✅ **Allowed** | DRF (`ModelViewSet`) |
| **`api/v1/<id>/`** | `GET` | `PostViewSet` | Retrieve a single post | ✅ **Allowed** | ✅ **Allowed** | DRF (`ModelViewSet`) |
| | `PUT` / `PATCH` | `PostViewSet` | Update a post | 🔐 **Only if Author of post** | 🔐 **Only if Author of post** | DRF (`ModelViewSet`) |
| | `DELETE` | `PostViewSet` | Delete a post | 🔐 **Only if Author of post** | 🔐 **Only if Author of post** | DRF (`ModelViewSet`) |
| **`api/v1/users/`** | `GET` | `UserViewSet` | List all custom users | ❌ **403 Forbidden** | ✅ **Allowed** | DRF (`ModelViewSet`) |
| | `POST` | `UserViewSet` | Create a custom user | ❌ **403 Forbidden** | ✅ **Allowed** | DRF (`ModelViewSet`) |
| **`api/v1/users/<id>/`** | `GET` | `UserViewSet` | Retrieve user details | ❌ **403 Forbidden** | ✅ **Allowed** | DRF (`ModelViewSet`) |
| | `PUT` / `PATCH` | `UserViewSet` | Update user details | ❌ **403 Forbidden** | ✅ **Allowed** | DRF (`ModelViewSet`) |
| | `DELETE` | `UserViewSet` | Delete user | ❌ **403 Forbidden** | ✅ **Allowed** | DRF (`ModelViewSet`) |
| **`api/v1/dj-rest-auth/registration/`** | `POST` | `RegisterView` | Register a new account | ✅ **Allowed (Anonymous)** | ✅ **Allowed** | `dj-rest-auth` & `allauth` |
| **`api/v1/dj-rest-auth/login/`** | `POST` | `LoginView` | Log in and get Token | ✅ **Allowed (Anonymous)** | ✅ **Allowed** | `dj-rest-auth` |
| **`api/v1/dj-rest-auth/logout/`** | `POST` | `LogoutView` | Log out / Invalidate Token | ✅ **Allowed** | ✅ **Allowed** | `dj-rest-auth` |
| **`api/v1/dj-rest-auth/user/`** | `GET` | `UserDetailsView` | Retrieve current user profile | ✅ **Allowed** | ✅ **Allowed** | `dj-rest-auth` |
| | `PUT` / `PATCH` | `UserDetailsView` | Update current user profile | ✅ **Allowed** | ✅ **Allowed** | `dj-rest-auth` |
| **`api/v1/dj-rest-auth/password/change/`** | `POST` | `PasswordChangeView` | Change password | ✅ **Allowed** | ✅ **Allowed** | `dj-rest-auth` |
| **`api/v1/dj-rest-auth/password/reset/`** | `POST` | `PasswordResetView` | Request password reset link | ✅ **Allowed (Anonymous)** | ✅ **Allowed** | `dj-rest-auth` |
| **`api/v1/dj-rest-auth/password/reset/confirm/`** | `POST` | `PasswordResetConfirmView` | Confirm password reset | ✅ **Allowed (Anonymous)** | ✅ **Allowed** | `dj-rest-auth` |
| **`api/schema/`** | `GET` | `SpectacularAPIView` | Retrieve OpenAPI 3 Schema | ✅ **Allowed** | ✅ **Allowed** | `drf-spectacular` |
| **`api/schema/swagger-ui/`** | `GET` | `SpectacularSwaggerView` | Interactive Swagger UI docs | ✅ **Allowed** | ✅ **Allowed** | `drf-spectacular` |
| **`api/schema/redoc/`** | `GET` | `SpectacularRedocView` | Interactive Redoc UI docs | ✅ **Allowed** | ✅ **Allowed** | `drf-spectacular` |
| **`api-auth/login/`** | `GET` / `POST` | DRF Auth View | Browsable API login screen | ✅ **Allowed (Anonymous)** | ✅ **Allowed** | DRF Core |
| **`api-auth/logout/`** | `GET` | DRF Auth View | Browsable API logout screen | ✅ **Allowed** | ✅ **Allowed** | DRF Core |
| **`admin/`** | `GET` / `POST` | Django Admin | System administration page | ❌ **403 Forbidden** | ✅ **Allowed** | Django Core |

> [!NOTE]  
> The custom permission class `IsAuthorOrReadOnly` protects post modifications. Note that **only the actual author of the post** can execute `PUT`, `PATCH`, or `DELETE` requests on a post endpoint. Even a Superuser is blocked from updating/deleting another user's post via this API endpoint unless they are designated as its author.

---

## 🏗️ Architectural Components: Views, Viewsets & Routers

### 📦 1. Routers
The application avoids mapping individual URLs manually. In `posts/urls.py`, a `SimpleRouter` dynamically hooks viewsets to standard REST conventions:
```python
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, PostViewSet

router = SimpleRouter()
router.register("users", UserViewSet, basename="users")
router.register("", PostViewSet, basename="posts")

urlpatterns = router.urls
```
*   `posts/` points directly to `api/v1/` routes.
*   `users/` points to `api/v1/users/` routes.

### 🎛️ 2. Viewsets & Custom Permissions
In `posts/views.py`, viewsets bundle list, retrieve, create, update, and delete actions together:

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Post
from .serializers import PostSerializer, UserSerializer
from .permissions import IsAuthorOrReadOnly
from django.contrib.auth import get_user_model

# Standard ModelViewSet for CRUD operations on blog posts
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
# Standard ModelViewSet for CRUD operations on User accounts (Admin-only)
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
```

The custom `IsAuthorOrReadOnly` permission is defined in `posts/permissions.py`:
```python
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow requests only if user is authenticated
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Read-only actions (GET, HEAD, OPTIONS) are allowed for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write actions (PUT, PATCH, DELETE) require the user to be the author
        return obj.author == request.user
```

---

## 👥 Custom User Model

The default Django User model is swapped for a custom user model configured in `accounts/models.py`:
```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    name = models.CharField(null=True, blank=True, max_length=100)
```
This enables flexible extension of user attributes in the future without database schema migration complications.

---

## ⚙️ Quick Start & Setup

### 1. Requirements
Ensure Python 3.10+ and `virtualenv` are installed.

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

### 3. Installation
1.  **Clone & Navigate**:
    ```bash
    git clone <repository-url>
    cd django-rest-framework-API
    ```
2.  **Create Virtual Environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```
5.  **Create Superuser**:
    ```bash
    python createsuperuser.py
    ```
6.  **Run Development Server**:
    ```bash
    python manage.py runserver
    ```
    Access the API at: `http://127.0.0.1:8000/api/v1/`

---

## 📖 Interactive Documentation
Once the server is running, you can explore, test, and document all the routes using the built-in Swagger or Redoc interfaces:
*   **Swagger UI**: [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
*   **Redoc**: [http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/)
*   **Raw OpenAPI Schema**: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)