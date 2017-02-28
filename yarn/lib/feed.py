#!/usr/bin/python

import feedparser


def get_channel(channel_url):
    return feedparser.parse(channel_url)
