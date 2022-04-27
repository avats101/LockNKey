from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
from tkinter import filedialog
from decimal import Decimal
import os
# from __future__ import print_function
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import random
from decimal import Decimal

FIELD_SIZE = 10 ** 3

SCOPES = ['https://www.googleapis.com/auth/drive']


def drive_init():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'secretdesk.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    return service


def search_file(service):
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)",
                                   q="name='encrypted.txt'").execute()
    items = results.get('files', [])
    op = ""

    if not items:
        print('No files found.')
    else:
        print('The File has been found.')
        for item in items:
            # print(u'{0} ({1})'.format(item['name'], item['id']))
            print(f"File Name : {item['name']} File ID : {item['id']}")
            op = item['id']
    return op


def upload_file(service):
    # Uploading a File
    file_metadata = {'name': "encrypted.txt"}
    filePath = "encrypted.txt"
    media = MediaFileUpload(filePath, mimetype="text/plain")
    file = service.files().create(body=file_metadata,
                                  media_body=media, fields='id').execute()
    fileID = file.get('id')
    print('File ID: ' + fileID)


def download_file(service, fileid):
    # Downloading A File
    print(f"The file is being downloaded. It will be stored in the downloads folder.")
    request = service.files().get_media(fileId=fileid)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open("Downloads/encrypted.txt", "wb") as f:
        fh.seek(0)
        f.write(fh.read())


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def coeff(t, secret):
    coeffs = [random.randrange(0, FIELD_SIZE) for _ in range(t - 1)]
    coeffs.append(secret)
    return coeffs


def polynom(x, coeffs):
    point = 0
    for coefficient_index, coefficient_value in enumerate(coeffs[::-1]):
        point += x ** coefficient_index * coefficient_value
    return point


def create_shares(a, b, secret):
    coeffs = coeff(b, secret)
    shares = []
    for i in range(1, a + 1):
        x = i
        shares.append((x, polynom(x, coeffs)))
        with open("shares.txt", "w", encoding='utf8') as fout:
            for i in shares:
                fout.write(str(i) + "\n")
    return shares


def reconstruct_secret(shares):
    sums = 0
    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)
        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                prod *= Decimal(Decimal(xi) / (xi - xj))
        prod *= yj
        sums += Decimal(prod)
    return int(round(Decimal(sums), 0))


# ########################## ########################## ########################## #########################
#  _____ _   _  ____ ______   ______ _____ ___ ___  _   _
# | ____| \ | |/ ___|  _ \ \ / /  _ \_   _|_ _/ _ \| \ | |
# |  _| |  \| | |   | |_) \ V /| |_) || |  | | | | |  \| |
# | |___| |\  | |___|  _ < | | |  __/ | |  | | |_| | |\  |
# |_____|_| \_|\____|_| \_\|_| |_|    |_| |___\___/|_| \_|
# ########################## ########################## ########################## #########################
class App1(ttk.Frame):
    """ This application Performs the encryption process on the txt file """

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.service = drive_init()

    def createWidgets(self):
        # text variables

        self.n = StringVar()
        self.t = StringVar()
        self.inp = StringVar()

        # labels
        self.label1 = ttk.Label(self, text="Enter the total number of shares you wish to make :").grid(
            row=0, column=0, sticky=W)
        self.label2 = ttk.Label(self,
                                text="Enter the threshold number of shares required to reconstruct the key :").grid(
            row=1, column=0, sticky=W)
        self.label3 = ttk.Label(self, text="Your keys are:").grid(
            row=2, column=0, sticky=W)
        self.label4 = ttk.Label(self, text="Selected file is:")
        self.label4.grid(
            row=4, column=0, sticky=W)
        # text boxes
        self.textbox1 = ttk.Entry(self, textvariable=self.n).grid(
            row=0, column=1, sticky=E)
        self.textbox2 = ttk.Entry(self, textvariable=self.t).grid(
            row=1, column=1, sticky=E)

        self.textbox4 = Text(self, width=40, height=20)
        self.textbox4.grid(
            row=3, column=1, sticky=E, ipady=0)
        # buttons
        self.button1 = ttk.Button(self, text="Ok", command=self.encrypt).grid(
            row=5, column=1, sticky=E)
        self.button_explore = Button(self,
                                     text="Browse",
                                     command=self.browseFiles).grid(row=5, column=0, sticky=E)

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                              title="Select a File",
                                              filetypes=(("Text files",
                                                          "*.txt*"),
                                                         ("all files",
                                                          "*.*")))
        self.inp.set(filename)
        # Change label contents
        self.label4.configure(text="File Opened: " + filename)

    def encrypt(self):
        p = 13
        q = 31
        r = 157
        s = 173
        n = p * q * r
        totient = (p - 1) * (q - 1) * (r - 1)*(s-1)
        e = d = -1
        ct = 0
        for i in range(2, totient):
            if ct == 1:
                break
            if gcd(i, totient) == 1:
                e = i
                ct += 1
        ed = 1
        while True:
            ed = ed + totient
            if ed % e == 0:
                d = int(ed / e)
                break
        try:
            numOfShares = int(self.n.get())
            threshold = int(self.t.get())
            shares = create_shares(numOfShares, threshold, d)
            txt = ''
            for i in shares:
                txt = txt + str(i) + '\n'

            self.textbox4.insert(
                END, "The shares are as follows \nPlease store them securely.\n")
            self.textbox4.insert(END, txt)

            with open(str(self.inp.get()), "r", encoding='utf8') as fin:
                message = fin.read()
            print(f"The message in the file is :\n{message}")
            msg = [ord(i) for i in message]
            enc = [pow(i, e, n) for i in msg]
            print("\nThe encrypted message is :")
            with open("encrypted.txt", "w", encoding='utf8') as fout:
                for i in enc:
                    fout.write(chr(i))
                    print(chr(i), end="")
            upload_file(self.service)
        except ValueError:
            messagebox.showinfo("Error", "You can only use numbers.")
        finally:
            self.n.set("")
            self.t.set("")


# ########################## ########################## ########################## #########################
#  ____  _____ ____ ______   ______ _____ ___ ___  _   _
# |  _ \| ____/ ___|  _ \ \ / /  _ \_   _|_ _/ _ \| \ | |
# | | | |  _|| |   | |_) \ V /| |_) || |  | | | | |  \| |
# | |_| | |__| |___|  _ < | | |  __/ | |  | | |_| | |\  |
# |____/|_____\____|_| \_\|_| |_|    |_| |___\___/|_| \_|
# ########################## ########################## ########################## #########################

class App2(ttk.Frame):
    """ Application to Perform decryption """

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.service = drive_init()

    def createWidgets(self):
        # text variables

        self.n = StringVar()
        self.t = StringVar()
        self.inp = StringVar()

        self.variable = StringVar()
        # labels
        # self.label1 = ttk.Label(self, text="Enter the total number of shares you posess :").grid(
        #     row=0, column=0, sticky=W)
        # self.label2 = ttk.Label(self, text="Enter the threshold number of shares required to reconstruct the key :").grid(
        #     row=1, column=0, sticky=W)
        self.label3 = ttk.Label(self, text="Your keys are:").grid(row=2, column=0, sticky=W)
        # self.label4 = ttk.Label(self, text="Selected file is:")
        # self.label4.grid(
        #     row=4, column=0, sticky=W)

        # text boxes
        # self.textbox1 = ttk.Entry(self, textvariable=self.n).grid(
        #     row=0, column=1, sticky=E)
        # self.textbox2 = ttk.Entry(self, textvariable=self.t).grid(
        #     row=1, column=1, sticky=E)

        self.textbox4 = Text(self, width=40, height=20)
        self.textbox4.grid(row=3, column=1, sticky=E, ipady=0)
        OPTIONS = [i for i in range(1, 101) ]

        # self.variable.set(OPTIONS[0])
        # self.w = OptionMenu(self, self.variable, *OPTIONS)
        # self.w.grid(row=0, column=1, sticky=E)
        # buttons
        self.button1 = ttk.Button(self, text="Ok", command=self.decrypt).grid(row=5, column=1, sticky=E)
        # self.button_explore = Button(self,
        #                              text="Browse",
        #                              command=self.browseFiles).grid(row=4, column=0, sticky=E)
        # self.button3 = Button(self, text="checkbutton", command=self.ok)
        # self.button3.grid(row=6, column=1)

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                              title="Select a File",
                                              filetypes=(("Text files",
                                                          "*.txt*"),
                                                         ("all files",
                                                          "*.*")))
        self.inp.set(filename)
        self.label4.configure(text="File Opened: " + filename)

    def decrypt(self):
        id = search_file(self.service)
        download_file(self.service, id)
        p = 13
        q = 31
        r = 157
        s = 173
        n = p * q * r
        totient = (p - 1) * (q - 1) * (r - 1)*(s-1)

        # t = int(input('Enter the number of shares you have :'))
        # t = int(self.variable.get())
        # print(t)
        shares = []
        st = self.textbox4.get(1.0, END)
        shares = st.split('\n')[:-1]
        print(shares)
        for i in range(len(shares)):
            shares[i] = shares[i][1:-1]
            shares[i] = tuple(map(int, shares[i].split(',')))
        print(shares)

        # for i in range(t):
        #     ind = int(input("Enter the index number of the share : "))
        #     val = int(input("Enter the value of the share : "))
        #     print()
        #     shares.append((ind, val))
        d = reconstruct_secret(shares)

        with open("encrypted.txt", "r", encoding='utf8') as fin:
            encmsg = fin.read()
        print(f"\nThe encrypted message is :\n{encmsg}")
        enc = [ord(i) for i in encmsg]
        dec = [pow(i, d, n) for i in enc]
        print("\nThe decrypted message is :")
        with open("decrypted.txt", "w", encoding='utf8') as fout:
            for i in dec:
                fout.write(chr(i))
                print(chr(i), end="")
        print()


window = Tk()
w = 770  # width for the Tk root
h = 450  # height for the Tk root

# get screen width and height
ws = window.winfo_screenwidth()  # width of the screen
hs = window.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk window window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

# set the dimensions of the screen
# and where it is placed
window.geometry('%dx%d+%d+%d' % (w, h, x, y))

# window.mainloop()  # starts the mainloop
# window.geometry(f"{x}x{y}")

# Setup the notebook (tabs)
notebook = ttk.Notebook(window)

frame1 = ttk.Frame(notebook, width=w, height=h)

frame2 = ttk.Frame(notebook, width=w, height=h)
notebook.add(frame1, text="Encrypt")
notebook.add(frame2, text="Decrypt")
notebook.grid()

# Create tab frames
app1 = App1(master=frame1)
app1.grid()
app2 = App2(master=frame2)
app2.grid()

# Main loop
window.mainloop()
