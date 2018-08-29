#!/usr/bin/python

import sys, os, django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("/Users/leon/PycharmProjects/test_project")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")
django.setup()
from test_project.models import User, ChatRoom
args = list(sys.argv)
email = args[1]
message = args[2]
user = User.objects.get(email=email)
chat_room = ChatRoom.objects.create(subject=user, text=message)
