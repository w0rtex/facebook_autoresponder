from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

username = input("Enter your username: ")
password = input("Enter your password: ")

print("Open the messanger conversation with your threat in the browser")
thread = str(input("Enter the thread ID (it comes after facebook.com/messanger/t/THREAT_ID): "))

# The logic
def react_to_message(message):
    print(f"{bcolors.OKBLUE}[+]{bcolors.ENDC} Reacting to message")

    if message == '':
        print(f"{bcolors.FAIL}[-]{bcolors.ENDC} Message is empty")
        return False

    # Find message field
    message = message.lower()

    if message.find('barev') > -1:
        send_message(driver, 'Բայլուս')
    elif message.find('inch ka') > -1:
        send_message(driver, 'Բան չէ, դու ասա')
    elif message.find('du asa') > -1:
        send_message(driver, 'Հլը սրան նայի, չէ դու ասա')
    else:
        send_message(driver, 'Հեսա գամ պատասխանեմ')

def send_message(driver, message):
    print(f"{bcolors.OKBLUE}[+]{bcolors.ENDC} Sending message")

    # Find message field
    message_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Message']"))
    )

    # Try to click on message field
    while True:
        try:
            message_field.click()
            break
        except:
            print("Wasn't able to click on message field")

        sleep(1)

    # Send message
    message_field.send_keys(message)
    message_field.send_keys(u'\ue007')

    print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Message sent")
    return True


# Terminal colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


options = Options()
#options.add_argument("--headless") # Hide browser
options.add_argument("--disable-notifications")

# service
s = Service(ChromeDriverManager().install())

# launching browser
driver = webdriver.Chrome(service = s, options=options)

driver.get("https://facebook.com")

print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Facebook login page loaded")

try:
    driver.find_element(By.ID, "email").send_keys(username)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "[name='login']").click()
    print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Facebook login successful")
except Exception as e:
    print(f"{bcolors.FAIL}[-]{bcolors.ENDC} Facebook login failed")
    print(e)
    driver.quit()
    exit()

# Get messanger
driver.get("https://www.facebook.com/messages/t/" + thread)

print(f"{bcolors.OKBLUE}[+]{bcolors.ENDC} Listening to messages")

while True:

    # print("-------------------------------------------------------")
    # print(last_messages_len)
    # print(len(current_messages))
    # print("iteration: " + str(i))
    # print('-------------------------------------------------------')

    try:
        check_new_messages = driver.find_element(By.CSS_SELECTOR, '[href="/messages/t/' + thread + '/"] .is6700om')
    except:
        sleep(.05)
        continue

    latest_message = driver.find_elements(By.CSS_SELECTOR, '[data-pagelet="MWV2MessageList"] [role="row"] [data-testid="message-container"] [style="background-color: var(--wash);"] [dir="auto"]')

    print(f"{bcolors.WARNING}[+]{bcolors.ENDC} New message")

    react_to_message(latest_message[-1].text)
    sleep(.1)
