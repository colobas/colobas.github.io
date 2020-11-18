<script>
  import { onMount } from 'svelte';
  import Base from "../Base.svelte";
  import Graph from "../Graph.svelte";
  import HierarchicalEdgeBundle from "../HierarchicalEdgeBundle.svelte";

  let graph = null;
  onMount(async () => {
    const response = await fetch("/graph.json");
    graph = await response.json();
  });

</script>

<Base>
  <div class="text-block intro">
    I'm Gui, a Machine Learning Engineer from Lisbon, currently living in
    Seattle. I'm interested in tech, philosphy, politics, economics, books, food, and most
    importantly, saving the World.
    You can find my CV <a href="/cv.pdf">here</a>.
  </div>
  <div class="map">
    {#if graph}
      <Graph graph={graph}/>
    {/if}
    <span class="helper"></span>
  </div>
  <div class="text-block map-label">
    This is a map of my brain. Hover over the graph to see the node labels. Click on a node
    to see the notes I've taken on its corresponding topic. These notes aren't tidy, and some
    may contain strange artifacts. Also, if your on mobile, you won't be able to see the node
    labels while hovering.
  </div>
</Base>
<style>
  .text-block {
    width: 50%;
    padding-top: 1em;
    margin: auto;
  }
  .intro {
    text-align: justify;
  }
  .map-label {
    text-align: justify;
  }
  .map {
    border: 3px solid black;
    width: 30%;
    height: 50%;
    margin: auto;
    margin-top: 1em;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .helper {
    display: inline-block;
    height: 100%;
    vertical-align: middle;
  }

  @media only screen and (max-width: 800px) {
    /* For mobile phones: */
    .text-block {
      width: 90%;
    }

    .map {
      width: 90%;
      height: 80%;
    }
  }

  @media only screen and (min-width: 800px) and (max-width: 1000px) {
    /* For mobile phones: */
    .text-block {
      width: 70%;
    }

    .map {
      width: 70%;
      height: 60%;
    }
  }


</style>
