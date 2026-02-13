# Blogicum – Social Blogging Platform

Blogicum is a fully-featured social blogging platform where users can create personal pages, publish posts, attach images, categorize their content, and interact through comments. The project is built with Django and incorporates user authentication, post management, comment system, custom error pages, pagination, and a file-based email backend for development.

---

## Features

### User Management
- Registration, login, logout, and password change (using Django’s built-in authentication).
- User profile page at `/profile/<username>/`:
  - Public information about the user.
  - Paginated list of user’s posts.
  - Links to edit profile and change password (only for the profile owner).
- Profile editing (first name, last name, username, email).

### Posts
- Create a new post: `/posts/create/` (authenticated users only).
- Edit a post: `/posts/<post_id>/edit/` (author only).
- Delete a post: `/posts/<post_id>/delete/` (author only, with confirmation page).
- Upload an image for each post.
- Scheduled (future) posts: visible to everyone only after the publication date; author sees them immediately.
- Categories and locations are managed only through the admin panel.

### Comments
- Add a comment: `/posts/<post_id>/comment/` (authenticated users only).
- Edit a comment: `/posts/<post_id>/edit_comment/<comment_id>/` (author only).
- Delete a comment: `/posts/<post_id>/delete_comment/<comment_id>/` (author only, with confirmation).
- Comments are displayed from oldest to newest.
- Comment count is shown on the homepage, profile page, and category page.

### Categories
- Category page: `/category/<slug:category_slug>/`.
- If a category is unpublished → 404.
- Only published posts belonging to that category are shown.

### Static Pages
- `/pages/about/` – About the project.
- `/pages/rules/` – Rules.
- Implemented with `TemplateView`.

### Custom Error Pages
- Custom 404, 403 CSRF, and 500 error pages (templates in `templates/pages/`).

### Pagination
- 10 posts per page on the homepage, profile page, and category page.

### Admin Panel
- Manage posts, categories, and locations.
- Russian localization with clear field labels and help texts.

### Email Backend (Development)
- File-based email backend: all emails are saved to `sent_emails/` directory (excluded from Git).

---

## Tech Stack

- Python 3.10
- Django 3.2.16
- SQLite3 (default database)
- Pytest (testing)
- Git / GitHub

---

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone git@github.com:AxineBro/Blogikum.git
   cd Blogikum
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Navigate to the project directory and apply migrations**
   ```bash
   cd blogicum
   python manage.py migrate
   ```

5. **Create a superuser (to access the admin panel)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser and visit**  
   - Homepage: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
   - Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Testing

The project includes a comprehensive test suite using pytest. To run the tests, execute the following command from the project root (where `pytest.ini` is located):

```bash
pytest
```

---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
