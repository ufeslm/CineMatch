# Movie Recommendation System

A Flask-based web application that provides personalized movie recommendations using the TMDB API. The application implements several design patterns to create a flexible and maintainable system.

## Features

- User authentication (login/register)
- Movie search functionality
- Personalized movie recommendations
- Favorite movies management
- Watch later list
- Email notifications for new recommendations
- Responsive design with Bootstrap

## Technologies Used

- **Backend**:
  - Python 3.x
  - Flask (Web Framework)
  - SQLAlchemy (ORM)
  - Flask-Login (Authentication)
  - Flask-Mail (Email Notifications)
  - Requests (API Calls)

- **Frontend**:
  - HTML5
  - CSS3
  - Bootstrap 5
  - Font Awesome (Icons)

- **Database**:
  - SQLite

- **External APIs**:
  - The Movie Database (TMDB) API

## Design Patterns Implementation

### 1. Strategy Pattern
Location: `app/recommendation_strategy.py`
- Used to switch between different recommendation algorithms
- Implemented through `RecommendationStrategy` abstract class
- Concrete strategies:
  - `CollaborativeFiltering`
  - `ContentBasedFiltering`
  - `HybridRecommendation`
- Allows easy addition of new recommendation algorithms

### 2. Observer Pattern
Location: `app/observer.py`
- Used for notification system
- Components:
  - `MovieSubject`: Manages observers and notifications
  - `MovieObserver`: Abstract observer class
  - `EmailNotification`: Sends email notifications
  - `RecommendationUpdate`: Handles recommendation updates
- Enables decoupled notification system

### 3. Decorator Pattern
Location: `app/filter_decorator.py`
- Used to add filtering capabilities to recommendations
- Components:
  - `FilteredRecommendation`: Base decorator
  - Concrete filters:
    - `RatingFilter`: Filters by minimum rating
    - `YearFilter`: Filters by release year
    - `GenreFilter`: Filters by genre
- Allows dynamic addition of filters

### 4. Command Pattern
Location: `app/command.py`
- Used for movie-related actions
- Components:
  - `Command`: Abstract command class
  - Concrete commands:
    - `AddFavoriteCommand`
    - `RemoveFavoriteCommand`
    - `AddWatchLaterCommand`
    - `RemoveWatchLaterCommand`
- Encapsulates actions as objects

### 5. State Pattern
Location: `app/state.py`
- Used to manage recommendation process states
- Components:
  - `RecommendationState`: Abstract state class
  - Concrete states:
    - `InitialState`
    - `ProcessingState`
    - `ReadyState`
  - `RecommendationContext`: Manages state transitions
- Handles different states of the recommendation process

## How It Works

1. **User Authentication**:
   - Users register with username and email
   - Login system using Flask-Login
   - Session management for authenticated users

2. **Movie Search**:
   - Search bar available in navigation
   - Real-time search using TMDB API
   - Results displayed with movie details and posters

3. **Recommendations System**:
   - Based on user's favorite movies
   - Uses hybrid recommendation strategy
   - Applies filters (rating, year)
   - Removes duplicates
   - Limits to top 20 recommendations

4. **Favorite Movies**:
   - Users can add/remove movies to favorites
   - Favorites influence recommendations
   - Stored in database for persistence

5. **Watch Later List**:
   - Available in recommendations section
   - Helps users track movies to watch
   - Separate from favorites

6. **Notifications**:
   - Email notifications for new recommendations
   - Uses observer pattern for decoupled notifications
   - Configurable through Flask-Mail

## Setup Instructions

1. **Prerequisites**:
   ```bash
   pip install flask flask-sqlalchemy flask-login flask-mail requests python-dotenv
   ```

2. **Configuration**:
   - Create a `.env` file with:
     ```
     TMDB_API_KEY=your_tmdb_api_key
     SECRET_KEY=your_secret_key
     MAIL_USERNAME=your_email
     MAIL_PASSWORD=your_app_password
     ```

3. **Database Setup**:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. **Run the Application**:
   ```bash
   flask run
   ```

## Usage Guide

1. **Registration**:
   - Click "Register" in the navigation bar
   - Fill in username, email, and password
   - Login with your credentials

2. **Searching Movies**:
   - Use the search bar in the navigation
   - View movie details
   - Add movies to favorites

3. **Getting Recommendations**:
   - Add movies to your favorites
   - Visit the Recommendations page
   - View personalized recommendations
   - Add interesting movies to watch later

4. **Managing Lists**:
   - View your favorites in the Favorites section
   - View your watch later list
   - Remove movies from either list

## Project Structure

```
movie-recommendation/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── main.py
│   │   └── auth.py
│   ├── recommendation_strategy.py
│   ├── observer.py
│   ├── filter_decorator.py
│   ├── command.py
│   └── state.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── search.html
│   ├── movie_details.html
│   ├── recommendations.html
│   ├── favorites.html
│   └── watch_later.html
├── config.py
├── requirements.txt
└── README.md
```

## Future Improvements

1. Add user preferences for recommendation filters
2. Implement social features (sharing recommendations)
3. Add movie reviews and ratings
4. Implement more sophisticated recommendation algorithms
5. Add movie streaming service integration
6. Implement user profile customization
7. Add movie genres preferences
8. Implement recommendation history

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License. 