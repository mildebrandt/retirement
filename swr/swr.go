package main

import (
	"fmt"
	"math"
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/PuerkitoBio/goquery"
)

const (
	bondFactor = 0.05
	peFactor   = 2.47
	mainFactor = 12.15
	bondURL    = "http://www.multpl.com/10-year-treasury-rate/table/by-year"
	peURL      = "http://www.multpl.com/shiller-pe/table"
)

func get(url string) (*http.Response, error) {
	client := &http.Client{
		Timeout: time.Duration(5 * time.Second),
	}

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}
	req.Header.Add("Cache-Control", "no-cache")

	res, err := client.Do(req)
	if err != nil {
		return nil, err
	}

	return res, err
}

func bondYield() (float64, error) {
	res, err := get(bondURL)
	doc, err := goquery.NewDocumentFromResponse(res)

	if err != nil {
		return 0.0, err
	}

	f, err := strconv.ParseFloat(strings.Trim(strings.TrimSpace(doc.Find("td").First().Next().Text()), "%"), 64)
	if err != nil {
		return 0.0, err
	}
	return f, nil
}

func getPE10() (float64, error) {
	res, err := get(peURL)
	doc, err := goquery.NewDocumentFromResponse(res)
	if err != nil {
		return 0.0, err
	}

	s := doc.Find("td").First().Next().Text()
	t := strings.TrimSpace(s)

	f, err := strconv.ParseFloat(t, 64)
	if err != nil {
		return 0.0, err
	}
	return f, nil
}

func main() {
	start := time.Now()
	pe10, err := getPE10()
	if err != nil {
		fmt.Println("OMG! PE Error: ", err)
		return
	}

	y, err := bondYield()
	if err != nil {
		fmt.Println("OMG! Bond Error: ", err)
		return
	}

	swr := mainFactor - peFactor*math.Log(pe10) + bondFactor*y
	brandonSWR := 3.5 + (30-pe10)/25*2
	end := time.Now()

	fmt.Printf("Bond yield: %0.2f%%\n", y)
	fmt.Printf("PE10: %0.2f\n", pe10)
	fmt.Printf("Safe withdrawl rate: %0.2f%%\n", swr)
	fmt.Printf("Brandon's safe withdrawl rate: %0.2f%%\n", brandonSWR)
	fmt.Printf("Total time: %0.2f\n", end.Sub(start).Seconds())
}
