from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models import FavoriteMovie, WatchLater
from app import db
from app.recommendation_strategy import CollaborativeFiltering, ContentBasedFiltering, HybridRecommendation
from app.filter_decorator import FilteredRecommendation, GenreFilter, RatingFilter, YearFilter
from app.state import RecommendationContext
from app.observer import MovieSubject, EmailNotification, RecommendationUpdate
import requests
import os

bp = Blueprint('main', __name__)

# Use TMDB API key from config
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

@bp.route('/')
def home():
    # Get featured movies from TMDB
    featured_movies = []
    try:
        response = requests.get(
            f'{TMDB_BASE_URL}/movie/popular',
            params={
                'api_key': current_app.config['TMDB_API_KEY'],
                'language': 'en-US',
                'page': 1
            }
        )
        if response.status_code == 200:
            featured_movies = response.json().get('results', [])[:6]  # Get top 6 popular movies
    except Exception as e:
        print(f"Error fetching featured movies: {str(e)}")
        flash('Error fetching featured movies', 'error')
    
    # Get user's favorites and watch later lists if authenticated
    favorites = []
    watch_later = []
    if current_user.is_authenticated:
        favorites = FavoriteMovie.query.filter_by(user_id=current_user.id).all()
        watch_later = WatchLater.query.filter_by(user_id=current_user.id).all()
    
    return render_template('home.html', 
                          featured_movies=featured_movies,
                          favorites=favorites,
                          watch_later=watch_later)

@bp.route('/search')
@login_required
def search():
    query = request.args.get('query', '')
    movies = []
    
    if query:
        try:
            response = requests.get(
                f'{TMDB_BASE_URL}/search/movie',
                params={
                    'api_key': current_app.config['TMDB_API_KEY'],
                    'query': query,
                    'language': 'en-US'
                }
            )
            if response.status_code == 200:
                movies = response.json().get('results', [])
        except Exception as e:
            print(f"Error searching for movies: {str(e)}")
            flash('Error searching for movies', 'error')
    
    return render_template('search.html', movies=movies, query=query)

@bp.route('/recommendations')
@login_required
def recommendations():
    # Get user's favorite movies
    favorites = FavoriteMovie.query.filter_by(user_id=current_user.id).all()
    
    print(f"Found {len(favorites)} favorite movies for user {current_user.username}")
    
    if not favorites:
        flash('Add some favorite movies to get recommendations!')
        return redirect(url_for('main.search'))
    
    # Initialize state context
    state_context = RecommendationContext()
    state_context.request()  # Initial -> Processing
    
    # Create subject for notifications
    subject = MovieSubject()
    
    # Add observers
    email_observer = EmailNotification(current_user.email)
    recommendation_observer = RecommendationUpdate()
    subject.attach(email_observer)
    subject.attach(recommendation_observer)
    
    # Get recommendations using strategy pattern
    strategy = HybridRecommendation()  # Can be changed to CollaborativeFiltering or ContentBasedFiltering
    
    # Get recommendations for each favorite movie
    recommended_movies = []
    for favorite in favorites:
        try:
            print(f"Fetching recommendations for movie: {favorite.title} (ID: {favorite.movie_id})")
            response = requests.get(
                f'{TMDB_BASE_URL}/movie/{favorite.movie_id}/recommendations',
                params={
                    'api_key': current_app.config['TMDB_API_KEY'],
                    'language': 'en-US',
                    'page': 1  # Get first page of recommendations
                }
            )
            if response.status_code == 200:
                movies = response.json().get('results', [])
                recommended_movies.extend(movies)
                print(f"Found {len(movies)} recommendations for movie {favorite.title}")
            else:
                print(f"Error getting recommendations for movie {favorite.title}: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Exception getting recommendations for movie {favorite.title}: {str(e)}")
    
    print(f"Total recommendations before filtering: {len(recommended_movies)}")
    
    # Remove duplicates based on movie ID
    seen = set()
    unique_movies = []
    for movie in recommended_movies:
        if movie['id'] not in seen:
            seen.add(movie['id'])
            unique_movies.append(movie)
    
    print(f"Unique recommendations after removing duplicates: {len(unique_movies)}")
    
    # Apply filters using decorator pattern
    filtered_recommendation = FilteredRecommendation(unique_movies)
    
    # Add filters based on user preferences - LESS RESTRICTIVE FILTERS
    filtered_recommendation.add_filter(RatingFilter(5.5))  # Lower minimum rating from 6.0 to 5.5
    
    # Get filtered recommendations
    final_recommendations = filtered_recommendation.get_filtered_recommendations()
    
    print(f"Final recommendations after filtering: {len(final_recommendations)}")
    
    # If no recommendations after filtering, try without filters
    if not final_recommendations:
        print("No recommendations after filtering, trying without filters")
        final_recommendations = unique_movies
    
    # Limit to top 20 recommendations by rating
    final_recommendations = sorted(final_recommendations, key=lambda x: x.get('vote_average', 0), reverse=True)[:20]
    
    state_context.request()  # Processing -> Ready
    
    # Notify observers about new recommendations
    subject.notify(f"New recommendations available! Check out {len(final_recommendations)} movies we think you'll love.")
    
    return render_template('recommendations.html', movies=final_recommendations)

@bp.route('/add_favorite', methods=['POST'])
@login_required
def add_favorite():
    movie_id = request.form.get('movie_id')
    title = request.form.get('title')
    rating = request.form.get('rating', 0.0)
    query = request.form.get('query', '')  # Get the current search query
    source_page = request.form.get('source_page', 'search')  # Get the source page
    
    if not movie_id or not title:
        flash('Missing movie information', 'error')
        return redirect(url_for('main.search'))
    
    # Check if movie is already in favorites
    existing_favorite = FavoriteMovie.query.filter_by(
        user_id=current_user.id,
        movie_id=movie_id
    ).first()
    
    if existing_favorite:
        flash(f'{title} is already in your favorites!', 'info')
        if source_page == 'recommendations':
            return redirect(url_for('main.recommendations'))
        elif source_page == 'movie_details':
            return redirect(url_for('main.movie_details', movie_id=movie_id))
        elif source_page == 'home':
            return redirect(url_for('main.home'))
        else:
            return redirect(url_for('main.search', query=query))
    
    favorite = FavoriteMovie(
        user_id=current_user.id,
        movie_id=movie_id,
        title=title,
        rating=float(rating)
    )
    
    db.session.add(favorite)
    db.session.commit()
    
    flash(f'Successfully added {title} to your favorites!', 'success')
    
    # Redirect based on source page
    if source_page == 'recommendations':
        return redirect(url_for('main.recommendations'))
    elif source_page == 'movie_details':
        return redirect(url_for('main.movie_details', movie_id=movie_id))
    elif source_page == 'home':
        return redirect(url_for('main.home'))
    else:
        return redirect(url_for('main.search', query=query))

@bp.route('/remove_favorite/<int:movie_id>', methods=['POST'])
@login_required
def remove_favorite(movie_id):
    movie = FavoriteMovie.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if movie:
        db.session.delete(movie)
        db.session.commit()
        flash(f'Removed {movie.title} from your favorites!', 'success')
    return redirect(url_for('main.favorites'))

@bp.route('/favorites')
@login_required
def favorites():
    favorites = FavoriteMovie.query.filter_by(user_id=current_user.id).all()
    
    # Fetch poster paths for each favorite movie
    for favorite in favorites:
        try:
            response = requests.get(
                f'{TMDB_BASE_URL}/movie/{favorite.movie_id}',
                params={
                    'api_key': current_app.config['TMDB_API_KEY'],
                    'language': 'en-US'
                }
            )
            if response.status_code == 200:
                movie_data = response.json()
                favorite.poster_path = movie_data.get('poster_path')
        except Exception as e:
            print(f"Error fetching poster for movie {favorite.title}: {str(e)}")
            favorite.poster_path = None
    
    return render_template('favorites.html', favorites=favorites)

@bp.route('/add_watch_later', methods=['POST'])
@login_required
def add_watch_later():
    movie_id = request.form.get('movie_id')
    title = request.form.get('title')
    query = request.form.get('query', '')  # Get the current search query
    source_page = request.form.get('source_page', 'search')  # Get the source page
    
    if not movie_id or not title:
        flash('Missing movie information', 'error')
        return redirect(url_for('main.search'))
    
    # Check if movie is already in watch later
    existing_watch_later = WatchLater.query.filter_by(
        user_id=current_user.id,
        movie_id=movie_id
    ).first()
    
    if existing_watch_later:
        flash(f'{title} is already in your watch later list!', 'info')
        if source_page == 'recommendations':
            return redirect(url_for('main.recommendations'))
        elif source_page == 'movie_details':
            return redirect(url_for('main.movie_details', movie_id=movie_id))
        elif source_page == 'home':
            return redirect(url_for('main.home'))
        else:
            return redirect(url_for('main.search', query=query))
    
    watch_later = WatchLater(
        user_id=current_user.id,
        movie_id=movie_id,
        title=title
    )
    
    db.session.add(watch_later)
    db.session.commit()
    
    flash(f'Successfully added {title} to your watch later list!', 'success')
    
    # Redirect based on source page
    if source_page == 'recommendations':
        return redirect(url_for('main.recommendations'))
    elif source_page == 'movie_details':
        return redirect(url_for('main.movie_details', movie_id=movie_id))
    elif source_page == 'home':
        return redirect(url_for('main.home'))
    else:
        return redirect(url_for('main.search', query=query))

@bp.route('/watch_later')
@login_required
def watch_later():
    movies = WatchLater.query.filter_by(user_id=current_user.id).order_by(WatchLater.added_date.desc()).all()
    
    # Fetch poster paths for each watch later movie
    for movie in movies:
        try:
            response = requests.get(
                f'{TMDB_BASE_URL}/movie/{movie.movie_id}',
                params={
                    'api_key': current_app.config['TMDB_API_KEY'],
                    'language': 'en-US'
                }
            )
            if response.status_code == 200:
                movie_data = response.json()
                movie.poster_path = movie_data.get('poster_path')
        except Exception as e:
            print(f"Error fetching poster for movie {movie.title}: {str(e)}")
            movie.poster_path = None
    
    return render_template('watch_later.html', movies=movies)

@bp.route('/remove_watch_later/<int:movie_id>', methods=['POST'])
@login_required
def remove_watch_later(movie_id):
    movie = WatchLater.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if movie:
        db.session.delete(movie)
        db.session.commit()
        flash(f'Removed {movie.title} from your watch later list!', 'success')
    return redirect(url_for('main.watch_later'))

@bp.route('/movie/<int:movie_id>')
@login_required
def movie_details(movie_id):
    try:
        print(f"Fetching details for movie ID: {movie_id}")
        
        # Check if TMDB API key is available
        api_key = current_app.config.get('TMDB_API_KEY')
        if not api_key:
            print("ERROR: TMDB_API_KEY not found in configuration")
            flash('Movie database configuration error', 'error')
            return redirect(url_for('main.search'))
        
        print(f"Using API key: {api_key[:10]}..." if api_key else "No API key")
        
        # Get movie details from TMDB
        url = f'{TMDB_BASE_URL}/movie/{movie_id}'
        params = {
            'api_key': api_key,
            'language': 'en-US',
            'append_to_response': 'credits,videos'  # Get additional details
        }
        
        print(f"Making request to: {url}")
        print(f"With params: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            movie = response.json()
            print(f"Successfully fetched movie: {movie.get('title', 'Unknown')}")
            
            # Check if movie is in favorites
            is_favorite = FavoriteMovie.query.filter_by(
                user_id=current_user.id,
                movie_id=movie_id
            ).first() is not None
            
            # Check if movie is in watch later
            is_watch_later = WatchLater.query.filter_by(
                user_id=current_user.id,
                movie_id=movie_id
            ).first() is not None
            
            print(f"Movie in favorites: {is_favorite}, in watchlist: {is_watch_later}")
            
            return render_template('movie_details.html', 
                                movie=movie,
                                is_favorite=is_favorite,
                                is_watch_later=is_watch_later)
        elif response.status_code == 404:
            print(f"Movie with ID {movie_id} not found on TMDB")
            flash('Movie not found', 'error')
            return redirect(url_for('main.search'))
        elif response.status_code == 401:
            print("TMDB API authentication failed - check API key")
            flash('Movie database authentication error', 'error')
            return redirect(url_for('main.search'))
        else:
            print(f"TMDB API error: {response.status_code}")
            print(f"Response text: {response.text}")
            flash(f'Movie database error (Status: {response.status_code})', 'error')
            return redirect(url_for('main.search'))
            
    except requests.exceptions.Timeout:
        print("Request to TMDB API timed out")
        flash('Request timed out. Please try again.', 'error')
        return redirect(url_for('main.search'))
    except requests.exceptions.ConnectionError:
        print("Connection error when contacting TMDB API")
        flash('Connection error. Please check your internet connection.', 'error')
        return redirect(url_for('main.search'))
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {str(e)}")
        flash('Network error occurred. Please try again.', 'error')
        return redirect(url_for('main.search'))
    except Exception as e:
        print(f"Unexpected error in movie_details: {str(e)}")
        import traceback
        traceback.print_exc()
        flash('An unexpected error occurred. Please try again.', 'error')
        return redirect(url_for('main.search')) 