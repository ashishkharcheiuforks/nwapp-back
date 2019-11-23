from django.urls import path

from . import views


urlpatterns = (
    path('api/v1/tags', views.TagListCreateAPIView.as_view(), name='nwapp_tag_list_create_api_endpoint'),
    path('api/v1/tag/<int:id>', views.TagRetrieveUpdateDestroyAPIView.as_view(), name='nwapp_tag_retrieve_update_delete_api_endpoint'),
    path('api/v1/how-hears', views.HowHearAboutUsItemListCreateAPIView.as_view(), name='nwapp_how_did_you_hear_list_create_api_endpoint'),
    path('api/v1/how-hear/<int:id>', views.HowHearAboutUsItemRetrieveUpdateDestroyAPIView.as_view(), name='nwapp_how_did_you_hear_retrieve_update_delete_api_endpoint'),
    path('api/v1/expectations', views.ExpectationItemListCreateAPIView.as_view(), name='nwapp_expectation_item_list_create_api_endpoint'),
    path('api/v1/expectation/<int:id>', views.ExpectationItemRetrieveUpdateDestroyAPIView.as_view(), name='nwapp_expectation_items_retrieve_update_delete_api_endpoint'),
    path('api/v1/meanings', views.MeaningItemListCreateAPIView.as_view(), name='nwapp_meaning_item_list_create_api_endpoint'),
    path('api/v1/meaning/<int:id>', views.MeaningItemRetrieveUpdateDestroyAPIView.as_view(), name='nwapp_meaning_item_retrieve_update_delete_api_endpoint'),
)