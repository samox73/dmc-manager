import json
import csv
import re


def fft_to_json(filename="fft.dat"):
    doc = {}
    with open(filename) as file:
        header = file.readline()
        titles = [t.strip() for t in header.split()]
        for title in titles:
            doc[title] = []
        for line in file:
            for title, value in zip(titles, line.split()):
                value = value.strip()
                v = value
                try:
                    v = float(value)
                except ValueError:
                    v = ((complex(value)).real, complex(value).imag)
                doc[title].append(v)
    return doc


def run_properties_to_json(filename="run_properties.json"):
    with open("run_properties.json", "r") as file:
        return json.load(file)
