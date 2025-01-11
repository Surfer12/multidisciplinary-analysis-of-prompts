/**
 * @name Analyze Claude Computer Interactions
 * @description Find patterns of how Claude interacts with the computer system
 * @kind problem
 * @problem.severity warning
 * @precision high
 * @id python/claude-computer-interactions
 * @tags security


import python
import semmle.python.ApiGraphs

class FileSystemAccess extends API::CallNode {
  FileSystemAccess() {
    this =
      API::moduleImport("os").getMember(["open", "read", "write", "mkdir", "remove"]).getACall()
    or
    this = API::moduleImport("shutil").getMember(["copy", "move", "rmtree"]).getACall()
  }
}

class SystemCommand extends API::CallNode {
  SystemCommand() {
    this = API::moduleImport("subprocess").getMember(["run", "Popen"]).getACall()
    or
    this = API::moduleImport("os").getMember("system").getACall()
  }
}

class NetworkOperation extends API::CallNode {
  NetworkOperation() {
    this = API::moduleImport("requests").getMember(["get", "post"]).getACall()
    or
    this = API::moduleImport("urllib.request").getMember("urlopen").getACall()
  }
}

from API::Node call
where
  call instanceof FileSystemAccess or
  call instanceof SystemCommand or
  call instanceof NetworkOperation
select call, "Found computer interaction"
