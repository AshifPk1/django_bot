from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.contrib.auth.models import AbstractUser, User
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from chatbot.models import ButtonCalls


def chat(request):
    context = {}
    return render(request, 'chatbot_tutorial/chatbot.html', context)


def respond_to_websockets(message, user_id):
    jokes = {
        'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                   """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
        'fat': ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
        'dumb': [
            """Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
            """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""]
    }

    result_message = {
        'type': 'text'
    }
    user = User.objects.get(id=user_id)
    if not user:
        return JsonResponse({"status": "error", "data": "User Not Found"})
    button_call = ButtonCalls.objects.get(user_id=user_id)
    if 'fat' in message['text']:
        result_message['text'] = random.choice(jokes['fat'])
        if button_call:
            fat = button_call.fat
            button_call.fat = fat + 1
            button_call.save()
        else:
            button_call = ButtonCalls.objects.create(user_id=user, fat=1, stupid=0,
                                                     dumb=0)

    elif 'stupid' in message['text']:
        result_message['text'] = random.choice(jokes['stupid'])
        if button_call:
            stupid = button_call.stupid
            button_call.stupid = stupid + 1
            button_call.save()
        else:
            button_call = ButtonCalls.objects.create(user_id=user, fat=0, stupid=1,
                                                     dumb=0)

    elif 'dumb' in message['text']:
        if button_call:
            dumb = button_call.dumb
            button_call.dumb = dumb + 1
            button_call.save()
        else:
            button_call = ButtonCalls.objects.create(user_id=user, fat=0, stupid=0,
                                                     dumb=1)

        result_message['text'] = random.choice(jokes['dumb'])

    elif message['text'] in ['hi', 'hey', 'hello']:
        result_message[
            'text'] = "Hello to you too! If you're interested in yo mama jokes, just tell me fat, stupid or dumb and i'll tell you an appropriate joke."
    else:
        result_message[
            'text'] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."

    return result_message
