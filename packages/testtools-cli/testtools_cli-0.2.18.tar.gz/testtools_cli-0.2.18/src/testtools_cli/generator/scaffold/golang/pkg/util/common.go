package util

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/OpenTestSolar/testtool-sdk-golang/model"
)

func UnmarshalCaseInfo(path string) (*model.EntryParam, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read case info failed, err: %v", err)
	}
	var config model.EntryParam
	err = json.Unmarshal(data, &config)
	if err != nil {
		return nil, fmt.Errorf("unmarshal case info into model failed, err: %v", err)
	}
	return &config, nil
}
