Disclaimer: Files have been written and altered with Claude Sonnet with Thinking enabled as well as without. These models from Anthropic can be unpredictable and the results have not been personally vetted for clarity as of 07/04/25. Review by this unique human is in progress. 
# 🧠 Meta-Optimized Hybrid Reasoning Framework  
**by Ryan Oates**  
**License: Dual — AGPLv3 + Peer Production License (PPL)**  
**Contact: ryan_oates@my.cuesta.edu**

---

## ✨ Purpose

This framework is part of an interdisciplinary vision to combine **symbolic rigor**, **neural adaptability**, and **cognitive-aligned reasoning**. It reflects years of integrated work at the intersection of computer science, biopsychology, and meta-epistemology.

It is not just software. It is a **cognitive architecture**, and its use is **ethically bounded**.

---

## 🔐 Licensing Model

This repository is licensed under a **hybrid model** to balance openness, reciprocity, and authorship protection.

### 1. For Commons-Aligned Users (students, researchers, cooperatives)
Use it under the **Peer Production License (PPL)**. You can:
- Study, adapt, and share it freely
- Use it in academic or nonprofit research
- Collaborate openly within the digital commons

### 2. For Public Use and Transparency
The AGPLv3 license guarantees:
- Network-based deployments must share modifications
- Derivatives must remain open source
- Attribution is mandatory

### 3. For Commercial or Extractive Use
You **must not use this work** if you are a:
- For-profit AI company
- Venture-backed foundation
- Closed-source platform
...unless you **negotiate a commercial license** directly.

---

## 📚 Attribution

This framework originated in:

> *Meta-Optimization in Hybrid Theorem Proving: Cognitive-Constrained Reasoning Framework*, Ryan Oates (2025)

DOI: [Insert Zenodo/ArXiv link here]  
Git commit hash of original release: `a17c3f9...`  
This project’s cognitive-theoretic roots come from studies in:
- Flow state modeling
- Symbolic logic systems
- Jungian epistemological structures

---

## 🤝 Community Contributor Agreement

If you are a student, educator, or aligned research group and want to contribute:
1. Fork this repo
2. Acknowledge the author and original framework
3. Use the “Contributors.md” file to describe your adaptation
4. Optional: Sign and return the [Community Contributor Agreement (CCA)](link) to join the federated research network

---

## 🚫 What You May Not Do

- Integrate this system into closed-source LLM deployments
- Resell it or offer derivative products without explicit approval
- Strip author tags or alter authorship metadata

---

## 📬 Contact

Want to collaborate, cite properly, or license commercially?  
Reach out: **ryan_oates@my.cuesta.edu**

# Project Overview

## Current State
The project currently has a series of test files, most of which are now passing after resolving several dependency issues. Remaining issues include:
- Plotly configuration errors with the 'titleside' property, suggesting 'title' as the correct attribute.
- Attribute errors related to , indicating potential import/mock setup issues.
- Deprecation warnings from Seaborn related to argument changes in future releases.

## Timeline of Changes
1. Installed necessary Python packages using  such as ============================= test session starts ==============================
platform darwin -- Python 3.11.11, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/ryanoates/multidisciplinary-analysis-of-prompts
configfile: pyproject.toml
plugins: anyio-4.8.0
collected 33 items / 14 errors

==================================== ERRORS ====================================
_ ERROR collecting references/anthropic-quickstarts/computer-use-demo/tests/loop_test.py _
ImportError while importing test module '/Users/ryanoates/multidisciplinary-analysis-of-prompts/references/anthropic-quickstarts/computer-use-demo/tests/loop_test.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
.magic/envs/default/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
references/anthropic-quickstarts/computer-use-demo/tests/loop_test.py:3: in <module>
    from anthropic.types import TextBlock, ToolUseBlock
E   ModuleNotFoundError: No module named 'anthropic'
_ ERROR collecting references/anthropic-quickstarts/computer-use-demo/tests/streamlit_test.py _
ImportError while importing test module '/Users/ryanoates/multidisciplinary-analysis-of-prompts/references/anthropic-quickstarts/computer-use-demo/tests/streamlit_test.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
.magic/envs/default/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
references/anthropic-quickstarts/computer-use-demo/tests/streamlit_test.py:4: in <module>
    from anthropic.types import TextBlockParam
E   ModuleNotFoundError: No module named 'anthropic'
_ ERROR collecting references/anthropic-quickstarts/computer-use-demo/tests/tools/bash_test.py _
ImportError while importing test module '/Users/ryanoates/multidisciplinary-analysis-of-prompts/references/anthropic-quickstarts/computer-use-demo/tests/tools/bash_test.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
.magic/envs/default/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
references/anthropic-quickstarts/computer-use-demo/tests/tools/bash_test.py:2: in <module>
    from computer_use_demo.tools.bash import BashTool, ToolError
E   ModuleNotFoundError: No module named 'computer_use_demo'
_ ERROR collecting references/anthropic-quickstarts/computer-use-demo/tests/tools/computer_test.py _
ImportError while importing test module '/Users/ryanoates/multidisciplinary-analysis-of-prompts/references/anthropic-quickstarts/computer-use-demo/tests/tools/computer_test.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
.magic/envs/default/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
references/anthropic-quickstarts/computer-use-demo/tests/tools/computer_test.py:4: in <module>
    from computer_use_demo.tools.computer import (
E   ModuleNotFoundError: No module named 'computer_use_demo'
_ ERROR collecting references/anthropic-quickstarts/computer-use-demo/tests/tools/edit_test.py _
ImportError while importing test module '/Users/ryanoates/multidisciplinary-analysis-of-prompts/references/anthropic-quickstarts/computer-use-demo/tests/tools/edit_test.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
.magic/envs/default/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
references/anthropic-quickstarts/computer-use-demo/tests/tools/edit_test.py:5: in <module>
    from computer_use_demo.tools.base import CLIResult, ToolError, ToolResult
E   ModuleNotFoundError: No module named 'computer_use_demo'
_ ERROR collecting references/anthropic-quickstarts/computer-use-demo/tests/tools/monitoring_test.py _
ImportError while importing test module '/Users/ryanoates/multidisciplinary-analysis-of-prompts/references/anthropic-quickstarts/computer-use-demo/tests/tools/monitoring_test.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
.magic/envs/default/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
references/anthropic-quickstarts/computer-use-demo/tests/tools/monitoring_test.py:7: in <module>
    from computer_use_demo.monitoring import MonitoringIntegration, PrometheusMonitoring
E   ModuleNotFoundError: No module named 'computer_use_demo'
____ ERROR collecting src/python/tests/examples/test_cognitive_processor.py ____
.magic/envs/default/lib/python3.11/site-packages/_pytest/python.py:493: in importtestmodule
    mod = import_path(
.magic/envs/default/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
.magic/envs/default/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
.magic/envs/default/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:175: in exec_module
    source_stat, co = _rewrite_test(fn, self.config)
.magic/envs/default/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:355: in _rewrite_test
    tree = ast.parse(source, filename=strfn)
.magic/envs/default/lib/python3.11/ast.py:50: in parse
    return compile(source, filename, mode, flags,
E     File "/Users/ryanoates/multidisciplinary-analysis-of-prompts/src/python/tests/examples/test_cognitive_processor.py", line 92
E       ```
E       ^
E   SyntaxError: invalid syntax
__________ ERROR collecting src/python/tests/tools/test_collection.py __________
.magic/envs/default/lib/python3.11/site-packages/_pytest/python.py:493: in importtestmodule
    mod = import_path(
.magic/envs/default/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
.magic/envs/default/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
.magic/envs/default/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:175: in exec_module
    source_stat, co = _rewrite_test(fn, self.config)
.magic/envs/default/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:355: in _rewrite_test
    tree = ast.parse(source, filename=strfn)
.magic/envs/default/lib/python3.11/ast.py:50: in parse
    return compile(source, filename, mode, flags,
E     File "/Users/ryanoates/multidisciplinary-analysis-of-prompts/src/python/tests/tools/test_collection.py", line 229
E       ```
E       ^
E   SyntaxError: invalid syntax
__________ ERROR collecting src/python/tests/tools/test_evolution.py ___________
.magic/envs/default/lib/python3.11/site-packages/_pytest/python.py:493: in importtestmodule
    mod = import_path(
.magic/envs/default/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
.magic/envs/default/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
.magic/envs/default/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:175: in exec_module
    source_stat, co = _rewrite_test(fn, self.config)
.magic/envs/default/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:355: in _rewrite_test
    tree = ast.parse(source, filename=strfn)
.magic/envs/default/lib/python3.11/ast.py:50: in parse
    return compile(source, filename, mode, flags,
E     File "/Users/ryanoates/multidisciplinary-analysis-of-prompts/src/python/tests/tools/test_evolution.py", line 265
E       ```
E       ^
E   SyntaxError: invalid syntax
________ ERROR collecting src/python/tests/tools/test_meta_analysis.py _________
ImportError while importing test module '/Users/ryanoates/multidisciplinary-analysis-of-prompts/src/python/tests/tools/test_meta_analysis.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
.magic/envs/default/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
src/python/tests/tools/test_meta_analysis.py:5: in <module>
    from cognitive_framework.tools import MetaAnalysisTool
E   ModuleNotFoundError: No module named 'cognitive_framework'
________ ERROR collecting src/python/tests/tools/test_meta_cognitive.py ________
ImportError while importing test module '/Users/ryanoates/multidisciplinary-analysis-of-prompts/src/python/tests/tools/test_meta_cognitive.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
.magic/envs/default/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
src/python/tests/tools/test_meta_cognitive.py:5: in <module>
    from cognitive_framework.tools import ToolResult
E   ModuleNotFoundError: No module named 'cognitive_framework'
__ ERROR collecting tests/python/meta_cognitive/test_pattern_visualization.py __
ImportError while importing test module '/Users/ryanoates/multidisciplinary-analysis-of-prompts/tests/python/meta_cognitive/test_pattern_visualization.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
.magic/envs/default/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/python/meta_cognitive/test_pattern_visualization.py:9: in <module>
    from visualization.pattern_viz import PatternVisualizer
E   ModuleNotFoundError: No module named 'visualization'
___________ ERROR collecting tests/test_tools/test_anthropic_tool.py ___________
ImportError while importing test module '/Users/ryanoates/multidisciplinary-analysis-of-prompts/tests/test_tools/test_anthropic_tool.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
.magic/envs/default/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_tools/test_anthropic_tool.py:6: in <module>
    from tools.anthropic_tool import AnthropicTool
E   ModuleNotFoundError: No module named 'tools.anthropic_tool'
________ ERROR collecting tests/test_visualization/test_pattern_viz.py _________
ImportError while importing test module '/Users/ryanoates/multidisciplinary-analysis-of-prompts/tests/test_visualization/test_pattern_viz.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
.magic/envs/default/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_visualization/test_pattern_viz.py:6: in <module>
    from visualization.pattern_viz import PatternVisualizer
E   ModuleNotFoundError: No module named 'visualization'
=========================== short test summary info ============================
ERROR references/anthropic-quickstarts/computer-use-demo/tests/loop_test.py
ERROR references/anthropic-quickstarts/computer-use-demo/tests/streamlit_test.py
ERROR references/anthropic-quickstarts/computer-use-demo/tests/tools/bash_test.py
ERROR references/anthropic-quickstarts/computer-use-demo/tests/tools/computer_test.py
ERROR references/anthropic-quickstarts/computer-use-demo/tests/tools/edit_test.py
ERROR references/anthropic-quickstarts/computer-use-demo/tests/tools/monitoring_test.py
ERROR src/python/tests/examples/test_cognitive_processor.py
ERROR src/python/tests/tools/test_collection.py
ERROR src/python/tests/tools/test_evolution.py
ERROR src/python/tests/tools/test_meta_analysis.py
ERROR src/python/tests/tools/test_meta_cognitive.py
ERROR tests/python/meta_cognitive/test_pattern_visualization.py
ERROR tests/test_tools/test_anthropic_tool.py
ERROR tests/test_visualization/test_pattern_viz.py
!!!!!!!!!!!!!!!!!!! Interrupted: 14 errors during collection !!!!!!!!!!!!!!!!!!!
============================== 14 errors in 0.96s ==============================, , , , , and .
2. Adjusted project structure by adding  files to directories to ensure they are recognized as packages.
3. Modified test import statements to match directory structure.
4. Conducted multiple rounds of testing and debug to resolve import errors and missing dependencies.

## Next Steps
- Update the Plotly configuration to fix invalid properties in the visualization code.
- Verify the correct implementation of  to eliminate attribute errors.
- Address the Seaborn deprecation warnings for future compatibility.
- Optional: Refactor code for better structure and maintenance.

## General Instructions
Run tests using:
============================= test session starts ==============================
platform darwin -- Python 3.11.11, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/ryanoates/multidisciplinary-analysis-of-prompts
configfile: pyproject.toml
plugins: anyio-4.8.0
collected 46 items

tests/python/framework_validation/test_advanced_operations.py ......     [ 13%]
tests/python/framework_validation/test_computer_interaction.py ........  [ 30%]
tests/python/framework_validation/test_environment_interaction.py .      [ 32%]
tests/python/meta_cognitive/test_advanced_meta_capabilities.py .....     [ 43%]
tests/python/meta_cognitive/test_meta_capabilities.py ....               [ 52%]
tests/python/meta_cognitive/test_pattern_recognition.py ..               [ 56%]
tests/python/meta_cognitive/test_pattern_visualization.py .F..           [ 65%]
tests/python/test_example.py .......                                     [ 80%]
tests/test_tools/test_anthropic_tool.py EEEEE                            [ 91%]
tests/test_visualization/test_pattern_viz.py .F..                        [100%]

==================================== ERRORS ====================================
___________________ ERROR at setup of test_generate_response ___________________

    @pytest.fixture
    def mock_anthropic_client():
        """Create a mock Anthropic client."""
>       with patch("anthropic.Client") as mock_client:

tests/test_tools/test_anthropic_tool.py:12: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.magic/envs/default/lib/python3.11/unittest/mock.py:1446: in __enter__
    original, local = self.get_original()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x16c481ad0>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'anthropic' (<_frozen_importlib_external.NamespaceLoader object at 0x16c74dc10>)> does not have the attribute 'Client'

.magic/envs/default/lib/python3.11/unittest/mock.py:1419: AttributeError
_____________________ ERROR at setup of test_analyze_code ______________________

    @pytest.fixture
    def mock_anthropic_client():
        """Create a mock Anthropic client."""
>       with patch("anthropic.Client") as mock_client:

tests/test_tools/test_anthropic_tool.py:12: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.magic/envs/default/lib/python3.11/unittest/mock.py:1446: in __enter__
    original, local = self.get_original()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x16d08d1d0>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'anthropic' (<_frozen_importlib_external.NamespaceLoader object at 0x16c74dc10>)> does not have the attribute 'Client'

.magic/envs/default/lib/python3.11/unittest/mock.py:1419: AttributeError
_________________ ERROR at setup of test_enhance_documentation _________________

    @pytest.fixture
    def mock_anthropic_client():
        """Create a mock Anthropic client."""
>       with patch("anthropic.Client") as mock_client:

tests/test_tools/test_anthropic_tool.py:12: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.magic/envs/default/lib/python3.11/unittest/mock.py:1446: in __enter__
    original, local = self.get_original()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x16d038d10>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'anthropic' (<_frozen_importlib_external.NamespaceLoader object at 0x16c74dc10>)> does not have the attribute 'Client'

.magic/envs/default/lib/python3.11/unittest/mock.py:1419: AttributeError
_________________ ERROR at setup of test_suggest_improvements __________________

    @pytest.fixture
    def mock_anthropic_client():
        """Create a mock Anthropic client."""
>       with patch("anthropic.Client") as mock_client:

tests/test_tools/test_anthropic_tool.py:12: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.magic/envs/default/lib/python3.11/unittest/mock.py:1446: in __enter__
    original, local = self.get_original()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x16c1ae2d0>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'anthropic' (<_frozen_importlib_external.NamespaceLoader object at 0x16c74dc10>)> does not have the attribute 'Client'

.magic/envs/default/lib/python3.11/unittest/mock.py:1419: AttributeError
____________________ ERROR at setup of test_error_handling _____________________

    @pytest.fixture
    def mock_anthropic_client():
        """Create a mock Anthropic client."""
>       with patch("anthropic.Client") as mock_client:

tests/test_tools/test_anthropic_tool.py:12: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.magic/envs/default/lib/python3.11/unittest/mock.py:1446: in __enter__
    original, local = self.get_original()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x16d61a450>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'anthropic' (<_frozen_importlib_external.NamespaceLoader object at 0x16c74dc10>)> does not have the attribute 'Client'

.magic/envs/default/lib/python3.11/unittest/mock.py:1419: AttributeError
=================================== FAILURES ===================================
________________________ test_create_cognitive_network _________________________

visualizer = <visualization.pattern_viz.PatternVisualizer object at 0x16d0ffe50>

    def test_create_cognitive_network(visualizer):
        """Test creation of cognitive network visualization."""
        nodes = ["Node A", "Node B", "Node C"]
        edges = [("Node A", "Node B"), ("Node B", "Node C")]
    
        # Test with default parameters
>       fig = visualizer.create_cognitive_network(nodes, edges)

tests/python/meta_cognitive/test_pattern_visualization.py:59: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/visualization/pattern_viz.py:171: in create_cognitive_network
    node_trace = go.Scatter(
.magic/envs/default/lib/python3.11/site-packages/plotly/graph_objs/_scatter.py:3534: in __init__
    self["marker"] = _v
.magic/envs/default/lib/python3.11/site-packages/plotly/basedatatypes.py:4852: in __setitem__
    self._set_compound_prop(prop, value)
.magic/envs/default/lib/python3.11/site-packages/plotly/basedatatypes.py:5263: in _set_compound_prop
    val = validator.validate_coerce(val, skip_invalid=self._skip_invalid)
.magic/envs/default/lib/python3.11/site-packages/_plotly_utils/basevalidators.py:2504: in validate_coerce
    v = self.data_class(v, skip_invalid=skip_invalid, _validate=_validate)
.magic/envs/default/lib/python3.11/site-packages/plotly/graph_objs/scatter/_marker.py:1622: in __init__
    self["colorbar"] = _v
.magic/envs/default/lib/python3.11/site-packages/plotly/basedatatypes.py:4852: in __setitem__
    self._set_compound_prop(prop, value)
.magic/envs/default/lib/python3.11/site-packages/plotly/basedatatypes.py:5263: in _set_compound_prop
    val = validator.validate_coerce(val, skip_invalid=self._skip_invalid)
.magic/envs/default/lib/python3.11/site-packages/_plotly_utils/basevalidators.py:2504: in validate_coerce
    v = self.data_class(v, skip_invalid=skip_invalid, _validate=_validate)
.magic/envs/default/lib/python3.11/site-packages/plotly/graph_objs/scatter/marker/_colorbar.py:2216: in __init__
    self._process_kwargs(**dict(arg, **kwargs))
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = scatter.marker.ColorBar({
    'thickness': 15, 'title': {'text': 'Node Connections'}, 'xanchor': 'left'
})
kwargs = {'titleside': 'right'}, k = 'titleside', v = 'right'
err = ValueError('Invalid property specified for object of type plotly.graph_objs.scatter.marker.ColorBar: \'titleside\'\n\n...       height of the plotting area only.\n        \nDid you mean "title"?\n\nBad property path:\ntitleside\n^^^^^^^^^')

    def _process_kwargs(self, **kwargs):
        """
        Process any extra kwargs that are not predefined as constructor params
        """
        for k, v in kwargs.items():
            err = _check_path_in_prop_tree(self, k, error_cast=ValueError)
            if err is None:
                # e.g. underscore kwargs like marker_line_color
                self[k] = v
            elif not self._validate:
                # Set extra property as-is
                self[k] = v
            elif not self._skip_invalid:
>               raise err
E               ValueError: Invalid property specified for object of type plotly.graph_objs.scatter.marker.ColorBar: 'titleside'
E               
E               Did you mean "title"?
E               
E                   Valid properties:
E                       bgcolor
E                           Sets the color of padded area.
E                       bordercolor
E                           Sets the axis line color.
E                       borderwidth
E                           Sets the width (in px) or the border enclosing this
E                           color bar.
E                       dtick
E                           Sets the step in-between ticks on this axis. Use with
E                           `tick0`. Must be a positive number, or special strings
E                           available to "log" and "date" axes. If the axis `type`
E                           is "log", then ticks are set every 10^(n*dtick) where n
E                           is the tick number. For example, to set a tick mark at
E                           1, 10, 100, 1000, ... set dtick to 1. To set tick marks
E                           at 1, 100, 10000, ... set dtick to 2. To set tick marks
E                           at 1, 5, 25, 125, 625, 3125, ... set dtick to
E                           log_10(5), or 0.69897000433. "log" has several special
E                           values; "L<f>", where `f` is a positive number, gives
E                           ticks linearly spaced in value (but not position). For
E                           example `tick0` = 0.1, `dtick` = "L0.5" will put ticks
E                           at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus
E                           small digits between, use "D1" (all digits) or "D2"
E                           (only 2 and 5). `tick0` is ignored for "D1" and "D2".
E                           If the axis `type` is "date", then you must convert the
E                           time to milliseconds. For example, to set the interval
E                           between ticks to one day, set `dtick` to 86400000.0.
E                           "date" also has special values "M<n>" gives ticks
E                           spaced by a number of months. `n` must be a positive
E                           integer. To set ticks on the 15th of every third month,
E                           set `tick0` to "2000-01-15" and `dtick` to "M3". To set
E                           ticks every 4 years, set `dtick` to "M48"
E                       exponentformat
E                           Determines a formatting rule for the tick exponents.
E                           For example, consider the number 1,000,000,000. If
E                           "none", it appears as 1,000,000,000. If "e", 1e+9. If
E                           "E", 1E+9. If "power", 1x10^9 (with 9 in a super
E                           script). If "SI", 1G. If "B", 1B.
E                       labelalias
E                           Replacement text for specific tick or hover labels. For
E                           example using {US: 'USA', CA: 'Canada'} changes US to
E                           USA and CA to Canada. The labels we would have shown
E                           must match the keys exactly, after adding any
E                           tickprefix or ticksuffix. For negative numbers the
E                           minus sign symbol used (U+2212) is wider than the
E                           regular ascii dash. That means you need to use −1
E                           instead of -1. labelalias can be used with any axis
E                           type, and both keys (if needed) and values (if desired)
E                           can include html-like tags or MathJax.
E                       len
E                           Sets the length of the color bar This measure excludes
E                           the padding of both ends. That is, the color bar length
E                           is this length minus the padding on both ends.
E                       lenmode
E                           Determines whether this color bar's length (i.e. the
E                           measure in the color variation direction) is set in
E                           units of plot "fraction" or in *pixels. Use `len` to
E                           set the value.
E                       minexponent
E                           Hide SI prefix for 10^n if |n| is below this number.
E                           This only has an effect when `tickformat` is "SI" or
E                           "B".
E                       nticks
E                           Specifies the maximum number of ticks for the
E                           particular axis. The actual number of ticks will be
E                           chosen automatically to be less than or equal to
E                           `nticks`. Has an effect only if `tickmode` is set to
E                           "auto".
E                       orientation
E                           Sets the orientation of the colorbar.
E                       outlinecolor
E                           Sets the axis line color.
E                       outlinewidth
E                           Sets the width (in px) of the axis line.
E                       separatethousands
E                           If "true", even 4-digit integers are separated
E                       showexponent
E                           If "all", all exponents are shown besides their
E                           significands. If "first", only the exponent of the
E                           first tick is shown. If "last", only the exponent of
E                           the last tick is shown. If "none", no exponents appear.
E                       showticklabels
E                           Determines whether or not the tick labels are drawn.
E                       showtickprefix
E                           If "all", all tick labels are displayed with a prefix.
E                           If "first", only the first tick is displayed with a
E                           prefix. If "last", only the last tick is displayed with
E                           a suffix. If "none", tick prefixes are hidden.
E                       showticksuffix
E                           Same as `showtickprefix` but for tick suffixes.
E                       thickness
E                           Sets the thickness of the color bar This measure
E                           excludes the size of the padding, ticks and labels.
E                       thicknessmode
E                           Determines whether this color bar's thickness (i.e. the
E                           measure in the constant color direction) is set in
E                           units of plot "fraction" or in "pixels". Use
E                           `thickness` to set the value.
E                       tick0
E                           Sets the placement of the first tick on this axis. Use
E                           with `dtick`. If the axis `type` is "log", then you
E                           must take the log of your starting tick (e.g. to set
E                           the starting tick to 100, set the `tick0` to 2) except
E                           when `dtick`=*L<f>* (see `dtick` for more info). If the
E                           axis `type` is "date", it should be a date string, like
E                           date data. If the axis `type` is "category", it should
E                           be a number, using the scale where each category is
E                           assigned a serial number from zero in the order it
E                           appears.
E                       tickangle
E                           Sets the angle of the tick labels with respect to the
E                           horizontal. For example, a `tickangle` of -90 draws the
E                           tick labels vertically.
E                       tickcolor
E                           Sets the tick color.
E                       tickfont
E                           Sets the color bar's tick label font
E                       tickformat
E                           Sets the tick label formatting rule using d3 formatting
E                           mini-languages which are very similar to those in
E                           Python. For numbers, see:
E                           https://github.com/d3/d3-format/tree/v1.4.5#d3-format.
E                           And for dates see: https://github.com/d3/d3-time-
E                           format/tree/v2.2.3#locale_format. We add two items to
E                           d3's date formatter: "%h" for half of the year as a
E                           decimal number as well as "%{n}f" for fractional
E                           seconds with n digits. For example, *2016-10-13
E                           09:15:23.456* with tickformat "%H~%M~%S.%2f" would
E                           display "09~15~23.46"
E                       tickformatstops
E                           A tuple of :class:`plotly.graph_objects.scatter.marker.
E                           colorbar.Tickformatstop` instances or dicts with
E                           compatible properties
E                       tickformatstopdefaults
E                           When used in a template (as layout.template.data.scatte
E                           r.marker.colorbar.tickformatstopdefaults), sets the
E                           default property values to use for elements of
E                           scatter.marker.colorbar.tickformatstops
E                       ticklabeloverflow
E                           Determines how we handle tick labels that would
E                           overflow either the graph div or the domain of the
E                           axis. The default value for inside tick labels is *hide
E                           past domain*. In other cases the default is *hide past
E                           div*.
E                       ticklabelposition
E                           Determines where tick labels are drawn relative to the
E                           ticks. Left and right options are used when
E                           `orientation` is "h", top and bottom when `orientation`
E                           is "v".
E                       ticklabelstep
E                           Sets the spacing between tick labels as compared to the
E                           spacing between ticks. A value of 1 (default) means
E                           each tick gets a label. A value of 2 means shows every
E                           2nd label. A larger value n means only every nth tick
E                           is labeled. `tick0` determines which labels are shown.
E                           Not implemented for axes with `type` "log" or
E                           "multicategory", or when `tickmode` is "array".
E                       ticklen
E                           Sets the tick length (in px).
E                       tickmode
E                           Sets the tick mode for this axis. If "auto", the number
E                           of ticks is set via `nticks`. If "linear", the
E                           placement of the ticks is determined by a starting
E                           position `tick0` and a tick step `dtick` ("linear" is
E                           the default value if `tick0` and `dtick` are provided).
E                           If "array", the placement of the ticks is set via
E                           `tickvals` and the tick text is `ticktext`. ("array" is
E                           the default value if `tickvals` is provided).
E                       tickprefix
E                           Sets a tick label prefix.
E                       ticks
E                           Determines whether ticks are drawn or not. If "", this
E                           axis' ticks are not drawn. If "outside" ("inside"),
E                           this axis' are drawn outside (inside) the axis lines.
E                       ticksuffix
E                           Sets a tick label suffix.
E                       ticktext
E                           Sets the text displayed at the ticks position via
E                           `tickvals`. Only has an effect if `tickmode` is set to
E                           "array". Used with `tickvals`.
E                       ticktextsrc
E                           Sets the source reference on Chart Studio Cloud for
E                           `ticktext`.
E                       tickvals
E                           Sets the values at which ticks on this axis appear.
E                           Only has an effect if `tickmode` is set to "array".
E                           Used with `ticktext`.
E                       tickvalssrc
E                           Sets the source reference on Chart Studio Cloud for
E                           `tickvals`.
E                       tickwidth
E                           Sets the tick width (in px).
E                       title
E                           :class:`plotly.graph_objects.scatter.marker.colorbar.Ti
E                           tle` instance or dict with compatible properties
E                       x
E                           Sets the x position with respect to `xref` of the color
E                           bar (in plot fraction). When `xref` is "paper",
E                           defaults to 1.02 when `orientation` is "v" and 0.5 when
E                           `orientation` is "h". When `xref` is "container",
E                           defaults to 1 when `orientation` is "v" and 0.5 when
E                           `orientation` is "h". Must be between 0 and 1 if `xref`
E                           is "container" and between "-2" and 3 if `xref` is
E                           "paper".
E                       xanchor
E                           Sets this color bar's horizontal position anchor. This
E                           anchor binds the `x` position to the "left", "center"
E                           or "right" of the color bar. Defaults to "left" when
E                           `orientation` is "v" and "center" when `orientation` is
E                           "h".
E                       xpad
E                           Sets the amount of padding (in px) along the x
E                           direction.
E                       xref
E                           Sets the container `x` refers to. "container" spans the
E                           entire `width` of the plot. "paper" refers to the width
E                           of the plotting area only.
E                       y
E                           Sets the y position with respect to `yref` of the color
E                           bar (in plot fraction). When `yref` is "paper",
E                           defaults to 0.5 when `orientation` is "v" and 1.02 when
E                           `orientation` is "h". When `yref` is "container",
E                           defaults to 0.5 when `orientation` is "v" and 1 when
E                           `orientation` is "h". Must be between 0 and 1 if `yref`
E                           is "container" and between "-2" and 3 if `yref` is
E                           "paper".
E                       yanchor
E                           Sets this color bar's vertical position anchor This
E                           anchor binds the `y` position to the "top", "middle" or
E                           "bottom" of the color bar. Defaults to "middle" when
E                           `orientation` is "v" and "bottom" when `orientation` is
E                           "h".
E                       ypad
E                           Sets the amount of padding (in px) along the y
E                           direction.
E                       yref
E                           Sets the container `y` refers to. "container" spans the
E                           entire `height` of the plot. "paper" refers to the
E                           height of the plotting area only.
E                       
E               Did you mean "title"?
E               
E               Bad property path:
E               titleside
E               ^^^^^^^^^

.magic/envs/default/lib/python3.11/site-packages/plotly/basedatatypes.py:4378: ValueError
----------------------------- Captured stdout call -----------------------------
Error creating network visualization: Invalid property specified for object of type plotly.graph_objs.scatter.marker.ColorBar: 'titleside'

Did you mean "title"?

    Valid properties:
        bgcolor
            Sets the color of padded area.
        bordercolor
            Sets the axis line color.
        borderwidth
            Sets the width (in px) or the border enclosing this
            color bar.
        dtick
            Sets the step in-between ticks on this axis. Use with
            `tick0`. Must be a positive number, or special strings
            available to "log" and "date" axes. If the axis `type`
            is "log", then ticks are set every 10^(n*dtick) where n
            is the tick number. For example, to set a tick mark at
            1, 10, 100, 1000, ... set dtick to 1. To set tick marks
            at 1, 100, 10000, ... set dtick to 2. To set tick marks
            at 1, 5, 25, 125, 625, 3125, ... set dtick to
            log_10(5), or 0.69897000433. "log" has several special
            values; "L<f>", where `f` is a positive number, gives
            ticks linearly spaced in value (but not position). For
            example `tick0` = 0.1, `dtick` = "L0.5" will put ticks
            at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus
            small digits between, use "D1" (all digits) or "D2"
            (only 2 and 5). `tick0` is ignored for "D1" and "D2".
            If the axis `type` is "date", then you must convert the
            time to milliseconds. For example, to set the interval
            between ticks to one day, set `dtick` to 86400000.0.
            "date" also has special values "M<n>" gives ticks
            spaced by a number of months. `n` must be a positive
            integer. To set ticks on the 15th of every third month,
            set `tick0` to "2000-01-15" and `dtick` to "M3". To set
            ticks every 4 years, set `dtick` to "M48"
        exponentformat
            Determines a formatting rule for the tick exponents.
            For example, consider the number 1,000,000,000. If
            "none", it appears as 1,000,000,000. If "e", 1e+9. If
            "E", 1E+9. If "power", 1x10^9 (with 9 in a super
            script). If "SI", 1G. If "B", 1B.
        labelalias
            Replacement text for specific tick or hover labels. For
            example using {US: 'USA', CA: 'Canada'} changes US to
            USA and CA to Canada. The labels we would have shown
            must match the keys exactly, after adding any
            tickprefix or ticksuffix. For negative numbers the
            minus sign symbol used (U+2212) is wider than the
            regular ascii dash. That means you need to use −1
            instead of -1. labelalias can be used with any axis
            type, and both keys (if needed) and values (if desired)
            can include html-like tags or MathJax.
        len
            Sets the length of the color bar This measure excludes
            the padding of both ends. That is, the color bar length
            is this length minus the padding on both ends.
        lenmode
            Determines whether this color bar's length (i.e. the
            measure in the color variation direction) is set in
            units of plot "fraction" or in *pixels. Use `len` to
            set the value.
        minexponent
            Hide SI prefix for 10^n if |n| is below this number.
            This only has an effect when `tickformat` is "SI" or
            "B".
        nticks
            Specifies the maximum number of ticks for the
            particular axis. The actual number of ticks will be
            chosen automatically to be less than or equal to
            `nticks`. Has an effect only if `tickmode` is set to
            "auto".
        orientation
            Sets the orientation of the colorbar.
        outlinecolor
            Sets the axis line color.
        outlinewidth
            Sets the width (in px) of the axis line.
        separatethousands
            If "true", even 4-digit integers are separated
        showexponent
            If "all", all exponents are shown besides their
            significands. If "first", only the exponent of the
            first tick is shown. If "last", only the exponent of
            the last tick is shown. If "none", no exponents appear.
        showticklabels
            Determines whether or not the tick labels are drawn.
        showtickprefix
            If "all", all tick labels are displayed with a prefix.
            If "first", only the first tick is displayed with a
            prefix. If "last", only the last tick is displayed with
            a suffix. If "none", tick prefixes are hidden.
        showticksuffix
            Same as `showtickprefix` but for tick suffixes.
        thickness
            Sets the thickness of the color bar This measure
            excludes the size of the padding, ticks and labels.
        thicknessmode
            Determines whether this color bar's thickness (i.e. the
            measure in the constant color direction) is set in
            units of plot "fraction" or in "pixels". Use
            `thickness` to set the value.
        tick0
            Sets the placement of the first tick on this axis. Use
            with `dtick`. If the axis `type` is "log", then you
            must take the log of your starting tick (e.g. to set
            the starting tick to 100, set the `tick0` to 2) except
            when `dtick`=*L<f>* (see `dtick` for more info). If the
            axis `type` is "date", it should be a date string, like
            date data. If the axis `type` is "category", it should
            be a number, using the scale where each category is
            assigned a serial number from zero in the order it
            appears.
        tickangle
            Sets the angle of the tick labels with respect to the
            horizontal. For example, a `tickangle` of -90 draws the
            tick labels vertically.
        tickcolor
            Sets the tick color.
        tickfont
            Sets the color bar's tick label font
        tickformat
            Sets the tick label formatting rule using d3 formatting
            mini-languages which are very similar to those in
            Python. For numbers, see:
            https://github.com/d3/d3-format/tree/v1.4.5#d3-format.
            And for dates see: https://github.com/d3/d3-time-
            format/tree/v2.2.3#locale_format. We add two items to
            d3's date formatter: "%h" for half of the year as a
            decimal number as well as "%{n}f" for fractional
            seconds with n digits. For example, *2016-10-13
            09:15:23.456* with tickformat "%H~%M~%S.%2f" would
            display "09~15~23.46"
        tickformatstops
            A tuple of :class:`plotly.graph_objects.scatter.marker.
            colorbar.Tickformatstop` instances or dicts with
            compatible properties
        tickformatstopdefaults
            When used in a template (as layout.template.data.scatte
            r.marker.colorbar.tickformatstopdefaults), sets the
            default property values to use for elements of
            scatter.marker.colorbar.tickformatstops
        ticklabeloverflow
            Determines how we handle tick labels that would
            overflow either the graph div or the domain of the
            axis. The default value for inside tick labels is *hide
            past domain*. In other cases the default is *hide past
            div*.
        ticklabelposition
            Determines where tick labels are drawn relative to the
            ticks. Left and right options are used when
            `orientation` is "h", top and bottom when `orientation`
            is "v".
        ticklabelstep
            Sets the spacing between tick labels as compared to the
            spacing between ticks. A value of 1 (default) means
            each tick gets a label. A value of 2 means shows every
            2nd label. A larger value n means only every nth tick
            is labeled. `tick0` determines which labels are shown.
            Not implemented for axes with `type` "log" or
            "multicategory", or when `tickmode` is "array".
        ticklen
            Sets the tick length (in px).
        tickmode
            Sets the tick mode for this axis. If "auto", the number
            of ticks is set via `nticks`. If "linear", the
            placement of the ticks is determined by a starting
            position `tick0` and a tick step `dtick` ("linear" is
            the default value if `tick0` and `dtick` are provided).
            If "array", the placement of the ticks is set via
            `tickvals` and the tick text is `ticktext`. ("array" is
            the default value if `tickvals` is provided).
        tickprefix
            Sets a tick label prefix.
        ticks
            Determines whether ticks are drawn or not. If "", this
            axis' ticks are not drawn. If "outside" ("inside"),
            this axis' are drawn outside (inside) the axis lines.
        ticksuffix
            Sets a tick label suffix.
        ticktext
            Sets the text displayed at the ticks position via
            `tickvals`. Only has an effect if `tickmode` is set to
            "array". Used with `tickvals`.
        ticktextsrc
            Sets the source reference on Chart Studio Cloud for
            `ticktext`.
        tickvals
            Sets the values at which ticks on this axis appear.
            Only has an effect if `tickmode` is set to "array".
            Used with `ticktext`.
        tickvalssrc
            Sets the source reference on Chart Studio Cloud for
            `tickvals`.
        tickwidth
            Sets the tick width (in px).
        title
            :class:`plotly.graph_objects.scatter.marker.colorbar.Ti
            tle` instance or dict with compatible properties
        x
            Sets the x position with respect to `xref` of the color
            bar (in plot fraction). When `xref` is "paper",
            defaults to 1.02 when `orientation` is "v" and 0.5 when
            `orientation` is "h". When `xref` is "container",
            defaults to 1 when `orientation` is "v" and 0.5 when
            `orientation` is "h". Must be between 0 and 1 if `xref`
            is "container" and between "-2" and 3 if `xref` is
            "paper".
        xanchor
            Sets this color bar's horizontal position anchor. This
            anchor binds the `x` position to the "left", "center"
            or "right" of the color bar. Defaults to "left" when
            `orientation` is "v" and "center" when `orientation` is
            "h".
        xpad
            Sets the amount of padding (in px) along the x
            direction.
        xref
            Sets the container `x` refers to. "container" spans the
            entire `width` of the plot. "paper" refers to the width
            of the plotting area only.
        y
            Sets the y position with respect to `yref` of the color
            bar (in plot fraction). When `yref` is "paper",
            defaults to 0.5 when `orientation` is "v" and 1.02 when
            `orientation` is "h". When `yref` is "container",
            defaults to 0.5 when `orientation` is "v" and 1 when
            `orientation` is "h". Must be between 0 and 1 if `yref`
            is "container" and between "-2" and 3 if `yref` is
            "paper".
        yanchor
            Sets this color bar's vertical position anchor This
            anchor binds the `y` position to the "top", "middle" or
            "bottom" of the color bar. Defaults to "middle" when
            `orientation` is "v" and "bottom" when `orientation` is
            "h".
        ypad
            Sets the amount of padding (in px) along the y
            direction.
        yref
            Sets the container `y` refers to. "container" spans the
            entire `height` of the plot. "paper" refers to the
            height of the plotting area only.
        
Did you mean "title"?

Bad property path:
titleside
^^^^^^^^^
________________________ test_create_cognitive_network _________________________

visualizer = <visualization.pattern_viz.PatternVisualizer object at 0x16e1258d0>

    def test_create_cognitive_network(visualizer):
        """Test creation of cognitive network visualization."""
        nodes = ['Node A', 'Node B', 'Node C']
        edges = [('Node A', 'Node B'), ('Node B', 'Node C')]
>       fig = visualizer.create_cognitive_network(nodes, edges)

tests/test_visualization/test_pattern_viz.py:43: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/visualization/pattern_viz.py:171: in create_cognitive_network
    node_trace = go.Scatter(
.magic/envs/default/lib/python3.11/site-packages/plotly/graph_objs/_scatter.py:3534: in __init__
    self["marker"] = _v
.magic/envs/default/lib/python3.11/site-packages/plotly/basedatatypes.py:4852: in __setitem__
    self._set_compound_prop(prop, value)
.magic/envs/default/lib/python3.11/site-packages/plotly/basedatatypes.py:5263: in _set_compound_prop
    val = validator.validate_coerce(val, skip_invalid=self._skip_invalid)
.magic/envs/default/lib/python3.11/site-packages/_plotly_utils/basevalidators.py:2504: in validate_coerce
    v = self.data_class(v, skip_invalid=skip_invalid, _validate=_validate)
.magic/envs/default/lib/python3.11/site-packages/plotly/graph_objs/scatter/_marker.py:1622: in __init__
    self["colorbar"] = _v
.magic/envs/default/lib/python3.11/site-packages/plotly/basedatatypes.py:4852: in __setitem__
    self._set_compound_prop(prop, value)
.magic/envs/default/lib/python3.11/site-packages/plotly/basedatatypes.py:5263: in _set_compound_prop
    val = validator.validate_coerce(val, skip_invalid=self._skip_invalid)
.magic/envs/default/lib/python3.11/site-packages/_plotly_utils/basevalidators.py:2504: in validate_coerce
    v = self.data_class(v, skip_invalid=skip_invalid, _validate=_validate)
.magic/envs/default/lib/python3.11/site-packages/plotly/graph_objs/scatter/marker/_colorbar.py:2216: in __init__
    self._process_kwargs(**dict(arg, **kwargs))
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = scatter.marker.ColorBar({
    'thickness': 15, 'title': {'text': 'Node Connections'}, 'xanchor': 'left'
})
kwargs = {'titleside': 'right'}, k = 'titleside', v = 'right'
err = ValueError('Invalid property specified for object of type plotly.graph_objs.scatter.marker.ColorBar: \'titleside\'\n\n...       height of the plotting area only.\n        \nDid you mean "title"?\n\nBad property path:\ntitleside\n^^^^^^^^^')

    def _process_kwargs(self, **kwargs):
        """
        Process any extra kwargs that are not predefined as constructor params
        """
        for k, v in kwargs.items():
            err = _check_path_in_prop_tree(self, k, error_cast=ValueError)
            if err is None:
                # e.g. underscore kwargs like marker_line_color
                self[k] = v
            elif not self._validate:
                # Set extra property as-is
                self[k] = v
            elif not self._skip_invalid:
>               raise err
E               ValueError: Invalid property specified for object of type plotly.graph_objs.scatter.marker.ColorBar: 'titleside'
E               
E               Did you mean "title"?
E               
E                   Valid properties:
E                       bgcolor
E                           Sets the color of padded area.
E                       bordercolor
E                           Sets the axis line color.
E                       borderwidth
E                           Sets the width (in px) or the border enclosing this
E                           color bar.
E                       dtick
E                           Sets the step in-between ticks on this axis. Use with
E                           `tick0`. Must be a positive number, or special strings
E                           available to "log" and "date" axes. If the axis `type`
E                           is "log", then ticks are set every 10^(n*dtick) where n
E                           is the tick number. For example, to set a tick mark at
E                           1, 10, 100, 1000, ... set dtick to 1. To set tick marks
E                           at 1, 100, 10000, ... set dtick to 2. To set tick marks
E                           at 1, 5, 25, 125, 625, 3125, ... set dtick to
E                           log_10(5), or 0.69897000433. "log" has several special
E                           values; "L<f>", where `f` is a positive number, gives
E                           ticks linearly spaced in value (but not position). For
E                           example `tick0` = 0.1, `dtick` = "L0.5" will put ticks
E                           at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus
E                           small digits between, use "D1" (all digits) or "D2"
E                           (only 2 and 5). `tick0` is ignored for "D1" and "D2".
E                           If the axis `type` is "date", then you must convert the
E                           time to milliseconds. For example, to set the interval
E                           between ticks to one day, set `dtick` to 86400000.0.
E                           "date" also has special values "M<n>" gives ticks
E                           spaced by a number of months. `n` must be a positive
E                           integer. To set ticks on the 15th of every third month,
E                           set `tick0` to "2000-01-15" and `dtick` to "M3". To set
E                           ticks every 4 years, set `dtick` to "M48"
E                       exponentformat
E                           Determines a formatting rule for the tick exponents.
E                           For example, consider the number 1,000,000,000. If
E                           "none", it appears as 1,000,000,000. If "e", 1e+9. If
E                           "E", 1E+9. If "power", 1x10^9 (with 9 in a super
E                           script). If "SI", 1G. If "B", 1B.
E                       labelalias
E                           Replacement text for specific tick or hover labels. For
E                           example using {US: 'USA', CA: 'Canada'} changes US to
E                           USA and CA to Canada. The labels we would have shown
E                           must match the keys exactly, after adding any
E                           tickprefix or ticksuffix. For negative numbers the
E                           minus sign symbol used (U+2212) is wider than the
E                           regular ascii dash. That means you need to use −1
E                           instead of -1. labelalias can be used with any axis
E                           type, and both keys (if needed) and values (if desired)
E                           can include html-like tags or MathJax.
E                       len
E                           Sets the length of the color bar This measure excludes
E                           the padding of both ends. That is, the color bar length
E                           is this length minus the padding on both ends.
E                       lenmode
E                           Determines whether this color bar's length (i.e. the
E                           measure in the color variation direction) is set in
E                           units of plot "fraction" or in *pixels. Use `len` to
E                           set the value.
E                       minexponent
E                           Hide SI prefix for 10^n if |n| is below this number.
E                           This only has an effect when `tickformat` is "SI" or
E                           "B".
E                       nticks
E                           Specifies the maximum number of ticks for the
E                           particular axis. The actual number of ticks will be
E                           chosen automatically to be less than or equal to
E                           `nticks`. Has an effect only if `tickmode` is set to
E                           "auto".
E                       orientation
E                           Sets the orientation of the colorbar.
E                       outlinecolor
E                           Sets the axis line color.
E                       outlinewidth
E                           Sets the width (in px) of the axis line.
E                       separatethousands
E                           If "true", even 4-digit integers are separated
E                       showexponent
E                           If "all", all exponents are shown besides their
E                           significands. If "first", only the exponent of the
E                           first tick is shown. If "last", only the exponent of
E                           the last tick is shown. If "none", no exponents appear.
E                       showticklabels
E                           Determines whether or not the tick labels are drawn.
E                       showtickprefix
E                           If "all", all tick labels are displayed with a prefix.
E                           If "first", only the first tick is displayed with a
E                           prefix. If "last", only the last tick is displayed with
E                           a suffix. If "none", tick prefixes are hidden.
E                       showticksuffix
E                           Same as `showtickprefix` but for tick suffixes.
E                       thickness
E                           Sets the thickness of the color bar This measure
E                           excludes the size of the padding, ticks and labels.
E                       thicknessmode
E                           Determines whether this color bar's thickness (i.e. the
E                           measure in the constant color direction) is set in
E                           units of plot "fraction" or in "pixels". Use
E                           `thickness` to set the value.
E                       tick0
E                           Sets the placement of the first tick on this axis. Use
E                           with `dtick`. If the axis `type` is "log", then you
E                           must take the log of your starting tick (e.g. to set
E                           the starting tick to 100, set the `tick0` to 2) except
E                           when `dtick`=*L<f>* (see `dtick` for more info). If the
E                           axis `type` is "date", it should be a date string, like
E                           date data. If the axis `type` is "category", it should
E                           be a number, using the scale where each category is
E                           assigned a serial number from zero in the order it
E                           appears.
E                       tickangle
E                           Sets the angle of the tick labels with respect to the
E                           horizontal. For example, a `tickangle` of -90 draws the
E                           tick labels vertically.
E                       tickcolor
E                           Sets the tick color.
E                       tickfont
E                           Sets the color bar's tick label font
E                       tickformat
E                           Sets the tick label formatting rule using d3 formatting
E                           mini-languages which are very similar to those in
E                           Python. For numbers, see:
E                           https://github.com/d3/d3-format/tree/v1.4.5#d3-format.
E                           And for dates see: https://github.com/d3/d3-time-
E                           format/tree/v2.2.3#locale_format. We add two items to
E                           d3's date formatter: "%h" for half of the year as a
E                           decimal number as well as "%{n}f" for fractional
E                           seconds with n digits. For example, *2016-10-13
E                           09:15:23.456* with tickformat "%H~%M~%S.%2f" would
E                           display "09~15~23.46"
E                       tickformatstops
E                           A tuple of :class:`plotly.graph_objects.scatter.marker.
E                           colorbar.Tickformatstop` instances or dicts with
E                           compatible properties
E                       tickformatstopdefaults
E                           When used in a template (as layout.template.data.scatte
E                           r.marker.colorbar.tickformatstopdefaults), sets the
E                           default property values to use for elements of
E                           scatter.marker.colorbar.tickformatstops
E                       ticklabeloverflow
E                           Determines how we handle tick labels that would
E                           overflow either the graph div or the domain of the
E                           axis. The default value for inside tick labels is *hide
E                           past domain*. In other cases the default is *hide past
E                           div*.
E                       ticklabelposition
E                           Determines where tick labels are drawn relative to the
E                           ticks. Left and right options are used when
E                           `orientation` is "h", top and bottom when `orientation`
E                           is "v".
E                       ticklabelstep
E                           Sets the spacing between tick labels as compared to the
E                           spacing between ticks. A value of 1 (default) means
E                           each tick gets a label. A value of 2 means shows every
E                           2nd label. A larger value n means only every nth tick
E                           is labeled. `tick0` determines which labels are shown.
E                           Not implemented for axes with `type` "log" or
E                           "multicategory", or when `tickmode` is "array".
E                       ticklen
E                           Sets the tick length (in px).
E                       tickmode
E                           Sets the tick mode for this axis. If "auto", the number
E                           of ticks is set via `nticks`. If "linear", the
E                           placement of the ticks is determined by a starting
E                           position `tick0` and a tick step `dtick` ("linear" is
E                           the default value if `tick0` and `dtick` are provided).
E                           If "array", the placement of the ticks is set via
E                           `tickvals` and the tick text is `ticktext`. ("array" is
E                           the default value if `tickvals` is provided).
E                       tickprefix
E                           Sets a tick label prefix.
E                       ticks
E                           Determines whether ticks are drawn or not. If "", this
E                           axis' ticks are not drawn. If "outside" ("inside"),
E                           this axis' are drawn outside (inside) the axis lines.
E                       ticksuffix
E                           Sets a tick label suffix.
E                       ticktext
E                           Sets the text displayed at the ticks position via
E                           `tickvals`. Only has an effect if `tickmode` is set to
E                           "array". Used with `tickvals`.
E                       ticktextsrc
E                           Sets the source reference on Chart Studio Cloud for
E                           `ticktext`.
E                       tickvals
E                           Sets the values at which ticks on this axis appear.
E                           Only has an effect if `tickmode` is set to "array".
E                           Used with `ticktext`.
E                       tickvalssrc
E                           Sets the source reference on Chart Studio Cloud for
E                           `tickvals`.
E                       tickwidth
E                           Sets the tick width (in px).
E                       title
E                           :class:`plotly.graph_objects.scatter.marker.colorbar.Ti
E                           tle` instance or dict with compatible properties
E                       x
E                           Sets the x position with respect to `xref` of the color
E                           bar (in plot fraction). When `xref` is "paper",
E                           defaults to 1.02 when `orientation` is "v" and 0.5 when
E                           `orientation` is "h". When `xref` is "container",
E                           defaults to 1 when `orientation` is "v" and 0.5 when
E                           `orientation` is "h". Must be between 0 and 1 if `xref`
E                           is "container" and between "-2" and 3 if `xref` is
E                           "paper".
E                       xanchor
E                           Sets this color bar's horizontal position anchor. This
E                           anchor binds the `x` position to the "left", "center"
E                           or "right" of the color bar. Defaults to "left" when
E                           `orientation` is "v" and "center" when `orientation` is
E                           "h".
E                       xpad
E                           Sets the amount of padding (in px) along the x
E                           direction.
E                       xref
E                           Sets the container `x` refers to. "container" spans the
E                           entire `width` of the plot. "paper" refers to the width
E                           of the plotting area only.
E                       y
E                           Sets the y position with respect to `yref` of the color
E                           bar (in plot fraction). When `yref` is "paper",
E                           defaults to 0.5 when `orientation` is "v" and 1.02 when
E                           `orientation` is "h". When `yref` is "container",
E                           defaults to 0.5 when `orientation` is "v" and 1 when
E                           `orientation` is "h". Must be between 0 and 1 if `yref`
E                           is "container" and between "-2" and 3 if `yref` is
E                           "paper".
E                       yanchor
E                           Sets this color bar's vertical position anchor This
E                           anchor binds the `y` position to the "top", "middle" or
E                           "bottom" of the color bar. Defaults to "middle" when
E                           `orientation` is "v" and "bottom" when `orientation` is
E                           "h".
E                       ypad
E                           Sets the amount of padding (in px) along the y
E                           direction.
E                       yref
E                           Sets the container `y` refers to. "container" spans the
E                           entire `height` of the plot. "paper" refers to the
E                           height of the plotting area only.
E                       
E               Did you mean "title"?
E               
E               Bad property path:
E               titleside
E               ^^^^^^^^^

.magic/envs/default/lib/python3.11/site-packages/plotly/basedatatypes.py:4378: ValueError
----------------------------- Captured stdout call -----------------------------
Error creating network visualization: Invalid property specified for object of type plotly.graph_objs.scatter.marker.ColorBar: 'titleside'

Did you mean "title"?

    Valid properties:
        bgcolor
            Sets the color of padded area.
        bordercolor
            Sets the axis line color.
        borderwidth
            Sets the width (in px) or the border enclosing this
            color bar.
        dtick
            Sets the step in-between ticks on this axis. Use with
            `tick0`. Must be a positive number, or special strings
            available to "log" and "date" axes. If the axis `type`
            is "log", then ticks are set every 10^(n*dtick) where n
            is the tick number. For example, to set a tick mark at
            1, 10, 100, 1000, ... set dtick to 1. To set tick marks
            at 1, 100, 10000, ... set dtick to 2. To set tick marks
            at 1, 5, 25, 125, 625, 3125, ... set dtick to
            log_10(5), or 0.69897000433. "log" has several special
            values; "L<f>", where `f` is a positive number, gives
            ticks linearly spaced in value (but not position). For
            example `tick0` = 0.1, `dtick` = "L0.5" will put ticks
            at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus
            small digits between, use "D1" (all digits) or "D2"
            (only 2 and 5). `tick0` is ignored for "D1" and "D2".
            If the axis `type` is "date", then you must convert the
            time to milliseconds. For example, to set the interval
            between ticks to one day, set `dtick` to 86400000.0.
            "date" also has special values "M<n>" gives ticks
            spaced by a number of months. `n` must be a positive
            integer. To set ticks on the 15th of every third month,
            set `tick0` to "2000-01-15" and `dtick` to "M3". To set
            ticks every 4 years, set `dtick` to "M48"
        exponentformat
            Determines a formatting rule for the tick exponents.
            For example, consider the number 1,000,000,000. If
            "none", it appears as 1,000,000,000. If "e", 1e+9. If
            "E", 1E+9. If "power", 1x10^9 (with 9 in a super
            script). If "SI", 1G. If "B", 1B.
        labelalias
            Replacement text for specific tick or hover labels. For
            example using {US: 'USA', CA: 'Canada'} changes US to
            USA and CA to Canada. The labels we would have shown
            must match the keys exactly, after adding any
            tickprefix or ticksuffix. For negative numbers the
            minus sign symbol used (U+2212) is wider than the
            regular ascii dash. That means you need to use −1
            instead of -1. labelalias can be used with any axis
            type, and both keys (if needed) and values (if desired)
            can include html-like tags or MathJax.
        len
            Sets the length of the color bar This measure excludes
            the padding of both ends. That is, the color bar length
            is this length minus the padding on both ends.
        lenmode
            Determines whether this color bar's length (i.e. the
            measure in the color variation direction) is set in
            units of plot "fraction" or in *pixels. Use `len` to
            set the value.
        minexponent
            Hide SI prefix for 10^n if |n| is below this number.
            This only has an effect when `tickformat` is "SI" or
            "B".
        nticks
            Specifies the maximum number of ticks for the
            particular axis. The actual number of ticks will be
            chosen automatically to be less than or equal to
            `nticks`. Has an effect only if `tickmode` is set to
            "auto".
        orientation
            Sets the orientation of the colorbar.
        outlinecolor
            Sets the axis line color.
        outlinewidth
            Sets the width (in px) of the axis line.
        separatethousands
            If "true", even 4-digit integers are separated
        showexponent
            If "all", all exponents are shown besides their
            significands. If "first", only the exponent of the
            first tick is shown. If "last", only the exponent of
            the last tick is shown. If "none", no exponents appear.
        showticklabels
            Determines whether or not the tick labels are drawn.
        showtickprefix
            If "all", all tick labels are displayed with a prefix.
            If "first", only the first tick is displayed with a
            prefix. If "last", only the last tick is displayed with
            a suffix. If "none", tick prefixes are hidden.
        showticksuffix
            Same as `showtickprefix` but for tick suffixes.
        thickness
            Sets the thickness of the color bar This measure
            excludes the size of the padding, ticks and labels.
        thicknessmode
            Determines whether this color bar's thickness (i.e. the
            measure in the constant color direction) is set in
            units of plot "fraction" or in "pixels". Use
            `thickness` to set the value.
        tick0
            Sets the placement of the first tick on this axis. Use
            with `dtick`. If the axis `type` is "log", then you
            must take the log of your starting tick (e.g. to set
            the starting tick to 100, set the `tick0` to 2) except
            when `dtick`=*L<f>* (see `dtick` for more info). If the
            axis `type` is "date", it should be a date string, like
            date data. If the axis `type` is "category", it should
            be a number, using the scale where each category is
            assigned a serial number from zero in the order it
            appears.
        tickangle
            Sets the angle of the tick labels with respect to the
            horizontal. For example, a `tickangle` of -90 draws the
            tick labels vertically.
        tickcolor
            Sets the tick color.
        tickfont
            Sets the color bar's tick label font
        tickformat
            Sets the tick label formatting rule using d3 formatting
            mini-languages which are very similar to those in
            Python. For numbers, see:
            https://github.com/d3/d3-format/tree/v1.4.5#d3-format.
            And for dates see: https://github.com/d3/d3-time-
            format/tree/v2.2.3#locale_format. We add two items to
            d3's date formatter: "%h" for half of the year as a
            decimal number as well as "%{n}f" for fractional
            seconds with n digits. For example, *2016-10-13
            09:15:23.456* with tickformat "%H~%M~%S.%2f" would
            display "09~15~23.46"
        tickformatstops
            A tuple of :class:`plotly.graph_objects.scatter.marker.
            colorbar.Tickformatstop` instances or dicts with
            compatible properties
        tickformatstopdefaults
            When used in a template (as layout.template.data.scatte
            r.marker.colorbar.tickformatstopdefaults), sets the
            default property values to use for elements of
            scatter.marker.colorbar.tickformatstops
        ticklabeloverflow
            Determines how we handle tick labels that would
            overflow either the graph div or the domain of the
            axis. The default value for inside tick labels is *hide
            past domain*. In other cases the default is *hide past
            div*.
        ticklabelposition
            Determines where tick labels are drawn relative to the
            ticks. Left and right options are used when
            `orientation` is "h", top and bottom when `orientation`
            is "v".
        ticklabelstep
            Sets the spacing between tick labels as compared to the
            spacing between ticks. A value of 1 (default) means
            each tick gets a label. A value of 2 means shows every
            2nd label. A larger value n means only every nth tick
            is labeled. `tick0` determines which labels are shown.
            Not implemented for axes with `type` "log" or
            "multicategory", or when `tickmode` is "array".
        ticklen
            Sets the tick length (in px).
        tickmode
            Sets the tick mode for this axis. If "auto", the number
            of ticks is set via `nticks`. If "linear", the
            placement of the ticks is determined by a starting
            position `tick0` and a tick step `dtick` ("linear" is
            the default value if `tick0` and `dtick` are provided).
            If "array", the placement of the ticks is set via
            `tickvals` and the tick text is `ticktext`. ("array" is
            the default value if `tickvals` is provided).
        tickprefix
            Sets a tick label prefix.
        ticks
            Determines whether ticks are drawn or not. If "", this
            axis' ticks are not drawn. If "outside" ("inside"),
            this axis' are drawn outside (inside) the axis lines.
        ticksuffix
            Sets a tick label suffix.
        ticktext
            Sets the text displayed at the ticks position via
            `tickvals`. Only has an effect if `tickmode` is set to
            "array". Used with `tickvals`.
        ticktextsrc
            Sets the source reference on Chart Studio Cloud for
            `ticktext`.
        tickvals
            Sets the values at which ticks on this axis appear.
            Only has an effect if `tickmode` is set to "array".
            Used with `ticktext`.
        tickvalssrc
            Sets the source reference on Chart Studio Cloud for
            `tickvals`.
        tickwidth
            Sets the tick width (in px).
        title
            :class:`plotly.graph_objects.scatter.marker.colorbar.Ti
            tle` instance or dict with compatible properties
        x
            Sets the x position with respect to `xref` of the color
            bar (in plot fraction). When `xref` is "paper",
            defaults to 1.02 when `orientation` is "v" and 0.5 when
            `orientation` is "h". When `xref` is "container",
            defaults to 1 when `orientation` is "v" and 0.5 when
            `orientation` is "h". Must be between 0 and 1 if `xref`
            is "container" and between "-2" and 3 if `xref` is
            "paper".
        xanchor
            Sets this color bar's horizontal position anchor. This
            anchor binds the `x` position to the "left", "center"
            or "right" of the color bar. Defaults to "left" when
            `orientation` is "v" and "center" when `orientation` is
            "h".
        xpad
            Sets the amount of padding (in px) along the x
            direction.
        xref
            Sets the container `x` refers to. "container" spans the
            entire `width` of the plot. "paper" refers to the width
            of the plotting area only.
        y
            Sets the y position with respect to `yref` of the color
            bar (in plot fraction). When `yref` is "paper",
            defaults to 0.5 when `orientation` is "v" and 1.02 when
            `orientation` is "h". When `yref` is "container",
            defaults to 0.5 when `orientation` is "v" and 1 when
            `orientation` is "h". Must be between 0 and 1 if `yref`
            is "container" and between "-2" and 3 if `yref` is
            "paper".
        yanchor
            Sets this color bar's vertical position anchor This
            anchor binds the `y` position to the "top", "middle" or
            "bottom" of the color bar. Defaults to "middle" when
            `orientation` is "v" and "bottom" when `orientation` is
            "h".
        ypad
            Sets the amount of padding (in px) along the y
            direction.
        yref
            Sets the container `y` refers to. "container" spans the
            entire `height` of the plot. "paper" refers to the
            height of the plotting area only.
        
Did you mean "title"?

Bad property path:
titleside
^^^^^^^^^
=============================== warnings summary ===============================
tests/python/meta_cognitive/test_pattern_visualization.py::test_plot_tool_performance
tests/python/meta_cognitive/test_pattern_visualization.py::test_plot_tool_performance
tests/python/meta_cognitive/test_pattern_visualization.py::test_plot_tool_performance
tests/python/meta_cognitive/test_pattern_visualization.py::test_plot_tool_performance
tests/python/meta_cognitive/test_pattern_visualization.py::test_plot_tool_performance
tests/python/meta_cognitive/test_pattern_visualization.py::test_plot_tool_performance
tests/test_visualization/test_pattern_viz.py::test_plot_tool_performance
tests/test_visualization/test_pattern_viz.py::test_plot_tool_performance
tests/test_visualization/test_pattern_viz.py::test_plot_tool_performance
  /Users/ryanoates/multidisciplinary-analysis-of-prompts/.magic/envs/default/lib/python3.11/site-packages/seaborn/categorical.py:700: PendingDeprecationWarning: vert: bool will be deprecated in a future version. Use orientation: {'vertical', 'horizontal'} instead.
    artists = ax.bxp(**boxplot_kws)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED tests/python/meta_cognitive/test_pattern_visualization.py::test_create_cognitive_network
FAILED tests/test_visualization/test_pattern_viz.py::test_create_cognitive_network
ERROR tests/test_tools/test_anthropic_tool.py::test_generate_response - Attri...
ERROR tests/test_tools/test_anthropic_tool.py::test_analyze_code - AttributeE...
ERROR tests/test_tools/test_anthropic_tool.py::test_enhance_documentation - A...
ERROR tests/test_tools/test_anthropic_tool.py::test_suggest_improvements - At...
ERROR tests/test_tools/test_anthropic_tool.py::test_error_handling - Attribut...
============== 2 failed, 39 passed, 9 warnings, 5 errors in 5.22s ==============

## Contact
For any queries or suggestions, please reach out to the development team.

