import asyncio
import argparse
from requests import get
import json
import logging
import pytest
from billiard import Pool

# Add logger for the task
logging.basicConfig(filename="AsyncioBilliarTask.log ", filemode="w", level=logging.INFO)
logger = logging.getLogger('my_logger')


def check_misspelled(keyword, suggestions):
    miss_spelled = True
    if keyword in suggestions:
        miss_spelled = False
    elif len(keyword) <= 2:
        miss_spelled = False
    else:
        res = None
        for j in suggestions:
            if res is None or len(j) < len(res):
                res = j
        if len(keyword) > len(res):
            miss_spelled = True
    # Now if miss spelled True then shorrtest suggestion is the correct keyword
    smallest_suggestion = None
    if miss_spelled:
        for k in suggestions:
            if smallest_suggestion is None or len(k) < len(keyword):
                smallest_suggestion = k

    return {
        "keyword": keyword,
        "suggestions": suggestions,
        "misspelled": miss_spelled,
        "correct_keyword": smallest_suggestion
    }

# hit api
# create an async function
async def fetch_suggestions(target_keyword):
    api =  get(f"http://suggestqueries.google.com/complete/search?client=firefox&q={target_keyword}")
    # we to show our data in json form
    jason_data = api.json()
    # now i want to separate keyword and suggetion only no need of extra data 
    keyword = jason_data[0]
    suggestions = jason_data[1]
    return (keyword, suggestions)


async def fetch_all_suggestions(keywords):
    all_results = await asyncio.gather(*[fetch_suggestions(keyword) for keyword in keywords])
    return all_results


def proess_results(keywords):

    results = asyncio.run(fetch_all_suggestions(keywords))
    with Pool() as pool:
        x = pool.starmap(check_misspelled, results)
    return x

if __name__ == '__main__':

    # pass Argument using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('my_list', nargs='+')
    args = parser.parse_args()
    keywords = args.my_list

    results = proess_results(keywords)
    # print(results)
    results = json.dumps(results, indent=4)
    logger.info(results)


    # for result in results:
    #     # print(check_misspelled(result[0], result[1]))
    #       print(result)































# class MyTestCase(TestCase):

#     def test_check_misspelled1(self):
#         result = check_misspelled("python", ["python", "pyhton", "pyth"])
#         self.assertEqual(result["misspelled"], False) 

#     def test_check_misspelled2(self):
#         result = check_misspelled("ijaz", ["Ijaz Ahmad", "Ijazat", "ijazat lyrics"])
#         self.assertEqual(result["misspelled"], True) 

#     def test_check_misspelled3(self):
#         result = check_misspelled("saad", ["Saad", "Saad Lamjarred", "Saadi Sherazi"])
#         self.assertEqual(result["misspelled"], True) 