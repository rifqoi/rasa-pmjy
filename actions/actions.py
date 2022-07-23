# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"


from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, FormValidationAction, ValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
from dotenv import load_dotenv
import requests
import os

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

load_dotenv()
TOKEN = os.environ.get("TOKEN")


class ActionPostKeluhan(Action):
    def name(self) -> Text:
        return "action_post_keluhan"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        head = {"Authorization": "Bearer " + TOKEN}
        isi_keluhan = tracker.get_slot("isi_keluhan")
        alamat = tracker.get_slot("alamat_lengkap")
        keterangan = tracker.get_slot("keterangan_keluhan")
        data = {
            "feedback_type": isi_keluhan,
            "comments": keterangan,
        }
        url = "https://apigw.withoracle.cloud/pamjaya/feedback/feedback/"

        response = requests.post(url, json=data, headers=head)
        print(response)

        dispatcher.utter_message("Keluhan kakak berhasil dikirim!")

        return []


class ActionDenyKeluhan(Action):
    def name(self) -> Text:
        return "action_deny_keluhan"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        pass


class ActionResetAllSlots(Action):
    def name(self) -> Text:
        return "action_reset_all_slots"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # events = tracker.current_state()["events"]
        # user_events = []
        # for e in events:
        #     if e["event"] == "user":
        #         user_events.append(e)

        # print(tracker.latest_message.get("metadata")["token"])

        return [AllSlotsReset()]


class ValidateKeluhan(Action):
    def name(self) -> Text:
        return "action_validate_keluhan"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        last_intent = tracker.get_intent_of_latest_message()
        if last_intent == "air_mati":
            msg_text = "Air Mati"
        else:
            msg_text = None

        return [SlotSet("isi_keluhan", msg_text)]


class ValidateKeluhanForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_keluhan_form"

    # async def required_slots(
    #     self,
    #     slots_mapped_in_domain: List[Text],
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,
    # ) -> Optional[List[Text]]:
    #     if isi_keluhan in list_keluhan:
    #         return ["keluhan_benar"] + slots_mapped_in_domain
    #     return slots_mapped_in_domain

    # async def extract_keluhan_benar(
    #     self,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,
    # ) -> Dict[Text, Any]:
    #     intent = tracker.get_intent_of_latest_message()
    #     print("extract", intent)
    #     if intent == "affirm":
    #         return {
    #             "keluhan_benar": intent == "affirm",
    #         }
    #     elif intent == "deny":
    #         return {
    #             "keluhan_benar": intent == "deny",
    #         }

    # async def validate_keluhan_benar(
    #     self,
    #     slot_value: Any,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,
    # ) -> Dict[Text, Any]:
    #     if tracker.get_slot("keluhan_benar"):
    #         print("validatae", tracker.get_slot("keluhan_benar"))
    #         return {
    #             "keluhan_benar": True,
    #             "isi_keluhan": "",
    #         }
    #     return {
    #         "keluhan_benar": None,
    #     }

    async def validate_isi_keluhan(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Text:
        list_keluhan = ["Air Mati", "Air Kecil", "Administrasi"]
        isi_keluhan = tracker.slots.get("isi_keluhan")

        if isi_keluhan == "air_mati":
            msg_text = "Air Mati"
        elif isi_keluhan == "air_kecil":
            msg_text = "Air Kecil"
        elif isi_keluhan == "administrasi":
            msg_text = "Administrasi"
        else:
            msg_text = None

        if isi_keluhan not in list_keluhan:
            return {"isi_keluhan", msg_text}

        buttons = [
            {"payload": "/air_mati", "title": "1. Air Mati"},
            # {"payload": "/air_kecil", "title": "2. Air Kecil"},
            # {"payload": "/administrasi", "title": "3. Administrasi"},
            # {"payload": "/keluhan_lainnya", "title": "4. Lainnya"},
        ]

        dispatcher.utter_message("Kakak mau komplain tentang apa?", buttons=buttons)
        return {"isi_keluhan", None}
