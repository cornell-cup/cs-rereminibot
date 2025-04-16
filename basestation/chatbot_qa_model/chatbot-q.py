''' Run this script to test that the server at the url is working.
'''
import requests
if __name__ == "__main__":
    # set your url here
    url = "http://10.48.143.231:8881/qa"
    while True:
        context = input(
            "Please enter the context you would like Minibot to know.\n")
        question = input(
            "\nPlease enter the question you would like to ask Minibot.\n")
        json = {"question": question, "context": context}
        response = requests.get(url=url, json=json)
        print(f"\nMinibot answers: {response.text}")
