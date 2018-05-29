#!/usr/bin/env python3

import socket
import argparse
import logging

if __name__ == "__main__":

    # Parse Arguments                                                                                                                                                                                              
    parser = argparse.ArgumentParser()                                                                                                                                                                             
    parser.add_argument("-v", "--verbose", action='store_true', help="Turn on Verbosity")
    
    args = parser.parse_args()
    
    VERBOSE=args.verbose
    
    FORMAT="%(levelname)s %(asctime)s %(name)s : %(message)s"

    if VERBOSE == True :
        logging.basicConfig(level=logging.DEBUG,
                            format=FORMAT)
        # URLLib3 is too verbose!
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    else :
        logging.basicConfig(level=logging.ERROR,
                            format=FORMAT)
        logging.getLogger("pika").setLevel(logging.WARNING)
        logging.getLogger("paramiko").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    logger = logging.getLogger("miniserver.py")

if __name__ == "__main__":
    
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    serversocket.bind(("0.0.0.0", 23))
    
    serversocket.listen(5)
    
    logger.info("Server should be listening")
    logger.info(serversocket)
    
    while True:
        
        logger.info("In Loop Wating for Connection")
        (clientsocket, address) = serversocket.accept()
        
        try:
        
            logger.info("Recieved Connection : {}".format(address))
            
            current_word = ""
            
            while True:
                data = clientsocket.recv(16)
                try:
                    thischar = data.decode("utf-8")
                    logger.info("Recieved Data {}".format(thischar))
                    
                    if thischar.isalnum():
                        current_word += thischar
                    elif thischar == " ":
                        if current_word == "ping" :
                            # Return Pong
                            logger.info("Should return pong here")
                            pass
                        else:
                            logger.info("non ping word recieved. Blanking word")
                            current_word = ""
                    else:
                        # Do Nothing
                        pass
                    
                    logger.info(current_word)
                    
                except Exception as decode_error:
                    logger.info("Recieved non String Data {}".format(decode_error))
                
                
                if data:
                    clientsocket.sendall(data)
                else:
                    break
        finally:
            clientsocket.close()
        
        logger.info(clientsocket)
        logger.info(address)
        
