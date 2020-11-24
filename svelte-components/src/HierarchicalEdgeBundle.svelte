<script>
  import { onMount } from 'svelte';

  import { select, selectAll } from 'd3-selection';
  import { hierarchy, cluster } from 'd3-hierarchy';
  import { radialLine, curveBundle } from 'd3-shape';
  let d3 = { select, selectAll, hierarchy, cluster, radialLine, curveBundle };

  export let graph;

  let svg;
  onMount(() => {

    let diameter = 500;
    let radius = diameter / 2;
    let innerRadius = radius - 120;

    let _cluster = d3.cluster()
        .size([360, innerRadius]);

    let line = d3.radialLine()
        .curve(d3.curveBundle.beta(0.5))
        .radius(function(d) { return d.y; })
        .angle(function(d) { return d.x / 180 * Math.PI; });

    let d3_svg = d3.select(svg)
    .attr("width", diameter)
    .attr("height", diameter)
    .append("g")
    .attr("transform", "translate(" + radius + "," + radius + ")");

    let link = d3_svg.append("g").selectAll(".link");
    let node = d3_svg.append("g").selectAll(".node");

    function packageHierarchy(classes) {
      var map = {};

      function find(name, data) {
        var node = map[name], i;
        if (!node) {
          node = map[name] = data || {name: name, children: []};
          if (name.length) {
            node.parent = find(name.substring(0, i = name.lastIndexOf(".")));
            node.parent.children.push(node);
            node.key = name.substring(i + 1);
          }
        }
        return node;
      }

      classes.forEach(function(d) {
        if( typeof d.name != 'undefined')
          find(d.name, d);
      });

      return d3.hierarchy(map[""]);
    }

    function packageImports(nodes) {
      var map = {},
          imports = [];

      // Compute a map from name to node.
      nodes.forEach(function(d) {
        map[d.data.name] = d;
      });

      // For each import, construct a link from the source to target node.
      nodes.forEach(function(d) {
        if (d.data.imports) {
          d.data.imports.forEach(function(i) {
            var input = map[d.data.name];
            var mapi = map[i];
            if( typeof mapi != 'undefined'){
              var path = input.path(mapi);
              imports.push(path);
            }
          });
        }
      });

      return imports;
    }

    let classes = [];
    Object.values(graph.edge_dict).forEach(
      function(d) { classes.push({name: d.name, imports: d.children})});

    let root = packageHierarchy(classes).sum(function(d) { return 1; });
    root = _cluster(root)

    link = link
      .data(packageImports(root.leaves()))
      .enter().append("path")
        .each(function(d) { d.source = d[0], d.target = d[d.length - 1]; })
        .attr("class", "link")
        .attr("d", line);

    node = node
      .data(root.leaves())
      .enter().append("text")
        .attr("class", "node")
        .attr("dy", "0.31em")
        .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + (d.y + 8) + ",0)" + (d.x < 180 ? "" : "rotate(180)"); })
        .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
        .text(function(d) { 
          if( d.data.key != "FULL NAME")
            return d.data.key; 
          })
        .on("mouseover", mouseovered)
        .on("mouseout", mouseouted);

    console.log(link)

    function mouseovered(d) {
      node
          .each(function(n) { n.target = n.source = false; });
    
      link
          .classed("link--target", function(l) { if (l.target === d) return l.source.source = true; })
          .classed("link--source", function(l) { if (l.source === d) return l.target.target = true; })
        .filter(function(l) { return l.target === d || l.source === d; })
          .raise();
    
      node
          .classed("node--target", function(n) { return n.target; })
          .classed("node--source", function(n) { return n.source; });
    }
    
    function mouseouted(d) {
      link
          .classed("link--target", false)
          .classed("link--source", false);
    
      node
          .classed("node--target", false)
          .classed("node--source", false);
    }
  });

</script>

<svg bind:this={svg}>
</svg>

<style>
  .node {
    font: 300 11px "Helvetica Neue", Helvetica, Arial, sans-serif;
    fill: #bbb;
  }
  
  .node:hover {
    fill: #000;
  }
  
  .link {
    stroke: steelblue;
    stroke-opacity: 0.4;
    fill: none;
    pointer-events: none;
  }
  
  .node:hover,
  .node--source,
  .node--target {
    font-weight: 700;
  }
  
  .node--source {
    fill: #2ca02c;
  }
  
  .node--target {
    fill: #d62728;
  }
  
  .link--source,
  .link--target {
    stroke-opacity: 1;
    stroke-width:1px;
  }
  
  .link--source {
    stroke: #d62728;
  }
  
  .link--target {
    stroke: #2ca02c;
  }
</style>
