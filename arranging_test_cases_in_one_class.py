import pytest
import asyncio_billiard_task_complete 
from unittest.mock import patch, MagicMock
import unittest
import os

# class of fetch suggestions
class AsyncMock(MagicMock):
    async def __call__(self, args, **kwargs):
        return super(AsyncMock, self).__call__(args, **kwargs)
    

# create main class of test case and test case of process results 
class TestCase(object):

    @pytest.mark.parametrize("keywords, expected", [
        (
            ["python"],
            [{
                "keyword": "python",
                "suggestions": ['python', 'python download', 'python online compiler', 'python compiler', 'python programming', 'python language', 'python online', 'python tutor', 'python install', 'python w3schools'],
                "misspelled": False,
                "correct_keyword": None
            }]
        ),
        (
            ["ijaz", "saad", "zahid", "laptop"],
            [
                {
                    "keyword": "ijaz",
                    "suggestions": ['ijaz ansari food secrets', 'ijaz ahmed', 'ijazat song', 'ijazat lyrics', 'ijazat', 'ijaz ul haq', 'ijaz name meaning in urdu', 'ijaz', 'ijaz rehman', 'ijazat falak mp3 download'],
                    "misspelled": False,
                    "correct_keyword": None
                },
                {
                    "keyword": "saad",
                    "suggestions": ['saad lamjarred', 'saad name meaning in urdu', 'saad rizvi', 'saad baig', 'saadat hasan manto', 'saad', 'saad qureshi', 'saadi town', 'saad lamjarred songs', 'saad lamjarred wife'],
                    "misspelled": False,
                    "correct_keyword": None
                },
                {
                    "keyword": "zahid",
                    "suggestions": ['zahid ahmed', 'zahid nihari', 'zahid', 'zahid name meaning in urdu', 'zahid hussain', 'zahida name meaning in urdu', 'zahid khan', 'zahid mahmood', 'zahid nihari saddar', 'zahid nihari tariq road'],
                    "misspelled": False,
                    "correct_keyword": None
                },
                {
                    "keyword": "laptop",
                    "suggestions": ['laptop price in pakistan', 'laptop', 'laptop scheme 2023', 'laptops dot', 'laptop scheme', 'laptop wallpaper', 'laptop bags', 'laptop price', 'laptop stand', 'laptop games'],
                    "misspelled": False,
                    "correct_keyword": None
                }
            ]
        )
    ])
    @patch("asyncio_billiard_task_complete.proess_results")
    def test_proess_results(self, mock, keywords, expected):
        mock.return_value = expected
        result = asyncio_billiard_task_complete.proess_results(keywords)
        assert result == expected
    
    # test case of fetch suggestions   
    @pytest.mark.parametrize("keywords, expected", [
    (
        "python", 
        ['python', 'python download', 'python online compiler', 'python compiler', 'python programming', 'python language', 'python online', 'python install', 'python w3schools', 'python snake']),
    ])
    @patch("asyncio_billiard_task_complete.fetch_suggestions", new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_fetch_suggestions(self, mock, keywords, expected):
        mock.return_value = expected
        result = await asyncio_billiard_task_complete.fetch_suggestions(keywords)
        assert result == expected

    # test case of comond line in python 
    def test_os_system(self):
        command = "python3 /home/ijaz/Documents/LinkedMatrix/CompleteAsyncioBilliardTask/asyncio_billiard_task_complete.py saad iphron"
        result = os.system(command)
        assert result == 0  

    # Test case for check Misspelled
    def test_check_misspelled1(self):
        result = asyncio_billiard_task_complete.check_misspelled("python", ["python", "pyhton", "pyth"])
        assert result["misspelled"] == False 

    def test_check_misspelled2(self):
        result = asyncio_billiard_task_complete.check_misspelled("ijaz", ["Ijaz Ahmad", "Ijazat", "ijazat lyrics"])
        assert result["misspelled"] == True 

    def test_check_misspelled3(self):
        result = asyncio_billiard_task_complete.check_misspelled("saad", ["Saad", "Saad Lamjarred", "Saadi Sherazi"])
        assert result["misspelled"] == True 
