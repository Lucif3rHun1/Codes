package main

import (
    "crypto/sha256"
    "encoding/hex"
    "encoding/json"
)

type ResponseData struct {
    Sensor         string `json:"sensor"`
    AndroidVersion string `json:"androidVersion"`
}

func getbmp(client tls_client.HttpClient) ResponseData {
	req, err := http.NewRequest(http.MethodPost, "http://127.0.0.1:1337/akamai/bmp", strings.NewReader("{\"app\": \"com.ihg.apps.android\",\"lang\": \"en\",\"version\": \"3.3.4\"}"))
	if err != nil {
		log.Println(err)
	}
	resp, err := client.Do(req)
	if err != nil {
		log.Println(err)
	}
	defer resp.Body.Close()
	if err != nil {
		fmt.Errorf("error executing request: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Errorf("error reading response body: %w", err)
	}

	var responseData ResponseData
	err = json.Unmarshal(body, &responseData)
	if err != nil {
		fmt.Errorf("error unmarshalling response JSON: %w", err)
	}
	return responseData
}
