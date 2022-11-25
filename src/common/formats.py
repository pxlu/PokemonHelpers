import json


def generate_format_json():

    formats = {}
    generations = [i for i in range(1, 10)]
    tiers = ['ubers', 'ou', 'uu', 'ru', 'nu', 'pu', 'zu']
    for generation in generations:
        for tier in tiers:
            format_key = 'gen' + str(generation) + tier
            formats[format_key] = {
                "name": format_key
            }

    return formats


if __name__ == '__main__':
    x = generate_format_json()
    print(x)
