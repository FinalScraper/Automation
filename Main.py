from AutoSignup import SignUp, Login, NewAccount
from declerations import AddToFile
from colorama import Fore
import time

N = 140  # loop range
sim_cards = []

for _ in range(N):
    print(Fore.BLACK + "Starting..")
    phone, name = SignUp()  # sign up with new account
    sim = Login(phone, name)  # login and return the new sim object
    AddToFile(sim)
    print(f"Added {sim.name} to file. cleaning up...")
    NewAccount()
    time.sleep(1)
