package discover

import (
	"replace_____me/pkg/testcase"
	"replace_____me/pkg/util"

	"time"

	"github.com/OpenTestSolar/testtool-sdk-golang/client"
	"github.com/OpenTestSolar/testtool-sdk-golang/model"
	"github.com/pkg/errors"
	"github.com/spf13/cobra"
)

type DiscoverOptions struct {
	discoverPath string
}

// NewDiscoverOptions NewBuildOptions new build options with default value
func NewDiscoverOptions() *DiscoverOptions {
	return &DiscoverOptions{}
}

// NewCmdDiscover NewCmdBuild create a build command
func NewCmdDiscover() *cobra.Command {
	o := NewDiscoverOptions()
	cmd := cobra.Command{
		Use:   "discover",
		Short: "Discover testcases",
		RunE: func(cmd *cobra.Command, args []string) error {
			return o.RunDiscover(cmd)
		},
	}
	cmd.Flags().StringVarP(&o.discoverPath, "path", "p", "", "Path of testcase info")
	_ = cmd.MarkFlagRequired("path")
	return &cmd
}

func reportTestcases(fileReportPath string, testcases []*testcase.TestCase, loadErrors []*model.LoadError) error {
	var tests []*model.TestCase

	reporter, err := client.NewReporterClient(fileReportPath)
	if err != nil {
		return errors.Wrapf(err, "failed to create reporter")
	}
	for _, testcase := range testcases {
		tests = append(tests, &model.TestCase{
			Name:       testcase.GetSelector(),
			Attributes: testcase.Attributes,
		})
	}
	err = reporter.ReportLoadResult(&model.LoadResult{
		Tests:      tests,
		LoadErrors: loadErrors,
	})
	if err != nil {
		return errors.Wrap(err, "failed to report load result")
	}
	return nil
}

func (o *DiscoverOptions) RunDiscover(cmd *cobra.Command) error {
	var testcases []*testcase.TestCase
	var loadErrors []*model.LoadError
	config, err := util.UnmarshalCaseInfo(o.discoverPath)
	if err != nil {
		return errors.Wrapf(err, "failed to unmarshal case info")
	}
	// 1. __TODO__: load test cases based on `config`
	// The following are the parameters that need attention:
	//   config.TestSelectors: expected list of test cases to load, possibly with multiple inputs
	//   example:
	//     - tests                                 // expected test case directory to be loaded
	//     - tests/test_hello.py                   // expected test case file to be loaded
	//     - tests/test_hello.py?name=MathTest     // expected test case to be loaded
	//     - tests/test_hello.py?MathTest/test_add // equivalent to the previous example, the 'name' parameter can be omitted
	//   config.ProjectPath: test cases root directory, example: /data/workspace
	//   config.TaskId: task id, as the unique identifier for this task, example: task-xxx
	//   config.FileReportPath: local test case result save file path, example: /data/report
	time.Sleep(1)

	// 2. __TODO__: after loading the test cases, report the results.
	// successfully loaded test cases can be added to load_result.Tests
	// and failed test cases can be added to load_result.LoadErrors
	// testcase.TestCase: single test case
	//      Path: test case path, example: tests/test_hello.py
	// 		Name: test case name, example: MathTest
	//      Attributes: test case attributes, represented in key-value pair form
	// model.LoadError
	//      name: load error name, example: tests/test_hello.py or tests/test_hello.py?LoadErrorTest
	//      message: load error message
	err = reportTestcases(config.FileReportPath, testcases, loadErrors)
	if err != nil {
		return errors.Wrapf(err, "failed to report testcases")
	}
	return nil
}
