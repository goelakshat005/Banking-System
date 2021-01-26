from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import creation_updation, enquiry_download

urlpatterns = [
    url(r'creationupdation/', creation_updation, name="Bank"),
    url(r'enquirydownload/', enquiry_download, name="Bank")
]