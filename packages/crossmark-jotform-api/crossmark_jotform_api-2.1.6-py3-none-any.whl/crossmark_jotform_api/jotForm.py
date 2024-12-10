"""## [JOTFORM API DOCS](https://www.api.jotform.com)"""

# pylint: disable=C0115, C0116, C0103
from abc import ABC
from datetime import datetime
from typing import Union, Dict
from urllib.parse import quote
from time import sleep
import requests
from requests.exceptions import RequestException


class JotForm(ABC):
    def __init__(self, api_key, form_id, timeout=45, debug=False):
        self.update_timestamp = datetime.now().timestamp()
        self.api_key = api_key
        self.form_id = form_id
        self.url = (
            "https://api.jotform.com/form/"
            + form_id
            + "/submissions?limit=1000&apiKey="
            + api_key
        )
        self.set_url_param("offset", "0")
        self.submission_ids = set()
        self.submission_data = {}
        self.updating_process = False
        self.submission_count = 0
        self.submissions = lambda: [
            i.to_dict() for k, i in self.submission_data.copy().items()
        ]
        self.timeout = timeout
        self.debug = debug
        self.set_data()

    def _print(self, text):
        if self.debug:
            print(text)

    def __set_get_submission_data(self, submissions):
        submissions_dict = {}
        for i in submissions:
            submissions_dict[i["id"]] = JotFormSubmission(i)
        return submissions_dict

    def get_submission_ids(self):
        return self.submission_ids

    def __set_submission_ids(self):
        """This function sets the submission memory. It is used for easier for loop for submissions.
        It is called in the constructor, and time to time in other functions"""
        self.submission_ids = set()
        for _, value in self.submission_data.copy().items():
            self.submission_ids.add(value.id)

    def set_submission_count(self):
        self.submission_count = len(self.submission_ids)

    def get_submission_data(self):
        self.update()
        return self.submission_data

    def get_submission_count(self):
        return self.submission_count

    def get_submission_answers(self, submission_id):
        self.update()
        return self.submission_data[submission_id].answers

    def get_submission_by_request(self, submission_id):
        url = (
            f"https://api.jotform.com/submission/{submission_id}?apiKey={self.api_key}"
        )
        response = requests.get(url, timeout=self.timeout)
        if response.status_code == 200:
            response = response.json()
            return response["content"]
        else:
            return None

    def get_submission(self, submission_id: Union[int, str]):
        return self.submission_data[submission_id]

    def get_submission_id_by_text(
        self, text: str, answer_text: str
    ) -> Union[int, None]:
        for _, submission_object in self.submission_data.copy().items():
            if submission_object.get_answer_by_text(text)["answer"] == answer_text:
                return submission_object
        return None

    def get_submission_by_case_id(self, case_id, tried=0):
        for _, submission_object in self.submission_data.copy().items():
            if submission_object.case_id == case_id:
                return submission_object
        if not tried:
            self.request_submission_by_case_id(case_id)
            return self.get_submission_by_case_id(case_id, 1)
        return None

    def get_answer_by_text(self, submission_id, text):
        try:
            return self.get_submission(submission_id).get_answer_by_text(text)
        except KeyError:
            self.update()
            return self.get_submission(submission_id).get_answer_by_text(text)

    def get_answer_by_name(self, submission_id, name):
        try:
            return self.get_submission(submission_id).get_answer_by_name(name)
        except KeyError:
            self.update()
            return self.get_submission(submission_id).get_answer_by_name(name)

    def get_answer_by_key(self, submission_id, key):
        try:
            return self.get_submission(submission_id).get_answer_by_key(key)
        except KeyError:
            self.update()
            return self.get_submission(submission_id).get_answer_by_key(key)

    def get_submission_answers_by_question(self, submission_id):
        self.update()
        submission_answers = self.get_submission_answers(submission_id)
        submission_answers_by_question = {}
        for answer in submission_answers:
            submission_answers_by_question[answer["id"]] = answer["answer"]
        return submission_answers_by_question

    def get_submission_answers_by_question_id(self, submission_id):
        self.update()
        submission_answers = self.get_submission_answers(submission_id)
        submission_answers_by_question_id = {}
        for answer in submission_answers:
            submission_answers_by_question_id[answer["id"]] = answer["answer"]

    def get_list_of_questions(self):
        """## jotform endpoint of form/{id}/questions

        ### Returns:
            - `object` or 'bool': questions list if successful, false if not
        """
        url = f"https://api.jotform.com/form/{self.form_id}/questions?apiKey={self.api_key}"
        response = requests.get(url, timeout=self.timeout)
        if response.status_code == 200:
            response = response.json()
            return response["content"]
        return None

    def delete_submission(self, submission_id):
        url = (
            f"https://api.jotform.com/submission/{submission_id}?apiKey={self.api_key}"
        )
        response = requests.delete(url, timeout=self.timeout)
        if response.status_code == 200:
            del self.submission_data[submission_id]
            return True
        return False

    def create_submission(self, submission):
        """## This function creates a submission in Jotform
        then sets the new submission to the submission data.

        ### Args:
            - `submission (pseudo sumbission dictionary)`:
               {
                    "submission[1]": "value",
                    "submission[2]": "value",
                    ...
               }

        ### Returns:
            - `bool` or 'string': new created submission's id if successful, false if not
        """
        url = f"https://api.jotform.com/form/{self.form_id}/submissions?apiKey={self.api_key}"
        response = requests.post(url, data=submission, timeout=self.timeout)
        if response.status_code == 200:
            response = response.json()
            _id = response["content"]["submissionID"]
            submission = self.get_submission_by_request(_id)
            self.set_new_submission(submission)
            return _id
        return False

    def create_submission_using_another(self, submission_data, submission_to_copy):
        """## This function creates a submission in Jotform
        then sets the new submission to the submission data.

        ### Args:
            - `submission_data (sumbission dictionary)`:
            contains name value pairs of the submission
            e.g:
               {
                    "data": "value",
                    "data2": "value",
                    ...
               }
            - submission_to_copy (JotFormSubmission): submission object to copy

        ### Returns:
            - `bool`: true if successful, false if not
        """
        data = {}
        questions = self.get_list_of_questions()
        for q in questions:
            name = questions[q]["name"]
            if name in submission_data:
                data[f"submission[{q}]"] = submission_data[name]
            else:
                answer = submission_to_copy.get_answer_by_name(name)["answer"]
                if answer:
                    data[f"submission[{q}]"] = answer
        return self.create_submission(data)

    def update_submission_answer(
        self, submission_id: Union[int, str], field_id: str, answer: Union[int, str]
    ) -> bool:
        """## This function updates the answer of the submission

        ### Args:
            - `submission_id (Union[int, str])`: _description_
            - `field_id (str)`: _description_
            - `answer (Union[int, str])`: _description_

        ### Returns:
            - `bool`: True if successful, False if not
        """
        if isinstance(answer, list):
            data = {f"submission[{field_id}][]": answer}
            response = requests.post(
                f"https://api.jotform.com/submission/{submission_id}",
                params={"apiKey": self.api_key},
                data=data,
                timeout=self.timeout,
            )
        else:
            query = f"submission[{field_id}]={answer}"
            url = f"https://api.jotform.com/submission/{submission_id}"
            url += f"?apiKey={self.api_key}&{query}"
            response = requests.post(url, timeout=self.timeout)
        if response.status_code == 200:
            self.submission_data[submission_id].set_answer(field_id, answer)
            return True
        return False

    def set_url_param(self, key: str, value: str) -> None:
        """## This function sets the url parameter

        ### Args:
            - `key (string)`: key to set into the url
            - `value (string)`: value to set into the url
        """
        value = str(value)
        if key in self.url:
            params = self.url.split("&")
            for i, param in enumerate(params):
                if key in param:
                    params[i] = key + "=" + value
            self.url = "&".join(params)
        else:
            self.url += "&" + key + "=" + value

    def _sort_submission_data_by_id(self):
        """
        Sorts the submission data by id
        """
        sorted_tuples = sorted(
            self.submission_data.copy().items(), key=lambda x: x[1].id, reverse=True
        )
        sorted_dict = {k: v for k, v in sorted_tuples}
        self.submission_data = sorted_dict

    def set_data(self, try_again: int = 0) -> None:
        """## This function sets the data from the Jotform API

        ### Args:
            - `try_again (int, optional)`: if fails try again for x times. Defaults to 0.

        ### Returns:
            - `None`: if fails
            - `True`: if successful
        """
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)

            self.data = response.json()
            count = self.data["resultSet"]["count"]
            self.submission_data.update(
                self.__set_get_submission_data(self.data["content"])
            )
            if count == self.data["resultSet"]["limit"]:
                self.set_url_param("offset", self.data["resultSet"]["offset"] + count)
                sleep(0.33)
                return self.set_data()

            self.set_global_data()
            return True

        except RequestException as e:
            self._print(f"Request failed: {e}")
            if try_again < 3:
                sleep(1)
                return self.set_data(try_again + 1)
            return None

        except KeyError as e:
            self._print(f"KeyError: {e}")
            return None

    def set_global_data(self) -> None:
        self._sort_submission_data_by_id()
        self.__set_submission_ids()
        self.set_submission_count()
        self.set_url_param("offset", "0")

    def request_submission_by_case_id(self, case_id):
        """
        Requests the submission by case id
        this function is used when the submission is not in the submission data
        """
        query = quote(f"""{{"q221:matches:answer":"{case_id}"}}""")
        url = f"https://api.jotform.com/form/{self.form_id}/submissions"
        url += f"?apiKey={self.api_key}&filter={query}"
        response = requests.get(url, timeout=self.timeout)
        if response.status_code != 200:
            return None
        _json = response.json()
        return _json

    def set_new_submission(self, submission):
        self.submission_data.update(self.__set_get_submission_data([submission]))
        self.set_global_data()

    def get_form(self):
        """
        Gets form data directly from Jotform so there is no data diffirence on this function.
        It is slow since we are requesting data from Jotform.

        Returns:
            _type_: either JSON or None
        """
        url = f"https://api.jotform.com/form/{self.form_id}?apiKey={self.api_key}"
        response = requests.get(url, timeout=self.timeout)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_submissions_count(self):
        form = self.get_form()
        if form:
            return int(form["content"]["count"])
        return 1

    def update(self, force=False):
        if not self.updating_process:
            self.updating_process = True
            count = self.get_submissions_count()
            if count <= self.submission_count and not force:
                self._print("[INFO] No new submissions.")
            else:
                now = datetime.now().timestamp()
                its_been = now - self.update_timestamp
                self._print(
                    f"[INFO] Update started. Last update was {int(its_been/60)} minutes ago."
                )
                self.set_data()
                self.update_timestamp = now
            self.updating_process = False

    def get_user_data_by_email(self, email):
        if not email:
            return None
        email = email.lower()
        self.update()
        submissions = []
        for _, submission in self.submission_data.copy().items():
            submission_object = self.get_submission(submission.id)
            email_objects = [i.lower() for i in submission_object.emails if i]
            if email in email_objects:
                submissions.append(submission_object)
        return submissions


class JotFormSubmission(ABC):
    """Base class for JotFormSubmission.
    Takes a submission object and creates a submission object from it.

    Args:
        ABC (_type_): parent class
    """

    def __init__(self, submission_object):
        self.id = submission_object["id"]
        self.form_id = submission_object["form_id"]
        self.ip = submission_object["ip"]
        self.created_at = submission_object["created_at"]
        self.status = submission_object["status"]
        self.new = submission_object["new"]
        self.flag = submission_object["flag"]
        self.notes = submission_object["notes"]
        self.updated_at = submission_object["updated_at"]
        self.answers = submission_object["answers"]
        self._clear_answers()
        self.answers_arr = self.set_answers(self.answers)
        self.case_id = self.get_answer_by_text("CASE")["answer"]
        self.store = self.get_answer_by_text("STORE")["answer"]
        self.client = self.get_answer_by_text("CLIENT")["answer"]
        self.emails = self.get_emails()

    def set_answers(self, answers) -> list:
        answers_arr = []
        for key, value in answers.items():
            name = None
            if "name" in value:
                name = value["name"]
            answer = None
            if "answer" in value:
                answer = value["answer"]
            _type = None
            if "type" in value:
                _type = value["type"]
            text = None
            if "text" in value:
                text = value["text"]
            file = None
            if "file" in value:
                file = value["file"]
            answers_arr.append(
                {
                    "key": key,
                    "name": name,
                    "answer": answer,
                    "type": _type,
                    "text": text,
                    "file": file,
                }
            )
        return answers_arr

    def _clear_answers(self) -> None:
        """## process of getting rid of unnecessary keys in the answers dictionary"""
        for _, answer in self.answers.items():
            if "maxValue" in answer:
                del answer["maxValue"]
            if "order" in answer:
                del answer["order"]
            if "selectedField" in answer:
                del answer["selectedField"]
            if "cfname" in answer:
                del answer["cfname"]
            if "static" in answer:
                del answer["static"]
            if "type" in answer and answer["type"] != "control_email":
                del answer["type"]
            if "sublabels" in answer:
                del answer["sublabels"]
            if "timeFormat" in answer:
                del answer["timeFormat"]

    def set_answer(self, answer_id: str, answer_value: str) -> None:
        """## sets answer value for the given answer id

        ### Args:
            - `answer_id (str)`: order integer of the answer
            - `answer_value (str)`: value you want to set for the answer
        """

        for i, answer in enumerate(self.answers_arr):
            if answer["key"] == answer_id:
                self.answers_arr[i]["answer"] = answer_value
        self.answers[answer_id]["answer"] = answer_value

    def get_answers(self) -> list:
        """## returns the answers array

        ### Returns:
            - `list`: answers array
        """
        return self.answers_arr

    def get_answer_by_text(self, text: str) -> dict:
        """## This function gets the answer by text
         Sensetive to the text, if the text is not exactly the same, it will return None

        ### Args:
            - `text (str)`: text element to search for

        ### Returns:
            - `dict`: jotform return object
            {
                "key": "key",
                "name": "name",
                "answer": "answer",
                "type": "type",
                "text": "text",
                "file": "file"
            }
        """
        for answer in self.answers_arr:
            if answer["text"] and text and answer["text"].upper() == text.upper():
                _answer = answer.copy()
                if not answer["answer"]:
                    _answer["answer"] = None
                return _answer
        return {"answer": None}

    def get_answer_by_name(self, name: str) -> dict:
        for answer in self.answers_arr:
            if answer["name"] and name and answer["name"] == name:
                _answer = answer.copy()
                if not answer["answer"]:
                    _answer["answer"] = None
                return _answer
        return {"answer": None}

    def get_answer_by_key(self, key: str) -> dict:
        for answer in self.answers_arr:
            if answer["key"] and key and answer["key"] == key:
                _answer = answer.copy()
                if not answer["answer"]:
                    _answer["answer"] = None
                return _answer
        return {"answer": None}

    def get_emails(self):
        """
            Unsafe call, ideally this function should not even exists,
                instead it periodically set itself after updates and always should be generic
        Returns:
            _type_: emails array
        """
        # unsafe method
        emails = []
        for answer in self.answers_arr:
            if "type" not in answer:
                continue
            if answer["type"] == "control_email":
                emails.append(answer["answer"])
        return emails

    def get_day_from_date(self, date):
        # YYYY-MM-DD hh:mm:ss
        now = datetime.now()
        return (now - datetime.strptime(date, "%Y-%m-%d %H:%M:%S")).days

    def get_store_number_from_store(self, store):
        return store.split(" | ")[0]

    def to_dict(self):
        return {
            "id": self.id,
            "form_id": self.form_id,
            "ip": self.ip,
            "created_at": self.get_day_from_date(self.created_at),
            "status": self.get_answer_by_text("STATUS")["answer"],
            "new": self.new,
            "flag": self.flag,
            "notes": self.notes,
            "updated_at": self.updated_at,
            "case_id": self.case_id,
            "store": self.store,
            "store_number": self.get_store_number_from_store(self.store),
            "client": self.client,
            "emails": self.get_emails(),
        }

    def turn_into_american_datetime_format(
        self,
        date: Union[str, Dict[str, str], datetime],
        cur_frmt: str = "%Y-%m-%d %H:%M:%S",
        end_frmt: str = "%m/%d/%Y %I:%M %p",
    ) -> str:
        if isinstance(date, dict):
            date = date.get("answer") or date.get("datetime")

        if isinstance(date, str):
            date = datetime.strptime(date, cur_frmt)

        if isinstance(date, datetime):
            return date.strftime(end_frmt)

        raise ValueError("Invalid date format")

    def text_to_html(self, text):
        if not text:
            return None
        text = text.replace("\r\n", "<br>")  # Convert Windows-style line breaks
        text = text.replace("\n", "<br>")  # Convert Unix-style line breaks
        text = text.replace("\r", "<br>")  # Convert Mac-style line breaks
        paragraphs = text.split("<br><br>")  # Split the text into paragraphs

        html = ""
        for paragraph in paragraphs:
            html += "<p>" + paragraph + "</p>"
        return html

    def split_domain_from_email(self, email: str):
        """if @ in email, split and return the first part of the string

        Args:
            email (str): string with @ in it

        Returns:
            _type_: first half of an email address.
            e.g: 'test' from 'test@test.com'
        """
        if not email:
            return None
        elif "@" in email:
            return email.split("@")[0]
        else:
            return email

    def get_value(self, obj):
        if isinstance(obj, str):
            return obj.strip()
        elif isinstance(obj, dict):
            if "answer" in obj:
                answer = obj["answer"]
                if isinstance(answer, list):
                    return answer[0]
                return answer
            elif len(obj) > 1:
                return obj
            elif len(obj) == 1:
                return next(iter(obj.values()))
        else:
            return None
