import os
import openai
from dotenv import load_dotenv
from youtubesearchpython import *
from app.db.models import TbMarketReport

try:
    # Load environment variables from the .env file
    load_dotenv(".env")
except Exception as e:
    print(f"Error occurred while loading .env file: {e}")


class GlobalMarketChat:
    def __init__(self, model: str = "gpt-3.5-turbo-16k"):
        # Setting the API key to use the OpenAI API
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.messages = [
            {
                "role": "system",
                "content": """
                    You are a global market analyst, your role involves understanding and analyzing
                    various financial markets, including stocks, bonds, commodities, and currencies.
                    This analysis is crucial for providing valuable insights and guidance to
                    investors, financial institutions, and corporations seeking to make informed
                    decisions about their investments and strategies.
                """,
            },
        ]
        self.report = ""

    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model=self.model, messages=self.messages
        )
        self.messages.append(
            {"role": "assistant", "content": response["choices"][0]["message"].content}
        )
        return response["choices"][0]["message"].content

    def watch_youtube(self, link: str) -> None:
        subtitles = Transcript.get(link)
        transcript = ""
        for subtitle in subtitles["segments"]:
            transcript += subtitle["text"] + " "
        return self.chat(
            f"""
!!! DO NOT GENERATE REPORT YET !!!
This is a disscussion trascripts by market analysts. Study and understand the content.
Transcript: {transcript}
Do not generate daily market briefing report until I tell you to.
Just reply `Complete` when you are done.
            """
        )

    def generate(self):
        self.report = self.chat(
            f"""
Now generate the daily market briefing. (in markdown format)

The report should provide a comprehensive understanding of the day's global market activities and
trends. It shoudl offer valuable insights and analysis on the investment and global macro economics.

Craft the briefing in a conversational tone that effectively engages investors, offering key
takeaways without overwhelming technical jargon. Please ensure that the content remains focused on
providing insightful analysis, omitting disclaimers and general information.

While delivering a cohesive narrative, avoid dividing the report into sections and exclude any
references to individuals or sponsors. Your primary objective is to aid investors in their
decision-making process by emphasizing accessibility and clarity in the presentation of global
market and economic status and trends.

Lastly, the report should not include any individual stocks analysis/information.

The length of the report should range between 500 and 600 words,
emphasizing only the most pertinent information for investors.

"""
        )
        return self.report


from youtubesearchpython import *

from datetime import timedelta


# Custom function to handle years and months
def parse_time_string(time_string):
    time_parts = time_string.split()
    if len(time_parts) == 2:
        if time_parts[1] in ["years", "year"]:
            return timedelta(days=int(time_parts[0]) * 365)
        elif time_parts[1] in ["months", "month"]:
            return timedelta(days=int(time_parts[0]) * 30)  # Approximation, can vary
        elif time_parts[1] in ["weeks", "week"]:
            return timedelta(weeks=int(time_parts[0]))
        elif time_parts[1] in ["days", "day"]:
            return timedelta(days=int(time_parts[0]))
        elif time_parts[1] in ["hours", "hour"]:
            return timedelta(hours=int(time_parts[0]))
        elif time_parts[1] in ["minutes", "minute"]:
            return timedelta(minutes=int(time_parts[0]))
        elif time_parts[1] in ["seconds", "second"]:
            return timedelta(seconds=int(time_parts[0]))
        else:
            raise ValueError("Unsupported time format.")
    else:
        raise ValueError("Invalid time string format.")


def get_report():
    yt_links = []

    channels = [
        {
            "name": "Investor's Business Daily",
            "id": "UC5fZv7bPcF5j2RsfO-9OiLA",
            "link": "https://www.youtube.com/channel/UC5fZv7bPcF5j2RsfO-9OiLA",
        },
        {
            "name": "Real Vision",
            "id": "UCBH5VZE_Y4F3CMcPIzPEB5A",
            "link": "https://www.youtube.com/channel/UCBH5VZE_Y4F3CMcPIzPEB5A",
        },
        {
            "name": "Top Traders Unplugged",
            "id": "UCt-_RaV_mFlyXDmhYnIm0Ug",
            "link": "https://www.youtube.com/channel/UCt-_RaV_mFlyXDmhYnIm0Ug",
        },
        {
            "name": "Investor Center",
            "id": "UC2cL3pI1H3tiozKif6A8fmA",
            "link": "https://www.youtube.com/channel/UC2cL3pI1H3tiozKif6A8fmA",
        },
        {
            "name": "Mauldin Economics",
            "id": "UCUb-ua-LxOZ1d6WhThgMGRA",
            "link": "https://www.youtube.com/channel/UCUb-ua-LxOZ1d6WhThgMGRA",
        },
    ]

    for chann in channels:
        channel = Channel(chann["id"])

        while channel.has_more_playlists():
            channel.next()
        for p in channel.result["playlists"]:
            try:
                playlist_link = f'https://www.youtube.com/playlist?list={p["id"]}'
                videos = Playlist.getVideos(playlist_link)["videos"]
                for video in videos:
                    text = video["accessibility"]["title"]
                    upload_time_string = (
                        text.rsplit("views", 1)[1]
                        .rsplit("Streamed", 1)[-1]
                        .split("ago")[0]
                        .strip()
                    )
                    time_delta = parse_time_string(upload_time_string)
                    if time_delta < timedelta(days=1):
                        yt_links.append(video["link"])

            except:
                pass

        if yt_links:
            chat = GlobalMarketChat()

            for l in yt_links:
                chat.watch_youtube(l)

            chat.generate()
            TbMarketReport.add(report=chat.messages)

            return chat.report
