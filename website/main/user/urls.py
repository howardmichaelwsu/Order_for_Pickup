from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
	path('register', views.register),
	path('login', views.login),
	path('success', views.success),
	path('logout', views.logout),
	path('usershome', views.usershome),
	path('neworder', views.neworder),
	path('review', views.review),
	path('comment', views.comment),
	path('edituser', views.edituser),
	path('editprofile/<int:id>', views.editprofile),
	path('item', views.item),
	path('additem', views.additem),
	path('pickitem', views.pickitem),
	path('complete', views.complete),
	path('deleteuser', views.deleteuser),
	path('likes/<int:id>', views.likes),
]