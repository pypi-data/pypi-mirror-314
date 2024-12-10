package main

import (
	"replace_____me/cmd/discover"
	"replace_____me/cmd/execute"

	"github.com/spf13/cobra"
)

func main() {
	rootCmd := cobra.Command{
		Use: "solar-replace_____me",
	}
	rootCmd.AddCommand(discover.NewCmdDiscover())
	rootCmd.AddCommand(execute.NewCmdExecute())
	_ = rootCmd.Execute()
}
