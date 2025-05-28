from flask_mail import Message
from app import mail
from flask import current_app

class MovieObserver:
    def update(self, message):
        pass

class MovieSubject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class EmailNotification(MovieObserver):
    def __init__(self, email):
        self.email = email

    def update(self, message):
        try:
            print(f"Attempting to send email to {self.email}")
            
            # Create modern HTML email template
            html_body = self._create_html_email(message)
            
            msg = Message(
                subject="🎬 Your Personalized Movie Recommendations are Ready!",
                recipients=[self.email],
                body=message,  # Fallback plain text
                html=html_body  # Rich HTML content
            )
            mail.send(msg)
            print(f"Email sent successfully to {self.email}")
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            # You might want to log this error in a production environment

    def _create_html_email(self, message):
        """Create a modern, responsive HTML email template"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CineMatch - New Recommendations</title>
    <style>
        /* Reset and base styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333333;
            background-color: #f8f9fa;
        }}
        
        /* Container */
        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border-radius: 12px;
            overflow: hidden;
        }}
        
        /* Header */
        .email-header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #e94560 100%);
            padding: 40px 30px;
            text-align: center;
            position: relative;
        }}
        
        .email-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            pointer-events: none;
        }}
        
        .logo {{
            position: relative;
            z-index: 1;
        }}
        
        .logo-icon {{
            width: 60px;
            height: 60px;
            background: linear-gradient(45deg, #e94560, #ff6b8a);
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 15px;
            font-size: 24px;
            color: white;
            box-shadow: 0 8px 25px rgba(233, 69, 96, 0.3);
        }}
        
        .brand-name {{
            color: white;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            position: relative;
            z-index: 1;
        }}
        
        .brand-tagline {{
            color: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            position: relative;
            z-index: 1;
        }}
        
        /* Content */
        .email-content {{
            padding: 40px 30px;
        }}
        
        .greeting {{
            font-size: 24px;
            font-weight: 600;
            color: #1a1a2e;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .message-box {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-left: 4px solid #e94560;
            padding: 25px;
            border-radius: 8px;
            margin: 25px 0;
            position: relative;
        }}
        
        .message-icon {{
            position: absolute;
            top: -10px;
            right: 20px;
            width: 40px;
            height: 40px;
            background: linear-gradient(45deg, #e94560, #ff6b8a);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 18px;
            box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
        }}
        
        .message-text {{
            font-size: 16px;
            color: #495057;
            line-height: 1.7;
            margin-bottom: 15px;
        }}
        
        .highlight {{
            color: #e94560;
            font-weight: 600;
        }}
        
        /* Features section */
        .features {{
            margin: 30px 0;
        }}
        
        .features-title {{
            font-size: 20px;
            font-weight: 600;
            color: #1a1a2e;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .feature-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }}
        
        .feature-item {{
            text-align: center;
            padding: 20px 15px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }}
        
        .feature-icon {{
            width: 50px;
            height: 50px;
            background: linear-gradient(45deg, #00d4aa, #00e6cc);
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 10px;
            color: white;
            font-size: 20px;
        }}
        
        .feature-text {{
            font-size: 14px;
            color: #6c757d;
            font-weight: 500;
        }}
        
        /* CTA Button */
        .cta-section {{
            text-align: center;
            margin: 35px 0;
        }}
        
        .cta-button {{
            display: inline-block;
            background: linear-gradient(45deg, #e94560, #ff6b8a);
            color: white;
            text-decoration: none;
            padding: 15px 35px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 16px;
            box-shadow: 0 8px 25px rgba(233, 69, 96, 0.3);
            transition: all 0.3s ease;
        }}
        
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 35px rgba(233, 69, 96, 0.4);
        }}
        
        /* Footer */
        .email-footer {{
            background: #1a1a2e;
            color: rgba(255, 255, 255, 0.8);
            padding: 30px;
            text-align: center;
        }}
        
        .footer-text {{
            font-size: 14px;
            margin-bottom: 15px;
        }}
        
        .social-links {{
            margin: 20px 0;
        }}
        
        .social-link {{
            display: inline-block;
            width: 40px;
            height: 40px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            margin: 0 8px;
            text-decoration: none;
            color: rgba(255, 255, 255, 0.8);
            line-height: 40px;
            transition: all 0.3s ease;
        }}
        
        .social-link:hover {{
            background: #e94560;
            color: white;
        }}
        
        .unsubscribe {{
            font-size: 12px;
            color: rgba(255, 255, 255, 0.6);
            margin-top: 15px;
        }}
        
        .unsubscribe a {{
            color: #e94560;
            text-decoration: none;
        }}
        
        /* Responsive */
        @media (max-width: 600px) {{
            .email-container {{
                margin: 10px;
                border-radius: 8px;
            }}
            
            .email-header, .email-content, .email-footer {{
                padding: 25px 20px;
            }}
            
            .feature-grid {{
                grid-template-columns: 1fr;
                gap: 15px;
            }}
            
            .greeting {{
                font-size: 20px;
            }}
            
            .brand-name {{
                font-size: 24px;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <!-- Header -->
        <div class="email-header">
            <div class="logo">
                <div class="logo-icon">🎬</div>
                <div class="brand-name">CineMatch</div>
                <div class="brand-tagline">Your Personal Movie Curator</div>
            </div>
        </div>
        
        <!-- Content -->
        <div class="email-content">
            <div class="greeting">🎉 Great News!</div>
            
            <div class="message-box">
                <div class="message-icon">✨</div>
                <div class="message-text">
                    {message}
                </div>
                <div class="message-text">
                    Our intelligent recommendation engine has analyzed your favorite movies and discovered 
                    <span class="highlight">personalized picks</span> that match your unique taste perfectly!
                </div>
            </div>
            
            <div class="features">
                <div class="features-title">What Makes These Recommendations Special?</div>
                <div class="feature-grid">
                    <div class="feature-item">
                        <div class="feature-icon">🎯</div>
                        <div class="feature-text">Tailored to Your Taste</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">⭐</div>
                        <div class="feature-text">High-Quality Picks</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">🔍</div>
                        <div class="feature-text">Smart Discovery</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">🎭</div>
                        <div class="feature-text">Diverse Genres</div>
                    </div>
                </div>
            </div>
            
            <div class="cta-section">
                <a href="#" class="cta-button">
                    🍿 View My Recommendations
                </a>
            </div>
            
            <div style="text-align: center; margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
                <div style="font-size: 16px; color: #6c757d; margin-bottom: 10px;">
                    💡 <strong>Pro Tip:</strong> The more movies you add to your favorites, the better our recommendations become!
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="email-footer">
            <div class="footer-text">
                Thank you for being part of the CineMatch community!
            </div>
            <div class="footer-text">
                Discover • Watch • Enjoy
            </div>
            
            <div class="social-links">
                <a href="#" class="social-link">📧</a>
                <a href="#" class="social-link">🐦</a>
                <a href="#" class="social-link">📘</a>
                <a href="#" class="social-link">📷</a>
            </div>
            
            <div class="unsubscribe">
                Don't want these emails? <a href="#">Unsubscribe here</a>
            </div>
        </div>
    </div>
</body>
</html>
        """

class RecommendationUpdate(MovieObserver):
    def update(self, message):
        print(f"Recommendation Update: {message}")
        # Here you could add logic to update a notification system
        # or send a push notification 