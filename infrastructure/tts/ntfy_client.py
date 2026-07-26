import requests
import json


class NtfyClient:

    BASE_URL = "https://ntfy.sh"


    def __init__(self, channel: str):

        self.channel = channel


    def get_latest_message(self):

        url = (
            f"{self.BASE_URL}/"
            f"{self.channel}/json"
        )


        try:

            response = requests.get(
                url,
                params={
                    "poll": "1",
                    "since": "24h"
                },
                timeout=15
            )


            response.raise_for_status()


            messages = []


            for line in response.text.splitlines():

                if not line.strip():
                    continue


                try:

                    data = json.loads(line)

                    if data.get("event") == "message":

                        messages.append(
                            data.get("message")
                        )

                except json.JSONDecodeError:
                    continue



            if not messages:
                return None



            return messages[-1]


        except Exception as e:

            print(
                f"[⚠️ Ntfy] Ne mogu da pročitam kanal: {e}"
            )

            return None