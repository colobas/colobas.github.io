<script>
  import { onMount, afterUpdate, beforeUpdate } from "svelte";
  import Card from "./Card.svelte";
  import md2json from 'md-2-json';

  export let data;
  export let mj;

  let colors = ["#3772ff","#1f1b12","#855251","#5cb695","#ccaa66",
                "#d2b0d4","#7f8a97","#81988c","#392841","#8d8180"];

  function get_children(node){
    var tmp = [];
    if (typeof(node) === "object") {
      tmp = Object.keys(node)
    } else {
      return [];
    }

    if (tmp.length == 1 && node.raw) {
      return [];
    }

    return tmp;
  }
  
  let parsed_data = md2json.parse(data);
  console.log(parsed_data);
  let root_list_ix = 0;
  let cur_obj = parsed_data;
  let highlighted_ix = 0;
  let prev_lvl_ixs = [];
  let prev_objs = [];
  

  $: cur_list = get_children(cur_obj);
  $: highlighted = cur_list[highlighted_ix];
  $: level1 = cur_list.slice(highlighted_ix + 1);
  $: level2 = get_children(cur_obj[highlighted]);

  function handleKeypress(event) {
    switch(event.key){
      case "ArrowDown":
        if (highlighted_ix < cur_list.length - 1) {
          highlighted_ix++;
          if (prev_objs.length == 0) {
            root_list_ix++;
          }
        }
        break;
      case "ArrowUp":
        if (highlighted_ix > 0) {
          highlighted_ix = highlighted_ix - 1;
          if (prev_objs.length == 0) {
            root_list_ix = root_list_ix - 1;
          }
        }
        break;
      case "ArrowRight":
        if (get_children(parsed_data[highlighted]).length > 0) {
          var new_highlighted_ix = 0;
          var first_child = get_children(cur_obj[highlighted])[0];
          var new_obj = cur_obj[highlighted][first_child];
          
          prev_lvl_ixs = [...prev_lvl_ixs, highlighted_ix];
          prev_objs = [...prev_objs, cur_obj];
          highlighted_ix = new_highlighted_ix;
          cur_obj = new_obj;

        }
        break;
      case "ArrowLeft":
        if (prev_objs.length > 0) {
          cur_obj = prev_objs.pop();
          prev_objs = prev_objs;
          highlighted_ix = prev_lvl_ixs.pop();
          prev_lvl_ixs = prev_lvl_ixs;
        }
    };
  };
  
  $: highlighted_color = colors[root_list_ix];
  
  function make_lvl1_colors(root_list_ix, top_level) {
    var tmp = [];
    for(var i=0; i < level1.length; i++) {
        tmp[i] = colors[(top_level) ? (root_list_ix + i + 1) : root_list_ix];
    }
    return tmp;
  }
  
  afterUpdate(() => {
    if (mj) { mj.typeset(); }
  });
  
  $: top_level = (prev_objs.length == 0);
  $: lvl1_colors = make_lvl1_colors(root_list_ix, top_level); 

</script>

<svelte:window on:keydown={handleKeypress}/>

<div id="row">
  <div id="col1" class="col">
    <Card key={highlighted} body={cur_obj[highlighted]} _class="card highlighted" color="{highlighted_color}"/>
    {#each level1 as card, i}
      <Card key={card} body={cur_obj[card]} _class="card" color="{lvl1_colors[i]}"/>
    {/each}
  </div>
  <div id="col2" class="col">
    {#each level2 as card}
      <Card key={card} body={cur_obj[highlighted][card]} _class="card" color="{highlighted_color}"/>
    {/each}
  </div>
</div>

<style>
    * { 
        -moz-box-sizing: border-box; 
        -webkit-box-sizing: border-box; 
         box-sizing: border-box; 
    }

    #row {
      display: flex;
      margin: auto;
    }
    
    .col {
      flex: 0 0 50%;
      min-width: 0;
    }
    
</style>
