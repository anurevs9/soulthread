# SoulThread README

## Introduction

SoulThread is a social networking platform designed to help users connect with friends, share moments, and engage in meaningful conversations. With an intuitive interface and robust features, SoulThread offers a seamless experience for all users.

## Key Features

1.  **User Authentication:**
    Users can easily sign up or log in to their accounts using email/password credentials.

    **Login Page**
    - https://saideepu99.pythonanywhere.com/login/
    

2.  **User Registration:**
    New users can create an account by providing basic information such as first name, last name, email, phone number, and password. The registration process is simple and user-friendly.

    **Sign Up Page**
    - https://saideepu99.pythonanywhere.com/register/
    

3.  **Friends Page:**
    Users can connect with other users by sending and accepting friend requests. They can manage their friend list, view their friends' profiles, and see updates from their friends in their feeds.

    **Friends Page**
    - https://saideepu99.pythonanywhere.com/friends/
   

4.  **Feeds and Posts:**
    The main feed allows users to view posts from the people they follow. Users can create their own posts, upload images, and attach files. Each post includes options to like, comment, and share.

    **Feeds Page**
    - https://saideepu99.pythonanywhere.com/
   

5.  **Forums and Discussions:**
    SoulThread provides a forum section where users can participate in discussions on various topics. Users can create new threads, reply to existing ones, and engage in community-driven conversations.

    **Forums Page**
    - https://saideepu99.pythonanywhere.com/forums/
    

6.  **Settings:**
    Users can manage their account settings, including updating their profile information, changing passwords, managing privacy settings, and customizing notification preferences.

    **Settings Page**
    - https://saideepu99.pythonanywhere.com/settings/
    


## Getting Started

### Prerequisites

*   Python 3.10
*   Django 5.1.5
*   Other dependencies listed in `requirements.txt`

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/anurevs9/soulthread.git
    cd soulthread
    ```

2.  **Create a virtual environment and install the required packages:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate      # On Windows
    pip install -r requirements.txt
    ```

3.  **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

4.  **Create a superuser (optional):**

    ```bash
    python manage.py createsuperuser
    ```

5.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

6.  **Open your browser and navigate to** `https://saideepu99.pythonanywhere.com/` to access SoulThread.

## Contributing

We welcome contributions from the community! If you'd like to contribute, please follow these steps:

1.  **Fork** the repository.
2.  **Create** a new branch for your feature or bug fix.
3.  **Make** your changes and commit them with descriptive commit messages.
4.  **Push** your changes to your forked repository.
5.  **Submit** a pull request detailing your changes.



## Contact

If you have any questions, suggestions, or issues, feel free to contact us at [support@soulthread.com](mailto:support@soulthread.com).

Thank you for choosing SoulThread! We hope you enjoy connecting and sharing moments with your friends.
