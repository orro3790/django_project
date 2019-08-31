from django import template
from ..models import Ad, Job

register = template.Library()

@register.simple_tag
def total_arts_and_crafts():
    qs = Ad.objects.all()
    total_arts_and_crafts = qs.filter(category="arts and crafts").count()
    return total_arts_and_crafts

@register.simple_tag
def total_baby_and_kids():
    qs = Ad.objects.all()
    total_baby_and_kids = qs.filter(category="baby and kids").count()
    return total_baby_and_kids

@register.simple_tag
def total_beauty_and_health():
    qs = Ad.objects.all()
    total_beauty_and_health = qs.filter(category="beauty and health").count()
    return total_beauty_and_health

@register.simple_tag
def total_bikes():
    qs = Ad.objects.all()
    total_bikes = qs.filter(category="bikes").count()
    return total_bikes

@register.simple_tag
def total_books():
    qs = Ad.objects.all()
    total_books = qs.filter(category="books").count()
    return total_books

@register.simple_tag
def total_cell_phones():
    qs = Ad.objects.all()
    total_cell_phones = qs.filter(category="cell phones").count()
    return total_cell_phones

@register.simple_tag
def total_clothing():
    qs = Ad.objects.all()
    total_clothing = qs.filter(category="clothing").count()
    return total_clothing

@register.simple_tag
def total_collectibles():
    qs = Ad.objects.all()
    total_collectibles = qs.filter(category="collectibles").count()
    return total_collectibles

@register.simple_tag
def total_computers():
    qs = Ad.objects.all()
    total_computers = qs.filter(category="computers").count()
    return total_computers

@register.simple_tag
def total_electronics():
    qs = Ad.objects.all()
    total_electronics = qs.filter(category="electronics").count()
    return total_electronics

@register.simple_tag
def total_garden():
    qs = Ad.objects.all()
    total_garden = qs.filter(category="garden").count()
    return total_garden

@register.simple_tag
def total_free():
    qs = Ad.objects.all()
    total_free = qs.filter(category="free").count()
    return total_free

@register.simple_tag
def total_life():
    qs = Ad.objects.all()
    total_life = qs.filter(category="life").count()
    return total_life

@register.simple_tag
def total_household():
    qs = Ad.objects.all()
    total_household = qs.filter(category="household").count()
    return total_household

@register.simple_tag
def total_pets():
    qs = Ad.objects.all()
    total_pets = qs.filter(category="pets").count()
    return total_pets

@register.simple_tag
def total_furniture():
    qs = Ad.objects.all()
    total_furniture = qs.filter(category="furniture").count()
    return total_furniture

@register.simple_tag
def total_jewelery():
    qs = Ad.objects.all()
    total_jewelery = qs.filter(category="jewelery").count()
    return total_jewelery

@register.simple_tag
def total_materials():
    qs = Ad.objects.all()
    total_materials = qs.filter(category="materials").count()
    return total_materials

@register.simple_tag
def total_musical_instruments():
    qs = Ad.objects.all()
    total_musical_instruments = qs.filter(category="musical instruments").count()
    return total_musical_instruments

@register.simple_tag
def total_cameras():
    qs = Ad.objects.all()
    total_cameras = qs.filter(category="cameras").count()
    return total_cameras

@register.simple_tag
def total_tools():
    qs = Ad.objects.all()
    total_tools = qs.filter(category="tools").count()
    return total_tools

@register.simple_tag
def total_games():
    qs = Ad.objects.all()
    total_games = qs.filter(category="games").count()
    return total_games

@register.simple_tag
def total_salary_50000():
    qs = Job.objects.all()
    total_salary_50000 = qs.filter(salary__gte="50000").count()
    return total_salary_50000

@register.simple_tag
def total_salary_60000():
    qs = Job.objects.all()
    total_salary_60000 = qs.filter(salary__gte="60000").count()
    return total_salary_60000

@register.simple_tag
def total_salary_70000():
    qs = Job.objects.all()
    total_salary_70000 = qs.filter(salary__gte="70000").count()
    return total_salary_70000

@register.simple_tag
def total_salary_80000():
    qs = Job.objects.all()
    total_salary_80000 = qs.filter(salary__gte="80000").count()
    return total_salary_80000

@register.simple_tag
def total_salary_90000():
    qs = Job.objects.all()
    total_salary_90000 = qs.filter(salary__gte="90000").count()
    return total_salary_90000

@register.simple_tag
def total_salary_100000():
    qs = Job.objects.all()
    total_salary_100000 = qs.filter(salary__gte="100000").count()
    return total_salary_100000