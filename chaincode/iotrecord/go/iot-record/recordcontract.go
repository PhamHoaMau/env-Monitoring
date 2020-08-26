/*
 * SPDX-License-Identifier: Apache-2.0
 */

package iotrecord

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// Contract chaincode that defines
// the business logic for managing commercial
// record
type Contract struct {
	contractapi.Contract
}

// Instantiate does nothing
func (c *Contract) Instantiate(ctx TransactionContextInterface) {
	fmt.Println("Instantiated")
	// t := time.Now()
	// jsonstr := `{"id":"DANANG_1", "dateTime":"` + t.Format("2006-01-02 15:04:05") + `", "data":{"name":"TEMPERATURE","value":12,"unit":"%"}}`
	// rec := IoTRecord{}
	// err := rec.parseJSON(jsonstr)
	// if err == nil {
	// 	ctx.GetRecordList().AddRecord(&rec)
	// }

	// jsonstr = `{"id":"DANANG_1", "dateTime":"` + t.Add(time.Second*5).Format("2006-01-02 15:04:05") + `", "data":{"name":"HUMIDITY","value":40,"unit":"%"}}`
	// rec2 := IoTRecord{}
	// err = rec2.parseJSON(jsonstr)
	// if err == nil {
	// 	ctx.GetRecordList().AddRecord(&rec2)
	// }

	// jsonstr = `{"id":"DANANG_1", "dateTime":"` + t.Add(time.Second*10).Format("2006-01-02 15:04:05") + `", "data":{"name":"UV","value":20.5,"unit":"%"}}`
	// rec3 := IoTRecord{}
	// err = rec3.parseJSON(jsonstr)
	// if err == nil {
	// 	ctx.GetRecordList().AddRecord(&rec3)
	// }

	// jsonstr = `{"id":"USER_01", "dateTime":"` + t.Add(time.Second*20).Format("2006-01-02 15:04:05") + `", "data":{"login":"true"}}`
	// rec4 := IoTRecord{}
	// err = rec4.parseJSON(jsonstr)
	// if err == nil {
	// 	ctx.GetRecordList().AddRecord(&rec4)
	// }
	// jsonstr = `{"id":"USER_01", "dateTime":"` + t.Add(time.Second*30).Format("2006-01-02 15:04:05") + `", "data":{"logout":"true"}}`
	// rec5 := IoTRecord{}
	// err = rec5.parseJSON(jsonstr)
	// if err == nil {
	// 	ctx.GetRecordList().AddRecord(&rec5)
	// }
	// fmt.Print("Result from Instantiate:\n")
	// fmt.Println(ctx.GetRecordList())
}

// AddRecord to save record
func (c *Contract) AddRecord(ctx TransactionContextInterface, jsonStr string) error {
	fmt.Println("AddRecord")
	var err error
	if json.Valid([]byte(jsonStr)) {
		record := IoTRecord{}
		err = record.parseJSON(jsonStr)
		if err == nil {
			ctx.GetRecordList().AddRecord(&record)
		}
	} else {
		err = errors.New("Invalid JSON string")
	}
	return err
}

// QueryRecord used to query record from world state
func (c *Contract) QueryRecord(ctx TransactionContextInterface, ID string) (string, error) {
	fmt.Println("QueryRecord")
	payload, err := ctx.GetRecordList().GetRecord(ID)
	if err != nil {
		return "", err
	}
	record := bytes.NewBuffer(payload).String()
	fmt.Println("QueryRecord Result:")

	fmt.Println(record)
	// s := string(payload)
	return record, err
}

// QueryRecordHistoryByTimeRange query record by time range
func (c *Contract) QueryRecordHistoryByTimeRange(ctx TransactionContextInterface, ID string, start string, end string) (string, error) {
	payload, err := ctx.GetRecordList().GetHistoryForRecordByTimeRange(ID, start, end)
	if err != nil {
		return "", err
	}
	record := bytes.NewBuffer(payload).String()
	fmt.Println("QueryRecordHistoryByTimeRange Result:")

	fmt.Println(record)
	// s := string(payload)
	return record, err
}

// QueryRecordHistory query record by time range
func (c *Contract) QueryRecordHistory(ctx TransactionContextInterface, ID string) (string, error) {
	payload, err := ctx.GetRecordList().GetHistoryForRecord(ID)
	if err != nil {
		return "", err
	}
	record := bytes.NewBuffer(payload).String()
	fmt.Println("QueryRecordHistory Result:")

	fmt.Println(record)
	// s := string(payload)
	return record, err
}
