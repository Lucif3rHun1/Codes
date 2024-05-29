package main

import (
	"log"
	"net/http"
	"sync"

	"github.com/gorilla/websocket"
)

func main() {
	// Define the URL for the WebSocket connection
	url := "wss://xtco.xtb.com/websocket/909/sop1ctmy/websocket"
	log.Println("Connecting to WebSocket at:", url)

	// Create a request header and add the cookies
	header := http.Header{}
	header.Add("Cookie", "JSESSIONID=AC618766EC45AEE7511FF9BE9E1E1FDE")
	header.Add("Cookie", "CASTGC=TGT-2127150-iH2P9ZeGnbBLRHsNNYJhtDNcQGl4HrGCEUNyY0wN3sdUWCRRc3-xstation.xtb.com")

	// Dialer to establish a WebSocket connection
	dialer := websocket.DefaultDialer

	// Establishing the WebSocket connection
	conn, resp, err := dialer.Dial(url, header)
	if err != nil {
		if resp != nil {
			log.Println("HTTP Response Status:", resp.Status)
		}
		log.Fatal("Error connecting to WebSocket server:", err)
	} else {
		log.Println("Connected to WebSocket server")
	}
	defer conn.Close()

	// Create a wait group to synchronize message handling
	var wg sync.WaitGroup

	// Function to send a message and print received messages twice
	sendAndPrint := func(message string) {
		defer wg.Done()

		// Send the message
		err := conn.WriteMessage(websocket.TextMessage, []byte(message))
		if err != nil {
			log.Println("Error sending message:", err)
			return
		}
		log.Printf("Sent message: %s\n", message)

		// Read and print received messages twice
		for i := 0; i < 2; i++ {
			messageType, message, err := conn.ReadMessage()
			if err != nil {
				log.Println("Error reading from WebSocket:", err)
				return
			}
			log.Printf("Received message: Type: %d, Message: %s\n", messageType, message)
		}
	}

	// Send the first message
	wg.Add(1)
	firstMessage := "CONNECT\naccept-version:1.1,1.0\nheart-beat:30000,30000\n\n\u0000"
	go sendAndPrint(firstMessage)
	// Wait for the first message handling to complete
	wg.Wait()

	// Send the second message
	wg.Add(1)
	translateMessage := "SEND\ndestination:/app/logs\ncontent-length:60\n\n{\"level\":\"info\",\"message\":\"TranslationService load started\"}\u0000"
	go sendAndPrint(translateMessage)
	wg.Wait()
	secondMessage := "SUBSCRIBE\nid:/app/topic/init\ndestination:/app/topic/init\n\n\u0000"
	go sendAndPrint(secondMessage)

	// Wait for the second message handling to complete
	wg.Wait()
}
