/**
 * @name Analyze Data Processing Pipeline
 * @description Find patterns and potential issues in data processing workflows
 * @kind path-problem
 * @problem.severity warning
 * @precision high
 * @id python/data-pipeline-analysis
 * @tags security
 *       data-processing
 *       pipeline
 */

import python
import semmle.python.dataflow.new.DataFlow
import semmle.python.dataflow.new.TaintTracking
import semmle.python.security.Paths

// Find data loading operations
class DataLoader extends DataFlow::CallCfgNode {
  DataLoader() {
    exists(string name |
      name = this.getFunction().getName() and
      (
        // Pandas operations
        name in ["pandas.read_csv", "pandas.read_json", "pandas.read_excel"]
        or
        // NumPy operations
        name in ["numpy.load", "numpy.loadtxt"]
        or
        // Raw file operations
        name in ["open", "read", "readline"]
      )
    )
  }
}

// Find data transformation operations
class DataTransformation extends DataFlow::CallCfgNode {
  DataTransformation() {
    exists(string name |
      name = this.getFunction().getName() and
      (
        // Pandas transformations
        name in ["DataFrame.apply", "DataFrame.transform", "DataFrame.map"]
        or
        // NumPy operations
        name in ["numpy.apply_along_axis", "numpy.vectorize"]
        or
        // List comprehensions and map operations
        name in ["map", "filter", "reduce"]
      )
    )
  }
}

// Find data validation operations
class DataValidation extends DataFlow::CallCfgNode {
  DataValidation() {
    exists(string name |
      name = this.getFunction().getName() and
      (
        // Type checking
        name in ["isinstance", "type", "hasattr"]
        or
        // Value validation
        name in ["validate", "check", "assert"]
        or
        // Schema validation
        name in ["pydantic.validate", "marshmallow.Schema"]
      )
    )
  }
}

// Find data storage operations
class DataStorage extends DataFlow::CallCfgNode {
  DataStorage() {
    exists(string name |
      name = this.getFunction().getName() and
      (
        // File storage
        name in ["to_csv", "to_json", "to_excel", "save"]
        or
        // Database operations
        name in ["execute", "commit", "insert", "update"]
        or
        // Cache operations
        name in ["cache.set", "cache.get"]
      )
    )
  }
}

// Track data flow through the pipeline
class Config extends TaintTracking::Configuration {
  Config() { this = "DataPipelineConfig" }

  override predicate isSource(DataFlow::Node source) { source instanceof DataLoader }

  override predicate isSink(DataFlow::Node sink) { sink instanceof DataStorage }

  override predicate isAdditionalTaintStep(DataFlow::Node node1, DataFlow::Node node2) {
    exists(DataTransformation transform |
      node1 = transform.getAnArgument() and
      node2 = transform
    )
  }
}

from Config config, DataFlow::PathNode source, DataFlow::PathNode sink
where config.hasFlowPath(source, sink)
select sink.getNode(), source, sink, "Data flows from $@ to $@", source.getNode(), "data source",
  sink.getNode(), "data sink"

// Additional query for finding potential data leaks
from DataFlow::Node source, DataStorage store
where
  source instanceof DataLoader and
  not exists(DataValidation validation | DataFlow::localFlow(source, validation.getAnArgument())) and
  DataFlow::localFlow(source, store.getAnArgument())
select store, "Data from $@ is stored without validation", source, source.toString()
