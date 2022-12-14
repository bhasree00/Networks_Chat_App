# So far this is being done following this tutorial (https://www.youtube.com/watch?v=ytu2yV3Gn1I)
# Or alternatively, this corresponding article (https://pythonprogramming.net/client-chatroom-sockets-tutorial-python-3/?completed=/server-chatroom-sockets-tutorial-python-3/)
import socket
import select
import errno
import pygame as pg
from googletrans import Translator
translator = Translator()

WHITE = (255,255,255)
BLACK = (0,0,0)

HEADER_LENGTH = 10

IP = "127.0.0.1" # input("IP: ") # Needs to be "127.0.0.1"
PORT = 1234 # input("Port: ") # Needs to be 1234
MY_USERNAME = input("Username: ")
MY_LANGUAGE = input("Language: ")


languages = [
    "aa",
"ab",
"af",
"ak",
"sq",
"am",
"ar",
"an",
"hy",
"as",
"av",
"ae",
"ay",
"az",
"ba",
"bm",
"eu",
"be",
"bn",
"bh",
"bi",
"bo",
"bs",
"br",
"bg",
"my",
"ca",
"cs",
"ch",
"ce",
"zh",
"cu",
"cv",
"kw",
"co",
"cr",
"cy",
"cs",
"da",
"de",
"dv",
"nl",
"dz",
"el",
"en",
"eo",
"et",
"eu",
"ee",
"fo",
"fa",
"fj",
"fi",
"fr",
"fy",
"ff",
"Ga",
"de",
"gd",
"ga",
"gl",
"gv",
"el",
"gn",
"gu",
"ht",
"ha",
"he",
"hz",
"hi",
"ho",
"hr",
"hu",
"hy",
"ig",
"is",
"io",
"ii",
"iu",
"ie",
"ia",
"id",
"ik",
"is",
"it",
"jv",
"ja",
"kl",
"kn",
"ks",
"ka",
"kr",
"kk",
"km",
"ki",
"rw",
"ky",
"kv",
"kg",
"ko",
"kj",
"ku",
"lo",
"la",
"lv",
"li",
"ln",
"lt",
"lb",
"lu",
"lg",
"mk",
"mh",
"ml",
"mi",
"mr",
"ms",
"Mi",
"mk",
"mg",
"mt",
"mn",
"mi",
"ms",
"my",
"na",
"nv",
"nr",
"nd",
"ng",
"ne",
"nl",
"nn",
"nb",
"no",
"oc",
"oj",
"or",
"om",
"os",
"pa",
"fa",
"pi",
"pl",
"pt",
"ps",
"qu",
"rm",
"ro",
"ro",
"rn",
"ru",
"sg",
"sa",
"si",
"sk",
"sk",
"sl",
"se",
"sm",
"sn",
"sd",
"so",
"st",
"es",
"sq",
"sc",
"sr",
"ss",
"su",
"sw",
"sv",
"ty",
"ta",
"tt",
"te",
"tg",
"tl",
"th",
"bo",
"ti",
"to",
"tn",
"ts",
"tk",
"tr",
"tw",
"ug",
"uk",
"ur",
"uz",
"ve",
"vi",
"vo",
"cy",
"wa",
"wo",
"xh",
"yi",
"yo",
"za",
"zh",
"zu"
]
while MY_LANGUAGE.lower() not in languages:
    print("Wrong Input, Please input the your language in two letters please")
    MY_LANGUAGE = input("Language: ")
    
    
MY_LANGUAGE = ' [' + MY_LANGUAGE + ']'

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
MY_USERNAME = MY_USERNAME + MY_LANGUAGE
username = MY_USERNAME.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)



def main():
    screen = pg.display.set_mode((640, 480))
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    color = pg.Color(WHITE)

    screenMode = 1 # 1 - Send message, 2 - Display message, 3 - Quit
    while True:
        if screenMode == 1: # Send message mode
            screenMode = sendMessage(screen, font, clock, color)
        elif screenMode == 2: # Display received message mode
            screenMode = displayMessage(screen, font, clock, color)
        elif screenMode == 3: # Quit mode
            return

def sendMessage(screen, font, clock, color):
    text = ""
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 3
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    print(f'{MY_USERNAME} > {text}')
                    # Wait for user to input a message
                    # message = input(f'{MY_USERNAME} > ')
                    message = text
                    text = ''
                    # If message is not empty - send it
                    if message:
                        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                        message = message.encode('utf-8')
                        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(message_header + message)
                        return 2
                elif event.key == pg.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        
        screen.fill(BLACK)
        thing_to_print = MY_USERNAME + " > " + text
        txt_surface = font.render(thing_to_print, True, color)
        screen.blit(txt_surface, (50, 100))

        pg.display.flip()
        clock.tick(30)

def displayMessage(screen, font, clock, color):
    # client_socket.send("\n".encode('utf-8'))
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 3
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return 1
        # print("Reached here")
        try:
            # Now we want to loop over received messages (there might be more than one) and print them
            # while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            # if not len(username_header):
            #     print('Connection closed by the server')
            #     continue

            try:
                # Convert header to int value
                username_length = int(username_header.decode('utf-8').strip())
            except:
                continue
            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')
           
            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            responseText = client_socket.recv(message_length).decode('utf-8')
            
            first_val = MY_LANGUAGE.index('[')
            second_val = MY_LANGUAGE.index(']')

            language_val = MY_LANGUAGE[first_val + 1:second_val]

            translations = translator.translate([responseText], dest = language_val)
            for translation in translations:
                new_val = translation.text
            # Print message
            print(f'{username} > {new_val}')
            #print(f'{username} > {new_response_text}')
            # return 1
        except BlockingIOError as e:
            continue
        # except IOError as e:
        #     # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        #     # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        #     # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        #     # If we got different error code - something happened
        #     if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
        #         print('Reading error: {}'.format(str(e)))
        #         sys.exit()

        #     # We just did not receive anything
        #     print("What the fuck")
        #     return 3
        # except Exception as e:
        #     # Any other exception - something happened, exit
        #     print('Reading error: '.format(str(e)))
        #     sys.exit()
        
        screen.fill(BLACK)
        thing_to_print = MY_USERNAME + " > "
        txt_surface = font.render(thing_to_print, True, color)
        screen.blit(txt_surface, (50, 200))

        thing_to_print = new_val + " < " + username
        txt_surface = font.render(thing_to_print, True, color)
        screen.blit(txt_surface, (350, 200))

        pg.display.flip()
        clock.tick(30)



if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()

