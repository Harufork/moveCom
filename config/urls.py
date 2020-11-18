from django.contrib import admin
from django.urls import path
from moving_company.views import HomePageView
from users.views import Authorization, Registration

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('authorization/', Authorization.as_view(), name='authorization'),
    path('registration/', Registration.as_view(), name='registration'),
]

# НУЖНЫ ХЭНДЛЕРЫ YE:YS
# path('addmusic/', addmusic.as_view(), name='addmusic'),
# <!--        <form action="{% url 'main' %}" method="post">-->
#             {% csrf_token %}
#             <input type="hidden" name="exit" value="1">
#             <button type="submit">Выйти</button>
#         </form>
# {% for  song in sosng %}
# { % endfor %}
# {% if isauth %}
# {% else %}
# {% endif %}
