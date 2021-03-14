import json;
import locale;

from staticjinja import Site


def format_price(value):
    if value is None or not isinstance(value, int):
        return value
    formatted_price = "{:,d}".format(value).replace(","," ")
    print('format_price',value,formatted_price)
    return formatted_price


filters = {
    'format_price': format_price,
}

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL,'')
    with open('data.json','r') as file:
        context = {
            'cars': json.loads(file.read()),
        }
    site = Site.make_site(env_globals=context,filters=filters)
    # enable automatic reloading
    site.render(use_reloader=True)