import os
try:
    import requests
except:
    os.system("pip install requests")

def main():
    session = requests.Session()

    mail = input("Mail: ")
    passw = input("Şifre: ")

    login_url = "https://www.blutv.com/api/login"
    login_data = {
        "remember": "false",
        "username": mail,
        "password": passw,
        "captchaVersion": "v3",
        "captchaToken": ""
    }

    headers = {
        "Host": "www.blutv.com",
        "Connection": "keep-alive",
        "AppPlatform": "com.blu",
        "Content-Type": "text/plain;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
        "AppCountry": "TUR",
        "AppLanguage": "tr-TR",
        "Accept": "*/*",
        "Origin": "https://www.blutv.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.blutv.com/giris",
        "Accept-Language": "tr-TR,tr;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    response = session.post(url=login_url, json=login_data, headers=headers).json()
    access_token = response["accessToken"]
    refresh_token = response["refreshToken"]

    profiles_url = f"https://www.blutv.com/api/get-profiles?accessToken={access_token}&refreshToken={refresh_token}"
    profiles_data = session.get(profiles_url).json()

    ids = []
    names = []

    for profile in profiles_data["profiles"]:
        if not profile["isAccountOwner"]:
            _id = profile["_id"]
            name = profile["name"]
            ids.append(_id)
            names.append(name)

    print("Profile Options:")
    print("1. Delete all profiles")
    print("2. Delete a specific profile")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        delete_all_profiles(session, ids)
    elif choice == "2":
        delete_specific_profile(session, ids, names)
    else:
        print("Invalid choice")

def delete_all_profiles(session, ids):
    print(f"Deleting all profiles...")
    for _id in ids:
        delete_response = session.get(f"https://www.blutv.com/api/delete-profile?profileId={_id}")
        if delete_response.status_code == 200:
            print(f"Deleted profile: {_id}")
        else:
            print(f"Failed to delete profile: {_id}")

def delete_specific_profile(session, ids, names):
    selected_name = input(f"Enter the profile name to delete: ({', '.join(names)})")
    
    if selected_name in names:
        selected_id = ids[names.index(selected_name)]
        delete_response = session.get(f"https://www.blutv.com/api/delete-profile?profileId={selected_id}")
        
        if delete_response.status_code == 200:
            print(f"Deleted profile: {selected_name} ({selected_id})")
        else:
            print(f"Failed to delete profile: {selected_name} ({selected_id})")
    else:
        print("Invalid profile name")


if __name__ == "__main__":
    main()
