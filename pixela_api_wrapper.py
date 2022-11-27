"""pixela api wrapper"""
import datetime as dt
import time
import webbrowser
import json
import requests
import os

now = dt.datetime.now()
TODAY= now.today()
stringftime = TODAY.strftime("%Y%m%d")

PIXELA_ENDPOINT = "https://pixe.la/v1/users"

def openwebpage():
    webbrowser.open(url=f"https://pixe.la/@{username}")

print(f"Welcome to Pixela Api Wrapper. \nToday is {TODAY.strftime('%A, %B the %dth')}")
input("Press any key to continue!")
time.sleep(1.2)

new_user_mode = True

while new_user_mode is True:

    try:
        with open("tokendat.json","r") as file:
            data = json.load(file)

    except FileNotFoundError:
        time.sleep(1)
        print("No user data found! \n Running new user mode")
        new_user_question = input("Do you already have a user account in pixela? ").lower()

        if new_user_question in ("no", "n"):
            token = input("please create your api token: ")
            username = input("please create your username: ")
            agreeTermsOfService = input("type yes or no whether you agree to the terms of service.: ")
            notMinor = input("Specify yes or no as to whether you are not a minor: ")

            user_data_json = {
            "token":token,
            "username":username
            }

            user_data = {
            "token":token,
            "username":username,
            "agreeTermsOfService":agreeTermsOfService,
            "notMinor": notMinor
            }

            with open("tokendat.json","w") as file:
                json.dump(user_data_json,file)

            response = requests.post(PIXELA_ENDPOINT, json=user_data)
            response.raise_for_status()
            print(response.text)
            break

        elif new_user_question in ("yes", "y"):
            token = input("please enter your api token: ")
            username = input("please enter your username: ")
            user_data = {
            "token":token,
            "username":username
            }
            try:
                with open("tokendat.json","w") as file:
                    json.dump(user_data,file)
                    break
            except FileNotFoundError:
                print("User file does not exist. Moving on.")
                break

        elif new_user_question not in ("yes","y","no","n"):
            print("invalid response!")
            continue

    else:
        with open("tokendat.json","r") as file:
            data = json.load(file)
            token = data["token"]
            username = data["username"]
            break



PIXELA_USER_PROFILE_ENDPOINT = f"https://pixe.la/@{username}"
PIXELA_UPDATE_USER_TOKEN_ENDPOINT = f"https://pixe.la/v1/users/{username}"

HEADERS = {
    "X-USER-TOKEN": token
}

GRAPH_ENDPOINT = f"{PIXELA_UPDATE_USER_TOKEN_ENDPOINT}/graphs"

while True:

    print("Select an option (type the corresponding number and press enter)")
    main_menu_selection = input("""1: User Options  \n2: View User Profile
3: Graph Options \n4: Pixel Options (post to a graph) \n5: Exit\n""")

    if main_menu_selection not in ("1","2","3","4","5"):
        print("\ninvalid input! \nPlease select a valid input.")
        continue

    elif main_menu_selection in ("5"):
        exit()

    elif main_menu_selection in ("1"):
        print("Select an option.")
        user_submenu_selection = input("1: Update token \n2: Delete user account \n3: Main Menu\n")

        if user_submenu_selection not in ("1","2","3"):
            print("\ninvalid input! \nPlease select a valid input.")
            continue

        elif user_submenu_selection in ("3"):
            print("Exiting to main menu")
            continue

        elif user_submenu_selection in ("1"):
            HEADERS = {
                "X-USER-TOKEN": token
            }
            new_user_token = input("Please enter your new token: ")
            user_parameters = {

                "newToken": new_user_token
            }
            response = requests.put(PIXELA_UPDATE_USER_TOKEN_ENDPOINT, json=user_parameters,headers=HEADERS )
            response.raise_for_status()
            print(response.text)

            user_data = {
                "token":new_user_token,
                "username":username
            }
            with open("tokendat.json","w") as file:
                json.dump(user_data,file)

        elif user_submenu_selection in ("2"):
            last_chance = input("Are you sure you want to delete your user account? (type yes or no) \nThis action cannot be undone! ").lower()
            if last_chance not in ("yes","no"):
                print("Exiting to main menu")
                continue
            elif last_chance in ("no"):
                print("Exiting to the main menu")
                continue
            elif last_chance in ("yes"):
                print("deleting user")
                HEADERS = {
                    "X-USER-TOKEN": token
                }
                response = requests.delete(PIXELA_UPDATE_USER_TOKEN_ENDPOINT,headers=HEADERS)
                response.raise_for_status()
                print(response.text)
                try:
                    os.remove("tokendat.json")
                except OSError:
                    print("Unable to delete tokendat.json")

    elif main_menu_selection in ("2"):
        openwebpage()

    elif main_menu_selection in ("3"):
        print("Please Select a graph option!")
        graph_menu_selection = input("""1: Create a graph \n2: Get graph definitions
3: Delete a graph \n4: Main Menu """)

        if graph_menu_selection not in ("1","2","3","4"):
            print("invalid selection.")
            continue

        elif graph_menu_selection in "1":
            new_graph_id = input("name your graphs id code/name(Cannot contain spaces or special characters)").lower()
            new_graph_name = input("name your graphs name (this is different from your graph id)").lower()
            unit_measurement = input("It is a unit of the quantity recorded in the pixelation graph. \n Ex. commits, weight, calories,pages written or read per day").lower()
            graph_color = input("Defines the display color of the pixel in the pixelation graph.\n(shibafu (green) / momiji (red) / sora (blue) / ichou (yellow) / ajisai(purple) / kuro(black) supported)").lower()
            graph_params = {
                "id":new_graph_id,
                "name":new_graph_name,
                "unit":unit_measurement,
                "type":"float",
                "color":graph_color
            }

            response = requests.post(url = GRAPH_ENDPOINT, json = graph_params, headers = HEADERS)
            response.raise_for_status()
            print(response.text)

            time.sleep(1.5)
            webbrowser.open(url=f"{GRAPH_ENDPOINT}/{new_graph_id}.html")
            continue

        elif graph_menu_selection in ("2"):
            response = requests.get(url = GRAPH_ENDPOINT, headers = HEADERS)
            # TODO: SLICE REQUEST DATA TO SHOW ONLY PERTINENT DATA
            response.raise_for_status()
            print(response.text)
            continue

        elif graph_menu_selection in ("3"):
            to_delete_graph_id = input("please enter the graphID of the graph you want to delete.")
            response = requests.delete(url = f"{GRAPH_ENDPOINT}/{to_delete_graph_id}", headers = HEADERS)
            response.raise_for_status()
            print(response.text)
            continue

        elif graph_menu_selection in ("4"):
            print("exiting to the main menu.")
            continue

    elif main_menu_selection in ("4"):
        print("Please Select an Option!")
        pixel_selection_menu = input("1: Post a Pixel \n2: Update a Pixel Post \n3: Delete a Pixel Post \n4: Main Menu")

        if pixel_selection_menu not in ("1","2","3","4"):
            print("invalid command! Returning to main menu")

        elif pixel_selection_menu in ("1"):
            graphid = input("please enter the graphID of the graph you want to post a pixel to.")
            pixel_post = {

                "date":  TODAY.strftime("%Y%m%d"),
                "quantity": input("add your progress in the form of a floating point number for today.")

            }
            response = requests.post(url = f"{GRAPH_ENDPOINT}/{graphid}", json = pixel_post, headers = HEADERS)
            print(response.text)
            webbrowser.open(url = f"{GRAPH_ENDPOINT}/{graphid}.html")
            time.sleep(1.2)
            continue

        elif pixel_selection_menu in ("2"):
            date_to_update = input("please specify the date you want to update example: 20220529 (note it must be yearmonthday in number format only)")
            graphid = input("please enter the graphID of the graph you want to post a pixel to.")
            updated_numbers = input("enter the new measurement or progress for the specified date.")
            update_put = {
                "quantity":updated_numbers
            }
            response = requests.put(url = f"{GRAPH_ENDPOINT}/{graphid}/{date_to_update}", json = update_put, headers = HEADERS)
            response.raise_for_status()
            print(response.text)
            webbrowser.open(url = f"{GRAPH_ENDPOINT}/{graphid}.html")
            continue

        elif pixel_selection_menu in ("3"):
            date_to_update = input("please specify the date you want to delete a pixel post example: 20220529 (note it must be yearmonthday in number format only)")
            graphid = input("please enter the graphID of the graph you want to delete a pixel from.")
            response = requests.delete(url = f"{GRAPH_ENDPOINT}/{graphid}/{date_to_update}", headers = HEADERS)
            response.raise_for_status()
            print(response.text)
            continue

        elif pixel_selection_menu in ("4"):
            continue
