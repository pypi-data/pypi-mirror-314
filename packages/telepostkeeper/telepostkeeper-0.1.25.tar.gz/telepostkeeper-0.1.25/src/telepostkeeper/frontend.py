import asyncio
import os
import pathlib
import pprint
import re
from datetime import datetime

import bleach
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

from telepostkeeper.utils import read_yaml

load_dotenv()

ENV_NAME_STORE = 'TPK_STORE_DIR'

store = os.getenv(ENV_NAME_STORE)
if not store or store == ".":
    store = pathlib.Path("..")
else:
    store = pathlib.Path(store.strip())
store.mkdir(parents=True, exist_ok=True)
print('🏈️ Store: ', store)

current_dir = os.path.dirname(__file__)
templates_dir = os.path.join(current_dir, "templates")

template_env = Environment(loader=FileSystemLoader(templates_dir))


def tuning_convert_tg_emoji_to_a(html: str) -> str:
    """
    Converts <tg-emoji> tags to <a> tags with a tg://emoji?id=... URL.

    Args:
        html (str): The HTML block to process.

    Returns:
        str: The modified HTML.
    """
    # Regex to match <tg-emoji> tags and capture emoji-id and inner content
    tg_emoji_pattern = r'<tg-emoji\s+emoji-id="([^"]+)">(.*?)</tg-emoji>'

    # Function to replace <tg-emoji> with <a> tags
    def replace_tag(match):
        emoji_id = match.group(1)  # Capture emoji-id
        inner_content = match.group(2)  # Capture inner content
        return f'<a href="tg://emoji?id={emoji_id}" class="tg-emoji">{inner_content}</a>'

    # Perform substitution
    return re.sub(tg_emoji_pattern, replace_tag, html)

def tuning_date(date: str) -> str:

    # Parse the string into a datetime object
    try:
        date_obj = datetime.fromisoformat(date)
    except Exception as e:
        return date

    # Remove the timezone info by converting it to a naive datetime object (without timezone)
    date_naive = date_obj.replace(tzinfo=None)

    # Convert back to string if needed
    long_space = '\u00A0'
    date_naive_str = date_naive.strftime(f"%Y-%m-%d {long_space} %H:%M:%S")

    return date_naive_str


async def make_index_post(post: pathlib.Path, about: dict) -> dict:
    print('🔹 Post: ', post)

    data = await read_yaml(post)

    if not data:
        return {}

    print('🥑 DATA')
    pprint.pprint(data)
    print()

    context = dict()
    context['title'] = f'Post {post.stem}'

    is_encrypted_post = False
    if data.get('encryption', ''):
        print('🔐 ENCRYPTION 🔐')
        is_encrypted_post = True
        context['encrypted_class'] = 'encrypted'

    if data.get('date'):
        context['date'] = tuning_date(str(data.get('date')))

    context['text'] = ''
    if data.get('text'):
        context['text'] = data.get('text')

    if data.get('caption'):
        context['text'] = data.get('caption')

    context['text'] = context['text'].replace('\n', '<br />')

    context['text'] = tuning_convert_tg_emoji_to_a(context['text'])


    if thumbnail_path := data.get('thumbnail_path'):
        thumbnail_path = pathlib.Path(thumbnail_path)
        if thumbnail_path.exists():
            if thumbnail_path.suffix != '.aes':
                context['photo'] = thumbnail_path.name

    if data.get('type') == 'photo':
        if path := data.get('path'):
            path = pathlib.Path(path)
            if path.exists():
                if path.suffix != '.aes':
                    context['photo'] = path.name

    if path := data.get('path'):
        path = pathlib.Path(path)
        context['path'] = path.name

    print()
    print('CONTEXT')
    pprint.pprint(context)
    print()

    return context



async def make_index_month(month: pathlib.Path, about: dict):
    print('🔶 Month: ', month)

    posts = sorted(list(filter(lambda file: file.is_file() and file.suffix == '.yaml', month.iterdir())), reverse=True)
    posts_cnt = []
    for post in posts:
        post_cnt = await make_index_post(post, about)
        if not post_cnt:
            continue
        posts_cnt.append(post_cnt)

    month_full_name = datetime.strptime(month.name, "%m").strftime("%B")

    title = f'{month_full_name} {month.parent.name}'
    description = month.parent.parent.name

    html_data = template_env.get_template("month.html").render({
        'title': title,
        'description': description,
        'posts': posts_cnt})

    with month.joinpath('index.html').open('w') as f:
        f.write(html_data)


async def make_index_year(year: pathlib.Path, about: dict):
    print('🔹 Year: ', year)

    months = sorted(list(filter(lambda file: file.is_dir() and file.name.isdigit(), year.iterdir())), reverse=True)
    months_context = []
    for month in months:
        await make_index_month(month, about)

        months_context.append({'title': datetime.strptime(month.name, "%m").strftime("%B"), 'folder': month,})

    html_data = template_env.get_template("year.html").render({'title': f'{year.name}', 'months': months_context})

    with year.joinpath('index.html').open('w') as f:
        f.write(html_data)


async def make_index_chat(chat: pathlib.Path, about: dict):
    print('🟢 Chat: ', chat)

    years = sorted(list(filter(lambda file: file.is_dir() and file.name.isdigit(), chat.iterdir())), reverse=True)
    years_context = []
    for year in years:
        await make_index_year(year, about)

        months = sorted(list(filter(lambda file: file.is_dir() and file.name.isdigit(), year.iterdir())), reverse=True)
        months_context = []
        for month in months:
            month = pathlib.Path(month)
            await make_index_month(month, about)

            months_context.append({
                'title': datetime.strptime(month.name, "%m").strftime("%B"),
                'folder': month.relative_to(chat)
            })
        years_context.append({'title': year.name, 'months': months_context})

    html_data = template_env.get_template("chat.html").render({'title': f'{chat.name}', 'years': years_context})

    with chat.joinpath('index.html').open('w') as f:
        f.write(html_data)


async def make_index_store():
    chats = sorted(list(filter(lambda file: file.is_dir() and file.name.startswith('chat-'), store.iterdir())), reverse=True)

    chats_all_context = []
    for chat in chats:
        about_path = chat / 'about.yaml'
        about = await read_yaml(about_path)

        attributes = ['id', 'title', 'full_name', 'username', 'last_name', 'first_name']
        context = dict()

        for attr in attributes:
            if attr in about:
                if value := about[attr]:
                    context[attr] = value

        context['folder'] = chat.name

        if 'encryption' in about:
            title = f'{chat.name} (🔐 encrypted)'
            context['title'] = title

        await make_index_chat(chat, context)

        chats_all_context.append(context)

    html_data = template_env.get_template("store.html").render({'title': f'Index of chats', 'chats': chats_all_context})

    with store.joinpath('index.html').open('w') as f:
        f.write(html_data)



def main():
    print('🏞 Frontend: ')

    asyncio.run(make_index_store())

    print('✅ Success!')


if __name__ == '__main__':
    main()






