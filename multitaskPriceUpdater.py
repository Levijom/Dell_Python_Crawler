# Multitask PriceUpdater.py
# Copyright (C) Joao A. Haddad 2021

import threading
import queue

from src.priceUpdater import PriceUpdater
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("sourceFile", type=str, help="Source File (txt format)")
parser.add_argument("--threads", nargs="?", const=1, type=int, default=1)
parser.add_argument("--retries", nargs="?", const=1, type=int, default=1)
args = parser.parse_args()
print(args)
print(args.threads)
if args.retries < 0 or args.retries > 10:
    print("Error, 0 <= retries <= 10")
    quit()

if args.threads < 1 or args.threads > 10:
    print("Error, 1 <= threads <= 10")
    quit()
try:
    sourceFile = open(args.sourceFile, "r")
    quote_list = sourceFile.readlines()  # List of Quotes
    sourceFile.close()

except:
    print("Error opening file " + args.sourceFile)
    quit()

in_que = queue.Queue()
out_que = queue.Queue()

work_threadlist = []
work_classlist = []

# Creating Threads
for i in range(args.threads):
    work_class = PriceUpdater()
    work_thread = threading.Thread(target=work_class.worker, args=(in_que, out_que, i))
    work_thread.start()
    work_threadlist.append(work_thread)
    work_classlist.append(work_class)

# Adding Items to the In Queue

pending_quotes = 0
for quoteNumberFromList in quote_list:
    # quoteNumberFromList = quoteNumberFromList.replace("\t", " ")
    quote = quoteNumberFromList.split()[0].strip("US-").replace("/", ".")
    price = quoteNumberFromList.split()[1].strip("$").replace(",", "")
    retries_done = 0
    in_que.put((quote, price, retries_done))
    pending_quotes += 1
    time.sleep(1)


answer = []

while pending_quotes:
    quoteNumberWithVersion, new_totalSellingPrice, retries = out_que.get()
    if retries > 0:
        # Didn't work
        if retries > args.retries:
            pending_quotes -= 1
            answer.append((quoteNumberWithVersion, None))
        else:
            in_que.put((quoteNumberWithVersion, new_totalSellingPrice, retries))
    else:
        pending_quotes -= 1
        answer.append((quoteNumberWithVersion, new_totalSellingPrice))

for i in range(args.threads):
    in_que.put(("done", None, 0))

for i in range(args.threads):
    work_threadlist[i].join()

print("done")
for quote, price in answer:
    if price is None:
        print(f"Quote {quote}: FAIL")
    else:
        print(f"Quote {quote}, price: {price}")
