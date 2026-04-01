def simulate_growth(days, severity, weather):

    results = []

    health = 80

    temp = weather.get("temperature", 30)
    rain = weather.get("rainfall", 100)

    for day in range(days):

        if temp > 35:
            health -= 3
        elif temp < 20:
            health -= 2
        else:
            health += 1

        if rain > 150:
            health -= 4
        elif rain < 50:
            health -= 3
        else:
            health += 1

        if severity == "high":
            health -= 8
        elif severity == "medium":
            health -= 5
        elif severity == "low":
            health -= 2

        health = max(0, min(100, health))

        results.append({
            "day": day + 1,
            "health": health
        })

    return results


def disease_spread(days, severity):

    spread = []
    level = 10

    for day in range(days):

        if severity == "high":
            level *= 1.3
        elif severity == "medium":
            level *= 1.15
        elif severity == "low":
            level *= 1.05

        level = min(level, 100)

        spread.append({
            "day": day + 1,
            "spread": level
        })

    return spread


def digital_twin(days, severity, weather):

    return {
        "health_curve": simulate_growth(days, severity, weather),
        "disease_curve": disease_spread(days, severity)
    }