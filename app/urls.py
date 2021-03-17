from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
    path('dashboard', views.dashboard),
    path('new_workout', views.new_workout),
    path('add_workout', views.add_workout),
    path('workouts/<workout_id>', views.workout_details),
    path('profile/<user_id>',views.profile),
    path('workouts/edit/<workout_id>',views.edit_workout),
    path('delete/<workout_id>',views.delete)



]
