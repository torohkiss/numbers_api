from django.shortcuts import render
from django.http import JsonResponse
import math
import requests

# Create your views here.


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n <= 1:
        return False
    sum_divisors = sum(i for i in range(1, n) if n % i == 0)
    return sum_divisors == n

def is_armstrong(n):
    num_str = str(n)
    power = len(num_str)
    return n == sum(int(digit) ** power for digit in num_str)

def get_digit_sum(n):
    return sum(int(digit) for digit in str(n))

def get_fun_fact(n):
    try:
        response = requests.get(f'http://numbersapi.com/{n}/math')
        if response.status_code == 200:
            return response.text
        return f"{n} is an interesting number with various mathematical properties."
    except:
        return f"{n} is an interesting number with various mathematical properties."

def number_details(request):
    if request.method != 'GET':
        return JsonResponse(
            {
                "error": True,
                "message": "Method not allowed",
            },
            status=405
        )

    number = request.GET.get('number')
    if not number:
        return JsonResponse(
            {
                "error": True,
                "number": None
            },
            status=400
        )

    try:
        number = int(number)
        properties = []

        if is_armstrong(number):
            properties.append("armstrong")
        if number % 2 == 0:
            properties.append("even")
        else:
            properties.append("odd")

        response_data = {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": get_digit_sum(number),
            "fun_fact": get_fun_fact(number)
        }

        return JsonResponse(response_data, json_dumps_params={'indent': 4})

    except ValueError:
        return JsonResponse(
            {
                "error": True,
                "number": request.GET.get('number')
            },
            status=400,
            json_dumps_params={'indent': 4}
        )
