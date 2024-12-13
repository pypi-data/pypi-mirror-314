import json
from datetime import datetime
from time import mktime

from django.conf.global_settings import LANGUAGES
from langdetect import detect, lang_detect_exception

languages_dict = dict(LANGUAGES)


def _get_source(d):
    source = {}
    if source_id := d.get("news_source"):
        source["id"] = source_id
    else:
        if "title" in d["feed"]:
            source["title"] = d["feed"]["title"]
        if "author" in d["feed"]:
            source["author"] = d["feed"]["author"]
        if "image" in d["feed"]:
            source["image"] = d["feed"]["image"]["href"]
        if "href" in d["feed"]:
            source["identifier"] = d["feed"]["href"]
        if "link" in d["feed"]:
            source["url"] = d["feed"]["link"]
    return source


def parse(import_source):
    content = json.load(import_source.file)
    data = []
    source = _get_source(content)

    for entry in content["entries"]:
        if summary := entry.get("summary", None):
            description = entry.get("description", summary)
            res = {
                "description": description,
                "summary": summary,
                "source": source,
                "title": entry.get("title", ""),
                "link": entry.get("link", None),
            }
            try:
                language = detect(entry["summary"])
                if language in languages_dict:
                    res["language"] = language
            except lang_detect_exception.LangDetectException:
                pass
            if published_parsed := entry.get("published_parsed", None):
                updated = datetime.fromtimestamp(mktime(tuple(published_parsed)))
                res["datetime"] = updated.strftime("%Y-%m-%dT%H:%M:%S")
            if enclosures := entry.get("enclosures", None):
                res["enclosures"] = [e.get("href", "") for e in enclosures]
            if (
                (media_content := entry.get("media_content", []))
                and isinstance(media_content, list)
                and len(media_content) > 0
                and (image_url := media_content[0].get("url", None))
            ):
                res["image_url"] = image_url
            data.append(res)
    return {"data": data}
