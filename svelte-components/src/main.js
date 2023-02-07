import BlinkingCursor from './BlinkingCursor.svelte';
import TypeTitle from './TypeTitle.svelte';
import Graph from './Graph.svelte';

//fetch("/graph.json")
//  //.then(response => response.json())
//  .then(async function(response){ response = await response;  return response.json(); })
//  .then(data =>
//    new Graph({
//      target: document.querySelector('#graph-holder'),
//      props: {
//      	graph: data
//      }
//    }),
//  );

new TypeTitle({
  target: document.querySelector('#hello-friend'),
  props: {
    content: "Hello friend"
  }
});
