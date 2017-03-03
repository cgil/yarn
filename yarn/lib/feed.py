#!/usr/bin/python
from time import mktime
from datetime import datetime

from yarn.models.publisher import Publisher
from yarn.models.channel import Channel
from yarn.models.entry import Entry

import feedparser


def to_datetime(struct_time):
    return datetime.fromtimestamp(mktime(struct_time))


def fetch_channel(channel_url):
    return feedparser.parse(channel_url)


def get_or_create_channel(channel_data, channel_url):
    attrs = {
        'title': channel_data.title,
        'link': channel_url,
        'publication_updated_datetime': to_datetime(channel_data.updated_parsed),
        'public_channel_id': channel_data.get('id', channel_data.link),
    }
    record = Channel.get_or_create_channel(attrs)
    return record


def update_or_create_entry(entry_data, channel_id):
    attrs = {
        'channel_id': channel_id,
        'title': entry_data.title,
        'link': entry_data.link,
        'description': entry_data.summary,
        'content': entry_data['content'][0].value if entry_data.get('content') else None,
        'content_type': entry_data['content'][0].type if entry_data.get('content') else None,
        'public_entry_id': entry_data.id,
        'published_datetime': to_datetime(entry_data.published_parsed),
        'published_updated_datetime': to_datetime(entry_data.updated_parsed),
    }
    found_entry = Entry.get_by_public_entry_id(attrs['public_entry_id'])
    if not found_entry:
        found_entry = Entry(**attrs)
        found_entry.save(found_entry)
    elif attrs['published_updated_datetime'] > found_entry.published_updated_datetime:
        found_entry.update_published_updated_datetime(
            attrs['published_updated_datetime']
        )


def create_entries(entries_data, channel_id):
    for e in entries_data:
        update_or_create_entry(e, channel_id)


def update_channel(channel_data, channel_record):
    channel_record.published_updated_datetime = to_datetime(channel_data.updated_parsed)
    channel_record.save(channel_record)


def update_channels():
    found_channels = Channel.get_all()
    for c in found_channels:
        fetched_channel_data = fetch_channel(c.link)
        # Only process updated channels.
        if to_datetime(fetched_channel_data.updated_parsed) > c.publication_updated_datetime:
            create_entries(fetched_channel_data.entries, c.id)
            update_channel(fetched_channel_data, c)
