package testcase

type TestCase struct {
	Path       string
	Name       string
	Attributes map[string]string
}

func (tc *TestCase) GetSelector() string {
	strSelector := tc.Path
	if tc.Name != "" {
		strSelector += "?" + tc.Name
	}
	return strSelector
}
