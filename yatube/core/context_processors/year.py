import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    year_today = datetime.date.today().year
    return {
        "year": year_today,
    }
