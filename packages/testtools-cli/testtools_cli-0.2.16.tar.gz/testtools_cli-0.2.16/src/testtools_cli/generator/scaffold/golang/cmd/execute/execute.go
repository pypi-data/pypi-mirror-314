package execute

import (
	"replace_____me/pkg/util"
	"time"

	"github.com/OpenTestSolar/testtool-sdk-golang/client"
	"github.com/OpenTestSolar/testtool-sdk-golang/model"
	"github.com/pkg/errors"
	"github.com/spf13/cobra"
)

type ExecuteOptions struct {
	executePath string
}

// NewExecuteOptions NewBuildOptions new build options with default value
func NewExecuteOptions() *ExecuteOptions {
	return &ExecuteOptions{}
}

// NewCmdExecute NewCmdBuild create a build command
func NewCmdExecute() *cobra.Command {
	o := NewExecuteOptions()
	cmd := cobra.Command{
		Use:   "execute",
		Short: "Execute testcases",
		RunE: func(cmd *cobra.Command, args []string) error {
			return o.RunExecute(cmd)
		},
	}
	cmd.Flags().StringVarP(&o.executePath, "path", "p", "", "Path of testcase info")
	_ = cmd.MarkFlagRequired("path")
	return &cmd
}

func reportTestResults(fileReportPath string, testResults []*model.TestResult) error {
	reporter, err := client.NewReporterClient(fileReportPath)
	if err != nil {
		return errors.Wrap(err, "failed to create reporter")
	}
	for _, result := range testResults {
		err := reporter.ReportCaseResult(result)
		if err != nil {
			return errors.Wrap(err, "failed to report load result")
		}
	}
	return nil
}

func (o *ExecuteOptions) RunExecute(cmd *cobra.Command) error {
	var testResults []*model.TestResult
	config, err := util.UnmarshalCaseInfo(o.executePath)
	if err != nil {
		return errors.Wrapf(err, "failed to pasrse case info")
	}
	// 1. __TODO__: execute test cases based on `config`
	// The following are the parameters that need attention:
	//   config.TestSelectors: expected list of test cases to execute, possibly with multiple inputs
	//   example:
	//     - tests                                 // expected test case directory to be executed
	//     - tests/test_hello.py                   // expected test case file to be executed
	//     - tests/test_hello.py?name=MathTest     // expected test case to be executed
	//     - tests/test_hello.py?MathTest/test_add // equivalent to the previous example, the 'name' parameter can be omitted
	//   config.ProjectPath: test cases root directory, example: /data/workspace
	//   config.TaskId: task id, as the unique identifier for this task, example: task-xxx
	//   config.FileReportPath: local test case result save file path, example: /data/report
	time.Sleep(1)

	// 2. __TODO__: After test cases had been executed, construct the test case results and report.
	// TestResult: test case execution result
	//     Test: test case name
	//           Name: name of testcase, example: tests/test_hello.py?MathTest/test_add
	//           Attributes: test case attributes, represented in key-value pair form
	//     StartTime: test case start time
	//     EndTime: test case end time
	//     ResultType: execution result of the test case
	//     TestCaseStep: execution steps of the test case,
	//                   one test case result can contain multiple steps,
	//                   and each step can contain multiple logs
	//                   Title: step name
	//                   Steps: test case logs in current step
	//                   [
	//                       TestCaseStep: single test case log
	//                           Time: record time
	//                           Level: log level
	//                           Content: log content
	//                   ]
	//                   StartTime: step start time
	//                   EndTime: step end time
	//                   ResultType: step result
	err = reportTestResults(config.FileReportPath, testResults)
	if err != nil {
		return errors.Wrapf(err, "failed to report test results")
	}
	return nil
}
