from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import math
import requests
from functools import lru_cache

# Cache calculations for common functions
@lru_cache(maxsize=1000)
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

@lru_cache(maxsize=1000)
def is_perfect(n):
    if n <= 1:
        return False
    sum_divisors = sum(i for i in range(1, n) if n % i == 0)
    return sum_divisors == n

@lru_cache(maxsize=1000)
def is_armstrong(n):
    num_str = str(n)
    power = len(num_str)
    return n == sum(int(digit) ** power for digit in num_str)

@lru_cache(maxsize=1000)
def get_digit_sum(n):
    return sum(int(digit) for digit in str(n))

def get_fun_fact(n):
    try:
        # Try to get from cache first
        cache_key = f'fun_fact_{n}'
        cached_fact = cache.get(cache_key)
        if cached_fact:
            return cached_fact

        # If not in cache, fetch from API
        response = requests.get(
            f'http://numbersapi.com/{n}/math',
            timeout=3
        )
        if response.status_code == 200:
            fact = response.text
        else:
            fact = f"{n} is an interesting number with various mathematical properties."

        # Try to cache the result
        try:
            cache.set(cache_key, fact, timeout=86400)
        except:
            pass  # If caching fails, continue without it
        
        return fact
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

        # Add input validation
        if number < 0 or number > 1000000:
            return JsonResponse(
                {
                    "error": True,
                    "message": "Number must be between 0 and 1,000,000"
                },
                status=400
            )

        # Try to get from cache first
        cache_key = f'number_details_{number}'
        cached_response = cache.get(cache_key)
        if cached_response:
            return JsonResponse(cached_response, json_dumps_params={'indent': 4})

        properties = []

        # Calculate properties
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

        # Try to cache the response
        try:
            cache.set(cache_key, response_data, timeout=3600)  # Cache for 1 hour
        except:
            pass  # If caching fails, continue without it

        return JsonResponse(
            response_data,
            json_dumps_params={'indent': 4}
        )

    except ValueError:
        return JsonResponse(
            {
                "error": True,
                "number": request.GET.get('number')
            },
            status=400,
            json_dumps_params={'indent': 4}
        )
