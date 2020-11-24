
<script>
  import { onMount } from 'svelte';

  import { scaleLinear, scaleOrdinal } from 'd3-scale';
  import { schemeCategory10 } from 'd3-scale-chromatic';
  import { select, selectAll } from 'd3-selection';
  import { drag } from 'd3-drag';
  import { forceSimulation, forceLink, forceManyBody, forceCenter, forceX, forceY } from 'd3-force';
  let d3 = { scaleLinear, scaleOrdinal, schemeCategory10, select, selectAll, drag, forceSimulation, forceLink, forceManyBody, forceCenter, forceX, forceY };

  export let graph;

  let svg;
  let width = 500;
  let height = 600;

  function resize() {
    ({ width, height } = svg.getBoundingClientRect());
  }
  
  let simulation
  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }
  
  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }
  
  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }
  
  function dragsubject(event) {
    return simulation.find(event.x, event.y);
  }

  function network() {
    resize();

    simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).strength(0.1))
      .force("charge", d3.forceManyBody().strength(-40))
      .force("x", d3.forceX().strength(0.05))
      .force("y", d3.forceY().strength(0.05))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .on('tick', function ticked() {
        simulation.tick();
        nodes = [...nodes];
        links = [...links];
      });
  
    d3.select(svg)
      .call(d3.drag()
            .container(svg)
            .subject(dragsubject)
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

  }

  $: links = graph.edges.map(d => d);
  $: nodes = graph.nodes.map(d => d);

  $: d3yScale = scaleLinear()
                  .domain([0, height])
                  .range([height, 0]);

  let pt;
  onMount(
    function() {
      pt = svg.createSVGPoint();
      network();
    }
  );

  let m = { x: 0, y: 0 };
  let radius = 10;

  function cursorPoint(evt){
    pt.x = evt.clientX; pt.y = evt.clientY;
    return pt.matrixTransform(svg.getScreenCTM().inverse());
  }

  function handleMousemove(event) {
    m = cursorPoint(event);
  }

  function test_close(m, point) {
    var res = (Math.sqrt((m.x - point.x) ** 2 + (m.y - point.y) ** 2) < radius);
    return res;
  }

</script>

<svelte:window on:resize='{resize}'/>

<svg bind:this={svg} on:mousemove={handleMousemove}>
  {#each links as link}
    <g stroke='#999' stroke-opacity='0.6'>
      <line x1='{link.source.x}' y1='{link.source.y}'
            x2='{link.target.x}' y2='{link.target.y}'>
            <title>{link.source.id}</title>
      </line>
    </g>
  {/each}

  {#each nodes as point}
    <a xlink:href="{point.url}">
    <circle class='node' r='5' cx='{point.x}' cy='{point.y}'>
    </circle>
    </a>
    {#if test_close(m, point)}
    <text class="label" x='{point.x}' y='{point.y}' dx=12 dy='.35em'>
          {point.title}</text>
    {/if}
  {/each}
</svg>
<style>
  svg {
    width: 100%;
    height: 100%;
    margin-left: auto;
    margin-right: auto;
    display: block;
    background-color: white;
  }

  circle {
    stroke: #fff;
    stroke-width: 1.5;
    fill: gray;
  }

  .tick line {
    stroke: #ddd;
    stroke-dasharray: 2;
  }

  text {
    font: 10px sans-serif;
    pointer-events: none;
  }
</style>
