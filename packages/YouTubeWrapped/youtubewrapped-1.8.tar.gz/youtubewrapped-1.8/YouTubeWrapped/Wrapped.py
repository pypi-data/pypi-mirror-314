import json
import time
import pandas as pd
import pkg_resources
from openpyxl import Workbook
import subprocess
import os
import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

def run_javascript():
    js_file_path = pkg_resources.resource_filename(__name__, 'Js_assets/login.js')
    result = subprocess.run(['node', js_file_path], capture_output=True, text=True)
    return result

def new_sheet(df, excel_file_path, sheet_name):
    with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

def reformat_date(date_str):

    patterns = [
        r"(\d{1,2})\s(\w+)\s(\d{2,4})",  # Matches formats like '29 Sept 23'
        r"(\d{1,2})\s(\w+)",             # Matches formats like '1 Sept', '2 September'
        r"(\d{1,2})/(\d{1,2})/\d{2,4}"   # Matches formats like '2/09/24'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, date_str)
        if match:
            if len(match.groups()) == 3:
                day, month, _ = match.groups()
                try:
                    month_abbr = datetime.strptime(month[:3], "%b").strftime("%b")
                    return f"{month_abbr} {int(day)}"
                except ValueError:
                    continue
            elif len(match.groups()) == 2:
                day, month = match.groups()
                try:
                    month_abbr = datetime.strptime(month[:3], "%b").strftime("%b")
                    return f"{month_abbr} {int(day)}"
                except ValueError:
                    continue
            elif len(match.groups()) == 3:
                day, month, _ = match.groups()
                try:
                    month_abbr = datetime.strptime(month, "%m").strftime("%b")
                    return f"{month_abbr} {int(day)}"
                except ValueError:
                    continue

    return date_str


def convert_to_date(date_str):
    current_date = datetime.now()
    current_weekday = current_date.weekday()
    date_str = reformat_date(date_str)

    if date_str.lower() == "today":
        return current_date
    if date_str.lower() == "yesterday":
        return current_date - timedelta(days=1)

    try:
        month_day = datetime.strptime(date_str, "%b %d")
        full_date = month_day.replace(year=current_date.year)
        return full_date
    except ValueError:
        pass

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    target_day = date_str.capitalize()

    if target_day in days_of_week:
        target_day_index = days_of_week.index(target_day)
        
        if target_day_index <= current_weekday:
            days_difference = current_weekday - target_day_index
        else:
            
            days_difference = 7 - (target_day_index - current_weekday)
        
        target_date = current_date - timedelta(days=days_difference)
        return target_date
    else:
        print(date_str)
        raise ValueError("Invalid date format or day name")


def time_to_minutes(time_str):
    parts = list(map(int, time_str.split(":")))
    if len(parts) == 3:  
        return parts[0] * 60 + parts[1] + parts[2] / 60
    elif len(parts) == 2:  
        return parts[0] + parts[1] / 60
    return 0  

def load_cookies(context, cookie_file):
    with open(cookie_file, "r") as file:
        cookies = json.load(file)
        context.add_cookies(cookies)

def scroll_until_date(page, target_date):
    previous_height = None
    retries = 0
    prev_date = convert_to_date("Dec 31")
    
    while retries < 5:
        page.evaluate("window.scrollBy(0, document.documentElement.scrollHeight)")
        time.sleep(2)

        sections = page.query_selector_all("ytd-item-section-renderer")
        section = sections[len(sections) - 1]

        date_tag = section.query_selector("div#title")
        if not date_tag:
            continue
        watch_date = date_tag.inner_text()
        watch_date = convert_to_date(watch_date)

        if watch_date.month > prev_date.month:
            print(f"{watch_date} | {prev_date} : breaking")
            return 0
        else:
            prev_date = watch_date
    
        if page.query_selector(f"div#title:has-text('{target_date}')"):
            print(f"Found target date: {target_date}")
            return 0

        current_height = page.evaluate("document.documentElement.scrollHeight")

            
        if previous_height == current_height:
            retries += 1
        else:
            retries = 0
            
            previous_height = current_height
    else:
        return 0


def extract_data(page):
    data = []
    
    sections = page.query_selector_all("ytd-item-section-renderer")
    for i, section in enumerate(sections):
        date_tag = section.query_selector("div#title")
        if not date_tag:
            continue
        watch_date = date_tag.inner_text()
        watch_date = convert_to_date(watch_date)

        if i % 20 == 0 and i > 1:
            print(f"{int((i / len(sections)) * 100) + 1}% Complete...")

        video_wrappers = section.query_selector_all("div#title-wrapper")
        channel_wrappers = section.query_selector_all("""ytd-channel-name#channel-name.long-byline.style-scope.ytd-video-renderer""")
        thumbnail_wrappers = section.query_selector_all("a#thumbnail")
        for wrapper,channel,thumbnail in zip(video_wrappers, channel_wrappers, thumbnail_wrappers):
            
            length_tag = thumbnail.query_selector("div.badge-shape-wiz__text")
            length = length_tag.inner_text() if length_tag else "Unknown Length"
            if length != "SHORTS":
                length = time_to_minutes(length)
                progress_style = thumbnail.query_selector('div#progress').get_attribute('style')

                if progress_style and "width" in progress_style:
                    width_value = progress_style.split("width:")[1].strip().split(";")[0]
                    width_value = int(width_value.replace('%', ''))
                else:
                    width_value = 100
                
                length = length * (width_value / 100)


                title_tag = wrapper.query_selector("yt-formatted-string")
                title = title_tag.inner_text() if title_tag else "Unknown Title"


                channel_tag = channel.query_selector("a.yt-simple-endpoint.style-scope.yt-formatted-string")
                channel = channel_tag.inner_text() if channel_tag else "Unknown Channel"
                channelID = channel_tag.get_attribute("href")
                
                thumbnail_tag1 = thumbnail.query_selector("yt-image.style-scope.ytd-thumbnail")
                
                thumbnail_tag2 = thumbnail_tag1.query_selector("img")
                
                thumbnailIMG = thumbnail_tag2.evaluate("img => img.getAttribute('src')")
                


                data.append({
                    "title": title,
                    "channel": channel,
                    "watch_date": watch_date,
                    "video_length": length,
                    "thumbnail" : thumbnailIMG,
                    "channelID": channelID[1:]
                })
            else:
                next
        
    
    return data

def save_to_excel(data, filename):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "YouTube History"

    
    sheet.append(["Title", "Channel", "Watch Date", "Video Length", "Thumbnail", "Channel ID"])

    
    for item in data:
        sheet.append([item["title"], item["channel"], item["watch_date"], item["video_length"], item["thumbnail"], item["channelID"]])

    workbook.save(filename)


def getTop5(data, accountname):

    df = pd.DataFrame(data)
    channel_info = df.groupby('channel').agg(
    total_watchtime=('video_length', 'sum'),
    earliest_watch_date=('watch_date', 'min'),
    )
    
    df['channelID'] = df.groupby('channel')['channelID'].transform('first')
    channel_info = channel_info.merge(df[['channel', 'channelID']].drop_duplicates(), on='channel', how='left')

    total_watchtime = channel_info.sort_values(by='total_watchtime', ascending=False)
    top_5_channels = total_watchtime.head(5)
    new_sheet(top_5_channels, f"{accountname}_WRAPPED2024.xlsx", "Top 5 Channels")

    top_5_titles = df['title'].value_counts().head(5)
    top_5_titles = top_5_titles.reset_index()
    new_sheet(top_5_titles, f"{accountname}_WRAPPED2024.xlsx", "Top 5 Rewatched Vidoes")


    channels_before_june = df[df['watch_date'].dt.month < 6]['channel'].unique()
    old_friend = total_watchtime[total_watchtime['channel'].isin(channels_before_june) & (total_watchtime['total_watchtime'] > 500)]
    new_sheet(old_friend, f"{accountname}_WRAPPED2024.xlsx", "Channel first half of year only")

    return top_5_channels, top_5_titles

def topchannelimg(top5):
    top = top5['channelID'].to_numpy()
    top = top[0]

    URL = "https://www.youtube.com/" + top
    soup = BeautifulSoup(requests.get(URL).content, "html.parser")

    data = re.search(r"var ytInitialData = ({.*});", str(soup.prettify())).group(1)

    json_data = json.loads(data)

    img_url = json_data['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']['image']['decoratedAvatarViewModel']['avatar']['avatarViewModel']['image']['sources'][2]['url']

    response = requests.get(img_url)

    if response.status_code == 200:
        with open(f"{top}.jpg", "wb") as file:
            file.write(response.content)
    else:
        exit(-1)
    
    return f"{top}.jpg"



def create_wrapped(top5C, img, WT, imgname):
    img_path = pkg_resources.resource_filename('YouTubeWrapped', 'WrappedTemplate.jpg')
    image = Image.open(img_path)
    draw = ImageDraw.Draw(image)

    channels = top5C['channel']
    watchtime = top5C['total_watchtime']

    font_path = "/Users/haziq/Library/Fonts/Gotham-Bold.otf"
    font_size = 48
    font = ImageFont.truetype(font_path, font_size)

    for i, (channel, wt) in enumerate(zip(channels, watchtime)):
        wt = int(wt)
        wt = f"{wt:,}"
        if len(channel) > 13:
            channel = channel[:18] + "..."

        draw.text((129, (1104 + (14 * i) + (font_size * i)) - (2 * i*2)), channel, fill="white", font=font)
        draw.text((603, (1102 + (14 * i) + (font_size * i) - (2 * i*2))), wt, fill="white", font=font)

    WT = int(WT)
    WT = f"{WT:,}"
    fontB = ImageFont.truetype(font_path, 100)
    draw.text((82, 1530), WT, fill="white", font=fontB)

    pp = Image.open(img)
    pp = pp.resize((615,615))

    image.paste(pp, (232,192))

    os.remove(img)

    image.save(f'{imgname}.png')


def install_js_dependencies():
    js_dir = pkg_resources.resource_filename(__name__, 'Js_assets')
    node_modules_path = os.path.join(js_dir, 'node_modules')

    if not os.path.exists(node_modules_path):
        print("JavaScript dependencies not found. Installing...")
        try:
            subprocess.run(['npm', 'install', '--silent'], cwd=js_dir, check=True)
        except subprocess.CalledProcessError as e:
            print("An error occurred during npm installation.")
            print(f"Error details: {e}")
    else:
        time.sleep(0.1)


def run_javascript():
    js_file_path = pkg_resources.resource_filename(__name__, 'Js_assets/login.js')
    result = subprocess.run(['node', js_file_path], capture_output=True, text=True)
    return result

def save_cookies(accountName, cookies):
    with open(f'YT_{accountName}_cookies.json', 'w') as file:
        json.dump(cookies, file, indent=4)

def getWrapped(accountName):
    target_date = "Jan 1"
    cookie_file = f"YT_{accountName}_cookies.json"
    output_file = f"{accountName}_WRAPPED2024.xlsx"

    if os.path.exists(f"YT_{accountName}_cookies.json"):
        next
    else:
        install_js_dependencies()
        print("Please Log-in to your YouTube account when prompted")
        result = run_javascript()
        os.rename('YT_cookies.json', f"YT_{accountName}_cookies.json")


    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=True)
        context = browser.new_context()
        
        
        load_cookies(context, cookie_file)

        
        page = context.new_page()
        page.goto("https://www.youtube.com/feed/history")
        time.sleep(5)
        print("Extracting your history, this may take a couple of minutes, depending on your activity...")

        
        _ = scroll_until_date(page, target_date)

        data = extract_data(page)

        save_to_excel(data, output_file)
        print(f"Data saved to {output_file}")

        browser.close()
    
    print("Done extracting data, creating your wrapped image now...")

    top5C, top5V = getTop5(data, accountName)
    totalWT = sum(item["video_length"] for item in data)
    channelimg = topchannelimg(top5C)

    create_wrapped(top5C=top5C, img=channelimg, WT=totalWT, imgname=f'{accountName}_WRAPPED2024.jpg')
    print(f"Wrapped Completed! Image path: {accountName}_WRAPPED2024.jpg")
    