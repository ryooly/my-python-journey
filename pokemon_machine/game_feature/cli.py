import asyncio
import requests
from game_feature.math_quiz import run_quiz
from pokemon_hunter.calling import get_pokemon

API_BASE = "http://localhost:8000"

def _input(prompt: str) -> str:
    """Thin wrapper so every input() call lives in one place."""
    return input(prompt).strip()

def do_register() -> dict | None:
    print("\n--- Register ---")
    name       = _input("Name       : ")
    age        = _input("Age        : ")
    personality = _input("Personality: ")
    password   = _input("Password   : ")

    try:
        res = requests.post(
            f"{API_BASE}/auth/register",
            json={
                "name": name,
                "age": int(age),
                "personality": personality,
                "password": password,
            },
        )

        if res.ok:
            print("\n  Registration successful! You may now log in.")
            return None  # no auto-login; user picks Login from the menu
        else: 
            body = res.json()
            print(f"\n  Registration failed: {body.get('message', res.text)}")
            return None

    except requests.exceptions.ConnectionError:
        print("\n  Cannot reach the server. Is it running?")
        return None

def do_login() -> dict | None:
    print("\n--- Login ---")
    name     = _input("Name     : ")
    password = _input("Password : ")

    try:
        res = requests.post(
            f"{API_BASE}/auth/login",
            json={"name": name, "password": password},
        )

        if res.ok:
            data = res.json()
            print(f"\n  Welcome back, {name}!")
            return data  # { owner: {...}, access_token: "..." }
        else:
            body = res.json()
            print(f"\n  Login failed: {body.get('message', res.text)}")
            return None

    except requests.exceptions.ConnectionError:
        print("\n  Cannot reach the server. Is it running?")
        return None


def do_logout(session: dict) -> None:
    owner = session.get("owner", {})
    user_id = owner.get("id")

    try:
        res = requests.post(
            f"{API_BASE}/auth/logout",
            json={"user_id": str(user_id)},
        )

        if res.ok:
            print("\n  Logged out successfully.")
        else:
            body = res.json()
            print(f"\n  Logout error: {body.get('message', res.text)}")

    except requests.exceptions.ConnectionError:
        print("\n  Cannot reach the server. Is it running?")

async def do_get_pokemon(session: dict) -> None:
    owner = session.get("owner", {})
    pokemon_count = owner.get("pokemon_count", 0)
    pokemon_limit = owner.get("pokemon_limit", 3)

    if pokemon_count >= pokemon_limit:
        print(f"\n  You already have {pokemon_count}/{pokemon_limit} Pokemon.")
        print("  Your storage is full! Release one before catching a new one.")
        return

    print(f"\n  You have {pokemon_count}/{pokemon_limit} Pokemon. Let's go!")
    
    pokemon_id = run_quiz()

    try:
        result = await get_pokemon(pokemon_id)

        if result:
            types = ", ".join(t["name"].capitalize() for t in result.types)
            abilities = ", ".join(a["name"].replace("-", " ").title() for a in result.abilities)

            stats_map = {s["name"]: s["base_stat"] for s in result.stats}
            hp = stats_map.get("hp", "?")
            attack = stats_map.get("attack", "?")
            defense = stats_map.get("defense", "?")
            speed = stats_map.get("speed", "?")

            print(f"\n  ╔══════════════════════════════════════╗")
            print(f"    You caught {result.name.upper()}! (#{result.pokeapi_id})")
            print(f"  ╚══════════════════════════════════════╝")
            print(f"    Type       : {types}")
            print(f"    Abilities  : {abilities}")
            print(f"    Height     : {result.height / 10} m")
            print(f"    Weight     : {result.weight / 10} kg")
            print(f"    Base EXP   : {result.base_experience}")
            print(f"\n    Stats")
            print(f"      HP      : {hp}")
            print(f"      Attack  : {attack}")
            print(f"      Defense : {defense}")
            print(f"      Speed   : {speed}")
        else:
            print(f"\n  No Pokemon found for ID #{pokemon_id}.")

    except Exception as exc:
        print(f"\n  Something went wrong while catching a Pokemon: {exc}")

def _entry_menu() -> str:
    print("\n===========================================")
    print("            POKEMATE  -  CLI               ")
    print("===========================================")
    print("  1. Login")
    print("  2. Register")
    print("  0. Exit")
    return _input("\n  Choose > ")


def _main_menu(name: str) -> str:
    print(f"\n===========================================")
    print(f"  Hello, {name}!")
    print(f"===========================================")
    print("  1. Get Pokemon")
    print("  2. Logout")
    return _input("\n  Choose > ")

async def main():
    session: dict | None = None

    while True:
        if session is None:
            choice = _entry_menu()

            if choice == "1":
                session = do_login()
            elif choice == "2":
                do_register()
            elif choice == "0":
                print("\n  Goodbye!")
                break
            else:
                print("\n  Invalid choice.")

        else:
            owner = session.get("owner", {})
            choice = _main_menu(owner.get("name", "Trainer"))

            if choice == "1":
                await do_get_pokemon(session)
            elif choice == "2":
                do_logout(session)
                session = None
            else:
                print("\n  Invalid choice.")


if __name__ == "__main__":
    asyncio.run(main())