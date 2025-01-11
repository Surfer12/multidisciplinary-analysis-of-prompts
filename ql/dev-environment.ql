/**
 * @name Analyze Development Environment
 * @description Find patterns and potential issues in development environment setup
 * @kind problem
 * @problem.severity warning
 * @precision high
 * @id python/dev-environment-analysis
 * @tags security
 *       development
 *       configuration
 */

import python
import semmle.python.dataflow.new.DataFlow
import semmle.python.security.Paths

// Find environment variable usage
class EnvironmentAccess extends DataFlow::CallCfgNode {
  EnvironmentAccess() {
    exists(string name |
      name = this.getFunction().getName() and
      (
        // OS environment access
        name in ["os.getenv", "os.environ.get"]
        or
        // Environment setup
        name in ["os.putenv", "os.environ.__setitem__"]
      )
    )
  }
}

// Find configuration file access
class ConfigAccess extends DataFlow::CallCfgNode {
  ConfigAccess() {
    exists(string name |
      name = this.getFunction().getName() and
      (
        // YAML config
        name in ["yaml.load", "yaml.safe_load"]
        or
        // JSON config
        name in ["json.load", "json.loads"]
        or
        // INI/ConfigParser
        name in ["configparser.ConfigParser", "configparser.read"]
      )
    )
  }
}

// Find development tool usage
class DevToolUsage extends DataFlow::CallCfgNode {
  DevToolUsage() {
    exists(string name |
      name = this.getFunction().getName() and
      (
        // Testing frameworks
        name in ["pytest.main", "unittest.main"]
        or
        // Debugging tools
        name in ["pdb.set_trace", "ipdb.set_trace"]
        or
        // Profiling tools
        name in ["cProfile.run", "profile.run"]
      )
    )
  }
}

// Find package management
class PackageManagement extends DataFlow::CallCfgNode {
  PackageManagement() {
    exists(string name |
      name = this.getFunction().getName() and
      (
        // Pip operations
        name in ["pip.main", "pip.get_installed_distributions"]
        or
        // Virtual environment
        name in ["venv.create", "virtualenv.create_environment"]
      )
    )
  }
}

from DataFlow::Node source
where
  source instanceof EnvironmentAccess or
  source instanceof ConfigAccess or
  source instanceof DevToolUsage or
  source instanceof PackageManagement
select source, "Development environment interaction: " + source.toString(),
  source.getLocation().getFile().getRelativePath(), source.getLocation().getStartLine()
