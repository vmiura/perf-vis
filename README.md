# perf-vis: Visualize profiles as sunburst diagrams.

View demo at http://vmiura.github.io/perf-vis/demo.html

[![Example](http://vmiura.github.io/perf-vis/demo-screenshot.png)](http://vmiura.github.io/perf-vis/demo-screenshot.png)

perf-vis is compatible with stacks collected with: https://github.com/brendangregg/FlameGraph/

The current version is configured to color Chromium code.

1. Capture & fold stacks using FlameGraph tools
===============================================

Usage example:

```
For instruments:
$ ./stackcollapse-instruments.pl out.txt > out.folded

For perf_events:
$ ./stackcollapse-perf.pl out.perf > out.folded

For DTrace:
$ ./stackcollapse.pl out.kern_stacks > out.kern_folded
```

2. Generate visualization with perf_vis_stacks.py
=================================================

Use perf_vis_stacks.py to render a HTML file.

```
$ ./perf_vis_stacks.py out.folded -o out.html

Or by default the output path will be out.stacks_todaysdate.html
```

Useful features
===============

### Navigate stacks

Drill into profile stacks by clicking on the graph, or by clicking links in the Callee table.

To return to a prior stack, use your browser's back button, or click in the center of the viualization.

**Hide** uninteresting methods.

[![Example](http://vmiura.github.io/perf-vis/callees.png)](http://vmiura.github.io/perf-vis/callees.png)

The stack view shows the currently selected stack.

[![Example](http://vmiura.github.io/perf-vis/stack-view.png)](http://vmiura.github.io/perf-vis/stack-view.png)

### Search for methods.  Merge call sites.

The **All methods** is a bottom-up view of all methods reachable in the current stack.

[![Example](http://vmiura.github.io/perf-vis/all-methods.png)](http://vmiura.github.io/perf-vis/all-methods.png)

Clicking a method with multiple call sites produces a merged view of the method from all callers.  This is very useful for analyzing performance of methods called in many places, or via recursive code.

### Linkable URLs.

Send colleagues deep links to your profile's stack view. Example: <http://vmiura.github.io/perf-vis/demo.html#{"stack":[0],"id":1141,"ignore":[],"hide":[],"merged":false}>
