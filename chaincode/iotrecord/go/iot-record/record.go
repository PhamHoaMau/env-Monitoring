/*
 * SPDX-License-Identifier: Apache-2.0
 */

package iotrecord

import (
	"encoding/json"
	"fmt"
	"sort"

	ledgerapi "jwclab/iotrecord/ledger-api"
)

// CreateIoTRecordKey creates a key for commercial papers
func CreateIoTRecordKey(ID string) string {
	return ledgerapi.MakeKey(ID)
}

// IoTRecord defines an IOT record
type IoTRecord struct {
	ID       string                 `json:"id"`
	DateTime string                 `json:"dateTime"`
	Data     map[string]interface{} `json:"data"`
}

func (rec *IoTRecord) parseJSON(jsonString string) error {
	bytes := []byte(jsonString)
	err := json.Unmarshal(bytes, &rec)
	if err != nil {
		return err
	}
	// err = json.Unmarshal(bytes, &rec.Data)
	// if err != nil {
	// 	return err
	// }
	// delete(rec.Data, "id")
	// delete(rec.Data, "dateTime")
	return nil
}

// By ...
type By func(p1, p2 *IoTRecord) bool

// Sort ...
func (by By) Sort(records []IoTRecord) {
	ps := &recordSorter{
		records: records,
		by:      by, // The Sort method's receiver is the function (closure) that defines the sort order.
	}
	sort.Sort(ps)
}

// planetSorter joins a By function and a slice of Planets to be sorted.
type recordSorter struct {
	records []IoTRecord
	by      func(p1, p2 *IoTRecord) bool // Closure used in the Less method.
}

// Len is part of sort.Interface.
func (s *recordSorter) Len() int {
	return len(s.records)
}

// Swap is part of sort.Interface.
func (s *recordSorter) Swap(i, j int) {
	s.records[i], s.records[j] = s.records[j], s.records[i]
}

// Less is part of sort.Interface. It is implemented by calling the "by" closure in the sorter.
func (s *recordSorter) Less(i, j int) bool {
	return s.by(&s.records[i], &s.records[j])
}

// GetKey returns values which should be used to form key
func (rec *IoTRecord) GetKey() string {
	return rec.ID
}

// Serialize formats the commercial paper as JSON bytes
func (rec *IoTRecord) Serialize() ([]byte, error) {
	return json.Marshal(rec)
}

// Deserialize formats the commercial paper from JSON bytes
func Deserialize(bytes []byte, cp *IoTRecord) error {
	err := json.Unmarshal(bytes, cp)

	if err != nil {
		return fmt.Errorf("Error deserializing commercial paper. %s", err.Error())
	}

	return nil
}
