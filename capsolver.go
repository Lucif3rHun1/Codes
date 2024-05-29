package main

import (
	"fmt"
	"log"

	capsolver_go "github.com/capsolver/capsolver-go"
)

func main() {
	// first you need to install sdk
	//go get github.com/capsolver/capsolver-go
	//export CAPSOLVER_API_KEY='...' or
	//capSolver := CapSolver{ApiKey:"..."}

	capSolver := capsolver_go.CapSolver{}
	solution, err := capSolver.Solve(map[string]any{
        "type": "FunCaptchaTaskProxyLess",
        "websiteURL": "https://auth.max.com/login",
        "websitePublicKey": "B0217B00-2CA4-41CC-925D-1EEB57BFFC2F",
        "funcaptchaApiJSSubdomain": "https://wbd-api.arkoselabs.com",
        "data": "{\"blob\":\"qre0YLBJ0mHINdNu.L2rWFpQbtjQzcM9r7R8+obD6tXIcW/C4evFnqvWTNOhWpk/yQTubwVD4qs6afL4OLvtz77IifVm8qSo+bVTVWAEY/m39oc+rVJ+5D1SDG12ATHIbTw8GmF33Sr5hk3tPm7J4r4BdkJZLkBJpTXHF0pdS1bCEffc8c76Dj0LS+MtlEzB0JRINcKo8FPbY1RdfEInx8skaQMWHCBT7JMSgnmcM2EPn1FVYN07mWwk+HqOT9pL6/7rBxrFB3zYENgFlYqgAPMHLYFjS+tFInhA0ud5ntm3RGD//kR4v+7gRW6E/WWOWDgYvJ1/xKc0tgDWM8zkRq04EqmUs/2e13a+D18DGlOoe1ut8KR7qnngmfqraRnhs0yWIwZS10vZnNxqPYPHj9vwfCWIs4QIWUm/QmQblkOV1g3V7qYnLgsaq0cpniDML7rIy69KxJ11sQVgk12OpYuv5EF5OtA4qrkcz3mazVmTi0ImyvyX9HS5fpgbu+9cg9FPJdvSfSVKEvrFVOg18GtAGchrQ4e2LAdfXT4nYXfnW+oPvakJOH5zrR11e4nKkScUHxJeMfjfnG3R6eyIkHFOU2JouGrRn0KChv0RWYplt92f1d2mntTgN\"}",
    })
	if err != nil {
		log.Fatal(err)
		return
	}
	fmt.Println(solution)
}