from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    # 1. Static Routes
    path('', views.home, name='home'),
    path('destinations/', views.category_view, {'slug': 'all'}, name='destinations'), # 'All' category chupistundi
    path('safety-guides/', views.safety_guides, name='safety_guides'),
    path('experience/', views.experience, name='experience'),
    
    # 2. Support & Legal
    path('help-center/', views.help_center, name='help_center'),
    path('privacy-policy/', views.privacy, name='privacy'),
    path('terms-of-use/', views.terms, name='terms'),

    # 3. Dynamic Routes (Slugs & IDs - Bottom lo undali)
    path('category/<slug:slug>/', views.category_view, name='category_view'),
    path('book/<int:dest_id>/', views.book_ride, name='book_ride'),
    path('process-payment/<int:dest_id>/', views.process_payment, name='process_payment'),
    path('registered-trips/', views.registered_trips, name='registered_trips'),
    path('cancel-ride/<int:dest_id>/', views.cancel_ride, name='cancel_ride'),
    path('newsletter/', views.newsletter_signup, name='newsletter_signup'),
    
    # 4. Settings & Account
    path('settings/', views.settings_view, name='settings_view'), 
    path('logout/', views.logout_view, name='logout'),
]